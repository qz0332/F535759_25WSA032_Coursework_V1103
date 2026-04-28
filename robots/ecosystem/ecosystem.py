
'''
Do not add your own imports here - place them in your coursework cells
'''

import time
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mpc
import math
import operator

from copy import copy, deepcopy
from random import random, randint


plt.ion() # turn on interactive mode for live updating of the ecosystem display
#Ecosystem Boundaries

default_width = 80
default_height = 40
default_altitude = 5
arena_limits = (default_width,default_height,default_altitude)


#Fading of robots  alpha = m_fade * soc/capacity + c_fade
c_fade = 0.1
m_fade = 0.9 - c_fade

#deliverable fading
delivered_fade = 0.50
delivered_fade_rate = .01   #d alpha at -1% per update

#maximum damage a robot can sustain
max_damage = 5

# sign functions
################################################################################

#randsign generates a random -1 or +1 to give a random sign of a vector
def randsign():
  return [-1,1][randint(0,1)]

#sign returns the sign x 1 of a number.
def sign(i):
  return [-1,0,1][0 if i < 0 else 1 if i == 0 else 2]

# now - datetime stamp
################################################################################

def now(format = "%d/%m/%Y %H:%M:%S"):
  return time.strftime (format, time.localtime())


# truth -
###############################################################################
'''
receives left value l and right value r for comparison
if r value is a tuple
  assumed of the form (o, r) where o is a comparison operator in ops keys
else
  equality is returned

'''
ops = { '>': operator.gt,
        '<': operator.lt,
        '>=': operator.ge,
        '<=': operator.le,
        '==': operator.eq,
        'in': operator.contains}   #note inversion of l and r in usage

def truth(l, r):
    # l, t left and right of operator function (if commutative)
    if type(r) is tuple:
      o = r[0]
      r = r[1]
      return ops[o](l, r) if o != 'in' else ops[o](r, l)
    else:
      return l == r

def dprint (*args):
  print (">>:", *args)


def stop(*args):
  args += ("stop",)
  dprint(*args)
  raise Exception("Exececution stopped")

#@title Shapes and Colors

# Matplotlib colors and shapes semantics # https://matplotlib.org/stable/api/markers_api.html
mpl_shapes = {'square':'s', 'circle':'o','triangle':'^', 'plus':'P', 'star':'*', 'diamond':'D', 'x':'x', 'filled-X':'X', 'hexagon':'h', 'triangle_up': '^', 'point': '.'}
mpl_colors = mpc.cnames
colors = mpl_colors.keys()
shapes = mpl_shapes.keys()

#@title Coordinate Functions

### random coordinates #########################################################
def random_coordinates(significance = 2):
   return [round(random() * default_width, significance), round(random() * default_height, significance)]

### same coordinates ###########################################################
def same_coordinates (coordinates1, coordinates2, significance = 2, length = 2):
  #note zip clips to the shortest list
  if coordinates1 and coordinates2:
    c = [round(c1,significance) == round(c2,significance)
         for c1, c2 in zip(coordinates1[:length], coordinates2[:length]) ]
    return all(c )
  else:
    return False  #if one set None

### Cartesian to Compass #######################################################
def cartesian_compass(x, y):
  return math.atan2(x, y) % (2* math.pi), math.sqrt(x**2 + y**2)

### Compass to Cartesian #######################################################
def compass_cartesian(compass_heading, r):
  #returns a tuple (x, y) for compass_heading (0-2*pi rads clockwise, 0=north)
  x = math.sin(compass_heading) * r
  y = math.cos(compass_heading) * r
  return x, y

### Valid Coordinates ##########################################################
def valid_coordinates(coordinates):
  #Use this to test if coordinates are valid. returns None if not
  valid = (type(coordinates) == list and
    0 < len(coordinates) < 4 and
    False not in [type(i) == int or type(i) == float for i in coordinates] and
    False not in [0 <= i <= limit for i, limit in zip(coordinates, arena_limits)])
  return valid

### distance ###################################################################
def distance (coordinates1, coordinates2, significance = 2):
  '''
  use pythag to return distance between coordinates1 and coordinates2
  round to significance
  '''
  return round(((coordinates1[0] - coordinates2[0])**2 + (coordinates1[1] - coordinates2[1])**2)**.5, significance)

#@title Tabulate
def tabulate (blank = "-", **kwargs):

  rows    = kwargs.get('rows', [])
  headers = list(kwargs.get('headers', []))
  title = kwargs.get('title', "Tabulated Display")

  print (title)
  if rows:

    if not headers:                                                               #this is quite expensive, but works. Best solution is to be explicit with required headers.
      for row in rows:
        for key in row.keys():
          if key not in headers:
            headers.append(key)

    # row = {}
    # header = ''
    # a = round(row.get(header),2) if type(row.get(header)) is float else row.get(header,blank)

    value_widths  = [max([len(repr(round(row.get(header),2) if type(row.get(header)) is float else row.get(header,blank))) for row in rows]) for header in headers]
    header_widths = [len(repr(header)) for header in headers]
    column_widths = [max([w1,w2]) for w1, w2 in zip (value_widths, header_widths)]

    head = "".join ([f"{header:<{width}} " for header, width in zip(headers, column_widths)])

    print (head)
    print (len(head) * "_")

    for row in rows:
      r = "".join ([f"{str(round(row.get(header),2) if type(row.get(header)) is float else row.get(header,blank)):<{width}} " for header, width in zip(headers, column_widths)])
      print (r)
  else:
    print ("No row data or column headers to tabulate data")


# Test data commented out - was running at import time
# tabulate (blank = "nul", rows = rows, headersX = ['kind', 'name', 'status', 'age', 'soc', 'capacity'])

#@title Energy Consumption Factors

# speed_factor
# calculates energy factor as a function of speed

coefficents = [0.014, 1.87, -1.12, 0.28]   # 3rd order polynomial coefficients
def speed_factor(v):
  f = sum([v**i * c for i, c in enumerate(coefficents)])
  return f

#weight factor kWh / kg / unit distance
weight_factor = 0.01

def flight_factor (volitant):
  return [1, 1.5][int(volitant)]

def energy_consumption (weight, speed, volitant):
    ec = weight * weight_factor * speed_factor(speed) * flight_factor(volitant)
    return ec


#@title Size Releated variables

def weight_fromsize(size, volitant):
  weight = size**2 / (2000 if volitant else 1000)
  return weight

def size_variables (size, volitant):
  variables = {}
  variables['weight'] = weight_fromsize ( size, volitant)
  variables['max_payload'] = variables['weight'] / 2
  variables['max_soc'] = variables['weight'] * (4 if volitant else 3)
  return variables

#@title Object Definitions

kinds = dict(
  Robot     = 'Bot',
  Droid     = 'Bot',
  Drone     = 'Bot',
  Pizza     = 'Deliverable',
  Charger   = 'Station',
  NZCharger = 'Station',
  Repair    = 'Station',
  Recycling = 'Station')

statuses = {
	'Bot':		     ['off', 'on', 'broken'],
	'Deliverable': ['ready', 'dispatched', 'in_transit', 'delivered'],
	'Station':     ['vacant', 'occupied']}

# Activites are used by bots only
activities =     ['idle', 'available','delivering', 'collecting', 'charging', 'busy',  'is_cargo', 'under_repair', 'moving']

# @title Validation

#Ecosystem Validation Lambda Expresssions (lambda inputs: output)

