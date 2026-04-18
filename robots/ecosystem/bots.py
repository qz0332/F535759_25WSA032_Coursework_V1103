"""
Bots Module

This module defines the Bot class and its child classes (Robot, Droid, Drone) for
use in the ecosystem. The Bot class serves as a base class for autonomous agents,
providing attributes and methods for tracking state, location, energy, and
performance metrics. The child classes inherit from Bot and specify unique 
characteristics such as color, shape, size, speed, and maximum speed.
The module also includes methods for charging, moving, delivering contracts, 
and displaying the bot's status. The bots interact with the ecosystem to
perform tasks such as charging at stations and delivering items based on contracts.
"""

from copy import copy
from robots.ecosystem.ecosystem import *

################################################################################
# Bot Base Class
################################################################################

class Bot():
  '''
    The Bot class serves as a parent or base class for autonomous agents in a simulated ecosystem.

    It provides a comprehensive set of attributes and methods for tracking a bot's state,
    location, energy, and performance metrics. It's designed to be inherited by child
    classes for specialized bot types.
  '''
  counter = {}
  ecosystem = None  #set to the ecosystem when the ecosystem is instantiated


  ### Constructor ##############################################################
  def __init__ (self):
    '''
        Initializes a new Bot instance.

        This constructor sets up all of the bot's core attributes, including its
        unique name, initial state, and various performance trackers.
    '''
    Bot.counter.setdefault(self.__class__.__name__, 0)    #if first use then make sure counter is present
    Bot.counter[self.__class__.__name__] += 1

    kind = self.__class__.__name__
    kind_class = kinds[kind]
    name = kind + str(Bot.counter[kind])                                   #default to kind and counter

    annotation = ['name', 'status', 'soc']

    self.kind =          kind            #  (r) Type of object (class)
    self.kind_class =    kind_class      #  (r) Parent class of kind
    self.coordinates =   None            #  (w) x, y of location
    self.status =        'off'           #  (w) thing status
    self.activity =      'idle'          #  (w) activity of bot
    self.age =           0               #  (r) age of thing
    self.alpha =         1               #  (r) arena display transparency
    self.color =         'blue'          #  (w) arena display colour
    self.name =          name            #  (w) named of robot
    self.on_arena =      False           #  (r) True if on the arena
    self.shape =         'square'        #  (w) arena display shape
    self.annotation =    annotation      #  (w) annotation of display marker
    self.active =        0               #  (r) active hours
    self.cargo =         []              #  (w) list of object robot is transporting
    self.contracts =     []              #  (w) list of object robot is contracted to deliver
    self.damage =        0               #  (r) damage points accrued by bot
    self.destination =   None            #  (w) x, y  of  destination
    self.distance =      0               #  (r) distance travelled by robot
    self.energy =        0               #  (r) energy consumed by robot
    self.max_payload =   0               #  (r) Maximum payload kg
    self.payload =       0               #  (r) current payload kg
    self.max_soc =       0               #  (r) Maximum state of charge
    self.units_delivered  =        0     #  (r) number of items delivered by bot
    self.weight_delivered =        0     #  (r) weight of items delivered by bot
    self.service_freq =  720             #  (r) service frequency
    self.serviced =      0               #  (r) age of robot at last service
    self.soc =           0               #  (r) state of charge of battery
    self.station =       None            #  (w) destination station for Bot
    self.speed =         0               #  (w) current speed
    self.max_speed =     0               #  (r) maximum speed
    self.volitant =      False           #  (r) Indicates if bot flys
    self.weight =        0               #  (r) weight of Bot


# Bot Class Properties
################################################################################
  @property
  def target_destination(self):
    '''
        A property to get the bot's current destination.

        This property returns the current coordinates the bot is moving towards.
    '''
    return self.destination

  @target_destination.setter
  def target_destination(self, destination):
    '''
        A setter for the bot's target destination.

        This method sets the bot's destination and updates its speed, status,
        and internal direction based on the new target coordinates.

        Args:
            destination (tuple): The (x, y) coordinates of the new destination.
    '''
    if same_coordinates(self.destination, destination):
      pass
    else:
      if not valid_coordinates (destination):
        self.destination = None
        self.speed = 0
        #self.status = 'off'
        if destination is not None:
          # raise warning Not deliberately invalid so we could raise warning here.
          pass
      else:
        self.destination = destination[:2]                                      # slicing forces a copy
        dx = self.destination[0] - self.coordinates[0]
        dy = self.destination[1] - self.coordinates[1]
        self.direction, self.target_distance = cartesian_compass(dx, dy)
        self.speed = self.max_speed                                             # default to max speed if given a target
        self.status = 'on'

