#-------------------------------------------------------------------------------
# Name:        c19
# Purpose:     WhoKnows
#
# Author:      icis4
#
# Created:     05.04.2020
# Copyright:   (c) icis4 2020
# Licence:     BSD
#-------------------------------------------------------------------------------
import json
from urllib import request
import datetime
import matplotlib
import matplotlib.pyplot as plt
import numpy as np

url = r"https://opendata.ecdc.europa.eu/covid19/casedistribution/json/"
response = request.urlopen(url)
data = json.loads(response.read())['records']

plt.ylabel('cases/deaths by pupulation 2019')
plt.grid(True)

for i, country in enumerate(['BG','RU', 'US']):#'IT', 'FR', 'US', 'CN']):
    country_data = list(filter(lambda x: x['geoId'] == country, data))
    result = list(map(lambda x: (datetime.date(*list(reversed(list( \
        map(int, x['dateRep'].split("/")))))), int(x['cases']), \
        int(x['deaths']), int(x['popData2019'])), country_data))

    dateRep = np.flip(np.array(list(map(lambda x: x[0].strftime("%Y-%m-%d"), \
        result)), dtype='datetime64[D]'))
    cases = np.flip(np.array(list(map(lambda x: x[1], result)), dtype='i'))
    deaths = np.flip(np.array(list(map(lambda x: x[2], result)), dtype='i'))
    popd = np.flip(np.array(list(map(lambda x: x[3], result)), dtype='i'))

    plt.subplot(2, 1, 1)
    plt.plot(dateRep, cases/popd * 1e6, label = country + "-cases per milion")
    plt.subplot(2, 1, 2)
    plt.plot(dateRep, deaths/popd * 1e6, label = country + "-deaths per milion")

plt.subplot(2, 1, 1)
plt.title(r"https://opendata.ecdc.europa.eu/covid19/casedistribution/json/")
plt.legend()
plt.grid(True)
plt.subplot(2, 1, 2)
plt.legend()
plt.grid(True)

plt.show()
