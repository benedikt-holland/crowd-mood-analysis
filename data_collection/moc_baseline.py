# Determine SGP30 baseline values for eCO2 and TVOC
import busio
import board
import adafruit_sgp30
i2c = busio.I2C(board.SCL, board.SDA, frequency=100000)
sgp30 = adafruit_sgp30.Adafruit_SGP30(i2c)
sgp30.iaq_init()
print(sgp30.baseline_eCO2)
print(sgp30.baseline_TVOC)