# Bot Class Methods
################################################################################


  ### Charge ###################################################################
  def charge (self, charger = None):
    '''
      Initiates the bot's charging process at a specified charging station.

        This method sets the bot's destination to the charger's location and
        triggers its workflow to begin the charging activity.

        Args:
            charger (object=None): The charging station object to move to.
    '''
    if self.station is not charger:
      self.station = charger
      self.target_destination = copy(self.station.coordinates)
      self._workflow()
    else:
      charger = None

  ### Display ##################################################################
  def display (self, *args, **kwargs):
    '''
        Prints a formatted string displaying the bot's attributes.

        This method can display attributes in different modes (horizontal, all, full)
        for detailed status reports or debugging.

        Args:
            *args: Variable length argument list of attribute names to display.
            **kwargs: Arbitrary keyword arguments, including 'mode' and 'print'.
    '''
    mode = kwargs.get('mode', 'horizontal')
    if mode == 'all':
      attributes = {k: v for k, v in self.__dict__.items()}
    elif mode == 'full':
      dictionary = register_default(self.kind, 'dictionary')
      register = self.ecosystem.registry()[id(self)]
      attributes = {k: (v, dictionary[k]['read'], dictionary[k]['type'], dictionary[k]['description']) for k,v in register.items()}
    else:
      attributes = {k: v for k, v in self.__dict__.items() if k in args}
    c=" :"
    if mode == 'horizontal':
      n = 2
      h = "; "
      text = self.kind + ": "
      for key, value in attributes.items():
        text += (f"{key+c:<{n}}{repr(value)}{h}")
    else:
      la = max([len(attribute) for attribute in attributes])                    # max length of attribute name

      # print (">>",lv)
      # print (attributes.values())
      h = "\n"

      if mode == "full":
        lv = max([len(repr(value[0])) for value in attributes.values()])        # max length of attribute value
        text =  self.kind
        text+= f"\n{'attribute':<{la}} {'value':<{lv}} {'rw':<3} {'datatype':<10} {'description'}{h}"
        text+=  "_"*(la+lv+4+10+30) + "\n"
        for key, value in attributes.items():
          text += (f"{key:<{la}} {repr(value[0]):<{lv}} {value[1]:<4} {value[2]:<10} {value[3]}{h}")
      else:
        text = self.kind + "\n" + "__"*la*2 + "\n"
        for key, value in attributes.items():
          text += (f"{key:<{la}} {repr(value)}{h}")

    if kwargs.get('print', False):
      print(text)
    else:
      return (text)

  # Register (protected method)
  ##############################################################################
  def _register(self, **kwargs):
    '''
        Registers the bot with the ecosystem and updates its attributes.

        This method is a protected part of the bot's initialization process. It
        should not be called directly from outside the class.

        Args:
            **kwargs: Arbitrary keyword arguments used to override default attributes.
    '''
    for k, v in kwargs.items():
      if hasattr(self, k):
        setattr(self, k, v)
      else:
        #unexpected kwarg!
        self.ecosystem.message = ("error", self.kind, id(self), self.kind + ".register", f"Attribute '{k}' is not used by a {self.kind} object")
    self.name = self.name.format(counter = Bot.counter[self.kind])
    if self.coordinates == None: self.coordinates = random_coordinates()        # ensure bot appears on the arena of non-specific coordinates given in kwargs
    self.ecosystem.register(self)

  ### Move #####################################################################
  def move(self, destination = None):
    '''
        Moves the bot toward its target destination.

        This method handles the bot's movement logic, including checking for a
        valid destination and updating the bot's coordinates and distance.

        Args:
            destination (tuple=None): The (x, y) coordinates of the desired destination.
    '''

    dt = 1 # time interval (hours)
    #some code is so hard to read - what does this do!
    fly = lambda l, v: [int(v) if i == 2 else c for i, c in enumerate(l + [0]*(3-len(l)))][:3]

    if destination:
      self.target_destination = destination

    if self.target_destination is None:                                         # No destination - we're going no where!
      self.ecosystem.message = ("warning", self.name, id(self),"bot.move", "Attempt to move without a destination" )
      pass
    elif self.status == 'broken':
      self.ecosystem.message = ("warning", self.name, id(self),"bot.move", "Attempt to move whilst broken" )
    else:
      if self.target_distance <= self.speed * dt:                               # Bot in spitting distance of the destination, so plop down on to the destination co-ordinates
        self.coordinates[0] = self.destination[0]
        self.coordinates[1] = self.destination[1]
        if len(self.coordinates) > 2: self.coordinates[2] = 0
        self.target_distance = 0
        self.ecosystem.message = ("info", self.name, id(self),"bot.move", f"{self.name} has arrived at destination {self.destination} at {self.ecosystem.hour}")
        self._workflow()                                                        # arrived at destination so check if there are workflow steps to follow
      else:
        self.speed = self.max_speed                                             # we have a flaw in the ecosystem validation which sets speed to pythagorean value for speed checking
        self.coordinates = fly(self.coordinates, self.volitant)                 # Sets the 3rd coordinate to 1 if volitant - automatic take off on move
        dx, dy = compass_cartesian(self.direction, self.speed * dt)
        self.coordinates[0] += dx
        self.coordinates[1] += dy
        self.coordinates = [round (c, 2) for c in self.coordinates]
        self.target_distance -= self.speed * dt
        #self.ecosystem.message = ("info", self.name, id(self),"bot.move", f"{self.name} is at {self.coordinates} heading for {self.destination}, speed {self.speed}, at {self.ecosystem.hour}")

  ### Deliver Contract to deliver ##############################################

  def deliver (self, deliverable):
    '''
        Attempts to complete a delivery contract for a given deliverable.

        This method checks for an existing contractor and attempts to 'agree'
        or 'collect' the contract with the ecosystem.

        Args:
            deliverable (object): The object being delivered.

        Returns:
            bool: True if the contract is accepted, False otherwise.
    '''
    if deliverable.contractor is None:
      if self.ecosystem.contract(self, deliverable , 'agree'):
        self.contracts.append(deliverable)    #contract is agreed - you must add to contracts or cancel contract
        self._workflow()
        return True
      else:
        self.ecosystem.message = ("warning", self.kind, id(self), self.kind + ".contract", f"contract refused for {deliverable.kind}.")
        return False
    else:
      if deliverable.contractor is self:
        self.ecosystem.message = ("warning", self.name, id(self), self.kind + ".contract", f"{deliverable.kind} is already in contracts list.")
      else:
        self.ecosystem.message = ("warning", self.name, id(self), self.kind + ".contract", f"{deliverable.kind} already has a contractor {deliverable.contractor.name}.")


  ### Workflow #################################################################

  def _workflow (self):
    '''
        An internal method that defines the bot's action logic for a single step.

        This method is the core decision-making logic. It determines whether the
        bot should charge, collect a contract, or deliver a contract based on its
        current status and state.
    '''

    if self.station:                                                            # We have a station and have arrived at it
      if self.station.kind == "Charger":
        if self.soc / self.max_soc > 0.90:                                      # should be 100% but choosing 90% as a safety threshold
          self.station = None
          self.activity = "charged"
          self._workflow()                                                      # bot charged so try recursive call to workflow to reset activity
        else:
          self.target_destination = self.station.coordinates
          self.activity = "charging"


    elif self.contracts:                                                        # We have delivery contracts in the contract list
      deliverable = self.contracts[0]                                           # Get the first contract in the contracts list

      if same_coordinates(self.coordinates, deliverable.destination):           # bot at deliverable destination then complete contract
        if self.ecosystem.contract(self, deliverable, 'complete'):
          self.contracts.pop(self.contracts.index(deliverable))
          self._workflow()                                                        # this will pick up the next deliverable contract if present

      elif same_coordinates(self.coordinates, deliverable.coordinates):         # bot is co-located with the deliverable,so collect, or continue if on board
        if (deliverable in self.cargo or                                        # this occurs if already carrying the deliverable and resuming from charging or
            self.ecosystem.contract(self, deliverable, 'collect')):             # bot has arrive at the deliverable to complete collection paperwork and load up for contract
            self.target_destination = copy(deliverable.destination)
            self.activity = 'delivering'
        else:
          #contract should be suspended
          pass
      else:
        self.target_destination = copy(deliverable.coordinates)
        self.activity = 'collecting'

    else:                                                                       # move method complete - destination reached with no contracts or stations to visit
      self.target_destination = None
      self.activity = "idle"
      self.status = 'off'

      pass

