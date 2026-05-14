import csv 
import matplotlib.pyplot as plt

# moving average function to smoothe the temperature data
def moving_average(values, window_size):
    smoothed_values = []
    half_window = window_size // 2
    
    for i in range(len(values)):
        start = max(0, i - half_window)
        end = min(len(values), i + half_window + 1)

        window = values[start:end]
        average = sum(window) / len(window)

        smoothed_values.append(average)

    return smoothed_values

# initialize emplty lists to store data from csv
times = []
temperatures = []
frequencies = []
magnitudes = []

csv_file = "task4data.csv" # path to the csv file containg data. might not work on on other machines, meaning it may need to be adjusted

# reading data from csv and inserting it into the lists
with open(csv_file, 'r', newline="") as f:
    reader = csv.DictReader(f)

    for row in reader:
        times.append(float(row["Time"]))
        temperatures.append(float(row["Temperature"]))

        if row["Frequency"] != "" and row["Magnitude"] != "":
            frequencies.append(float(row["Frequency"]))
            magnitudes.append(float(row["Magnitude"]))

smoothed_temperature = moving_average(temperatures, 10)

# calculate tempertuare change rate between samples

change_times = times[1:]
change_rates = []

for i in range(1, len(times)):
    time_diff = times[i] - times[i-1]
    temp_diff = temperatures[i] - temperatures[i-1]

    if time_diff != 0:
        change_rate = temp_diff / time_diff
    else:
        change_rate = 0
    change_rates.append(change_rate)

# plotting temperture change rate vs time using matplotlib
plt.figure(figsize=(10, 5))
plt.plot(change_times, change_rates)

plt.xlabel("Time (s)")
plt.ylabel("Temperature Change Rate (C/s)")
plt.title("Temperature Change Rate vs Time")

plt.grid(True)
plt.tight_layout()
plt.savefig("/Users/sk/Code/F535759_25WSA032_Coursework_V1103/Task 4 Deliverables/Figures/temperature_change_rate_vs_time.png")
plt.show()


# plotting temp vs time using matplotlib
plt.figure(figsize=(10, 5))
plt.plot(times, temperatures)

plt.xlabel("Time (s)")
plt.ylabel("Temperature (Celsius)")
plt.title("Temperature vs Time")

plt.grid(True)
plt.tight_layout()
plt.savefig("/Users/sk/Code/F535759_25WSA032_Coursework_V1103/Task 4 Deliverables/Figures/temperature_vs_time.png")
plt.show()

# plotting magnitude vs freuency using matplotlib
plt.figure(figsize=(10, 5))
plt.stem(frequencies[1:], magnitudes[1:]) # skip the first element to not plot DC coponent & plot as stem to show discrete values clearly


plt.xlabel("Frequency (Hz)")
plt.ylabel("Magnitude")
plt.title("DFT Magnitudes vs Frequency")

plt.grid(True)
plt.tight_layout()
plt.savefig("/Users/sk/Code/F535759_25WSA032_Coursework_V1103/Task 4 Deliverables/Figures/dft_magnitudes_vs_frequency.png")
plt.show()

# plotting ogrinal vs smoothed temperature using matplotlib
plt.figure(figsize=(10, 5))

plt.plot(times, temperatures, label="Original Temperature")
plt.plot(times, smoothed_temperature, label="Smoothed Temperature")

plt.xlabel("Time (s)")
plt.ylabel("Temperature (Celsius)")
plt.title("Original vs Smoothed Temperature")

plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig("/Users/sk/Code/F535759_25WSA032_Coursework_V1103/Task 4 Deliverables/Figures/original_vs_smoothed_temperature.png")
plt.show()

# plotting the histogram
plt.figure(figsize=(10, 5))
plt.hist(temperatures, bins=12)

plt.xlabel("Temperature (Celsius)")
plt.ylabel("Number of readings")
plt.title("Histogram of Temperature readings")

plt.grid(True)
plt.tight_layout()
plt.savefig("/Users/sk/Code/F535759_25WSA032_Coursework_V1103/Task 4 Deliverables/Figures/temperature_histogram.png")
plt.show()
