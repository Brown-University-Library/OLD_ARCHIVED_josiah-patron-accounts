
import json
import os
import time

import pytest
import vcr

from iii_account import IIIAccount

name, barcode = ( os.environ[u'iii_TEST_NAME'], os.environ[u'iii_TEST_BARCODE'] )

# Show logging
import logging
formatter = logging.Formatter(u'%(asctime)s - %(levelname)s - %(funcName)s()::%(lineno)d - %(message)s')
logger = logging.getLogger('iii_account')
logger.setLevel(logging.DEBUG)
console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)

# Custom VCR config.
bul_vcr = vcr.VCR(
    cassette_library_dir = os.environ.get('iii_FIXTURE_DIR', 'fixtures'),
    filter_post_data_parameters=['name', 'code'],
    # This prevents new HTTP requests.  Comment or remove to record
    # new fixtures.
    record_mode = 'none',
)


@bul_vcr.use_cassette('login-out.yaml')
def test_login():
    sess = IIIAccount(name, barcode)
    #These should raise errors if login fails.
    sess.login()
    sess.logout()


@bul_vcr.use_cassette('login-bad.yaml')
def test_login_bad():
    ( name, barcode ) = ( 'foo', 'bar' )
    sess = IIIAccount( name, barcode )
    exception = None
    try:
        sess.login()  # should raise error
    except Exception as e:
        exception = repr(e)
    assert exception == "Exception('Login failed.',)"


@bul_vcr.use_cassette('checkouts.yaml')
def test_get_checkouts():
    sess = IIIAccount(name, barcode)
    sess.login()
    checkouts = sess.get_checkouts()
    assert "Z695.Z8 F373 2010" in [i['call_number'] for i in checkouts]
    sess.logout()


@bul_vcr.use_cassette('grad-hold-open-circ.yaml')
def test_complete_hold():
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


@bul_vcr.use_cassette('get-holds.yaml')
def test_get_holds():
    sess = IIIAccount(name, barcode)
    sess.login()
    existing_holds = sess.get_holds()
    assert existing_holds[0]['key'] == 'canceli11425642x00'
    sess.logout()


@bul_vcr.use_cassette('cancel-single-hold.yaml')
def test_cancel_hold():
    cancel_key = 'canceli11425642x00'
    sess = IIIAccount(name, barcode)
    sess.login()
    canceled = sess.cancel_hold(cancel_key)
    print json.dumps(canceled, indent=2)
    sess.logout()


@bul_vcr.use_cassette('undergrad-hold-denied-open-circ.yaml')
def test_denied_hold():
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
    raise Exception("Run with py.test.")
