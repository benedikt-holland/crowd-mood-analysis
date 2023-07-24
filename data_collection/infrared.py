# Display AMG88XX sensor data as an image
import time
import busio
import board
import adafruit_amg88xx
import numpy as np
from PIL import Image


MAX_TEMP = 30
MIN_TEMP = 22

i2c = busio.I2C(board.SCL, board.SDA)
amg = adafruit_amg88xx.AMG88XX(i2c)

data = np.zeros( (8, 8, 3), dtype=np.uint8)

while True:
	max_temp = 1000
	time.sleep(10)
	for cidx, row in enumerate(amg.pixels):
		for ridx, temp in enumerate(row):
			r_value = int(((temp - MIN_TEMP) / (MAX_TEMP - MIN_TEMP)) * 255) 
			r_value = min(r_value, 255)
			r_value = max(r_value, 0)
			data[ridx, cidx] = [r_value, 0, 0]
	img = Image.fromarray(data)
	img.show()

