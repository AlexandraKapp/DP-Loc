import pickle
import numpy as np
import csv

# TODO: you need to get the used words in the algorithm
# I added the following line to the preproc.py file in line 170:
# pickle.dump(used_words, open(f"output/simra/used_words_{cnf.CELL_SIZE}_eps{cnf.EPS}.pickle", "wb"))

CELL_SIZE = 820
MCMC = 100
EPS = 2.0
iteration = 0
#USED_WORDS_PATH = f"/Users/alexandra/Documents/GitHub/DP-Loc/Pout/used_words_{CELL_SIZE}_eps{EPS}.pickle"
USED_WORDS_PATH = f"/Users/alexandra/Documents/GitHub/DP-Loc/output/simra/used_words_{CELL_SIZE}_eps{EPS}.pickle"
#TRACES_PATH = f"/Users/alexandra/Documents/GitHub/DP-Loc/Pout/generated_traces-cell_820-eps__mh100.pickle"
TRACES_PATH = f"/Users/alexandra/Documents/GitHub/DP-Loc/output/simra/generated_traces-cell_{CELL_SIZE}-eps_{EPS}_{MCMC}.pickle"
OUTPUT_CSV_PATH = f"/Users/alexandra/Documents/GitHub/synth_data_evaluation/data/synthetic/dploc/simra_output_cell{CELL_SIZE}_eps{EPS}_mcmc_{MCMC}_iter{iteration}.csv"
#USED_WORDS_PATH = f"/Users/alexandra/Documents/GitHub/DP-Loc/output/Geolife/no_dp/used_words_{CELL_SIZE}_eps{EPS}.pickle"
#TRACES_PATH = f"/Users/alexandra/Documents/GitHub/DP-Loc/output/Geolife/no_dp/generated_traces-cell_{CELL_SIZE}-eps_{EPS}_{MCMC}.pickle"
#OUTPUT_CSV_PATH = f"/Users/alexandra/Documents/GitHub/DP-Loc/output/Geolife/no_dp/geolife_output_cell{CELL_SIZE}_no_dp_mcmc_{MCMC}.csv"


# this needs to be run in the DP-Loc folder, otherwise these imports don't work
from utils import *
#cnf = load_cfg("cfg/cfg_general_porto.json")
#cnf = load_cfg("cfg/cfg_general_Tapas.json")
cnf = load_cfg("cfg/cfg_general_Simra.json")
#cnf = load_cfg("cfg/cfg_general_Geo.json")

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

# get the generated traces
traces = pickle.load(open(TRACES_PATH, "rb"))
seq = np.array(traces, dtype=object)[:,2]

# write these as readable and mapped csv file
with open(OUTPUT_CSV_PATH, 'w') as csvfile: 
    write = csv.writer(csvfile) 
    write.writerow(["tid", "lng", "lat", "datetime"])
    counter = 0
    for i in range(0, len(traces)-1):
        ids = [id2cell[token2cell[cell_id]] for cell_id in traces[i][2]]
        coords_projected = [(y*cnf.CELL_SIZE, x*cnf.CELL_SIZE) for x,y in ids]
        coords_gps = list(projector.toGPS_list(coords_projected))
        for coord_pair in coords_gps:
            x, y = coord_pair
            write.writerow([i, x, y, traces[i][1]]) #TODO: now the same timestamp for each point in a trajectory is used. Maybe convert this to a timestamp and make it increasing?
            counter += 1 
