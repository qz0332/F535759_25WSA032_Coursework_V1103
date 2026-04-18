from robots.ecosystem.factory import ecofactory

# Duration is set to two weeks for development and rapid testing. Set to 52 weeks for your final tests.

import matplotlib.pyplot as plt
plt.close('all')  # optional: cleans up leftovers from prior runs
plt.ion()         # interactive mode ON (non-blocking windows)

# Create and configure the ecosystem using the factory function. 
# Study the factory function code to understand how the ecosystem is being created 
# and configured. Adjust the parameters as needed for your testing and development.  
es = ecofactory(robots = 1, droids = 1, drones = 1)

#charger = es.chargers()[0]
es.display(show = 1, pause = 10)                                                # show = 0 will turn off the display and speed up the run. Set to 1 for development and debugging, set to 0 for final runs. Note that when show = 0, you will not see the ecosystem or any messages, so it is wise to turn on messages (es.messages_on = True) when show = 0 for development and debugging. 
es.debug = False                                                                # this will directly display damage and warning messages. Note show needs to be zero  (show = 0)
es.messages_on = False                                                          # over 52 weeks it is wise to turn messages off as there are too many. But when researching turn on for shorter runs
es.duration = "1 week"                                                          # We are aiming to run for a year with minimum or no bot breakages

home = [40,20, 0]                                                               # Place to which bots will return when idle and from which they will start. This is also the location of the charger in this example, but it doesn't have to be. You can change this and the charger location to test the bots' ability to navigate around the ecosystem.
charge_threshold = 0.20   

for bot in es.bots():
  for k,v in bot.__dict__.items():
    print (f"{k:<20}:{v}")