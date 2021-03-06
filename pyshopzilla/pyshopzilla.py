import urllib
import simplejson
import types
import logging
from random import randint
from django.conf import settings

log = logging.getLogger('pyshopzilla.ShopzillaAPI')
hdlr = logging.StreamHandler()   # Logs to stderr by default
formatter = logging.Formatter('\n--\n  shop - api \
    %(asctime)s %(levelname)s %(message)s \n--\n')
hdlr.setFormatter(formatter)
log.addHandler(hdlr)
log.setLevel(logging.INFO)
log.setLevel(logging.DEBUG)

# try to load settings from a django project
try:
  from django.conf import settings
  apikey = getattr(settings, "SHOPZILLA_API_KEY", 'DEFAULT_API_KEY')
  JSON_RESPONSE_FILE = getattr(settings, "SHOPZILLA_RESPONSE_LOGFILE", "/tmp/shopzilla.log")
  DEBUG = getattr(settings, "DEBUG", False)
except ImportError:
  apikey, JSON_RESPONSE_FILE, DEBUG = None, '/tmp/shopzilla.log', False

_params = {
    'apiKey': '',
    'minRelevancyScore': '100',
    'placementId': '1',
    'resultsAttributeValues': '100',
    'productIdType': '',
    'results': '250',
    'showAttributes': '',
    'backfillResults': '0',
    'showRawUrl': '',
    'offersOnly': '',
    'startOffers': '0',
    'resultsOffers': 3,
    'merchantId': '',
    'attFilter': '',
    'freeShipping': '',
    'imageOnly': '',
    'showProductAttributes': '',
    'biddedOnly': '',
    'start': '0',
    'maxAge': '',
    'minMarkdown': '',
    'categoryId': '',
    'productId': '',
    'sort': 'relevancy_desc',
    'format': 'json',
    'zipCode': '',
    'brandId': '',
    'minPrice': '',
    'keyword': '',
    'maxPrice': '',
    'callback': 'callback',
    'attributeId': '',
    'attWeights': '',
    'publisherId': '69109',
    'resultsAttribute': '20',
  }

_taxonomy_params = {'apiKey': 'apiKey', 'publisherId':'', 'placementId': '1', 'categoryId': '1',\
      'keyword': '', 'results': '50', 'format': 'json', 'sort': 'name_asc'}

class PyShopzillaError(Exception):
    """ 
    Handle basic exceptions for Shopzilla class
    """
    def __init__(self, message):
      if DEBUG:
        log.debug(message)
      Exception.__init__(self, message)


class ShopzillaAPI(object):
  """ Base shopzilla api class """
  params = _params
  url = 'http://catalog.bizrate.com/services/catalog/v1/us/product/?'
  response = None
  response_data = None
  result_param = 'products'
  json_data = None
  
  def __init__(self, *args, **kwargs):
    """ 
    Overwrite any param data and call
    apiKey is required, params list sent should be in self.params
    Set the response to self.response
    """
    if not kwargs.get('apiKey'):
      raise PyShopzillaError('Required: apiKey')

    # set the params
    for i in kwargs.keys():
      if not i in self.params.keys():
        raise PyShopzillaError('Parameter Sent %s is not in allowed' % i)
      self.params[i] = kwargs.get(i)

    params = urllib.urlencode(self.params)
    url = '%s%s' % (self.url, params)
    log.info("Shopzilla Query URL: %s" % url)
    self.response = urllib.urlopen(url)

  def bidded_only(self):
    """
    Run this method before searching to select 
    only the products which will give you commission
    """
    self.params['biddedOnly'] = "true"

  def contains_images(self):
    """
    Run this method before searching to 
    select only the products that contain contains_images
    """
    self.params['imageOnly'] = "true"

  def read_response(self, debug=DEBUG, debug_filename=None):
    """ 
    Read the response from the api call 
    call .read() and get the response data 
    overwritable debug
    """
    self.response_data = self.response.read()
    f = JSON_RESPONSE_FILE
    if debug_filename:
      f = debug_filename

    if debug:
      # pass debug_filename or JSON_RESPONSE_FILE if nothing passed
      o = open('%s/jsondump%s' % (f, randint(1111,99999)), 'w')
      o.write(self.response_data)
      o.close()

  def parse_json(self):
    """ 
    Read the response_data into json and deserialize that bitch!
    """
    self.json_data = simplejson.loads(self.response_data)



class ShopzillaTaxonomyAPI(ShopzillaAPI):
  """
  Subclass shopzillaapi class 
  overwrite params and url
  """
  url = 'http://catalog.bizrate.com/services/catalog/v1/us/taxonomy?'

  params = _taxonomy_params

  def __init__(self, *args, **kwargs):
    super(ShopzillaTaxonomyAPI, self).__init__(self, *args, **kwargs)

  def overwrite_url(self):
    """ overwrite the url from base class with taxonomy url """
    self.url = 'http://catalog.bizrate.com/services/catalog/v1/us/taxonomy?'

  def overwrite_params(self):
    """ overwrite the params 
    -apiKey
    -publisherId
    -placementId
    -categoryId
    -keyword
    -results
    -format
    -name_asc
    """
    self.params = _taxonomy_params
