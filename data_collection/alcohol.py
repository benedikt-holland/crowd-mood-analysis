# Unused
# Attempt at using air alcohol concentration
import spidev
import time

spi = spidev.SpiDev()
spi.open(0, 0)
value = 0

def readadc(adcnum):
	if adcnum > 7 or adcnum < 0:
		return -1
	r = spi.xfer([1, (8 + adcnum) << 4, 0])
	#print("r[0]: %d, r[1]: %d, r[2]: %d" % (r[0], r[1], r[2]))
	adcout = ((r[1] & 3) << 8) + r[2]
	return adcout

while True:
	adc = readadc(0)
	if True or adc != value:
		value = adc
		volts = (value * 3.3) / 1024
		print("%4d/1023 => %5.3f" % (value, volts))
	time.sleep(10)
