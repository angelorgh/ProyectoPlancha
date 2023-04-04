import json
import AS7262_Pi as spec

# Reboot the spectrometer, just in case
spec.soft_reset()

# Set the gain of the device between 0 and 3. Higher gain = higher readings
spec.set_gain(3)

# Set the integration time between 1 and 255. Higher means longer readings
spec.set_integration_time(50)

# Set the board to continuously measure all colours
spec.set_measurement_mode(2)

try:
    # Turn on the main LED
    spec.enable_main_led()

    while True:
        # Get the readings and calculate the label
        results = spec.get_calibrated_values()
        max_red_orange = results[0] + results[1]
        max_green_yellow = results[2] + results[3]
        max_blue_violet = results[4] + results[5]
        if max_red_orange > max_blue_violet and max_red_orange > max_green_yellow:
            label = "red"
        elif max_blue_violet > max_red_orange and max_blue_violet > max_green_yellow:
            label = "blue"
        else:
            label = "green"

        # Get the temperature
        temp = spec.get_temperature()

        # Create a dictionary with the measurement data
        measurement = {
            "R": str(results[0]),
            "O": str(results[1]),
            "Y": str(results[2]),
            "G": str(results[3]),
            "B": str(results[4]),
            "V": str(results[5]),
            "temp": str(temp),
            "label": label
        }

        # Load the existing data from data.json, if any
        try:
            with open("data.json", "r") as file:
                data = json.load(file)
        except FileNotFoundError:
            data = {"dataset": []}

        # Append the new measurement to the data list
        data["dataset"].append(measurement)

        # Write the updated data to data.json
        with open("data.json", "w") as file:
            json.dump(data, file)

except KeyboardInterrupt:
    # Set the board to measure just once (it stops after that)
    spec.set_measurement_mode(3)
    # Turn off the main LED
    spec.disable_main_led()
    # Notify the user
    print("Manually stopped")
