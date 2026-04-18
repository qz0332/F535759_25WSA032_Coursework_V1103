##############################################################
# Ecosystem Factory Function 
##############################################################

from .ecosystem import *
from .bots import *

def ecofactory(**kwargs) :
  """
  Create and configure an ecosystem using the provided parameters.

  This function generates a preconfigured ecosystem by creating robots, droids,
  and drones according to the specified numbers or sizes. It returns an instance
  of the Ecosystem class populated with the generated robots and other components.

  Keyword Args:
    robots (list or int):     Number of robots or list of robot sizes.
    droids (list or int):     Number of droids or list of droid sizes.
    drones (list or int):     Number of drones or list of drone sizes.
    pizzas (int):             Number of pizzas to create.
    chargers (list or tuple):
                              single charger x, y coordinate e.g. [40,20], or
                              tuple of charger x, y coordinates e.g. ([20,20], [60,20])
  Returns:
    Ecosystem: An instance of the Ecosystem class with configured components.
  """
  print ("Creating ecosystem with parameters:", kwargs)  # Debug statement to show input parameters
  es = Ecosystem()

  Bots = [Robot, Droid, Drone]

  es = Ecosystem()

  for B in Bots:
    # Set the ecosystem reference for each bot class to ensure they can interact with the ecosystem instance.
    B.ecosystem = es

  factory  = {'robots':[Robot, 'rob'], 'droids':[Droid, 'drd'], 'drones':[Drone, 'drn']}
  for kind, values in factory.items():
    values.append(kwargs.get(kind, 0))

  es.display(show = 0, clear = True, annotations = 'value' )
  es.title = "Ecosystem time {hour} of {duration} | Bots: {count_bots}"

  for Kind, name, iterator in factory.values():
    if type(iterator) is int: iterator = range(iterator)
    for item in iterator:
      attributes = {'status': 'on', 'name': name + "{counter}"}
      if type(iterator) is list: attributes.update({'size': item})
      bot = Kind(**attributes)

  chargers = kwargs.get('chargers', [])  #this should be list of coordinates'
  if len(chargers) == 2 and all(isinstance(c, int) for c in chargers): chargers = (chargers,)
  if all([isinstance(item,list) and len(item) == 2 and all(isinstance(i, int) for i in item) for item in chargers]):
    for charger in chargers:
      es.create_thing("Charger", charger)

  for i in range(kwargs.get('pizzas', 0)):
    es.create_thing("Pizza")

  return es

