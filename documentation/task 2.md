# **Task 2 Arduino Programming Optimisation**

## Overview

In this Task, students are required to design a low-power, dynamically optimised temperature monitoring system using Arduino. The aim is to develop an efficient and responsive system that minimises energy consumption while maintaining effective memory management.

In a smart home environment, a temperature monitoring system plays a key role in regulating indoor conditions. The system uses a temperature sensor to collect real-time data, which is processed by an Arduino-based controller. Based on the temperature readings, the CPU determines whether to activate a heater. This decision-making process is essential for maintaining occupant comfort while ensuring energy efficiency.

However, continuously sampling temperature data at a high frequency leads to unnecessary energy consumption. In such cases, the processor remains active even when temperature changes are minimal, resulting in wasted power. Additionally, frequent sensor readings generate large volumes of data, increasing memory usage and potentially slowing down system performance. To address these challenges, the system adopts dynamic sampling strategies, allowing it to switch between different power modes based on the rate of temperature change. This approach enables a balance between system responsiveness, power efficiency, and memory optimisation.

## The Temperature Monitoring System and Its Three Modes
The temperature monitoring system acts as an intelligent **environmental regulator**, which continuously assesses temperature fluctuations to determine the optimal response. It operates using an **adaptive control mechanism**, adjusting its **sampling rate and power mode** dynamically to balance energy efficiency and data accuracy.

The **sampling rate** defines how often temperature data is collected. If a fixed high **sampling rate** is used, it leads to **unnecessary energy consumption and excessive data storage**. **Sampling Frequency** refers to the number of samples taken per second when measuring a signal, which is expressed in Hertz (Hz), where 1 Hz = 1 sample per second. For example: If a system samples temperature data at 10 Hz, it means 10 temperature readings are taken every second.

The system features **three operating modes**, each designed to optimize energy use and performance:

- **Active Mode**: The system enters this mode when **rapid temperature fluctuations** are detected. In this state, the **sampling frequency is high**, allowing for quick responses to environmental changes. This ensures that the system can react promptly, such as turning on a heater when a sudden drop in temperature occurs.
- **Idle Mode**: When **temperature fluctuations are minor**, the system reduces its sampling frequency to a moderate level. This prevents unnecessary power consumption while still maintaining sufficient responsiveness to gradual temperature changes.
- **Power Down Mode**: If the temperature remains **stable** over an extended period, the system further reduces its sampling frequency to the lowest level. This significantly **minimizes power consumption**, allowing the system to run efficiently without excessive data logging or energy waste.

Below is an **example** of the three modes (Table 1), each with a different sampling frequency. The amount of stored temperature data depends on how often the system logs temperature readings.

### Table 1: Sampling Modes and Data Generation
| Mode | Sampling Rate | Samples per Hour | Samples per Day |
|------|---------------|------------------|-----------------|
| Power Down Mode | 1 sample every 30 seconds | 120 | 2,880 |
| Idle Mode | 1 sample every 5 seconds | 720 | 17,280 |
| Active Mode | 1 sample every 1 second | 3,600 | 86,400 |

**Interpretation**  
If the system remains in **Active Mode**, it can generate up to **86,400 data points per day**, which may exceed available storage capacity and lead to inefficient memory usage. In contrast, if the system operates primarily in **Power Down Mode**, it records only **2,880 samples per day**, resulting in a substantial reduction in memory requirements and energy consumption.

By dynamically switching between these operating modes, the system avoids unnecessary data logging and ensures that only meaningful temperature variations are recorded. This adaptive behaviour allows computational and energy resources to be allocated efficiently, activating higher sampling rates only when significant temperature changes are detected.

The transitions between modes are governed by real-time analysis of temperature trends, enabling the monitoring system to respond intelligently to environmental changes. Consequently, this task focuses on **dynamic sampling rate adjustment based on temperature fluctuations** as a key strategy for optimising both energy efficiency and memory usage.

---

## How to Start
It is important to approach this task methodically. A key learning outcome is to understand how to integrate hardware and software in an embedded system, as well as how to develop and optimize an existing system. This does not mean that you must fully understand every line of the provided Arduino code before starting, so do not feel overwhelmed.

