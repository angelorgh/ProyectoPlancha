import board
import adafruit_mlx90614


i2c = board.I2C()  # uses board.SCL and board.SDA

mlx = adafruit_mlx90614.MLX90614(i2c)


print("Ambent Temp: ", mlx.ambient_temperature)
print("Object Temp: ", mlx.object_temperature)