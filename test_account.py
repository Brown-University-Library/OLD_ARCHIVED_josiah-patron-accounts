from __future__ import unicode_literals

import json
import os
import time

import pytest
import vcr

from iii_account import IIIAccount


name, barcode = ( os.environ['iii_TEST_NAME'], os.environ['iii_TEST_BARCODE'] )


# Show logging
import logging
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(funcName)s()::%(lineno)d - %(message)s')
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
    assert sess.patron_id == None
    sess.login()
    assert len( sess.patron_id ) == 7
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
    assert sess.patron_id == None


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
    assert hold['confirmed'] == True
    sess.logout()


@bul_vcr.use_cassette('grad-hold-open-circ-annex.yaml')
def test_place_hold_annex():
    """ Tests known requestable item from Annex. """
    sess = IIIAccount(name, barcode)
    sess.login()
    bib = 'b4069600'
    item = 'i11788360'  # year 1996, volume 53, from <http://josiah.brown.edu/record=b4069600>
    hold = sess.place_hold( bib, item, availability_location='ANNEX' )
    print json.dumps(hold, indent=2)
    assert hold['confirmed'] == True
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
    canceled_output = sess.cancel_hold(cancel_key)
    assert canceled_output['cancelled'] == True
    print json.dumps(canceled_output, indent=2)
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


@bul_vcr.use_cassette('grad-hold-open-circ.yaml')
def test_get_items():
    sess = IIIAccount(name, barcode)
    sess.login()
    bib = 'b2305331'
    # Get the items available for requesting.
    items = sess.get_items(bib)
    assert items == [ {
        'barcode': '31236011741298',
        'callnumber': 'PS3568.U812 R57x 1994',
        'id': 'i11425642',
        'location': 'ROCK',
        'status': 'AVAILABLE'} ]
    sess.logout()


if __name__ == "__main__":
    raise Exception("Run with py.test.")
