
from googleapiclient.discovery import build
import ssl
import httplib2

http = httplib2.Http(disable_ssl_certificate_validation=True)


#service = build('distance-matrix', 'v1',  developerKey='AIzaSyAj5ma2wuEOnPE2-DBbpGr2qRHWqqfXTlM', http=http)


import pyzipcode

zcdb = pyzipcode.ZipCodeDatabase()

def calc_zip_distance(z1, z2):
    zip1, zip2 = zcdb[z1], zcdb[z2]
    return haversine(zip1.latitude, zip1.longitude, zip2.latitude, zip2.longitude)


# https://github.com/cmhulett/zipcode_distance/blob/master/zipcode_distance.py

# AIzaSyAj5ma2wuEOnPE2-DBbpGr2qRHWqqfXTlM
import math
def haversine(lat1, long1, lat2, long2):
    """
    haversine formula to calculate the distance from lat/long coords on a sphere.
    Because the earth is somewhat elliptical can give errors up to 0.3%
    """
    radius = 3963.1676 #Radius of earth in miles
    lat1, long1, lat2, long2 = map(math.radians, [lat1, long1, lat2, long2])
    dlat = lat2 - lat1
    dlong = long2 - long1


    a = math.sin(dlat/2) * math.sin(dlat/2) + math.cos(math.radians(lat1)) \
        * math.cos(math.radians(lat2)) * math.sin(dlong/2) * math.sin(dlong/2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    d = radius * c

    return d
