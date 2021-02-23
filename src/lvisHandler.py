from processLVIS import lvisGround
import numpy as np
import pandas as pd
import os, sys


class lvisHandler():
    def __init__(self, filenames, recover_data=False):
        self.lat = np.array([])
        self.lon = np.array([])
        self.z = np.array([])
        self.filenames = filenames
        self.getData()
        if recover_data:
            for file in os.listdir("./data"):
                if '.csv' in file.lower():
                    data = pd.read_csv(file)
                    self.lat = np.append(self.lat, np.array(data['lat']))
                    self.lon = np.append(self.lon, np.array(data['lon']))
                    self.z = np.append(self.z, data['z'])

    def getData(self):
        for filepath in self.filenames:
            filename = os.path.basename(filepath)
            lvis = lvisGround(filepath)
            # set elevation
            lvis.setElevations()
            # find the ground (repeating some of the last three lines)
            lvis.estimateGround()
            lvis.reproject(4326, 3857)

            pd.DataFrame({'lat': np.array(lvis.lat), 'lon': np.array(lvis.lon), 'z': np.array(lvis.zG)}).to_csv(
                os.path.join('../data/2009/', ''.join(filename.split('.')[:-1]) + '.csv'), index=False)


if __name__ == '__main__':
    import os

    filepath = sys.argv[1] # '../2009'
    finishedpath = sys.argv[2] #'../data/2009'

    filenames = []
    for file in os.listdir(filepath):
        if '.h5' in file.lower() and file.replace('.h5', '.csv') not in os.listdir(finishedpath):
            filenames.append(os.path.join(filepath, file))
    print(filenames)
    handler = lvisHandler(filenames)


    data = pd.read_csv('../data/2009/all2009.csv')
    selected = data[(data.lon > 261) & (data.lon < 262) & (data.lat < -75) & (data.lat > -75.5)]
    selected.to_csv('../data/2009/selectedxy.csv')

    data = pd.read_csv('../data/2015/all2015.csv')
    selected = data[(data.lon > 261) & (data.lon < 262) & (data.lat < -75) & (data.lat > -75.5)]
    selected.to_csv('../data/2015/selectedxy.csv')