################################################################################
# Robot Child Class
################################################################################
class Robot(Bot):

  ### Constructor ##############################################################
  def __init__(self, **kwargs):

    super().__init__()  #get the Bot defaults

    self.color =         'red'                #  (w) arena display colour
    self.resources =     [70, 4, 5, 1, 20, 1] #  (r) Percent materials
    self.shape =         'square'             #  (w) arena display shape
    self.size =          500                  #  (w0) arena display size
    self.speed =         0                    #  (w) current speed
    self.max_speed =     1                    #  (r) maximum speed

    self._register(**kwargs)     #over-write with kwargs and register

################################################################################
# Droid Child Class
################################################################################
class Droid(Bot):

  ### Constructor ##############################################################
  def __init__(self, **kwargs):

    super().__init__()  #get the Bot defaults

    self.color =         'blue'               #  (w) arena display colour
    self.resources =     [70, 4, 5, 1, 20, 1] #  (r) Percent materials
    self.shape =         'circle'             #  (w) arena display shape
    self.size =          400                  #  (w) arena display size
    self.speed =         0                    #  (w) current speed
    self.max_speed =     2                    #  (r) maximum speed

    self._register(**kwargs)     #over-write with kwargs and register

################################################################################
# Drone Child Class
################################################################################
class Drone(Bot):

  ### Constructor ##############################################################
  def __init__(self, **kwargs):
    super().__init__()  #get the Bot defaults

    self.color =         'yellow'             #  (w) arena display colour
    self.resources =     [5, 4, 70, 1, 20, 1] #  (r) Percent materials and energy
    self.shape =         'triangle'           #  (w) arena display shape
    self.size =          300                  #  (w) arena display size
    self.speed =         0                    #  (w) current speed
    self.max_speed =     3                    #  (r) maximum speed
    self.volitant =      True                 #  (r) Indicates if bot flys

    self._register(**kwargs)     #over-write with kwargs and register