First, begin by setting up the Arduino hardware. Students will build an **Arduino-based temperature monitoring system** that collects and logs temperature data using the **Grove - Temperature Sensor V1.2**. You should familiarize yourself with the correct wiring configuration, ensuring that the sensor's **VCC**, **GND**, and **Data Pin** are connected properly to the Arduino. Make sure to verify that the connections are stable before proceeding. Log the collected temperature data and develop an understanding of how the data can be processed for further analysis.

- Connect the Grove Temperature Sensor to the Arduino according to the Table 2 below.

### Table 2: Sensor Wiring
| Grove Temperature Sensor Pin | Arduino Connection |
|------------------------------|--------------------|
| VCC | 5V |
| GND | GND |
| Signal | A0 (Analog Pin) |

Second, study the following Arduino program, which is provided in order to enable you to get the temperature sensor working. It reads temperature values from the sensor and prints them to the **Serial Monitor**. You should download the Arduino IDE to run the code. The university computer Lab WPL107 installed the software, and you can also find it via [Arduino IDE]. The tutorials on using Arduino Software tools are available from: [Software tools]. Connect your Arduino board and temperature sensor, then using Arduino IDE to run the code below to see how it works.

- The demo code is avaliable from seedstudio.

```cpp
// Loovee @ 2015-8-26
#include <math.h>
const int B = 4275000; // B value of the thermistor
const int R0 = 100000; // R0 = 100k
const int pinTempSensor = A0; // Grove - Temperature Sensor connect to A0

void setup()
{
  Serial.begin(9600);
}

void loop()
{
  int a = analogRead(pinTempSensor);
  float R = 1023.0/a-1.0;
  R = R0*R;
  float temperature = 1.0/(log(R/R0)/B+1/298.15)-273.15; // convert to temperature via datasheet
  Serial.print("temperature = ");
  Serial.println(temperature);
  delay(100);
}
```

Identify key functions responsible for reading sensor data. Try modifying different parameters such as the sampling interval to observe how the system behaves. Work through this step interactively, compile the code, run it on the Arduino, and monitor the output in the serial console.

Next, analyse how the collected data is stored. The system logs temperature readings and outputs them directly to a file on the computer through the serial connection. Introduce a function called `collect_temperature_data()` to collect the temperature from the Grove Temperature Sensor for around 3 minutes, and save it in an array for DFT processing later. The function should use suitable sampling intervals for collecting data. You can test your code using the active mode, the sampling rate in Table 1 (see above).

Once data is collected, students will implement the **Discrete Fourier Transform (DFT)** in C to analyse the dominant temperature change frequencies.

Before implementing the DFT function, students need to self-study the theory below to understand how the DFT works and how to apply it to temperature data. The Discrete Fourier Transform converts a time-domain signal (temperature readings over time) into a frequency-domain representation (how frequently the temperature changes).

The formula for computing the magnitude of the frequency components is:

$X[k] = Σ_{n=0}^{N-1} x[n] · e^{-j 2πkn/N}$   (Eq. 3.1)


Where:
- $X[k]$ = Frequency component at index k  
- $x[n]$ = Temperature data at index n  
- $N$ = Total number of samples  
- $k$ = Frequency index (ranging from 0 to N-1)  
- $j$ = Imaginary unit √-1

The index $k$ in the DFT output represents the frequency component of the original signal, but to obtain actual frequency values in Hz, we use the following equation:

$f_k = (k · f_s) / N   (Eq. 3.2)$


where:
- $f_k$ is the frequency corresponding to index k.  
- $f_s$ is the sampling frequency (in Hz).  
- $N$ is the total number of samples.

Since Arduino does not support complex numbers, we implement the real and imaginary parts using two arrays:

$real[k] = Σ_{n=0}^{N-1} x[n] · cos(2πkn/N)$      (Eq. 3.3)

$imag[k] = - Σ_{n=0}^{N-1} x[n] · sin(2πkn/N)$    (Eq. 3.4)


