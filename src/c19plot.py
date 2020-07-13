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
import time
import os

plt.style.use('bmh')
fig, (ax1, ax2) = plt.subplots(2, 1, sharex = True)
fig.subplots_adjust(left = 0.10, right = 0.90, top = 0.90, bottom = 0.10,\
    wspace = 0)
fig.set_size_inches(10,8)

ax1.set_title(\
    r"https://opendata.ecdc.europa.eu/covid19/casedistribution/json/")
ax1.grid(color='#333333')
ax1.set_ylabel('cases per million')
ax2.grid(color='#333333')
ax2.set_ylabel('deaths per million')

url = r"https://opendata.ecdc.europa.eu/covid19/casedistribution/json/"
response = request.urlopen(url)
data = json.loads(response.read())['records']

for i, country in enumerate(['BG', 'US', 'RU',]):
    country_data = list(filter(lambda x: x['geoId'] == country, data))
    result = list(map(lambda x: (datetime.date(*list(reversed(list( \
        map(int, x['dateRep'].split("/")))))), int(x['cases']), \
        int(x['deaths']), int(x['popData2019'])), country_data))

    dateRep = np.flip(np.array(list(map(lambda x: x[0].strftime("%Y-%m-%d"), \
        result)), dtype='datetime64[D]'))
    cases = np.flip(np.array(list(map(lambda x: x[1], result)), dtype='d'))
    deaths = np.flip(np.array(list(map(lambda x: x[2], result)), dtype='d'))
    popd = np.flip(np.array(list(map(lambda x: x[3], result)), dtype='d'))

    ax1.plot(dateRep, cases/popd * 1.0e+6, '-', color ='C%d' % i, \
        label = country)
    z = np.polyfit(range(len(dateRep)) , cases/popd * 1.0e+6, 6)
    p = np.poly1d(z)
    ax1.plot(dateRep, p(range(len(dateRep))), "--", color ='C%d' % i)

    ax2.plot(dateRep, deaths/popd * 1.0e+6, '-', color ='C%d' % i,\
        label = country)
    z = np.polyfit(range(len(dateRep)) , deaths/popd * 1.0e+6, 6)
    p = np.poly1d(z)
    ax2.plot(dateRep, p(range(len(dateRep))), '--', color ='C%d' % i)

ax1.legend()
ax2.legend()
plt.savefig(
    os.path.normpath(
        os.path.join(
            os.path.dirname(__file__),
            "..",
            "img",
            time.strftime("plot-%Y-%m-%d.png")
        )
    ),
    format="png"
)
#plt.show()
