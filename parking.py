from bluepy import btle
import RPi.GPIO as GPIO
import time
import struct  # To unpack binary data

# Set up GPIO for LED
LED_PIN = 17  # Define the GPIO pin for the LED
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)  # Suppress GPIO warnings
GPIO.setup(LED_PIN, GPIO.OUT)  # Set up the LED pin as output

# Connect to Bluetooth device
target_address = "08:B6:1F:82:20:22"  # Replace with your Arduino's MAC address
try:
    device = btle.Peripheral(target_address)  # Add addrType if necessary

    while True:
        # Read the characteristic (assuming handle 12)
        data = device.readCharacteristic(12)  # Handle 12, adjust if necessary
        
        # Check the length of the received data
        print(f"Received data length: {len(data)} bytes")

        if len(data) == 4:
            # Unpack the data as an unsigned integer (4 bytes)
            distance = struct.unpack('I', data)[0]  # 'I' means unsigned int (4 bytes)
            print(f"Distance: {distance} cm")

            # Control LED based on distance
            if distance < 20:
                # Turn LED ON for distance < 20 cm
                GPIO.output(LED_PIN, GPIO.HIGH)  # LED ON
            else:
                GPIO.output(LED_PIN, GPIO.LOW)  # LED OFF for distance >= 20 cm

        else:
            print(f"Unexpected data length: {len(data)}. Skipping this reading.")

        time.sleep(0.5)  # Slightly increase the delay between measurements

except btle.BTLEDisconnectError as e:
    print(f"Failed to connect to peripheral: {e}")
except Exception as e:
    print(f"An error occurred: {e}")
finally:
    try:
        device.disconnect()
    except:
        pass
    GPIO.cleanup()
