# -*- coding: utf-8 -*-

''' Sequentially goes through steps of placing a hold to determine failure point. '''

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
log.debug( '- doc, ```%s```' % doc.prettify() )  # doc.prettify() output is unicode
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
