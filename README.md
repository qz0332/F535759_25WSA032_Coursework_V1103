# 25WSA032 COURESWORK - QZ0332 - SZYMON KALUZA

## Overview 

This repo contains my semester 2 coursework for PSE. It includes the following:

 - Task 1: Git source control 
 - Task 2: Arduino temperature optimisation
 - Task 3: RObot delivery optimisation
 - Task 4: Data analytics and visualisation (taken from task 2)

Structure:

F535759_25WSA032_Coursework/
├── .git/                              
├── arduino/
│   └── temperature_optimisation.ino  ← Task 2 
├── documentation/
│   └── (your documentation files)
├── robots/
│   └── robot_optimisation.py         ← Task 3 
├── Task 4 Deliverables/.             ← Task 4 contents
└── README.md                         


# Task 2: Arduino Temperature Optimisation

Here i implemented a temperature monitoring system using an arduino & the grove tempereature sensor provided
This has 3 modes;
    - Active Mode: used when temperature variation is high
    - Idle Mode: used when temperature variation is moderate
    - Power Down Mode: used when temperature variation is very stable (low)

## Memory Usage 

Arduino has a very low amount of RAM and it is hence very limited, meaning I had to take memory efficiency into account. 

The vast chunk of memory is occupied by the following:
    - temperature samples
    - DFT frequency values
    - DFT magnitude values
    - recent temperature variation values for moving average

As large arrays occupy lots of memory, i tried my best to minimize them. This was done both by using a smaller time, and hence lower sample count, 
as well as using the first half of the DFT magnitudes as they are mirrored. This let me cutdown from, at its peak, 180% of memory usage, to 50%.

# Task 3: Robot delivery optimisation 

Task 3 optimmises the robot pizza delivery ecosystem. The original system uses one charger, a fixed 20% threshold to charge, and first-come-first-serve pizza allocation

My optimised system changes this by using: 
    - multiple chargers
    - nearest charger selection
    - different charging thresholds for each bot type
    - nearest ready pizza allocation
    - battery check before accepting jobs

Aim was to reduce wasted travel distance, decrease the possibility of a bot running out of charge and improve job allocation to hence improve delivery performance

## Charging optimisation
The baseline system uses one charger and a fixed charging threshold, in order to improve overall efficiency, i added multiple chargers and made it so that the bot would go to the nearest charger rather than looking for a specific one. This hence then decreases travel time, which increases the amount of jobs that can be done !
Different bot types also use different thresholds for charging as they have varying capacities, speeds; this all contributes to a different amount of energy used.

## Pizza allocation optimisation 

Instead of assigning the first available pizza, i chose to have it search for the nearest pizza that the bot can carry, without exceeding its limit. This reduces any unnecessary travel before collection can happen. Also checks if the pizza is within capacity -> Avoids null contracts

## KPI Comparison

These were the following parameters:
 - Robots: 3
 - Droids: 3
 - Drones: 3
 - Charger Location(s): (55, 20)

 Baseline KPI RESULTS
----------------------------------------
Delivered units          1463
Delivered weight         22017.00
Total distance           98562.76
Total energy             115620.00
Total damage             15
Broken bots              3

Optimised KPI RESULTS
----------------------------------------
Delivered units          3028
Delivered weight         45095.00
Total distance           139078.75
Total energy             141698.00
Total damage             0
Broken bots              0

Going from Baseline -> Optimised. 
- There was a 106.9% increase in pizza's delivered
- There was a 104.8% increase in weight delivered
- There was a 41.1% increase in travel distance
- There was as 22.6% increase in Energy generated
There was then a 100% drop in both damage, and broken bots.

As can be seen, this is a very significant jump and improvement. 

# Task 4: Data analytics and Visualisation
Task 4 uses temperature data collected from task 2. It was a 3 minute sampling of the temperature outside my window (second floor) and saved into a CSV file to be parsed through in order to plot the data via matplotlib.
This generates the following:
- Temperature vs Time
- DFT Magnitude vs Frequency
- Original vs smoothed tempreature
- Histogram of temperature readings
- Temperature change rate vs time

Results showed general stability between 8-9 degrees Centigrade, but there were a couple of spikes to ~7 and ~11. This is likely gusts of wind or warm air from people below me (?).

# How to run

## Task 2:
1. Open **temperature_optimisation.ino** in Arduino IDE, or via platformIO, whatever works. 
2. Connect the grove tempreature sensor to A0, assuming you have the grove shield.
3. Upload the sketch **temperature_optimisation.ino** to the arduino after selecting the correct board.
4. Open serial monitor to view live results.

## Task 3:

Run the following command in terminal
**python3 -m robots.robot_optimisation**
Outputs are also displayed in terminal.

## Task 4:

This was pre processed, no need to run.

very fun coursework 10/10 recommend, thumbs up