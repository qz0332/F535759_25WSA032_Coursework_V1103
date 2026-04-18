# **Bot Pizza Delivery Optimisation**

## **Overview**
In this task you will work with a code base in which you will develop a number of classes which represent robots. These robots will deliver pizza's within a defined robot **ecosystem**. However, they do not organise themselves very efficiently - in fact they do not organise themselves at all - they just follow the code's instructions. Your job is to rewrite those instructions so they do it better. This is explained in more detail below.

The code base contains several key python modules which you will use in your own code:
- ecosystem
- bots
- factory

Your code will import these module or object from them. A code module which uses these is available to study and run. 

## **The Ecosystem**

The ecosystem is a virtual environment in a virtual universe in which virtual bots are created by the programmer. The ecosytem enforces rules if the bots follow, or they can come to a premature demise. It is up to the programmer to programme their bots to follow system rules. A well programmed bot _colony_ can thrive and prosper; if it is poorly programmed it may not perform so well.

There are a number of system indicators which measure the health of the ecosystem. These are recorded by the ecosystem. Students can interogate this data and display them in meaninful ways.

## **Bots**

This section contains class definition for the robot classes. These are carefully designed to function within the Ecosystem.

Study the design of the robot classes here. You should identify the following OOP features which were covered in the Python Introductory course:

  * The use of a parent or **base** robot class called ```Bot```
  * The use of child or **derived** bot classes of which there are three:
      - Robot
      - Droid
      - Drone
  * The use of partial inheritance of the base class constructor method using super().__init__
  * The inheritance of key Bot methods by the main robot child classes.
  * The use of encapsulation on some of the properties

You may develop these classes further to achieve coursework objectives as long as they remain functional within the robot ecosystem. You must not refactor (modify) the ecosystem to suit your own requirements.

As part of the general documentation requirements (task 1) you may modify the Bot class below to insert _DocStrings_ as appropriate.

## Factory Function

In software programming, a factory is a construct (often a class or method) whose responsibility is to create and return object instances.
Instead of directly calling constructors the factory provides a convenient method to instantiate an ecosystem and bots which you can then operate in a structured way. The use of this is shown in the demo.

## The Demo

The demo is a top level main module which will use the factory to create an ecosystem and populate it with bots and _pizzas_. The task of bots is to deliver pizzas to target destinations. The code is well documented and you should '_train_' yourself as an ecosystem operator by varying parameters you use for the factory method. You will be provided with some training exercises in the laboratory session to enhance your understanding.

## Performance Enhancement 

It should not escape your notice, in watching some of the bot activities, that some '_decisions_' made by the colony are probably not the best. Much could be done to improve the performance, and yield better key performance indicators (_**KPIs**_). Your core task is to improve the performance. 

But how might bot decision making be improved to improve performance - and how do we measure it using KPIs? You must study the section on Bot KPIs which is also relevant to task 4.

Much of this centres around pizza allocation and collection, and journeys to the charging station. As a stretch target there is also the contracting with the ecosystem of delivering larger (heavier) pizzas.

Below are some ideas on performance optimisation. You do not need to implement all of these ideas to do well in this task. Remember also to tell your development story with Git as per task 1.

> ### **Charging**
The second area is charging optimisation. There are three possible areas to develop: decision threshold, charger availability, and opportunistic charging

> #### **Threshold**

 The decision making for charging is currently fixed at a 20% threshold; for all kinds of bot. This is not necessarily well researched, but simply a heuristic evaluation of when the bots rarely run out of battery and break. Furthermore, bots of different kinds will probably require different thresholds.

> #### **Charger Availability**

The demo uses one centrally located charger. What if there were two or even three or four chargers distributed over the arena and the bot chose the nearest one? We would need to develop an algorythm to choose the nearest charger but once chosen charging would become a quicker turn around and the bot could get on with the delivery job again.

Furthermore, always-closer chargers should significantly lower the charging decision threshold since we can guarantee getting there sooner with a lower required soc. This will reduce charging frequency and thereby further elevate efficiency KPIs.

> #### **Opportunistic Charging**

Why pass close to, or even pass right over a charger when on a delivery journey without stopping to charge? Opportunistic charging could save unnecessary travelling to a charging station.

> ### **Pizza Allocation**

Right at the begining of a 'run' you may have 15 idle bots and 15 ready pizzas. The create_deliverables function will always create enough ready pizzas in advance, one for each idle bot. Allocation of a pizza to a bot, as currently coded, is done on a first-come-first-serve basis. Thus, a bot may have to travel right across the arena to collect its pizza, when it could have collected a nearer one, had a smarter allocation algorithm been implemented. How much time and energy, over a year would that save? How many kg more of pizza could have been delivered?

> #### **Targeted pizza allocation**
When a pizza is assigned for collection by a bot, another pizza is automatically ready, so there are alway multiple pizzas waiting to be collected to choose from. Therefore you need to develop code to select a more optimum pizza from the pool of those available for delivery.

> #### **Heavier Pizzas**

Currently the maximum pizza weight is fixed (how?). You can raise this weight and increase the size, and therefore the maximum delivery payload. However you run the risk of allocating pizzas which are too heavy. This causes the ecosystem to reject contracts. Therefore you would need to implement weight control as part of pizza-to-bot allocation.

## Learning Resources
The following learning materials are directly relevant to this task
- python notebooks from semester 1
---
## **Deliverables**
What you must deliver for assessment of this task:
* A python file `robot_optimisation.py`
* This file should be located in the `python` folder
* Note that other python files or documentation related to the task 3 may be placed in the `python` folder. These will not be be assessed but may beneficially referenced in task 1 to demonstrate your development process.
---

## **Assessment Criteria**

Task 3 is worth a total of **30** marks. This is assessed according to the following four criteria:
* Implementation of Charging Optimisation
* Implementation of Pizza distance and/or Pizza Weight allocation optimisation
* Calculation and tabulation of KPIs using formatted print statements e.g. f-strings
* Code Quality

These are discussed detailed below. The points listed describe what a high‑performing solution might typically demonstrates. They are not mandatory design choices—students should set their own goals and justify their approach. Different, well‑reasoned solutions can still achieve high marks. 
### 1. Implementation of Charging Optimisation 
Study the discussion above on charging optimisations and what you might do. Marks are awarded for 
- Sound evidence based implementation of threshhold optimsation
- optimisation of additional chargers and commensurate adjustment of thresholds
- Effective implementation of oportunistic charging
> 9 Marks
### 2. Implementation of Pizza Allocation Optimisation
- Implementation of an effective pizza allocation strategy to enhance performance KPIs
- Implementation of heavier pizza weights to enhance performance KPIs
> 9 Marks
### 3. Calculation and tabulation of KPI Performance Enhancements
- Effective presentation of KPI performance enhancements for measure inplemented **relative to counter-factual scenarios** using formatted print statements e.g. f-strings or pandas dataframes.
> 6 marks


### 4. Code Quality

Your code will be evaluated for the quality of your written code, not just its ability to run but also to convey to future readers its function and how it work.

See the [Code Quality](<coursework code quality.md>) document for how code might be evaluated 

> 6 marks



