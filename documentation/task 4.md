# **Task 4 - Data Analytics**

## **Outline**

Data analyisis, presentation and visualisation is a crucial part of science and engineering the bedrock of which is empirical evidence. Tasks 2 and 3 can produce a lot of data. 

In this section your task is to analyse and present data using Python's matplotlib library. You can choose the bot ecosystem in task 3, or the arduino optimisation in task 2 as your data source.

## Learning Resources
The following learning materials are directly relevant to this task


## Description

## Assessment 


### Arduino (Task 2): Temperature Data Recording, Frequency Analysis, and Python Visualisation

In this task, you are required to use your Arduino-based temperature monitoring system to collect temperature data over time, save the recorded data, and analyse the results using Python.

#### Objective
The aim of this task is to help you:
- collect real temperature data using Arduino,
- perform basic signal analysis,
- understand the relationship between temperature variation in the time domain and frequency content in the frequency domain,
- visualise the results clearly using Python.
---

#### Task Requirements

##### 1. Record Temperature Data
Use your Arduino system to record temperature readings continuously for **3 minutes**.

Your program should:
- measure temperature at an appropriate sampling rate,
- store or transmit the readings in a structured format,
- include a corresponding time value for each measurement.

At minimum, your recorded dataset should contain (you need you decide the time interval yourself):
- **Time**
- **Temperature**

For example:

| Time (s) | Temperature (°C) |
|----------|------------------|
| 0.0      | 24.1             |
| 0.5      | 24.2             |
| 1.0      | 24.3             |

---

##### 2. Perform Frequency Analysis
You should analyse the recorded temperature signal using a **Discrete Fourier Transform (DFT)**.

This may be done:
- directly in the Arduino code, or
- after exporting the temperature data for analysis in Python.

Your analysis should calculate the **magnitude of the frequency components** in the signal.

At minimum, the frequency-domain results should contain:
- **Frequency (Hz)**
- **Magnitude**

For example:

| Frequency (Hz) | Magnitude |
|----------------|-----------|
| 0.00           | 75.2      |
| 0.10           | 12.8      |
| 0.20           | 4.5       |

---

##### 3. Save Data to a File
You are required to save the recorded data in a file format that can be read by Python, such as: **CSV**

The saved file should include:
- temperature against time,
- frequency magnitude results for all frequency bins.

You may use:
- one worksheet/file for time-domain data and one for frequency-domain data, or
- a single file containing both datasets clearly labelled.

---

##### 4. Read the File in Python
Write a Python script that:
- reads the exported CSV or Excel file,
- extracts the temperature-time data,
- extracts the frequency-magnitude data,
- generates appropriate plots.

---

#### Required Plots

##### Plot 1: Temperature vs Time
Plot the recorded temperature signal as:

**Temperature (°C) vs Time (s)**

This plot should show how the measured temperature changes during the 3-minute recording period.

###### What this plot should help show:
- whether temperature is stable or changing,
- whether there are sudden fluctuations,
- whether the signal contains noise,
- whether the sampling is sufficiently smooth.

---

##### Plot 2: Magnitude vs Frequency
Plot the DFT result as:

**Magnitude vs Frequency (Hz)**

This plot should show the strength of each frequency component present in the temperature signal.

###### What this plot should help show:
- whether the signal is dominated by low-frequency content,
- whether there are repeated oscillations,
- whether noise appears at higher frequencies,
- which frequency component is dominant.

---

##### Plot 3: Smoothed Temperature vs Time
Apply a simple smoothing technique such as a moving average, then plot below in one figure:

- original temperature vs time,
- smoothed temperature vs time.

This helps demonstrate:
- noise reduction,
- trend visibility,
- differences between raw and filtered signals.

---

##### Plot 4: Histogram of Temperature Readings
Plot a histogram of all temperature values.

This helps show:
- the distribution of the readings,
- whether the temperature stayed within a narrow range,
- whether there were unusual values or outliers.

---

##### Plot 5: Temperature Change Rate vs Time
You may calculate the rate of temperature change between consecutive samples and plot:

**Temperature change rate vs Time**

This helps identify:
- rapid transitions,
- stable periods,
- the logic behind adaptive sampling or power mode switching.

#### Discussion of Findings
You should include a short discussion of your results.

Your discussion should comment on:

### Time-domain behaviour
- Was the temperature stable over the 3 minutes?
- Were there any sudden rises or drops?
- Did the signal appear noisy?

### Frequency-domain behaviour
- Which frequency component had the highest magnitude?
- Was the signal mainly low-frequency?
- Did the DFT reveal any repeated pattern or periodic fluctuation?
- Was there evidence of noise in higher-frequency components?

### System behaviour
- Did the adaptive sampling strategy behave as expected?
- Did the power mode selection appear sensible?
- Would you improve the system further?

### Data quality
- Was the recording duration sufficient?
- Was the sampling rate appropriate?
- Were there any limitations in your measurement method?

---

## Expected Workflow
A typical workflow for this task may be:

1. Use Arduino to measure temperature for 3 minutes.
2. Save time and temperature readings to a CSV or Excel file.
3. Perform DFT either:
   - in Arduino and save frequency results, or
   - in Python after reading the recorded data.
4. Use Python to read the file.
5. Plot:
   - temperature vs time,
   - magnitude vs frequency,
   - any additional useful plots.
6. Write a short discussion explaining the meaning of the results.

---

## Minimum Deliverables
Your submission for Task 4 should include:

- Arduino code used to record the data
- Saved CSV or Excel file containing the results
- Python script used to read and plot the data
- A set of figures with appropriate labels and titles
- A short discussion of the results

---

## Assessment Criteria
Marks for this task will be awarded based on:

- correct recording of temperature data,
- correct saving of the data in a readable file format,
- correct implementation of Python file reading,
- quality and correctness of the plots,
- correct frequency-domain representation,
- clarity of discussion and interpretation,
- overall organisation and presentation of the analysis.

---

## Good Practice Expectations
A strong submission will:
- use clearly labelled axes and units,
- include readable figure titles,
- organise the data file clearly,
- write Python code that is easy to follow,
- explain both the time-domain and frequency-domain plots,
- discuss what the plots mean rather than simply presenting them.