The magnitude of the frequency components is then calculated as:

$Magnitude[k] = sqrt( real[k]^2 + imag[k]^2 )$   (Eq. 3.5)


This analysis will allow the system to adjust the sampling rate dynamically, ensuring efficient energy use by detecting when high-frequency temperature variations occur.

- Write a function called `apply_dft()` that applies Discrete Fourier Transform (DFT) in Eq. 3.1 – Eq. 3.5 on the collected temperature data to convert the signal into frequency-domain components. The function should return the computed frequency (Eq. 3.2) as a **pointer**. The magnitude of the frequency components should be **calculated and stored** as Eq. 3.5.
- Write a function called `send_data_to_pc()` that sends time-domain and frequency-domain data via the Serial Monitor. The function should print time-domain temperature values. Compute the DFT magnitude spectrum and send the computed frequency values. Send frequency-domain data to the Serial Monitor for further analysis. **Hint:** The format should be **Time, Temperature, Frequency, Magnitude**.
- Write a function `decide_power_mode()` that determines whether the system should **operate in Active, Idle, or Power-down mode** based on the collected temperature and calculated average temperature fluctuation frequency. If the average frequency is > 0.5 Hz, use a high sampling rate (Active Mode). If 0.1 Hz < average frequency ≤ 0.5 Hz, use a medium sampling rate (Idle Mode). If the average frequency is ≤ 0.1 Hz, switch to Power-down Mode (low sampling rate to conserve energy). The function should return a mode indicator (ACTIVE, IDLE, or POWER_DOWN) based on the computed frequency.

Finally, after gaining a good understanding of how the system operates, move on to the optimization task. The goal is to implement an adaptive sampling strategy to adjust the system’s power consumption based on temperature fluctuations. The more stable the temperature, the less frequent the readings should be. This ensures that the system runs efficiently without unnecessary energy waste.

In this task, students will develop an intelligent temperature monitoring system that dynamically adjusts its sampling rate and power mode based on real-time temperature variations. The system will progressively transition between three power modes: Active Mode, Idle Mode, and Power Down Mode to optimize energy consumption while ensuring accurate temperature tracking. The key challenge is to implement a two-stage decision process that determines both the appropriate power mode and the optimal sampling rate based on temperature trends and frequency analysis.

Consider a scenario that the room temperature changes dynamically due to external factors (heater, air conditioner, or human influence).

Instead of using a fixed sampling rate in Table 1, your system should adjust its sampling rate dynamically based on observed temperature fluctuations.

The system starts by collecting temperature data for one minute (one cycle) at an initial sampling rate (the students have the freedom to select the initial sampling rate). The collected data is then analysed to determine whether temperature fluctuations are significant. This is done by computing the total difference between consecutive samples to assess how much the temperature changes over time. If the variation remains within a small, predefined threshold (again, in the design, students need to define the threshold value based on their collected temperature data), the system switches to Idle Mode to reduce power consumption. If Idle Mode persists for five consecutive cycles, indicating long-term stability, the system enters Power Down Mode to further conserve energy. However, if a sudden temperature fluctuation occurs at any stage, the system immediately reactivates Active Mode to ensure accurate monitoring. Additionally, Discrete Fourier Transform analysis is used to detect dominant frequency components, dynamically adjusting the sampling rate based on real-time temperature trends. This adaptive strategy prevents unnecessary high-frequency sampling when the environment remains stable, while ensuring quick responsiveness to sudden changes, ultimately balancing accuracy and power efficiency.

To further refine the decision-making process, DFT extracts dominant frequency components from the temperature variations. By transforming the data into the frequency domain, the system can identify periodic patterns in temperature changes. The DC component (k = 0), representing the overall average temperature, should be ignored, and only frequency components relevant to temperature fluctuations should be considered. The dominant frequency will be used as a reference to adjust the sampling rate dynamically.

