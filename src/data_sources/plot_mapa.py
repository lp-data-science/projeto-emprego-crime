import shapefile
import numpy as np
import matplotlib.pyplot as plt

r = shapefile.Reader("BRUFE250GC_SIR.shp")
for shape in list(r.iterShapes()):
    npoints=len(shape.points) # total points
    nparts = len(shape.parts) # total parts

    if nparts == 1:
       x_lon = np.zeros((len(shape.points),1))
       y_lat = np.zeros((len(shape.points),1))
       for ip in range(len(shape.points)):
           x_lon[ip] = shape.points[ip][0]
           y_lat[ip] = shape.points[ip][1]
       plt.plot(x_lon,y_lat)

    else: # loop over parts of each shape, plot separately
       for ip in range(nparts): # loop over parts, plot separately
            i0=shape.parts[ip]
            if ip < nparts-1:
              i1 = shape.parts[ip+1]-1
            else:
              i1 = npoints

            seg=shape.points[i0:i1+1]
            x_lon = np.zeros((len(seg),1))
            y_lat = np.zeros((len(seg),1))
            for ip in range(len(seg)):
                x_lon[ip] = seg[ip][0]
                y_lat[ip] = seg[ip][1]

            plt.plot(x_lon,y_lat)

plt.show()

    
