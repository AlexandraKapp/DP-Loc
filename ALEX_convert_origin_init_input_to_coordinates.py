import pickle
import numpy as np
import csv
import pandas as pd


from tables import *
from utils import *
cnf = load_cfg("cfg/cfg_general_Simra.json")

USED_WORDS_PATH = "/Users/alexandra/Documents/GitHub/DP-Loc/output/simra/no_dp/cell_500/used_words_500_epsNone.pickle"
ORIG_INIT_PATH = "/Users/alexandra/Documents/GitHub/DP-Loc/output/simra/no_dp/cell_500/orig_init_data-cell_500.pickle"
OUTPUT_CSV_PATH = "/Users/alexandra/Documents/GitHub/DP-Loc/output/simra/no_dp/cell_500/orig_init_data_cell.csv"


# create a projector class, as in the algorithm
projector = Projector(cnf.MIN_X, cnf.MIN_Y, cnf.MAX_X, cnf.MAX_Y)

MAP_HEIGHT = int(ceil(projector.toProjected(cnf.MAX_X, cnf.MAX_Y)[1] / cnf.CELL_SIZE))
MAP_WIDTH = int(ceil(projector.toProjected(cnf.MAX_X, cnf.MAX_Y)[0] / cnf.CELL_SIZE))

# dicts for conversion as in projector class
cells = [(x, y) for x in range(MAP_HEIGHT + 1) for y in range(MAP_WIDTH + 1)]
cell2id = dict(zip(cells, range(1, len(cells) + 1)))
id2cell = dict(zip(range(1, len(cells) + 1), cells))

# this needs to be run in the DP-Loc folder, otherwise these imports don't work
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

used_words = pickle.load(open(USED_WORDS_PATH, "rb"))

# dicts for conversion of token and cells
cell2token = dict(zip(used_words, range(1, len(used_words) + 1)))
token2cell = {v: k for k, v in cell2token.items()}

# get the data
orig_init = pickle.load(open(ORIG_INIT_PATH, "rb"))

# write these as readable and mapped csv file
with open(OUTPUT_CSV_PATH, 'w') as csvfile: 
    write = csv.writer(csvfile) 
    write.writerow(["tid", "lng", "lat", "datetime"])
    counter = 0
    for i in range(0, len(orig_init)-1):
        start_id = id2cell[token2cell[orig_init[i][0]]]
        dest_id = id2cell[token2cell[orig_init[i][1]]]
        time = orig_init[i][2]
        coords_projected_start = (start_id[1]*cnf.CELL_SIZE, start_id[0]*cnf.CELL_SIZE)
        coords_projected_dest = (dest_id[1]*cnf.CELL_SIZE, dest_id[0]*cnf.CELL_SIZE)
        coords_gps = list(projector.toGPS_list([coords_projected_start, coords_projected_dest]))
        for coord_pair in coords_gps:
            x, y = coord_pair
            write.writerow([i, x, y, time]) #TODO: now the same timestamp for each point in a trajectory is used. Maybe convert this to a timestamp and make it increasing?
            counter += 1 

