from __future__ import division

import os, sys
from processLVIS import lvisGround
import numpy as np
import pandas as pd
from handleTiff import tiffHandle
from pyproj import Proj, transform
from scipy.ndimage.filters import gaussian_filter1d

instructions = """
use     
    python3 lvisSingleline.py filepath resolution outputpath
to handle a single flight.
"""

def distance(p1, p2):
    return np.sqrt((p1[0] - p2[0]) * (p1[0] - p2[0]) + (p1[1] - p2[1]) * (p1[1] - p2[1]))

def interpolation(lon, lat, lst, res=1):
    backres = res
    p0 = np.array([lon, lat])
    sum0  = 0
    sum1 = 0
    N = 15
    temp = np.array([])
    dists = []

    pos = np.where((lst[:, 0] > lon-res) & (lst[:,0] < lon+res) & (lst[:, 1] > lat-res) & (lst[:,1] < lat+res))
    while(len(pos) !=1 or len(pos[0]) <= N) :
        if res > backres**2:
            return -999
        res *= 2
        pos = np.where(
            (lst[:, 0] > lon - res) & (lst[:, 0] < lon + res) & (lst[:, 1] > lat - res) & (lst[:, 1] < lat + res))

    temp = lst[pos]
    for point in temp:
        d = distance(point, (lon, lat))
        sum0 += point[2] / np.power(d, 2)
        sum1 += 1 / np.power(d, 2)
    return sum0 / sum1


def reproject(lat, lon, inEPSG, outEPSG):
    '''
    Reproject footprint coordinates
    '''
    # set projections
    inProj = Proj(init="epsg:" + str(inEPSG))
    outProj = Proj(init="epsg:" + str(outEPSG))
    # reproject data
    return transform(inProj, outProj, lon, lat)

def debug():

    filepath = sys.argv[1]
    resolution = int(sys.argv[2])
    outputpath = sys.argv[3]
    lvis = pd.read_csv(filepath)
    lat = lvis.lat
    lon = lvis.lon
    z = lvis.z
    lon, lat = reproject(lat, lon, 4326, 3857)
    point_list = np.array([lat, lon, z]).T
    minx = min(lon)
    miny = min(lat)
    maxx = max(lon)
    maxy = max(lat)
    minx = int(minx)
    miny = int(miny)
    maxx = int(maxx)
    maxy = int(maxy)

    data = []

    LON = np.arange(minx, maxx, resolution)
    LAT = np.arange(miny, maxy, resolution)
    for x in LON:
        for y in LAT:
            data.append(interpolation(x, y, point_list, resolution))
    data = np.array(data).reshape((len(LON), len(LAT)))
    tiffhandler = tiffHandle(minx, miny, maxx, maxy)
    tiffhandler.writeTiff(data, filename=outputpath, epsg=3857)

    print("finished")


if __name__ == "__main__":
    if len(sys.argv) != 4:
        print(instructions)
        exit(1)

    filepath = sys.argv[1]
    resolution = int(sys.argv[2])
    outputpath = sys.argv[3]

    lvisData = lvisGround(filepath)
    lvisData.setElevations()
    lvisData.estimateGround()
    lvisData.reproject(4326, 3857)
    lat = np.array(lvisData.lat)
    lon = np.array(lvisData.lon)
    z = np.array(lvisData.zG)
    point_list = np.array([lat, lon, z]).T
    minx, miny, maxx, maxy = lvisData.dumpBounds()



    minx = int(minx)
    miny = int(miny)
    maxx = int(maxx)
    maxy = int(maxy)

    data = []

    LON = np.arange(minx, maxx, resolution)
    LAT = np.arange(miny, maxy, resolution)
    for x in LON:
        for y in LAT:
            data.append(interpolation(x, y, point_list, resolution))
    data = np.array(data).reshape((len(LON), len(LAT)))
    tiffhandler = tiffHandle(minx, miny, maxx, maxy)
    tiffhandler.writeTiff(data, filename=outputpath, epsg=3857)

    print("finished")