inlist =      lambda value, rule: value in rule                                 # rule is a list or tuple of valid items
inrange =     lambda value, rule: rule[0] <= value <= rule[1]                   # rule is a tuple (min, max)
length =      lambda value, rule: rule[0] <= len(value) <= rule[1]              # rule is a tuple (min, max)
nochange =    lambda value, rule: value == rule                                 # rule is the old value from the register
none =        lambda value, rule: True                                          # no rule or value required, always true
objects =     lambda value, rule: all([getattr(c, rule[0], None) == rule[1] for c in value])       # rule is a tuple (attribute, value)
validxy =     lambda value, rule: all([0 <= c <= limit for c, limit in zip(value, arena_limits)])  # rule not required

validation_functions = {                                                        # so we can store lambda/function names as string literals
    'none':       none,
    'inlist':     inlist,
    'nochange':   nochange,
    'inrange':    inrange,
    'validxy':    validxy,
    'length':     length,
    'objects':    objects}

validation_lists = {                                                            # so we can store the validation list names as string literals
    'kinds':              kinds,
    'kind_classes':       kinds.values(),
    'colors':             colors,
    'shapes':             shapes,
    'activities':         activities,
    'bot_status':         statuses['Bot'],
    'deliverable_status': statuses['Deliverable'],
    'station_status':     statuses['Station']}

def validation (value, function_name, rule):

  function = validation_functions[function_name]
  if function_name == 'inlist': rule = validation_lists [rule]
  return function (value, rule)

#@title Default Table
#Date:12/03/2023 18:54
#don't paste! Some rad changes made here
#Deliverable- contractor; weight and size made class attributes
#Bot cargo is now a list but not used (initially), new attribute - contracts, also a list
#coords None

default_table = [
  [ 'object',      'attribute',   'default',             'rule',        'validation','read', 'type',      'description' ],
  [ '*',           'kind',        None,                  None,          'nochange',  'r',    'string',    'Type of object (class)' ],
  [ '*',           'kind_class',  None,                  None,          'nochange',  'r',    'string',    'Parent class of kind' ],
  [ '*',           'coordinates', None,                  None,          'validxy',   'w',    'list',      'x, y of location' ],
  [ '*',           'status',      None,                  None,          'nochange',  'r',    'string',    'thing status' ],
  [ '*',           'age',         0,                     None,          'nochange',  'r',    'integer',   'age of thing' ],
  [ '*',           'alpha',       1,                     None,          'nochange',  'r',    'float',     'arena display transparency' ],
  [ '*',           'color',       'blue',                'colors',      'inlist',    'w',    'string',    'arena display colour' ],
  [ '*',           'name',        'thing',               (2, 20),       'length',    'w',    'string',    'named of robot' ],
  [ '*',           'on_arena',    False,                 None,          'nochange',  'r',    'boolean',   'True if on the arena' ],
  [ '*',           'shape',       'square',              'shapes',      'inlist',    'w',    'string',    'arena display shape' ],
  [ '*',           'annotation',  ['status'],            None,          'none',      'w',    'list',      'annotation to display on arena' ],
  [ 'Bot',         'status',      'off',                 'bot_status',  'inlist',    'w',    'string',    'bot status'],
  [ 'Bot',         'activity',    'idle',                'activities',  'inlist',    'w',    'string',    'current activity of thing'],
  [ 'Bot',         'active',      0,                     None,          'nochange',  'r',    'integer',   'active hours' ],
  [ 'Bot',         'cargo',       [],      ('kind_class','Deliverable'),'objects',   'w',    'list',      'list of objects robot is transporting'],
  [ 'Bot',         'contracts',   [],      ('kind_class','Deliverable'),'objects',   'w',    'list',      'list of objects robot is contracted to deliver'],
  [ 'Bot',         'damage',      0,                     None,          'nochange',  'r',    'integer',   'damage points accrued by bot' ],
  [ 'Bot',         'destination', None,                  None,          'none',      'w',    'list',      'x, y  of  destination' ],
  [ 'Bot',         'distance',    0,                     None,          'nochange',  'r',    'float',     'distance travelled by robot' ],
  [ 'Bot',         'energy',      0,                     None,          'nochange',  'r',    'float',     'energy consumed by robot' ],
  [ 'Bot',         'max_payload', 0,                     None,          'nochange',  'r',    'integer',   'maximum payload' ],
  [ 'Bot',         'payload',     0,                     None,          'nochange',  'r',    'integer',   'current payload' ],
  [ 'Bot',         'max_soc',     0,                     None,          'nochange',  'r',    'integer',   'maximum state of charge' ],
  [ 'Bot',         'units_delivered',       0,                     None,          'nochange',  'r',    'integer',   'number of items delivered by bot' ],
  [ 'Bot',         'weight_delivered',      0,                     None,          'nochange',  'r',    'integer',   'weight of items delivered by bot' ],
  [ 'Bot',         'service_freq',720,                   None,          'nochange',  'r',    'integer',   'service frequency' ],
  [ 'Bot',         'serviced',    0,                     None,          'nochange',  'r',    'integer',   'age of robot at last service' ],
  [ 'Bot',         'soc',         0,                     None,          'nochange',  'r',    'integer',   'state of charge of battery' ],
  [ 'Bot',         'station',     None,                  'object',      'none',      'w',    'object',    'station robot is heading for' ],
  [ 'Bot',         'speed',       0,                     (0, 1),        'inrange',   'w',    'integer',   'current speed' ],
  [ 'Bot',         'max_speed',   0,                     None,          'nochange',  'r',    'integer',   'maximum speed' ],
  [ 'Bot',         'volitant',    False,                 None,          'nochange',  'r',    'boolean',   'Indicates if bot flys' ],
  [ 'Bot',         'weight',      0,                     None,          'nochange',  'r',    'integer',   'weight of Bot' ],
  [ 'Robot',       'color',       'red',                 'colors',      'inlist',    'w',    'string',    'arena display colour' ],
  [ 'Robot',       'resources',   [70, 4, 5, 1, 20, 1],  None,          'nochange',  'r',    'list',      'Percent materials' ],
  [ 'Robot',       'shape',       'square',              'shapes',      'inlist',    'w',    'string',    'arena display shape' ],
  [ 'Robot',       'size',        500,                   (100,1000),    'inrange',   'i',    'integer',   'arena display size' ],
  [ 'Robot',       'speed',       0,                     (0, 1),        'inrange',   'w',    'integer',   'current speed' ],
  [ 'Droid',       'color',       'blue',                'colors',      'inlist',    'w',    'string',    'arena display colour' ],
  [ 'Droid',       'resources',   [70, 4, 5, 1, 20, 1],  None,          'nochange',  'r',    'list',      'Percent materials' ],
  [ 'Droid',       'shape',       'circle',              'shapes',      'inlist',    'w',    'string',    'arena display shape' ],
  [ 'Droid',       'size',        400,                   (100,1000),    'inrange',   'i',   ' integer',   'arena display size' ],
  [ 'Droid',       'speed',       0,                     (0, 2),        'inrange',   'w',    'integer',   'current speed' ],
  [ 'Drone',       'color',       'yellow',              'colors',      'inlist',    'w',    'string',    'arena display colour' ],
  [ 'Drone',       'resources',   [5, 4, 70, 1, 20, 1],  None,          'nochange',  'r',    'list',      'Percent materials and energy' ],
  [ 'Drone',       'shape',       'triangle',            'shapes',      'inlist',    'w',    'string',    'arena display shape' ],
  [ 'Drone',       'size',        300,                   (100,1000),    'inrange',   'i',    'integer',   'arena display size' ],
  [ 'Drone',       'speed',       0,                     (0, 3),        'inrange',   'w',    'integer',   'current speed' ],
  [ 'Drone',       'volitant',    True,                  True,          'nochange',  'r',    'boolean',   'Indicates if bot flys' ],
  [ 'Deliverable', 'destination', None,                  'none',        'none',      'r',    'list',      'x, y  of  destination' ],
  [ 'Deliverable', 'contractor',   None,                 'none',        'none',      'r',    'object',    'object allocated to delivery'],
  [ 'Deliverable', 'size',        200,                   (100,1000),    'inrange',   'i',    'integer',   'arena display size' ],
  [ 'Deliverable', 'weight',      50,                    (10, 100),     'inrange',   'r',    'integer',   'Pizza' ],
  [ 'Deliverable', 'annotation',  ['status'],            None,          'none',      'w',    'string',    'annotation to display on arena' ],
  [ 'Pizza',       'color',       'white',               'colors',      'inlist',    'w',    'string',    'arena display colour' ],
  [ 'Pizza',       'shape',       'circle',              'shapes',      'inlist',    'w',    'string',    'arena display shape' ],
  [ 'Pizza',       'resources',   [0, 0, 0, 0, 1, 5],    None,          'nochange',  'r',    'list',      'Percent materials and energy' ],
  [ 'Station',     'resources',   [5, 4, 70, 1, 20, 1],  None,          'nochange',  'r',    'list',      'Percent materials and energy' ],
  [ 'Station',     'capacity',    1,                     None,          'nochange',  'r',    'integer',   'max number of station users' ],
  [ 'Station',     'annotation',  ['status'],            None,          'none',      'w',    'string',    'annotation to display on arena' ],
  [ 'Charger',     'capacity',    1,                     None,          'nochange',  'r',    'integer',   'occupancy' ],
  [ 'Charger',     'color',       'blue',                'colors',      'inlist',    'w',    'string',    'arena display colour' ],
  [ 'Charger',     'shape',       'diamond',             'shapes',      'inlist',    'w',    'string',    'arena display shape' ],
  [ 'Charger',     'size',        400,                   (100,1000),    'inrange',   'i',    'integer',   'size of object' ],
  [ 'NZCharger',   'capacity',    1,                     None,          'nochange',  'r',    'integer',   'occupancy' ],
  [ 'NZCharger',   'color',       'green',               'colors',      'inlist',    'w',    'string',    'arena display colour' ],
  [ 'NZCharger',   'shape',       'diamond',             'shapes',      'inlist',    'w',    'string',    'arena display shape' ],
  [ 'NZCharger',   'size',        300,                   (100,1000),    'inrange',   'i',    'integer',   'arena display size' ],
  [ 'Repair',      'capacity',    1,                     None,          'nochange',  'r',    'integer',   'occupancy' ],
  [ 'Repair',      'color',       'red',                 'colors',      'inlist',    'w',    'string',    'arena display colour' ],
  [ 'Repair',      'shape',       'diamond',             'shapes',      'inlist',    'w',    'string',    'arena display shape' ],
  [ 'Repair',      'size',        300,                   (100,1000),    'inrange',   'i',    'integer',   'arena display size' ],
  [ 'Rycycling',   'capacity',    1,                     None,          'nochange',  'r',    'integer',   'occupancy' ],
  [ 'Rycycling',   'color',       'pink',                'colors',      'inlist',    'w',    'string',    'arena display colour' ],
  [ 'Rycycling',   'shape',       'diamond',             'shapes',      'inlist',    'w',    'string',    'arena display shape' ],
  [ 'Rycycling',   'size',        300,                   (100,1000),    'inrange',   'i',    'integer',   'arena display size' ],
]


