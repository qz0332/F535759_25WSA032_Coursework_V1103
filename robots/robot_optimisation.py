import math
from .ecosystem.factory import *
from .ecosystem.ecosystem import distance, energy_consumption, same_coordinates

# Duration is set to two weeks for development and rapid testing. Set to 52 weeks for your final tests.

import matplotlib.pyplot as plt
plt.close('all')  # optional: cleans up leftovers from prior runs
plt.ion()         # interactive mode ON (non-blocking windows)

# Easily adjustable central-settings-esque variables for easy testing
ROBOTS = 3
DROIDS = 3
DRONES = 3
PIZZAS = 9

BASELINE_CHARGERS = [55, 20]

OPTIMISED_CHARGERS = [
    [60, 20],
    [20, 20]
]

HOME = [40, 20, 0]                     

# different bot types have different rates of discharge, so thresholds must vary accordingly to prevent bot breakage
CHARGE_THRESHOLDS = {
    "Robot": 0.25,
    "Droid": 0.20,
    "Drone": 0.35
}                                        


# Helper function to return fraction of remaining charge
def bot_get_charge(bot) -> float:
    return bot.soc / bot.max_soc


def choose_charger(bot, chargers) -> int:                                                                    
    # Return the index of the nearest charger#
    
    min_dist = math.inf
    min_index = -1
    
    for index, charger in enumerate(chargers):
        dist = distance(charger.coordinates, bot.coordinates)

        if dist < min_dist:
            min_dist = dist
            min_index = index

    return min_index


# Helper function to find and choose the nearest charger
def charge_from_nearest(bot, chargers):
    nearest_charger = choose_charger(bot, chargers)

    if nearest_charger != -1:
        bot.charge(chargers[nearest_charger])
    else:
        print("no chargers found !?")


def is_pizza_in_weight(pizza, bot):
    return pizza.weight <= (bot.max_payload - bot.payload)


def find_nearest_pizza(bot, pizzas) -> int:

    dist_min = math.inf
    nearest_pizza = -1 # Potentially a cause of crashing / failed interpretation - add bounds checking on access
    
    for pizza_index, pizza in enumerate(pizzas):
        if not is_pizza_in_weight(pizza, bot):
            continue # Skip pizzas that would overflow the payload

        if pizza.status != 'ready':
            #Only use ready pizzas
            continue

        dist = distance(pizza.coordinates, bot.coordinates)

        if dist < dist_min:
            dist_min = dist
            nearest_pizza = pizza_index
    
    return nearest_pizza


def has_charge_to_start_job(bot, pizza, chargers) -> bool:
    """
    estimate if the bot has enough charge to;
    1 . travel to the pizza 
    2. deliver said pizza
    3. keep a small emergency reserve afterwards
    """

    distance_to_pizza = distance(bot.coordinates, pizza.coordinates)
    distance_to_destination = distance(pizza.coordinates, pizza.destination)

    # The ecosystem consumes energy per update/hour, so estimate how many
    # movement updates the journey will take instead of multiplying by raw distance.
    hours_to_pizza = math.ceil(distance_to_pizza / bot.max_speed)
    hours_to_destination = math.ceil(distance_to_destination / bot.max_speed)

    # Bot travels empty to the pizza, then loaded to the destination.
    empty_energy_per_hour = energy_consumption(
        bot.weight + bot.payload,
        bot.max_speed,
        bot.volitant
    )

    loaded_energy_per_hour = energy_consumption(
        bot.weight + bot.payload + pizza.weight,
        bot.max_speed,
        bot.volitant
    )

    estimated_energy = (
        empty_energy_per_hour * hours_to_pizza +
        loaded_energy_per_hour * hours_to_destination
    )

    # Keep a reserve so the bot does not fully drain itself.
    reserve = bot.max_soc * 0.10

    return estimated_energy < (bot.soc - reserve)


def run_baseline(duration="1 week", show=0):
    """ 
    Runs the original baseline from ecosystem_operation to provide a comparison point:
    - one charger
    - fixed 20% charge threshold
    - first ready pizza allocation
    """

    es = ecofactory(
        robots=ROBOTS,
        droids=DROIDS,
        drones=DRONES,
        chargers=BASELINE_CHARGERS,
        pizzas=PIZZAS
    )

    charger = es.chargers()[0]

    es.display(show=show, pause=10)
    es.debug = False
    es.messages_on = False
    es.duration = duration

    charge_threshold = 0.20

    while es.active:
        for bot in es.bots():

            if bot.soc / bot.max_soc < charge_threshold and bot.station is None:
                bot.charge(charger)
        
            if bot.activity == "idle":
                for pizza in es.deliverables():
                    if pizza.status == "ready":
                        bot.deliver(pizza)
                        break
            
                if not bot.destination and not same_coordinates(bot.coordinates, HOME):
                    bot.target_destination = HOME
        
            if bot.target_destination:
                bot.move()
        
        es.update()

    return es


def run_optimized(duration="1 week", show=0):    
    """
    runs optimized version with the following:
    - multiple chargers
    - closest charger allocation
    - per bot charging thresholds
    - nearest pizza allocation 
    - weight filtering
    - charge check prior to taking contracts
    """

    es = ecofactory(
        robots=ROBOTS, 
        droids=DROIDS, 
        drones=DRONES, 
        chargers=OPTIMISED_CHARGERS, 
        pizzas=PIZZAS
    )
        
    es.display(show=show, pause=10)
    es.debug = False
    es.messages_on = False
    es.duration = duration

    while es.active:
        chargers = es.chargers()

        for bot in es.bots():

            threshold = CHARGE_THRESHOLDS.get(bot.kind, 0.20)

            # Charging optimisation
            if bot_get_charge(bot) < threshold and bot.station is None:
                charge_from_nearest(bot, chargers)

            # Pizza allocation optimisation
            if bot.activity == "idle" and bot.station is None:
                pizza_index = find_nearest_pizza(bot, es.deliverables())

                if pizza_index != -1:
                    pizza = es.deliverables()[pizza_index]

                    if has_charge_to_start_job(bot, pizza, chargers):
                        bot.deliver(pizza)
                    else:
                        charge_from_nearest(bot, chargers)

                elif not bot.destination and not same_coordinates(bot.coordinates, HOME):
                    bot.target_destination = HOME

            if bot.target_destination:
                bot.move()
        
        es.update()
        
    return es


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


if __name__ == "__main__":
  duration = "52 week"

  baseline_es = run_baseline(duration=duration, show=0)
  print_kpis(baseline_es, "Baseline")

  optimised_es = run_optimized(duration=duration, show=0)
  print_kpis(optimised_es, "Optimised")