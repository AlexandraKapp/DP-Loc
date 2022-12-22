import pickle
import numpy as np
import csv
import pandas as pd


from tables import *
from utils import *
cnf = load_cfg("cfg/cfg_general_Simra.json")

# create a projector class, as in the algorithm
projector = Projector(cnf.MIN_X, cnf.MIN_Y, cnf.MAX_X, cnf.MAX_Y)

MAP_HEIGHT = int(ceil(projector.toProjected(cnf.MAX_X, cnf.MAX_Y)[1] / cnf.CELL_SIZE))
MAP_WIDTH = int(ceil(projector.toProjected(cnf.MAX_X, cnf.MAX_Y)[0] / cnf.CELL_SIZE))

# dicts for conversion as in projector class
cells = [(x, y) for x in range(MAP_HEIGHT + 1) for y in range(MAP_WIDTH + 1)]
cell2id = dict(zip(cells, range(1, len(cells) + 1)))
id2cell = dict(zip(range(1, len(cells) + 1), cells))

h5file = open_file("datasets/simra/mapped_data-304.h5", mode="r")
input_traces = h5file.root.Traces

ids_input = []
for i in range(0, len(input_traces)-1):
    for j in range(0, len(input_traces[i])-1):    
        ids_input.append(input_traces[i][j][0])

grid_ids_input = pd.Series(ids_input)

# grid input to coordinates
with open("/data/input_reversed.csv", 'w') as csvfile: 
    write = csv.writer(csvfile) 
    write.writerow(["tid", "lng", "lat"])
    for i in range(0, len(input_traces)-1):
        ids = [id2cell[cell_id[0]] for cell_id in input_traces[i]]
        coords_projected = [(y*cnf.CELL_SIZE, x*cnf.CELL_SIZE) for x,y in ids]
        coords_gps = list(projector.toGPS_list(coords_projected))
        for coord_pair in coords_gps:
            x, y = coord_pair
            write.writerow([i, x, y]) 

h5file.close()


# all cords in mapping
all_coords_input = [(x*cnf.CELL_SIZE, y*cnf.CELL_SIZE) for x,y in cell2id.keys()]
all_coords = list(projector.toGPS_list(all_coords_input))

import csv
with open("/data/grid_coords.csv", 'w') as csvfile: 
    write = csv.writer(csvfile) 
    write.writerow(["lng", "lat"])
    for coords in all_coords:
        write.writerow(coords)  

