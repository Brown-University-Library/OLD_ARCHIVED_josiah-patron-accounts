import vcr
import json, os

from iii_account import IIIAccount
import time

name, barcode = ( os.environ[u'iii_acc__TEST_NAME'], os.environ[u'iii_acc__TEST_BARCODE'] )

# Show logging
import logging
formatter = logging.Formatter(u'%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger('iii_account')
logger.setLevel(logging.DEBUG)
console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)

def test_login():
    with vcr.use_cassette('fixtures/login-out.yaml', filter_post_data_parameters=['name', 'code']):
        sess = IIIAccount(name, barcode)
        #These should raise errors if login fails.
        sess.login()
        sess.logout()

def test_login_bad():
    with vcr.use_cassette('fixtures/login-bad.yaml', filter_post_data_parameters=['name', 'code']):
        ( name, barcode ) = ( 'foo', 'bar' )
        sess = IIIAccount( name, barcode )
        exception = None
        try:
            sess.login()  # should raise error
        except Exception as e:
            exception = repr(e)
        assert exception == 'Login failed.'

def test_get_checkouts():
    with vcr.use_cassette('fixtures/checkouts.yaml', filter_post_data_parameters=['name', 'code']):
        sess = IIIAccount(name, barcode)
        sess.login()
        checkouts = sess.get_checkouts()
        assert "Z695.Z8 F373 2010" in [i['call_number'] for i in checkouts]
        sess.logout()

def test_complete_hold():
    with vcr.use_cassette('fixtures/grad-hold-open-circ.yaml', filter_post_data_parameters=['name', 'code']):
        sess = IIIAccount(name, barcode)
        sess.login()
        bib = 'b2305331'
        # Get the items available for requesting.
        items = sess.get_items(bib)
        # Hold an item - the interface would offer a choice
        item = items[0]['id']
        hold = sess.place_hold(bib, item)
        print json.dumps(hold, indent=2)
        sess.logout()

def test_get_holds():
    with vcr.use_cassette('fixtures/get-holds.yaml', filter_post_data_parameters=['name', 'code']):
        sess = IIIAccount(name, barcode)
        sess.login()
        existing_holds = sess.get_holds()
        assert existing_holds[0]['key'] == 'canceli11425642x00'
        sess.logout()

def test_cancel_hold():
    cancel_key = 'canceli11425642x00'
    with vcr.use_cassette('fixtures/cancel-single-hold.yaml', filter_post_data_parameters=['name', 'code']):
        sess = IIIAccount(name, barcode)
        sess.login()
        canceled = sess.cancel_hold(cancel_key)
        print json.dumps(canceled, indent=2)
        sess.logout()


def test_denied_hold():
    with vcr.use_cassette('fixtures/undergrad-hold-denied-open-circ.yaml', filter_post_data_parameters=['name', 'code']):
        sess = IIIAccount(name, barcode)
        sess.login()
        bib = 'b2305331'
        # Get the items available for requesting.
        items = sess.get_items(bib)
        # Hold an item - the interface would offer a choice
        item = items[0]['id']
        hold = sess.place_hold(bib, item)
        assert hold['confirmed'] == False
        assert hold['message'] == "No requestable items are available"
        sess.logout()



if __name__ == "__main__":
    test_cancel_hold()