################################################################################
# @title Default Registers
################################################################################

def register_default (kind, mode = 'register'):
  """
  Function to return a default register (a dictionary of attributes and default
  values) or a validation dictionary containing validation rules, for an
  ecosystem thing

  Arguments:
  kind - they kind of thing for which the default register is required
  mode - indicates if a default register or a validation dictionary is required (default 'register')

  This function uses the master 'default_table list and is regularly called by
  the ecosystem to instantiate objects and check and enforce default values.

  It is quite expensive and therefore a cacheing mechanism has been implemented
  so that it dictionary is only ever constructed once.
  """

  def cache_dictionary (kind, mode):
    kind_class = kinds[kind]
    if mode == 'dictionary':
      t = default_table
      cols = t[0]
      d = {r[1]: {k: v for k, v in zip(cols[2:], r[2:])} for r in t[1:] if r[0] in [kind, kind_class, "*"] }
      d['kind']['default']       = kind
      d['kind_class']['default'] = kind_class
      d['status']['default']     = statuses[kind_class][0]
      d['name']['default']       = kind.lower()
      cache['dictionary'][kind]  = d
    else:
      dictionary = cache['dictionary'].get(kind)
      if not dictionary:
        dictionary = cache_dictionary(kind, 'dictionary')                       # recursive call
      if mode == 'register':
        d = {k: v['default'] for k, v in dictionary.items()}
        if kind_class == "Bot": d['max_speed'] = dictionary['speed']['rule'][1] # ensure max_speed is reflective of the speed rule
        cache['register'][kind] = d
      elif mode == 'validation':
        d = {k: (v['validation'], v['rule'], v['type'], v['read']) for k, v in dictionary.items()}
        cache['validation'][kind] = d
    return deepcopy(d)

  cache = register_default.cache

  d = cache[mode].get(kind)
  if not d:                                                                     # dictionary is not cached yet
    d = cache_dictionary (kind, mode)


  return deepcopy(d) if mode =="register" else d                                # always return deep copy of register due to mutable values

register_default.cache = {'register': {}, 'validation': {}, 'dictionary': {}}   # create a cache attribute for the function

#%matplotlib inline

import matplotlib.markers as mmarkers

class Bot():
  #dummy Bot pending class definitions
  counter = {}
  ecosystem = None

