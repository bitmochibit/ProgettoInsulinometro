#include <BLEDevice.h>
#include <BLEServer.h>
#include <BLEUtils.h>
#include <BLE2902.h>

#define LED_PIN 2

long currentTemp = 30;  // Initial temperature
String command;
bool isUpdating = true; // Flag to control temperature updates

// BLE Service and Characteristic UUIDs
#define SERVICE_UUID        "1809"  // Standard Health Thermometer Service UUID
#define CHARACTERISTIC_UUID "2A1C" // Temperature Characteristic UUID

BLEServer* pServer = nullptr;
BLECharacteristic* tempCharacteristic = nullptr;
bool deviceConnected = false;

void processCommand();

// BLE Command Characteristic UUID
#define COMMAND_CHARACTERISTIC_UUID "2A56" // Custom characteristic for command input
BLECharacteristic* commandCharacteristic = nullptr;

// Callback class to handle BLE server events
class ServerCallbacks : public BLEServerCallbacks {
  void onConnect(BLEServer* pServer) {
    deviceConnected = true;
    Serial.println("Device connected.");
  }

  void onDisconnect(BLEServer* pServer) {
    deviceConnected = false;
    Serial.println("Device disconnected.");
    // Restart advertising
    BLEDevice::startAdvertising();
    Serial.println("Advertising restarted.");
  }
};

// Callback class to handle BLE command writes
class CommandCallbacks : public BLECharacteristicCallbacks {
  void onWrite(BLECharacteristic* pCharacteristic) {
    String value = pCharacteristic->getValue();
    if (value.length() > 0) {
      command = String(value.c_str());
      command.trim();
      processCommand();
    }
  }
};

void setup() {
  pinMode(LED_PIN, OUTPUT);
  Serial.begin(115200);

  // Initialize BLE
  BLEDevice::init("ESP32_TempSensor"); // Set the BLE device name
  pServer = BLEDevice::createServer();

  // Callback to handle connection events
  pServer->setCallbacks(new ServerCallbacks());

  // Create BLE Service
  BLEService* tempService = pServer->createService(SERVICE_UUID);

  // Create BLE Temperature Characteristic
  tempCharacteristic = tempService->createCharacteristic(
    CHARACTERISTIC_UUID,
    BLECharacteristic::PROPERTY_READ | BLECharacteristic::PROPERTY_NOTIFY
  );
  
  // Add descriptor for notifications
  tempCharacteristic->addDescriptor(new BLE2902());

  // Create BLE Command Characteristic
  commandCharacteristic = tempService->createCharacteristic(
    COMMAND_CHARACTERISTIC_UUID,
    BLECharacteristic::PROPERTY_WRITE
  );
  commandCharacteristic->setCallbacks(new CommandCallbacks());

  // Start the service
  tempService->start();

  // Start advertising
  BLEAdvertising* pAdvertising = BLEDevice::getAdvertising();
  pAdvertising->addServiceUUID(SERVICE_UUID);
  pAdvertising->setScanResponse(true);
  pAdvertising->setMinPreferred(0x06);  // Set minimum advertising interval
  pAdvertising->setMaxPreferred(0x12); // Set maximum advertising interval
  BLEDevice::startAdvertising();

  Serial.println("BLE is ready and advertising.");
}

void loop() {
  if (isUpdating) {
    updateTemperature();
    // Notify connected BLE devices about the new temperature
    if (deviceConnected) {
      tempCharacteristic->setValue((uint8_t *)&currentTemp, sizeof(currentTemp));
      tempCharacteristic->notify();
    }
  }
  checkSerialInput();
  delay(10); // Simulate a time gap between temperature updates
}

void updateTemperature() {
  // Slightly randomize temperature (-2 to 2)
  currentTemp += random(-2, 3);
}

void checkSerialInput() {
  // Check if data is available on Serial
  if (!Serial.available()) return;

  // Read and process the input command
  command = Serial.readStringUntil('\n'); // Read input until newline
  command.trim(); // Remove whitespace
  processCommand();
}

void processCommand() {
  if (command.equalsIgnoreCase("read")) {
    blinkLED(); // Blink to indicate activity
    Serial.println(currentTemp); // Send the current temperature as a string
  } else if (command.equalsIgnoreCase("pause")) {
    isUpdating = false; // Pause temperature updates
    Serial.println("Temperature updates paused.");
  } else if (command.equalsIgnoreCase("resume")) {
    isUpdating = true; // Resume temperature updates
    Serial.println("Temperature updates resumed.");
  } else {
    Serial.println("Unknown command.");
  }
}

void blinkLED() {
  // Blink the LED once
  digitalWrite(LED_PIN, HIGH);
  delay(200); // LED on for 200ms
  digitalWrite(LED_PIN, LOW);
}
