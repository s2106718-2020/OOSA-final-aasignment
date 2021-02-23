
'''
An example of how to use the 
LVIS python scripts
'''

from processLVIS import lvisGround

if __name__=="__main__":
  '''Main block'''

  # an example LVIS file
  filename='../2009/ILVIS1B_AQ2009_1020_R1408_052195.LGW4'

  # find bounds
  b=lvisGround(filename,onlyBounds=True)

  # set some bounds
  x0=b.bounds[0]
  y0=b.bounds[1]
  x1=(b.bounds[2]-b.bounds[0])/15+b.bounds[0]
  y1=(b.bounds[3]-b.bounds[1])/15+b.bounds[1]


  # read in bounds
  lvis=lvisGround(filename,minX=x0,minY=y0,maxX=x1,maxY=y1)

  # set elevation
  lvis.setElevations()

  # find the ground (repeating some of the last three lines)
  lvis.estimateGround()