Once the system determines whether to operate in Active, Idle, or Power Down Mode, the sampling rate must be adjusted dynamically. The dominant frequency extracted from `apply_dft()` in your Task 3 should be rewrite to guide this adjustment. The sampling rate must be at least twice the dominant frequency to satisfy **Nyquist’s sampling theorem** and avoid data loss. For instance, if the dominant frequency is 1.8 Hz, the sampling rate should be 3.6 Hz or higher. However, if temperature variations remain stable, the sampling rate should gradually decrease to minimize energy usage. The system must ensure the sampling rate remains within a predefined range, such as between 0.5 Hz and 4.0 Hz, to maintain efficiency.

A future temperature variation trend must also be predicted using a moving average method. Students should track temperature variation trends over the last 5 to 10 monitoring cycles and compute a moving average based on the last 10 temperature differences. This prediction helps determine whether temperature fluctuations are increasing, decreasing, or remaining stable, which directly influences the choice of power mode. If the predicted variation is large, the system remains in Active Mode; if it is moderate, the system enters Idle Mode. If temperature fluctuations stay consistently low for five consecutive cycles, the system transitions into Power Down Mode to further conserve energy. To learn how to implementation of the moving average in Arduino, please refer to: https://www.aranacorp.com/en/implementation-of-the-moving-average-in-arduino/

In addition to power mode optimization, students must also consider memory storage limitations. Since Arduino devices have limited RAM, inefficient storage can lead to system failures. Students must evaluate how memory is utilized in their implementation and identify ways to optimize storage.

---
## Expected System Behaviour
1. It **analyses the variations of collected temperature** to determine if the temperature is fluctuating significantly.
2. **DFT is applied** to find the **dominant frequency** of temperature variations.
3. **The best power mode is selected** based on predicted variations.
4. **Adjust the sampling rate dynamically** to reduce **power consumption** while maintaining accurate monitoring.
5. A **future variation trend is predicted** using a moving average.
6. Explain how memory is utilized in your implementation of your design. Are there any memory optimizations that could be made to reduce usage? What is the impact of storing large arrays in an Arduino environment? Provide a justified explanation and suggest at least one possible enhancement to improve memory efficiency in this task.

---
## **Deliverable**
What you must deliver for assessment of this task:
* A sketch file `temperature_optimisation.ino` used to operate your Arduino for this task
* The file should be located in the `arduino` folder
* Note that other sketches or documentation related to the task 2 may be placed in the `arduino` folder. These will not be be assessed but may beneficially referenced in task 1 to demonstrate your process.

---
## **Assessment Criteria**

Task 2 is worth a total of **30** marks. This is assessed according to the following four criteria:
* Implementation of Adaptive Sampling Strategy
* Implementation of DFT-Based Frequency Analysis
* Power Mode Control Strategy
* Code Quality

These are discussed detailed below. The points listed describe what a high‑performing solution might typically demonstrates. They are not mandatory design choices—students should set their own goals and justify their approach. Different, well‑reasoned solutions can still achieve high marks. 

### 1. Implementation of Adaptive Sampling Strategy
- Correct implementation of **dynamic sampling rate optimisation** based on temperature trends.
- The program should **increase sampling frequency when temperature changes rapidly** and **reduce sampling frequency when the signal is stable** to save computational resources and power.
- Logical decision rules should be clearly defined and justified in the code.
> 8 marks

### 2. Implementation of DFT-Based Frequency Analysis
- Correct implementation of a **Discrete Fourier Transform (DFT)** to analyse the temperature signal.
- Ability to **identify dominant frequency components** in the signal.
- The frequency analysis should be correctly integrated into the optimisation strategy (e.g., adjusting sampling or power modes based on signal characteristics).
> 8 marks

### 3. Power Mode Control Strategy
- Implementation of a **power management system** that switches between operating modes (e.g., *Active*, *Idle*, *Low-Power*).
- The system should demonstrate **intelligent decision-making** based on sensor behaviour or signal analysis.
- The control logic should be efficient and avoid unnecessary transitions.
> 8 marks

### 4. Code Quality

Your code will be evaluated for the quality of your written code, not just its ability to run but also to convey to future readers its function and how it work.

See the [Code Quality](<coursework code quality.md>) document for how code might be evaluated 

> 6 marks
