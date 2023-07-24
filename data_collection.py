# Collect temperature, humdity, eCO2, TVOC and infrared data from Raspberry Pi
import pandas as pd
import numpy as np
import time
import logging
import sys
# Raspberry libraries
import board
import busio
# Device libraries
import adafruit_dht
import adafruit_sgp30
import adafruit_amg88xx

DELAY = 10
SAVE_INTERVAL = 1
FREQUENCY = 100000
MOX_BASELINE = [0x9c61, 0x94e7]

logging.basicConfig(filename='party.log', filemode='a', format='%(asctime)s -  %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger()
logger.setLevel(logging.INFO)
logging.info("Delay: {0}s, Save interval: {1}".format(DELAY, SAVE_INTERVAL))

columns = ["timestamp", "temperature", "humidity", "eCO2", "TVOC"]
for i in range(64):
	columns.append("inf" + str(i))
try:
	data = pd.read_csv("party.csv", index_col = 0)
	logging.info("party.csv found")
except Exception:
	data = pd.DataFrame(columns=columns, dtype="float64")
	logging.warning("party.csv not found, creating new one...")
count = 0

# DHT22 temperature & humidity sensor	
try:
	dhtDevice = adafruit_dht.DHT22(board.D4)
	logging.info("DHT22 initialised")
	temperature_on = True
except RuntimeError as e:
	logging.error(e)
	temperature_on = False

# SGP30 CO2 equivalent & total volatile organic compound
try:
	i2c = busio.I2C(board.SCL, board.SDA, frequency=FREQUENCY)
	sgp30 = adafruit_sgp30.Adafruit_SGP30(i2c)
	sgp30.set_iaq_baseline(MOX_BASELINE[0], MOX_BASELINE[1])
	sgp30.iaq_init()
	logging.info("SGP30 initialised")
	co2_on = True
except Exception as e:
	logging.error(e)
	co2_on = False

# AMG8833 8x8 infrared sensor
try:
	i2c = busio.I2C(board.SCL, board.SDA, frequency=FREQUENCY)
	amg = adafruit_amg88xx.AMG88XX(i2c)
	logging.info("AMG8833 initialised")
	infrared_on = True
except Exception as e:
	logging.error(e)
	infrared_on = False

# Main loop
time.sleep(60)
while True:
	try:
		datapoint = pd.Series(index = columns, dtype="float64")
		datapoint["timestamp"] = pd.Timestamp.now()
		# temperature + humidity
		if temperature_on:
			try:
				datapoint["temperature"] = dhtDevice.temperature
				datapoint["humidity"] = dhtDevice.humidity
			except RuntimeError:
				datapoint["temperature"] = np.nan
				datapoint["humidity"] = np.nan
		else:
			datapoint["temperature"] = np.nan
			datapoint["humidity"] = np.nan
			# DHT22 temperature & humidity sensor
			try:
				dhtDevice = adafruit_dht.DHT22(board.D4)
				logging.info("DHT22 initialised")
				temperature_on = True
			except Exception as e:
				logging.error(e)
				temperature_on = False

		# CO2 equivalent + total volatile organic compounds
		if co2_on:
			try:
				datapoint["eCO2"] = sgp30.eCO2
				datapoint["TVOC"] = sgp30.TVOC
			except Exception:
				datapoint["eCO2"] = np.nan
				datapoint["TVOC"] = np.nan
		else:
			datapoint["eCO2"] = np.nan
			datapoint["TVOC"] = np.nan
			# SGP30 CO2 equivalent & total volatile organic compound
			try:
				i2c = busio.I2C(board.SCL, board.SDA, frequency=FREQUENCY)
				sgp30 = adafruit_sgp30.Adafruit_SGP30(i2c)
				sgp30.iaq_init()
				logging.info("SGP30 initialised")
				co2_on = True
			except Exception as e:
				logging.error(e)
				co2_on = False

		# 8x8 infrared picture
		if infrared_on:
			i = 0
			for row in amg.pixels:
				for temp in row:
					temp_column = "inf" + str(i)
					assert temp_column in columns
					i += 1
					try:
						datapoint[temp_column] = temp
					except Exception:
						datapoint[temp_column] = np.nan	
		else:
			# AMG8833 8x8 infrared sensor
			try:
				i2c = busio.I2C(board.SCL, board.SDA, frequency=FREQUENCY)
				amg = adafruit_amg88xx.AMG88XX(i2c)
				logging.info("AMG8833 initialised")
				infrared_on = True
			except Exception as e:
				logging.error(e)
				infrared_on = False

		logger.info(datapoint[["timestamp", "temperature", "humidity", "eCO2", "TVOC", "inf0"]])
		data = data.append(datapoint, ignore_index=True)
		count += 1
		if count >= SAVE_INTERVAL:
			data.to_csv("party.csv")
			count = 0
		time.sleep(DELAY)

	except KeyboardInterrupt:
		data.to_csv("party.csv")
		logging.warning("Keyboard interrupt")
		break

