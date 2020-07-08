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

fig, (ax1, ax2) = plt.subplots(2, 1, sharex = True)
fig.subplots_adjust(left = 0.05, right = 0.95, top = 0.95, bottom = 0.05,\
    wspace = 0)

url = r"https://opendata.ecdc.europa.eu/covid19/casedistribution/json/"
response = request.urlopen(url)
data = json.loads(response.read())['records']

for i, country in enumerate(['BG','RU', 'US']):
    country_data = list(filter(lambda x: x['geoId'] == country, data))
    result = list(map(lambda x: (datetime.date(*list(reversed(list( \
        map(int, x['dateRep'].split("/")))))), int(x['cases']), \
        int(x['deaths']), int(x['popData2019'])), country_data))

    dateRep = np.flip(np.array(list(map(lambda x: x[0].strftime("%Y-%m-%d"), \
        result)), dtype='datetime64[D]'))
    cases = np.flip(np.array(list(map(lambda x: x[1], result)), dtype='d'))
    deaths = np.flip(np.array(list(map(lambda x: x[2], result)), dtype='d'))
    popd = np.flip(np.array(list(map(lambda x: x[3], result)), dtype='d'))

    ax1.plot(dateRep, cases/popd * 1.0e+6, label = country)
    ax2.plot(dateRep, deaths/popd * 1.0e+6, label = country)

ax1.set_title(r"https://opendata.ecdc.europa.eu/covid19/casedistribution/json/")
ax1.legend()
ax1.grid()
ax1.ylabel = 'cases per million'

ax2.legend()
ax2.grid()
ax2.ylabel = 'deaths per million'

plt.show()
