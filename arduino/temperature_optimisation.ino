// Loovee @ 2015-8-26
#include <math.h>
// grove sensor constants
const int B = 4275;            // B value of the thermistor
const int R0 = 100000;         // R0 = 100k
const int pinTempSensor = A0;  // Grove - Temperature Sensor connect to A0

// data collection settings
const int sampleCount = 60;
float samplingRateHz = 1.0; // default into active mode

// list of all samples
float temperatureData[sampleCount];

// dft arrays to display complete dft spectrum
float frequencyData[sampleCount];
float magnitudeData[sampleCount];

// sample rates for each power mode
const float activeSamplingRateHz = 1.0;
const float idleSamplingRateHz = 0.2;
const float powerDownSamplingRateHz = 0.03; 
// create an enumerator in order to have the 3 power modes as constant values

enum powerMode
{
  Active, 
  Idle, 
  Power_down
};

powerMode currentMode = Active;
float dominantFrequency = 0.0;

// just prints current mode to serial monitor
const char* mode2string(powerMode mode)
{
  if(mode == Active)
  {
    return "Active mode";
  }
  else if(mode == Idle)
  {
    return "Idle mode";
  }
  else
  {
    return "Power down mode";
  }
}

// declared constants for thresholds; these are used to change the power mode
const float lowVarThreshold = 0.05;
const float highVarThreshold = 0.20;

void setup() 
{
  Serial.begin(9600);
  delay(1000);
  Serial.println("Temperature data collection has begun:");
}

void loop() 
{
  collect_temperature_data();

  float averageVariation = calculate_temperature_variation();

  apply_dft();
  dominantFrequency = find_dominant_freq();

  currentMode = decideMode(averageVariation, dominantFrequency);

  send_data_to_pc();

  updateSamplingRate(currentMode);

  Serial.print("Average temperature variation: ");
  Serial.println(averageVariation);

  Serial.print("Dominant frequency: ");
  Serial.print(dominantFrequency);
  Serial.println(" Hz");
  
  Serial.print("Selected power mode & sampling rate:");
  Serial.println(mode2string(currentMode));

  Serial.print("Sampling rate for next cycle: ");
  Serial.print(samplingRateHz);
  Serial.println(" Hz");
  
  Serial.println("Temperature collection cycle has finished");
  Serial.println();

  delay(5000);  // 5 second wait before collecting another block
}

float read_temperature() 
{
  int rawValue = analogRead(pinTempSensor);
  // check if value read is less than zero to avoid error
  if (rawValue <= 0) {
    Serial.println("Error: Invalid reading");
    return NAN;  // return 'not a number'
  }
  float resistance = 1023.0 / rawValue - 1.0;
  resistance = R0 * resistance;

  float temperature = 1.0 / (log(resistance / R0) / B + 1.0 / 298.15) - 273.15;  // converting to celsius using provided info (grove)
  return temperature;
}

void collect_temperature_data() 
{
  unsigned int sampleInterval = 1000.0 / samplingRateHz;
  Serial.println("collecting temperature data ^-^");

  for (int i = 0; i < sampleCount; i++) 
  {
    float temperature = read_temperature();
    if (isnan(temperature)) 
    {
      if (i > 0)  // if the sensor fails, reuse the previous values as a precaution to not get any funky changes
      {
        temperatureData[i] = temperatureData[i - 1];
      } else {
        temperatureData[i] = 0.0;
      }
    } else {
      temperatureData[i] = temperature;
    }
    Serial.print("Sample ");
    Serial.print(i);
    Serial.print(" : ");
    Serial.print(temperatureData[i]);
    Serial.println(" C");
    delay(sampleInterval);
  }
}
powerMode decideMode(float averageVariation, float dominantFrequency)
{
  if(dominantFrequency > 0.5 || averageVariation > highVarThreshold)
  {
    return Active;
  }
  else if(dominantFrequency > 0.1 ||averageVariation > lowVarThreshold)
  {
    return Idle;
  }
  else
  {
    return Power_down;
  }
}

void updateSamplingRate(powerMode mode)
{
  if(mode == Active)
  {
    samplingRateHz = activeSamplingRateHz;
  }
  else if(mode == Idle)
  {
    samplingRateHz = idleSamplingRateHz;
  }
  else
  {
    samplingRateHz = powerDownSamplingRateHz;
  }
}

float calculate_temperature_variation() 
{
  float difference = 0.0;
  for (int i = 1; i < sampleCount; i++) 
  {
    difference += fabs(temperatureData[i] - temperatureData[i - 1]);
  }
  return difference / (sampleCount - 1);
}

float* apply_dft()
{
  for(int k=0; k < sampleCount; k++)
  {
    float real = 0.0;
    float imaginary = 0.0;

    for(int n =0; n < sampleCount; n++)
    {
      float angle = 2.0 * PI * k * n / sampleCount;

      real += temperatureData[n] * cos(angle);
      imaginary -= temperatureData[n] * sin(angle);
    }
    magnitudeData[k] = sqrt(real * real+ imaginary * imaginary);
    frequencyData[k] = (k * samplingRateHz) / sampleCount;
  }
  return frequencyData;
}

float find_dominant_freq()
{
  int dominantIndex = 1; // skip k=0 as it is the average temperature, not a real temp fluctuation
  float highestMagnitude = magnitudeData[1];

  for(int k = 2; k < sampleCount; k++)
  {
    if(magnitudeData[k] > highestMagnitude)
    {
      highestMagnitude = magnitudeData[k];
      dominantIndex = k;
    }
  }
  
  return frequencyData[dominantIndex];
}

void send_data_to_pc() 
{
  Serial.println("Time, Temperature, Frequency, Magnitude");

  for (int i = 0; i < sampleCount; i++) 
  {
    float timeSeconds = i / samplingRateHz;
    Serial.print(timeSeconds);
    Serial.print(" , ");
    Serial.print(temperatureData[i]);
    Serial.print(" , ");
    Serial.print(frequencyData[i]);
    Serial.print(" , ");
    Serial.println(magnitudeData[i]);
  }
}