########################################################
# @title Ecosystem Class
########################################################
class Ecosystem:
  '''
  The ecosystem class is the is used to instantiate an ecosystem.
  The eco system is a virtual environment in which users create and manage
  different types of automated bots (robots). The main task for bots is to
  create contracts to deliver items, usually pizzas, which the ecosystem
  creates.

  Whilst going about this daily task bots consume resources and accrues a
  performance record of pizza delivered by weight and number.

  Users can configure the number or robots and some of their capabilities such
  as maximum payload, speed and size.

  Users can visualise the ecosystem using the display method, and configure the
  duration of the ecosystem. The ecosystem may come to premature end however if
  all the bots are broken or otherwise inactive.
  '''

  ##############################################################################
  # Embedded classes
  ##############################################################################
  class _Thing():
    counter = {}
    ecosystem = None
    def __init__(self, register):
      self.__class__.counter.setdefault(self.__class__.__name__, 0)     #if first use then make sure counter is present
      self.__class__.counter[self.__class__.__name__] += 1
      self.__dict__ = register                                          #use the passed registry as the attributes
      self.__class__.ecosystem.register(self, register)

  ##############################################################################
  # Constructor
  ##############################################################################
  def __init__(self, **kwargs):

    '''
    The constructor accepts the following kwargs which determine the operation
    of the ecosystem:

    name              type     default description
    --------------------------------------------------------------------------
    duration          integer    168    maximum duration of ecosystem in hours
    max_weight        integer    20     maximum weight of deliverables
    delivery_rate     integer    10
    debug             True/False False  print messages in real time
    show              integer    1      (see display method)
    message_on        True/False True   cache messages

    The following kwargs can also be passed:
      mode, width, height, pause, title, clear, hour, brightness, facecolor,
      annotations.

    These are passed to the display function and are described there.
    '''

    #Attributes or properties

    self._min_weight = 10                                                       # minimum weight of deliverables
    self._hour = 0                                                              # current hour of ecosystem
    self.start_time = 0                                                         # clock time stamp of first update (hour zero)

    # Attributes configurable by Kwargs
    self.duration = str(kwargs.get('duration', 1)) + " week"                    # maximum duration of ecosystem (default 1 week)
    self._max_weight = kwargs.get('max_weight', 20)                             # maximum weight of deliverables
    self._delivery_rate = kwargs.get('delivery_rate', 10)                       # items created for delivery each per day
    self._debug = kwargs.get('debug', False)                                    # causes messages to print in real time as will as added to the queue
    self._show = kwargs.get('show', 1)                                          # display when modulus hour % show = 0
    self._messages_on = kwargs.get('messages_on' ,True)                         # switch message caching on (True) [default] or off (False)
    self.duration = kwargs.get('duration', 24 * 7)                              # maximum duration of ecosystem (decorated setter)

    # These are permitted kwargs for the display function
    self._permitted_display_kwargs = {
      'width': 'width of the display arena',
      'height': 'height of display arena',
      'pause': 'duration of pause to view display in ms',
      'title': 'title of the display',
      'clear': 'clear the Jupyter Notebook output cell before displaying',
      'hour': 'current hour',
      'brightness': 'brightness of display (not in use)',
      'facecolor': 'color of the display arena surface',
      'annotations': "annotation setting (none, 'label', 'value')",
      'annot_xy': 'spacing between marker and annotation (dx, dy)',
      'placeholders': 'ecosystem attributes for inserting into title place holders'}

    # Attributes passed to display function.
    self._display_properties = {key: value for key, value in kwargs.items() if key in self._permitted_display_kwargs}

    self._things = []                                                           # cache of created things - bots, deliverables, stations
    self._Things = {}                                                           # cache of object types, Things for new creating new things
    self._registry = {}                                                         # The registry contains the dictionaries of all things in the ecosystem!
    self._messages = []                                                         # message cache
    self._delivered = {}                                                        #cache of delivered objects transferred from live register
    self._distancelog = [1]
    self._distancelog_max = 5
    self._permitted_placeholders = ('active', 'count_bots', 'count_broken', 'count_deliverables', 'count_off', 'count_on', 'count_stations', 'duration', 'hour', 'stop')

    #Set object class attributes to the ecosystem for reference by all instances
    self._Thing.ecosystem = self
    # Bot = kwargs.get("Bot") 
    # Bot.ecosystem = self

    self._start_coordinates = None

 ###############################################################################
 # Decorated Properties   ##
 ###############################################################################


  ### Active (property get)############### #####################################
  @property
  def active(self):
    '''
    returns True if distance log shows activity and the hour is less
    than the set ecosystem duration.
    '''
    return sum(self._distancelog) > 0 and self._hour < self._duration

  ### Debug (property) #########################################################
  @property
  def debug(self):
    '''
    Get the debug property
    '''
    return self._debug
  @debug.setter
  def debug(self, value):
    self._debug = value

  ### Hour (property) ##########################################################
  @property
  def hour(self):
    '''Returns the current hour of the ecosystem'''
    return self._hour

  @property
  def stop(self):
    ''' returns True if the ecosystem hour is equalt to the set duration'''
    return self._hour >= self._duration

  ### Display Properties #######################################################

  @property
  def display_properties(self):
    '''
    Current set of properties configured for the display function
    See display method
    '''
    return self._display_properties

  ### Duration (property) ######################################################
  @property
  def duration(self):
    '''
    The duration of the ecosystem is the maximum number of hours the
    to ecosystem will run. It can be set on instantiation using a kwarg.
    '''
    return self._duration

  @duration.setter
  def duration(self, value):
    '''
    The duration of the ecosystem is the maximum number of hours the
    to ecosystem will run. It can be set on instantiation using a kwarg.
    '''
    #convert duration in to hours if y, m, w or d used to markup the passed time
    if type(value) == int:
      self._duration = value
    elif type(value) == str:
      value, period = tuple(value.split())
      self._duration = int(value) *  {'y': 365*24, 'm': 31*24, 'w': 7*24, 'd': 24, 'h':1}[period[0]]
    self._duration

  ### Show (property) ##########################################################
  @property
  def show(self):
    '''
    Get the show property
    '''
    return self._show
  @show.setter
  def show(self, value):
    self._show = value


  ### Timer  (property) ########################################################
  @property
  def timer (self):
    '''
    returns the elapsed time in hours, minutes and seconds since the first
    update (hour = 0).
    '''
    elapsed = round(time.time() - self.start_time)
    return time.strftime("%Hh%Mm%Ss", time.gmtime(elapsed))


  ### Title  (property) ########################################################
  @property
  def title(self):
    '''
    Set the title for the display function
    This updates the display properties
    See display method
    '''
    return self._display_properties.get('title',"Ecosystem Display | hour: {hour}")
  @title.setter
  def title(self, value):
    self._display_properties['title'] = value

  ### Messages  (property) #####################################################
  @property
  def messages(self):
    '''
    Return all messages in the messages list as a string, one line per message

    THe list is a log of messages which shows key ecosystem events. Once
    accessed and returned the messages cache is emptied.

    Messages are characterised in to one of the following types:
      'damage', 'info', 'broken', 'warning', 'error'
    '''
    text = ''
    while self._messages:
      message = self._messages.pop(0)
      hour, message_type, name, id, function, comment = message                 # messages are a tuple of 5 objects unpacked as follows
      try:
        text += f'{hour:<5}{message_type:<8} {repr(name):<14} {str(id):<16} {function[:15]:<15} {comment}' + '\n'
      except Exception as e:
        text += "Exception formatting message tuple:\n"
        text += str([message_type, name, id, function, comment]) + '\n' + repr(e) + '\n'
    return text

  ### Message  (property get and set) ##########################################
  @property
  def message (self):
    '''
    Return oldest message in the messages list
    '''
    try:
      return self._messages.pop(0)
    except:
      return None

  @message.setter
  def message(self, value):
    if self._messages_on:
      try:
        if value[0] in ('damage', 'error', 'info', 'broken', 'warning'):
          self._messages.append ((self.hour,) + value)
      except TypeError:
        self._messages.append ("error", "ecosystem", self.title, "message", "Bad message tuple " + repr(value))
    if self._debug and value[0] in ('damage', 'error'):
      print ((self.hour,) + value)

  ### Messages On  (property get and set) ######################################
  @property
  def messages_on(self):
    '''
    True - messages are cached
    False - messages are ignored
    It can be useful to turn messages off (set messages_on to False) for long
    ecosystem runs.
    '''
    return self._messages_on
  @messages_on.setter
  def messages_on(self, value):
    self._messages_on = value

  @property
  def count_on (self):
    return self.count(status = 'on')
  @property
  def count_off (self):
    return self.count(status = 'off')
  @property
  def count_broken (self):
    return self.count(status = 'broken')
  @property
  def count_bots(self):
    return self.count(kind_class = 'Bot')
  @property
  def count_deliverables(self):
    return self.count(kind_class = 'Deliverable')
  @property
  def count_stations(self):
    return self.count(kind_class = 'Station')

