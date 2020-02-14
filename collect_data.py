import bme280
from time import sleep
from datetime import datetime
import pandas as pd

df = pd.DataFrame(columns=["Zeit", "Temperatur", "Druck", "Luftfeuchtigkeit"])

k = 0
while True:
    tstamp = datetime.now()
    if tstamp.second % 5 == 0:
        temp, pres, humi = bme280.readBME280All()
        df.loc[k] = [tstamp.strftime("%Y/%m/%d - %H:%M:%S"), round(temp, 1), round(pres, 0), round(humi, 1)]
        df.to_csv("data/bme280.csv")
        k += 1
        sleep(4)
    
    else:
        sleep(0.5)
