# -*- coding: utf-8 -*-

""" Sequentially goes through steps of placing a hold to determine Annex-hold failure point.
    Note: Testing indicates that initial login is not needed.
          Am doing it here to mimic standard library flow.
    Note: This code works; indicates payload must be different for Annex requests. """

from __future__ import unicode_literals
import logging, os, pprint, sys
import requests
from bs4 import BeautifulSoup


## set up file logger
LOG_PATH = os.environ['iii_bjd__LOG_PATH']
logging.basicConfig(
    filename=LOG_PATH,
    level=logging.DEBUG,
    format='[%(asctime)s] %(levelname)s [%(module)s-%(funcName)s()::%(lineno)d] %(message)s',
    datefmt='%d/%b/%Y %H:%M:%S' )
log = logging.getLogger(__name__)
log.info( 'hold_placer log started' )


## vars
LAST_NAME = os.environ['iii_bjd__LAST_NAME']
BARCODE = os.environ['iii_bjd__BARCODE']
OPAC_URL = 'https://josiah.brown.edu/'
BIB = 'b4069600'
ITEM = 'i117883608'  # year 1996, volume 53, from <http://josiah.brown.edu/record=b4069600>
PICKUP_LOCATION = 'ROCK'


## login
work_dct = {
    'authenticated': False,
    'patron_id': None,
    'staff_mode': False }
session = requests.Session()
url = OPAC_URL + 'patroninfo'
log.debug( 'url, `%s`' % url )
payload = {
    'name': LAST_NAME,
    'code': BARCODE,
    'submit': 'submit'
    }
log.debug( 'payload, `%s`' % pprint.pformat(payload) )
rsp = session.post( url, data=payload, allow_redirects=True, verify=False )
log.debug( 'rsp.url, `%s`' % rsp.url )
doc = BeautifulSoup( rsp.content.decode('utf-8') )
log.debug( 'login rsp doc, ```%s```' % doc.prettify() )  # doc.prettify() output is unicode
login_error = doc.find( "span", class_="login_error" )  # <span class="login_error"> exists if login fails
if (login_error):
    raise Exception("Login failed.")
log.debug( 'login successful' )
work_dct['authenticated'] = True
work_dct['patron_id'] = rsp.url.split('/')[-2]
log.debug( 'patron_id, `%s`' % work_dct['patron_id'] )
log.debug( 'rsp.url, `%s`' % rsp.url )
if 'logged into staff mode' in rsp.content.lower():
    work_dct['staff_mode'] = True
log.debug( 'work_dct, `%s`' % pprint.pformat(work_dct) )


## submit hold
# session = requests.Session()
url_a = OPAC_URL + 'search~S7?/.{{bib}}/.{{bib}}/1%2C1%2C1%2CB/request~{{bib}}'
url = url_a.replace( '{{bib}}', BIB )
log.debug( 'initial hold url, `%s`' % url )
payload = {
    'locx00': 'r0001',
    'radio': 'i11788360',
    'name': LAST_NAME,
    'code': BARCODE,
    'pat_submit': 'Request item',
    'submit': 'Submit',
    }
rsp = session.post( url, data=payload, allow_redirects=True, verify=False )
log.debug( 'actual hold url, `%s`' % url )
doc = BeautifulSoup( rsp.content.decode('utf-8') )
log.debug( 'hold rsp doc, ```%s```' % doc.prettify() )