################################################################################
# METHODS (Public)
################################################################################

  # contract (Method)
  ##############################################################################

  def contract(self, bot, d, mode = 'agree'):

    '''
    The contract method is used (by bots) to formally manage delivery contracts
    with the ecosystem.

    Arguments - to manage a contract a bot makes a contract method call passing
    itself, bot, the deliverable, d, and the 'mode' as arguments. The mode
    represents the three stages of the contract process as follows:

    agree (default) - this establishes a delivery contract. If agreed the bot is
    formally entered in the deliverable's attributes as the contractor. The
    ecosystem checks if the bots maximum payload is less than the item's weight.
    If heavier the contract will be refused.

    collect - a contract collect call is made when the bot arrives at the
    deliverable to pick it up. The ecosystem checks the bot is the agreed
    contractor, is co-located with the item, and ensures the bot has spare
    capacity in its cargo hold by checking the curernt cargo weight. Collection
    is unsuccesful if these checks fail. If succesful, the deliverable is placed
    in the bots cargo list.

    complete - a contract complete call can be made when the deliverable has
    reached its destination coordinates in the bot's cargo list. The ecosystem
    checks the bot is the agreed contractor, is at the destination. If true
    the contract is complete, the cargo unloaded, the delivered tallies are
    incremented.

    cancel - a contract can be cancelled in which case the deliverable has its
    contractor attribute set to None and is made available.
    '''
    def payload(bot):
      return sum([deliverable.weight for deliverable in bot.cargo])

    # agree --------------------------------------------------------------------
    if mode == "agree":
      if d.weight > bot.max_payload:
        self.message = ("warning", bot.name, id(bot), "contract", f"{bot.name} was refused contract for {d.name}. Weight {d.weight} exceeds maximum payload {bot.max_payload}).")
        return False                                                            #unsuccessful contract agreement
      else:
        d.contractor = bot                                                      #note - bot is responsible for managing its contracts and is advised to update its contracts list.
        d.status = "dispatched"
        d.shape = 'circle'
        d.size = 200
        d.color = 'pink'
        self._registry[id(d)] = d.__dict__  #update the registry
        self.message = ("info", bot.name, id(bot), "contract", f"{bot.name} has agreed contract for delivery of {d.name}")

        self.create_thing("Pizza")    # replace contract agreement with a new deliverable to keep the ecosystem supplied with deliverables to contract for.
        return True     #successful contract agreement

    # collect ------------------------------------------------------------------
    elif mode == "collect":
      if d.contractor is bot:
        if d in bot.cargo:
          self.message = ("warning", bot.name, id(bot), "contract", f"{bot.name} has already {d.name} in the cargo hold.")
        else:
          if same_coordinates(bot.coordinates, d.coordinates):
            if (payload(bot) + d.weight) > bot.max_payload:                     # check bot has enough capacity in cargo hold
              self.message = ("warning", bot.name, id(bot), "contract", f"{bot.name} refused permission to load {d.name}. Payload {payload} would exceed maximum payload {bot.max_payload}).")
            else:
              d.status = "in_transit"
              d.size = 125
              d.shape = 'square'
              d.color = 'pink'
              d.coordinates = bot.coordinates  # deliverable should move with bot!
              self.message = ("info", bot.name, id(bot), "contract", f"{bot.name} has collected for delivery of {d.name}")
              self._registry[id(d)] = d.__dict__  #update the registry
              bot.cargo.append (d)
              self._registry[id(bot)]['cargo'] = bot.cargo
              bot.payload = payload(bot)
              self._registry[id(bot)]['payload'] = bot.payload                  # note payload is a read-only writable value so needs reflecting to the register
              return True   #successful fulfillment
          else:
            self.message = ("warning", bot.name, id(bot), "contract", f"{bot.name} is at the wrong location to collect for delivery of {d.name}")
      else:
        self.message = ("warning", bot.name, id(bot), "contract", f"{bot.name} is not a party so not permitted to collect for delivery of {d.name}")
        return False  #unsuccessful fulfilment attempt

    # complete -----------------------------------------------------------------
    elif mode == "complete":
      if d.contractor is bot:
        if same_coordinates(bot.coordinates,d.destination):                     #note cannot use d.coordinates as preferred because es.update has not synchronised movements
          d.contractor = None                                                   #note - bot is responsible for managing its contracts and is advised to update its contracts list.
          d.status = "delivered"
          d.color = "white"
          d.shape = 'circle'
          d.alpha = delivered_fade
          d.end = self.hour
          d.coordinates = d.destination                                         # disassociate d coordinates from the bot
          self.message = ("info", bot.name, id(bot), "contract",
                          f"{bot.name} has fulfilled contract for delivery of {d.name}")
          self._registry[id(d)] = d.__dict__                                    # update the deliverable registry

          bot.units_delivered += 1                                                    # increment delivered tally by one
          bot.weight_delivered += d.weight                                                # weight_delivered according to weight of deliverable
          bot.cargo.pop(bot.cargo.index(d))                                     # remove from the cargo hold
          self._registry[id(bot)]['units_delivered'] = bot.units_delivered                  # reflect delivered to registry to prevent accusations of cheating
          self._registry[id(bot)]['weight_delivered'] = bot.weight_delivered                        # reflect weight_delivered to registry to prevent accusations of cheating #todo implement generic registry reflection for permitted changes by the es
          self._registry[id(bot)]['cargo'] = bot.cargo                          # reflect cargo to registry
          bot.payload = payload(bot)
          self._registry[id(bot)]['payload'] = bot.payload                      # note payload is a read-only writable value so needs reflecting to the register

          return True   #successful collection
        else:
          self.message = ("warning", bot.name, id(bot), "contract", f"{bot.name} has not fulfilled contract for delivery of {d.name}")
      else:
        self.message = ("warning", bot.name, id(bot), "contract", f"{bot.name} is not a party so not permitted to complete contract for delivery of {d.name}")
        return False  #unsuccessful complete attempt

    # cancel -------------------------------------------------------------------
    elif mode == "cancel":
      if d.contractor is bot:
        d.contractor = None   #note - bot is responsible for managing its contracts and is advised to update its contracts list.
        d.status = "ready"
        self.message = ("info", bot.name, id(bot), "contract", f"{bot.name} has cancelled contract for delivery of {d.name}")
        self._registry[id(d)] = d.__dict__  #update the registry
        return True   #successful cancellation
      else:
        self.message = ("warning", bot.name, id(bot), "contract", f"{bot.name} is not a party so not permitted to cancel contract for delivery of {d.name}")
        return False  #unsuccessful cancellation

    else:
      raise Exception(f"'{mode}' is not a valid mode parameter for contract method")

  # Count (Method)
  ##############################################################################
  def count (self, **kwargs):
    '''
    count returns a count of the number of registry items returned by a call to
    the registry. Thus is works like a registry call but returns a number of
    registry entries instead of the actual register.
    '''

    return len(self.registry(**kwargs))

  # create thing (method)
  ##############################################################################
  def create_thing(self, kind, coordinates = [0,0,0], **kwargs):
    '''
      This method is use to create ecosystem object instances of the kind_class
      Deliverable or Station.

      In this version of the ecosystem only Deliverables of kind Pizza and
      stations of kind Charger are operable.

      To call this method you must specify an object kind. Stations must have
      x, y coordinate whereas deliverables are randomly located.

      The method returns the thing that was created.
    '''

    # Thing classes are cached in _things with kind as the key.
    # create_Thing is only called on first Thing use if not in the cache
    def create_Thing(kind):
      # registry = register_default(kind)
      Thing = type(kind, (self._Thing,), {})
      # self._Things[kind] = (Thing, registry)  #cache this definition
      self._Things[kind] = Thing  # cache this definition
      return Thing

    # Here we get the Thing class from the _Things dictionary. If not yet there it is created and added by create_Thing
    # caution: _things is the list of things created from a Thing cached in the _Things dictionary
    try:
      #Thing, registry = self._Things[kind]
      Thing = self._Things[kind]
    except Exception as e:
      # Thing, registry = create_Thing(kind)
      Thing = create_Thing(kind)
    register = register_default(kind)
    if register['kind_class'] == 'Deliverable':
      #deliverables and destinations are always randomly placed
      register['destination'] = random_coordinates()
      register['coordinates'] = random_coordinates()
      register['weight'] = randint(self._min_weight, self._max_weight)
    else:
      register['coordinates'] = [ c for c in (coordinates + [0, 0])[:3]]
    register['start'] = self.hour
    register['name'] += str(self._Thing.counter.setdefault(kind, 1))

    #Create the instance. Note we do this last since it will auto register with all the attributes
    thing = Thing(register)     #Use a copy - caught out here by mutability!

    return thing

  #   display (method)
  ##############################################################################
  def display (self, **kwargs):
    '''
    The ecosystem display method calls the display function. This uses
    matplotlib to display the ecosystem arena with markers for bots,
    deliverables, and stations along with their respective annotations.

    The display method is generally called whenever the ecosystem update method
    is called. The show parameter can regulate this to be less
    frequent (see below) as required.

    When the ecosystem is instantiated any kwargs intended for the display
    function are retained in the display properties dictionary.

    These can be added to, or updated, by a display method call with the same
    set of permitted kwargs: mode, width, height, pause, title, clear, hour,
    brightness, facecolor, and annotations. See the display function help for
    further detail of these arguments.

    show is an integer n where 0 <= n <= duration
    -----
    This determines the frequency of how often the ecosytem displays the arena:
      0                   no display
      1 <= n <= duration  display every nth update hour

    Note that if the hour reaches the ecosystem duration value and show > 0 then
    the display method is executed.

    '''
    if kwargs:
      self._show = kwargs.get('show', self._show)
      self._display_properties.update({key: value for key, value in kwargs.items() if key in self._permitted_display_kwargs})       #overwrite or add current display_properties with permitted kwarg values

    if self._show and (self.hour % self._show == 0 or (self._show and self.hour == self.duration)):
      markers =  self._registry.values()
      placeholders = [word[1:-1] for word in self.title.split() if word[0] == "{" and word[-1] == "}"]              #title can have fields defined by {} like an f-string. Resolved by format
      if placeholders:
        self._display_properties['placeholders'] = {placeholder: getattr(self, placeholder,"#err#") for placeholder in placeholders if placeholder in self._permitted_placeholders}
      self._display(markers, **self._display_properties)

  #   Print Messages (method)
  ##############################################################################

  def print_messages (self):
    if self._messages:
      print(self.messages)


  #   Register (method)
  ##############################################################################

  def register (self, thing, register = None):
    '''
    register creates a registry entry for an ecosystem thing (bots,
    deliverables, and stations). This is a deep copy of the instance attributes
    (see registry).

    The method is called automatically by the Bot child classes (Robot, Droid
    and Drone) upon instantiation. Users should ensure they do not
    impair this registration process. In order for it to operate, all Bots and
    child classes must inherit the ecosystem class variable which is set on
    instantiation of an ecosystem.

    Part of registration is to validate all attributes by applying rules as
    documented in te default table. This means respecting read only (r)
    attributes (cannot be altered by bots) and the rules for writable (w)
    attributes.

    Size is a special writable attribute (w0) which may only be
    altered at or just after instantiation. Parameters which depend on
    size (weight, max_soc, max_payload) are also updated.
    '''

    if thing in self._things:
      self.message = ('warning', thing.name, id(thing), 'register', f"{thing.name} is already registered." )
    else:

      if not register:                                                          # ecosystem classes (stations and deliverable) pass their creation register but bots need one to compare with the class defintions
        register = register_default (thing.kind)                                # get a new register entry for validation purposes

      if kinds[thing.kind] == "Bot":

        variables = size_variables (thing.size, thing.volitant)                 # calculate size related variables using the global function size_variables (weight, max_soc, max_payload)
        variables['coordinates'] = copy(thing.coordinates)                      # register needs the starting coordinate
        variables['soc'] = variables['max_soc']
        self._register_changes (thing, register, **variables)

        self._start_coordinates = thing.coordinates                             # used for assessment

      if self._validate (thing, register):                                      # validate returns true if everything accepted
        self.message = ('info', thing.name, id(thing), 'register', f"Registration of {thing.name} of class {thing.kind} was succesful with status {thing.status}." )
      else:
        self.message = ('info', thing.name, id(thing), 'register', f"Registration of {thing.name} of class {thing.kind} result in permanent damage due to invalid attributes.")
        self._register_changes (thing, register, status = "broken")             # this will trigger 50% alpha and blackening

      register.update(thing.__dict__)                                           # update the register from the things attributes
      self._registry[id(thing)] = deepcopy(register)                            # append the register to the registry
      self._things.append(thing)




  #   Register Changes (protected method)
  ##############################################################################
  def _register_changes (self, thing, register, **kwargs):

    '''
    Make changes permitted by the ecosystem to a thing's attributes and
    reflect these changes to the things register in registry

    Note that since these are mutable no need to return the updates
    '''
    #triggers

    if thing.kind_class == "Bot":
      if kwargs.get('status') == 'broken': kwargs.update({'alpha': 0.5, 'color': 'black'})
      if kwargs.get('damage'):  # assume this is a damage increment
        pass

    register.update(copy(kwargs))
    thing.__dict__.update(kwargs)


  #   Deregister (undocumented method)
  ##############################################################################
  def deregister (self, *args):
    '''(not documented)'''
    for thing in args:
      try:
        del self._registry[id(thing)]
        self._things.remove(thing)
        del thing
      except:
        pass


  #   Registry (Method)
  ##############################################################################
  def registry(self, **kwargs):
    '''
    The registry method returns a copy of the ecosystem registry in which
    object instances are registered.

    The registry entry of each object instance consists as an up to date copy
    of its dictionary of attributes (properties); more formally a copy of its
    dictionary attribute' __dict__'. The whole ecosystem registry is a
    dictionary of such disctionaries, where the object instance's ID is the key.

    Thus, using the syntax: ecosystem.registry[id(object)] will return the
    dictionary for that object.

    The registry can be filtered using kwargs to return any subset of registered
    object instances e.g. to return a registry of only drones one can write:

    drones = ecosystem.registry(kind = 'drone')
    '''
    if kwargs == {}:
      return self._registry
    else:
      try:
        # The value is a register and is a dictionary. Each one passes the filter if all the key values in kwargs match the key values in the register
        return {key: value for key, value in self._registry.items() if (all([value.get(filter_key) == filter_value for filter_key, filter_value in kwargs.items()]))}
      except Exception as error:
        return "Could not filter register using "   + str(kwargs) + ' ' + str(error)

  #   Tabulate
  ##############################################################################

  def tabulate (self, *attributes, **kwargs):
    '''

    Tabulate will print or return the text of a tabular view of registry data
    with attributes as column headers and values in a rows for each thing.

    attributes - list of columns which will be used in the table (*args)
    kwargs     - used to filter the registry for things of interest

    If no attributes are passed, then all the columns in the registry will be
    tabulated.
    '''
    title = kwargs.pop('title', "Tabulated Data")
    rows =  list(self.registry(  **kwargs).values())                              # convert to a list otherwise we have a dicvalue generator object
    headers = list(attributes) or (list(rows[0].keys()) if rows else [])          # derive headers from first row if none specified
    tabulate (headers = headers, rows = rows, title = title)


  #   Things and related lists (Method)
  ##############################################################################
  def things(self, **kwargs):
    '''
    The things method returns a reference to the things list. This is a Python
    list to which all ecosystem objects (bots, deliverables, and stations) are
    automatically appended after their instantiation.

    Users use the list to access, and itereate, objects instances as required.

    kwargs are used to filter the lists for specific attributes. For example
    ecosystem.things(kind = 'drone') returns Bot instances of child class drone.

    using filter tuples
    -------------------

    Normally kwargs are equality filters. This means in the above example things
    are returned where kind == 'drone'. The things function also implements
    comparative filters by passing a tuple as a keywork argument. The tuple
    is of the form (operator, value). The operator is a string representing the
    permitted operators '>', '>=', '<', '<='. Calling things with kwargs:

    ecosystem.things(kind = 'drone', weight = (">", 40))

    returns a list of drones with a weight greater than 40.

    common use case shortcuts
    -------------------------

    Three common use cases are to filter things to return lists of bots,
    deliverables or stations, e.g. things( kind_class = 'Bot'). For this purpose
    the ecosystem provides three methods to return specific object classes:

      bots()            equivalent to things(kind_class = 'Bot')
      deliverables()    equivalent to things(kind_class = 'Deliverable')
      stations()        equivalent to things(kind_class = 'Station')

    These can be filtered with kwargs in the same way as things()
    '''
    # this implements the new truth function which allows comparison tumple as a key work argument value
    return [thing for thing in self._things if all( [truth(getattr(thing, key, None), value) for key, value in kwargs.items()])]

  def deliverables (self, **kwargs):
    '''See the things method'''
    kwargs.update({'kind_class': 'Deliverable'})
    return self.things (**kwargs)

  def bots (self, **kwargs):
    '''See the things method'''
    kwargs.update({'kind_class': 'Bot'})
    return self.things (**kwargs)

  def chargers (self, **kwargs):
    '''See the things method'''
    kwargs.update({'kind': 'Charger'})
    return self.things (**kwargs)

  def _fifo_list (self, v):
    if len(self._distancelog) > self._distancelog_max:
      self._distancelog.pop(0)
    self._distancelog.append(v)
    return sum(self._distancelog)

  # update (method)
  ##############################################################################

  def update(self, show = None):

    '''
    The update method reflects the advancement of time in the ecosystem by one
    hour. Several key process occurs

    show: if not None this updates the show (display) parameter (see display
    method)

    All bot attributes are verified and reflected to the ecosystem registry
    Illegal changes are cancelled and damages are logged
    energy consumption is calculated and recorded
    Bots which have no soc are rendered 'broken'
    Charging is actioned and recorded.
    Deliverable which are delivered are faded and eventually removed.
    New deliverables are create according to the delivery rate for the ecosystem

    '''
    if self._hour == 0:
      self.start_time = time.time()

    self._hour += 1                                                             # increment the hour

    if show: self._show = show

    update_distance = 0                                                         # so we can see if anything is moving

    for robot in self.bots():                                                   # note - robots now contains pizzas, so use the internal property which filters
      register = self._registry[id(robot)]                                      # get the current dictionary copy from ecosystem register

      if register['status'] == 'broken':                                        # bot already registered as broken
        robot.status = 'broken'                                                 # do not allow user 'unbreaking'
      if register['status'] == robot.status:                                    # no change in status
        if robot.status == "on":
          changes_permitted = True
        else:
          changes_permitted = False
      else:                                                                     # status switched
        if robot.status == "on":                                                # bot has just gone on so we have to register changes
          changes_permitted = True
        else:                                                                   # bot has just gone off but we have to register changes
          changes_permitted = True

      self._register_changes (robot, register, age = robot.age + 1)             #register age increment

      if self._validate (robot, register, changes_permitted):

        # ecosystem approves all changes to writable attributes
        pass

      if changes_permitted:                                                  # increment active hours count if on
        robot.active += 1

        cargo_weight = 0
        for d in robot.cargo:
          cargo_weight += d.weight                                              # sum weigh of cargo deliverables
          d.coordinates = robot.coordinates                                     # ensure cargo moves with the bot

        #Station (Charging)
        if robot.station:
          if robot.station.status == 'vacant':
            if same_coordinates (robot.station.coordinates, robot.coordinates):
              robot.station.status = 'occupied'
              robot.station.occupant = robot
              robot.station.color = 'cyan'
              robot.station.size = 500
              self.message = ("info", robot.name, id(robot), "update", f"{robot.name} has arrived for charging at {robot.station.name}")
          elif robot.station.status == 'occupied':
            if robot.station.occupant is robot:
              delivered_charge = robot.max_soc - robot.soc                      # todo - create station attribute to account for energy use
              robot.soc = robot.max_soc
              robot.station.status = 'vacant'
              robot.station.occupant = None
              robot.station.color = 'blue'                #todo this should use default
              robot.station.size = 250
              self.message = ("info", robot.name, id(robot), "update", f"{robot.name} has charged by {delivered_charge} to {robot.soc} at {robot.station.name}")
          self._registry[id(robot.station)] = robot.station.__dict__

        update_distance += robot.speed                                          # increment the aggregated update distance for movement detection

        weight = robot.weight + cargo_weight
        motion_energy = energy_consumption (weight, robot.speed, robot.volitant)# kWh note speed is calculated by trusted validate method

        energy = int(min(motion_energy, robot.soc))                             # Only subtract remaining charge if energy consumed is greater
        robot.energy += energy
        robot.soc -= energy

        if robot.soc < 1:
          if robot.station is not None and same_coordinates(robot.station.coordinates, robot.coordinates):
            #low charge robot is in queue for charger so do not break
            self.message = ('warning', robot.kind, robot.name, 'update', 'out of power in charger queue')
          else:
            robot.damage = max_damage
            self.message = ('damage', robot.kind, robot.name, 'update', 'out of power')

        if robot.damage >= max_damage:
          self.message = ('broken', robot.kind, robot.name, 'update', 'max damage score')
          robot.status = 'broken'

        if robot.status == 'broken':
          robot.alpha = 0.5
          robot.color = 'black'
          robot.speed = 0
        else:
          robot.alpha = m_fade * robot.soc/robot.max_soc + c_fade               # alpha determines display the transparency of robots. Running out of fuel makes robots fade


        register.update(copy(robot.__dict__))                                   # update the registry entry
      # End of status == on block
      else:                                                                     # validation failed - nothing to do here since validation now roll's back errant changes
        pass

    delivered = self.registry(kind_class = 'Deliverable')                       # update deliverables

    for d_id, register in delivered.items():
      alpha = register.get('alpha')
      if alpha <= delivered_fade:

        if alpha <= 0:
          self._delivered[d_id] = self._registry.pop(d_id)                      # transfer to delivered list
        else:
          alpha = max(alpha - delivered_fade_rate, 0)
          if alpha < 0.25: self._registry[d_id]['status'] = 'consumed'
          register['alpha'] = alpha

    self._update_distance = self._fifo_list (round(update_distance,2))
    if self._update_distance == 0:
      self.message = ('warning', "Ecosystem", id(self), 'update', f'No bots have moved for {self._distancelog_max} updates')
    if self._hour == self._duration:
      self.message = ('warning', "Ecosystem", id(self), 'update', f"Ecosystem has reached the set duration of {self._duration} hours")

    self.display()

  # validate (protected method)
  ##############################################################################
  def _validate (self, thing, register, changes_permitted = True):
    damage = 0
    validation_dict = register_default(thing.kind, 'validation')

    if thing.kind_class == "Bot":
      ds = distance(thing.coordinates, register['coordinates'])
      thing.speed = round(0.99 * ds,2)                                          # calculate speed (u = s / t  with unit time). 99% to prevent rounding issues
      thing.payload =  sum([deliverable.weight for deliverable in thing.cargo]) # calculate payload (read only but precaculated by contracts)
      coordinates = copy(register['coordinates'])                               # if damage occurs bot will be prevented from moving - this is the rollback value
      thing.distance += ds                                                      # increment distance travelled
      register['distance'] = thing.distance                                     # reflect back to register as it is read-only

    for attribute, validation_parameters in validation_dict.items():

      value = getattr(thing, attribute)                                         # get the new value from the thing's attributes.
      registered_value = register [attribute]                                   # get copy of the registered value from the thing's registry entry.

      if value != registered_value:                                             # the attribute has changed, so validate it

        function_name, rule, date_type, rw = validation_parameters              # unpack validation parameters from the tuple

        if rw  == 'r' or (rw == 'i' and thing.age > 0) or not changes_permitted:# r = read only, i = writable at instantiation, i.e read only after first update
          setattr(thing, attribute, copy(registered_value))                     # roll back the attribute back to the registered value
          damage += 1
          self.message = ('damage', thing.name, id(thing), 'validate', f"Attempt to change read-only registered value to {repr(value)} for '{attribute}' was disallowed at {self.hour}.")
        else:
          valid = validation (value, function_name, rule)
          if not valid:
            setattr(thing, attribute, copy(registered_value))                   # set the value back to the registered value
            damage += 1
            self.message = ('damage', thing.name, id(thing), 'validate', f"Attempt to change writable registered value to {repr(value)} for '{attribute}' was disallowed at {self.hour} ({function_name} rule:{rule}).")

    if damage:
      self._register_changes(thing, register, damage = register['damage'] + damage, coordinates = coordinates)# register a damage point
      valid = False
    else:
      valid = True

    return valid

  # display (Method)
  ##############################################################################
  def _display(self, markers, **kwargs):
    '''
    The display function displays all the things in the ecosystem registry which
    are currently visible. Things with an alpha value of 0 are rendered invisible.
    Deliverables are gradually faded after delivery so as not to simplify the
    display.

    markers - this is the values from the ecosystem registry dictionary and thus
    contains all essential information about each thing.

    kwargs - the following kwargs are passed by the ecosystem.display method.
    Note that these same kwargs can be passed by the user to the ecosystem either
    upon instantiation of the ecosystem, or, during an ecosystem.display() method
    call.

    width                width of the display arena
    height               height of the display arena
    pause                duration of pause to view display in ms
    title                title of the display area
    clear                clear the Jupyter Notebook output cell before displaying
    hour                 current hour of the day
    brightness           brightness of display (not in use)
    facecolor            color of the display arena surface
    annotations          annotation setting (None, 'label', 'value')
    annot_xy             spacing between marker and annotation (dx, dy)
    '''

    # self = display.__dict__   # this is to use the functions dict for static variables
    # self['arguments'] = ['width', 'height', 'pause', 'title', 'clear', 'hour', 'brightness', 'facecolor', 'annotations']

    CM = 1/2.54                                                                  # const for conversion cm to inches matplotlib works in inches but we pass in cm
    width =        kwargs.get('width', 30) * CM                                   # width of arena (inches)
    height =       kwargs.get('height', 15) * CM                                  # height of arena (inches)
    pause =        kwargs.get('pause', 100)                                       # pause whilst displaying in ms
    title =        kwargs.get('title','Ecosystem Display')                        # title of arena
    clear =        kwargs.get('clear', True)                                      # clear output cell before showing chart (Jupyter only)
    hour =         kwargs.get('hour', 12)                                         # current hour of the day
    brightness =   kwargs.get('brightness', False)                                # brightness on or off to reflect solar intensity
    facecolor =    kwargs.get('facecolor', 'white')                               # color of display
    annotations =  kwargs.get('annotations', 'label')                             # annotation switch  (None, 'label', 'value')
    annot_xy =     kwargs.get('annot_xy', (1,1,))                                 # annotation spacing from marker (dx, dy)
    placeholders = kwargs.get('placeholders', {})                                 # ecosystem attributes for inserting into title placeholders

    x_max = default_width
    y_max = default_height
    dx, dy = annot_xy

    # If you still run in Jupyter/Interactive Window, you may keep this (no harm in scripts either).
    # if clear:
    #   from IPython.display import clear_output
    #   clear_output(wait=True)

     # ---------- MVP change: create the figure ONCE, reuse thereafter ----------
    if not hasattr(self, '_fig') or self._fig is None:
      self._fig, self._ax = plt.subplots(figsize=(width, height))
      self._first_show = True
    else:
      # If width/height changed, update the existing figure size
      self._fig.set_size_inches(width, height, forward=True)

    fig = self._fig
    ax = self._ax

    # Clear the axes EACH FRAME so you don't accumulate artists
    ax.clear()

    # Re-apply styling each frame after clear()
    fig.patch.set_facecolor('grey')
    fig.patch.set_alpha(0.6)
    ax.patch.set_facecolor(facecolor)
    ax.patch.set_alpha(1)

    # Title / limits
    title = title.format(**placeholders)
    ax.set_title(title)
    ax.set_xlim(-2, x_max + 2)
    ax.set_ylim(-2, y_max + 2)

    # Draw markers
    for p in markers:
      try:
        x = p['coordinates'][0]
        y = p['coordinates'][1]
        scale = p['size']
        color = p['color']
        shape = p['shape']
        alpha = p['alpha']
        annot = p['annotation']
        marker_shape = mpl_shapes[shape]

        ax.scatter(x, y, s=scale, c=color, marker=marker_shape, alpha=alpha, edgecolors='b')

        if p.get('volitant', False):
          ax.scatter(x, y, s=scale * 3, c='k', marker='1', alpha=alpha)  # add helicoptor wings

        if annotations and p['status'] != 'in_transit':
          try:
            annotation = ';'.join(
              repr(p.get(label, '#err#')) if annotations == 'value'
              else label + ":" + repr(p.get(label, '#err#'))
              for label in annot
            )
            ax.annotate(annotation, (x + dx, y + dy), alpha=alpha)
          except Exception:
            pass

      except Exception as error:
        # Keep your original lenient error handling
        print(error)
        continue

    # Ticks / grid (after ax.clear())
    ax.set_xticks(range(0, x_max + 1, 10))
    ax.set_yticks(range(0, y_max + 1, 10))
    ax.grid(color='red', linestyle='--', linewidth=0.25)

    # ---------- MVP change: non-blocking show once, then refresh ----------
    if getattr(self, '_first_show', False):
      plt.show(block=False)
      self._first_show = False

    fig.canvas.draw_idle()
    fig.canvas.flush_events()
    plt.pause(pause / 1000)
    # time.sleep(pause / 1000)  # alternative if you prefer sleep over pause



















