# Render a video based on the infrared image data in the csv file
import numpy as np
import pandas as pd
import time
from PIL import Image
import cv2

# Cutoff temperatures to determine RGB range
MAX_TEMP = 28
MIN_TEMP = 19
TEMP_RANGE = MAX_TEMP- MIN_TEMP

# Filter date
START_DATE = '2022-07-29'
END_DATE = '2022-06-13'
FPS = 0.1
FILENAME = "party.csv"
# Column index where infrared data starts
START_COL = 5
# Length of one side of the square frame in pixels
RESOLUTION = 8

pd.options.display.max_rows = 100
party = pd.read_csv(FILENAME, index_col=0)
party["timestamp"] = pd.to_datetime(party["timestamp"])
party1 = party.query(f"timestamp >= '{START_DATE} 00:00:00' & timestamp < '{END_DATE} 23:59:59'")

video_name = "{}_inf.avi".format(START_DATE)
fourcc = cv2.VideoWriter_fourcc(*'DIVX')
video = cv2.VideoWriter(video_name, fourcc, FPS, (8, 8))
rgb_ranges = [[0, 0, 0], [255, 0, 255], [0, 0, 255], [0, 255, 255], [255, 255, 255]]

for datapoint in party1.values:
    frame = np.zeros( (RESOLUTION, RESOLUTION, 3), dtype=np.uint8)
    for ridx in range(RESOLUTION):
        for cidx in range(RESOLUTION):
            temp = datapoint[cidx + ridx*RESOLUTION + START_COL]
            rgb_idx = int(((temp-MIN_TEMP)/TEMP_RANGE)*(len(rgb_ranges)-1))
            rgb_idx = max(0, min(len(rgb_ranges)-1, rgb_idx))
            rgb_percent = (temp-(MIN_TEMP + (len(rgb_ranges)-1) * rgb_idx)) / (MIN_TEMP + (len(rgb_ranges)-1) * (rgb_idx + 1))
            rgb_value = [0, 0, 0]
            for i in range(3):
                try:
                    rgb_value[i] = rgb_percent * (rgb_ranges[rgb_idx+1][i] - rgb_ranges[rgb_idx][i]) + rgb_ranges[rgb_idx][i]
                except IndexError:
                    pass
            frame[ridx, cidx] =  rgb_value
    video.write(frame)

cv2.destroyAllWindows()
video.release()




