// Loovee @ 2015-8-26
#include <math.h>
// grove sensor constants
const int B = 4275; // B value of the thermistor
const int R0 = 100000; // R0 = 100k
const int pinTempSensor = A0; // Grove - Temperature Sensor connect to A0

// data collection settings
const int sampleCount = 180;
const float samplingRateHz = 1;

// list of all samples
float temperatureData[sampleCount];

void setup()
{
  Serial.begin(9600);
  delay(1000);
  Serial.println("Temperature data collection has begun:");
}

void loop()
{
  collect_temperature_data();

  send_data_to_pc();

  Serial.println("Temperature collection cycle has finished");
  Serial.println();
  delay(5000); // 5 second wait before collecting another block
}

float read_temperature()
{
  int rawValue = analogRead(pinTempSensor);
  // check if value read is less than zero to avoid error
  if(rawValue <= 0)
  {
    Serial.println("Error: Invalid reading");
    return NAN; // return 'not a number' 
  }
  float resistance = 1023.0 / rawValue - 1.0;
  resistance = R0 * resistance;

  float temperature = 1.0 / (log(resistance / R0) / B + 1.0 / 298.15) -273.15; // converting to celsius using provided info (grove)
  return temperature;
}

void collect_temperature_data()
{
  unsigned int sampleInterval = 1000 / samplingRateHz;
  Serial.println("collecting temperature data ^-^");

  for (int i=0; i<sampleCount; i++)
  {
    float temperature = read_temperature();
    if(isnan(temperature))
    {
      if(i>0) // if the sensor fails, reuse the previous values as a precaution to not get any funky changes
      {
        temperatureData[i] = temperatureData[i-1];
      } else {
        temperatureData[i] = 0.0;
      }
    } else{ 
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

void send_data_to_pc()
{
  Serial.println("Time, Temperature");
  
  for(int i =0; i<sampleCount; i++)
  {
    float timeSeconds = i / samplingRateHz;
    Serial.print(timeSeconds);
    Serial.print(",");
    Serial.println(temperatureData[i]);
  }
}
