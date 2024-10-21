#include <ArduinoBLE.h>
#include <NewPing.h>

#define TRIG_PIN 11
#define ECHO_PIN 12
#define MAX_DISTANCE 200  // Max distance we want to ping for (in cm)

NewPing sonar(TRIG_PIN, ECHO_PIN, MAX_DISTANCE);

// Create a BLE service and characteristic
BLEService distanceService("180D");  // Custom service UUID
BLEUnsignedIntCharacteristic distanceCharacteristic("2A37", BLERead | BLENotify);

void setup() {
  Serial.begin(9600);
  
  // Initialize the BLE hardware
  if (!BLE.begin()) {
    Serial.println("Starting BLE failed!");
    while (1);
  }

  BLE.setLocalName("ParkingSensor");
  BLE.setAdvertisedService(distanceService);
  
  distanceService.addCharacteristic(distanceCharacteristic);
  BLE.addService(distanceService);

  BLE.advertise();
}

void loop() {
  BLEDevice central = BLE.central();
  
  if (central) {
    while (central.connected()) {
      // Get the distance from the ultrasonic sensor
      unsigned int distance = sonar.ping_cm();

      // Update the characteristic with the new distance
      distanceCharacteristic.writeValue(distance);
      

      delay(1000);
    }
  }
}