**Discussion of results**

# Introduction
I took a 3 minute sampling of the temperature on a night, with the sensor dangling out of my window, hence it was so cold. (8-9C average).

# Time domain, temperature vs time plot
This clearly shows that the overall temperature trend was fairly stable, however the raw signal contained many single point readings which were sudden spikes. These are likely can be caused by many things however I have come to the conclusion;
   1. My accomodation is on the second floor, where wind speed is higher, meaning that cold gusts could lead to sudden temperature changes
   2. Sensor noise. Meaning that the sensor may be not properly calibrated, or the equation is not that accurate, or rounding occurs too early somewhere. in the future it may be worth it to up the sampling rate.

# Frequency Domain, dft_magnitudes vs frequency plot
This does not particularly show one clear, isolated, dominating frequency. Instead, most frequency components are at **very** similar magnitudes. Likely due to the aforementioned conditions that the readings were taken in. Assuming in homes, the temperature is likely to be periodic due to climate control, the randomness of the outside is reinforced by these readings. I chose to ignore the DC component as it's only a representation of average temperature rather than variation.

# Original vs smoothed plot
As the title suggests, this is the original data changes against the smoothed. This shows how when averaged, the data is much cleaner and more readable for any calculations that may be needed, which I personally think would be more useful than the normal temperature against time plot, due to the lack of noise. 

# System behaviour
Based on the aforementioned smoothed temperature change, the system would hence be expected to remain in idle or power down mode as there is very minor variation in temperature (when smoothed!). This further highlights the importance of the smoothing as reading solely pure values could falsely trigger the system to change into active mode, spiking power draw unnecessarily. 

# System limitations
I think that leaving it loose out of my window was worse than perhaps holding it in place due to wind possibly moving it around. In a perfect world I would've been able to mount it down & shield it from the window or anything that may cause major deltas. A longer reading, perhaps over a day, may be better if we had wanted to detect periodic patterns outside. 