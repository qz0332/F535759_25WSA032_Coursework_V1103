import math
from .ecosystem.factory import *

# Duration is set to two weeks for development and rapid testing. Set to 52 weeks for your final tests.

import matplotlib.pyplot as plt
plt.close('all')  # optional: cleans up leftovers from prior runs
plt.ion()         # interactive mode ON (non-blocking windows)

# Create and configure the ecosystem using the factory function. 
# Study the factory function code to understand how the ecosystem is being created 
# and configured. Adjust the parameters as needed for your testing and development.  
es = ecofactory(
            robots = 3, 
            droids = 3, 
            drones = 3, 
            chargers = [[60,20], 
                        [20, 20]], 
            pizzas = 9)



es.display(show = 1, pause = 10)                                                # show = 0 will turn off the display and speed up the run. Set to 1 for development and debugging, set to 0 for final runs. Note that when show = 0, you will not see the ecosystem or any messages, so it is wise to turn on messages (es.messages_on = True) when show = 0 for development and debugging. 
es.debug = True                                                            # this will directly display damage and warning messages. Note show needs to be zero  (show = 0)
es.messages_on = False                                                          # over 52 weeks it is wise to turn messages off as there are too many. But when researching turn on for shorter runs
es.duration = "1 week"                                                          # We are aiming to run for a year with minimum or no bot breakages

home = [40,20, 0]                                                               # Place to which bots will return when idle and from which they will start. This is also the location of the charger in this example, but it doesn't have to be. You can change this and the charger location to test the bots' ability to navigate around the ecosystem.
charge_threshold = 0.20    



# Helper function to return fraction of remaining charge
def bot_get_charge(bot) -> float:
  return (bot.soc / bot.max_soc)

def choose_charger(bot, chargers) -> int:                                                                    
    # Return the index of the nearest charger#
    
    min_dist = math.inf
    min_index = -1
    
    for index, charger in enumerate(chargers):
      dist = distance(charger.coordinates, bot.coordinates)

      if (dist < min_dist):
        min_dist = dist
        min_index = index

    return min_index


# Helper function to find and choose the nearest charger
def charge_from_nearest(bot, chargers):
  # Prior to being assigned a task, check charge
  nearest_charger = choose_charger(bot, chargers)
  # print(f'Nearest Charger Index: {nearest_charger}')

  if (nearest_charger != -1):
    bot.charge(chargers[nearest_charger])
  else:
    print("no chargers found !?")
    quit()
  

def is_pizza_in_weight(pizza, bot):
  return pizza.weight <= (bot.max_payload - bot.payload)

def find_nearest_pizza(bot, pizzas) -> int:

  dist_min = math.inf
  nearest_pizza = -1 # Potentially a cause of crashing / failed interpretation - add bounds checking on access
  
  for pizza_index, pizza in enumerate(pizzas):
    if (not is_pizza_in_weight(pizza, bot)):
      continue # Skip pizzas that would overflow the payload
    if (pizza.status != 'ready'):
      #Only use ready pizzas
      continue
    dist = distance(pizza.coordinates, bot.coordinates)
    if (dist < dist_min):
      dist_min = dist
      nearest_pizza = pizza_index
  
  return nearest_pizza

while es.active:
  for bot in es.bots():

    #create_deliverables(es)                                                     # Use the create deliverables function to maintain a stock of ready pizzas

    if bot_get_charge(bot) < charge_threshold and bot.station is None:  
      # decision to charge when percent soc = 20%. This can be optimised and varied for each kind (see stretch objective)
      # ISSUE - Optimise by charging near a station when no pizzas are near
      charge_from_nearest(bot, es.chargers())
      #bot.charge(charger)                                                       # initiate charging.
    if bot.activity == 'idle':                                                  # if bot is idle, contract to deliver a ready pizza.
        pizza_index = find_nearest_pizza(bot, es.deliverables())

        if pizza_index == -1:
          continue
        pizza = es.deliverables()[pizza_index]
        
        if pizza.status == 'ready':
          # ISSUE - non optimal, choose correct bot type
          bot.deliver(pizza)                                             # ensure we do not contract to deliver a pizza already contracted by another bot
          
        if not bot.destination and bot.coordinates != home:
          # IF A SLOWER BOT IS EN ROUTE, FASTER BOT TAKES OVER
          bot.target_destination = home                                           # if we get here, we've gone through the list of pizzas and none was ready
    if bot.target_destination:bot.move()                                        # move whilst we have a destination. At the end of delivery, the bot status will be set to idle

  es.update()                                                                   # update when all bots have been processed and moved



def print_kpis(es, label):
    bots = es.bots()

    delivered_units = sum(bot.units_delivered for bot in bots)
    delivered_weight = sum(bot.weight_delivered for bot in bots)
    total_distance = sum(bot.distance for bot in bots)
    total_energy = sum(bot.energy for bot in bots)
    total_damage = sum(bot.damage for bot in bots)
    broken_bots = sum(1 for bot in bots if bot.status == "broken")

    print(f"\n{label} KPI RESULTS")
    print("-" * 40)
    print(f"{'Delivered units':<25}{delivered_units}")
    print(f"{'Delivered weight':<25}{delivered_weight:.2f}")
    print(f"{'Total distance':<25}{total_distance:.2f}")
    print(f"{'Total energy':<25}{total_energy:.2f}")
    print(f"{'Total damage':<25}{total_damage}")
    print(f"{'Broken bots':<25}{broken_bots}")


print_kpis(es, "Optimized File")