# Unused
# Attempt at using low quality microphone sensor
import spidev
import time
import numpy as np
import matplotlib.pyplot as plt

channel = 0
spi = spidev.SpiDev()
spi.open(0, 0)
value = 0
array = list()
high = True
mid = 600
osc = 0
end = 0
interval = 0.1

try:
	print("Listening")
	end = time.time()
	while True:
		start = time.time()
		spi_result = spi.xfer( [1, (8+channel) << 4, 0] )
		adc_out = ((spi_result[1] & 3) << 8 ) + spi_result[2]
		if (not high and adc_out >= mid) or (high and adc_out < mid):
			osc += 1
			high = not high
		if start >= end + interval:
			array.append(osc/(2*interval))
			osc = 0
			end = start

finally:
	plt.plot(array)
	plt.show()
	spi.close()
