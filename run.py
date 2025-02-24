import os
import sys
import time
import utils


cnf = utils.load_cfg("cfg/cfg_general_Simra.json")
#cnf = utils.load_cfg("cfg/cfg_general_Tapas.json")
#cnf = utils.load_cfg("cfg/cfg_general_porto.json")


def run_sim(cfg, cell_size):
    print(cfg, cell_size)
   
    # Step 2: Train for your life...
    if os.system("python training.py VAE %d %s" % (cell_size, cfg)):
        sys.exit(1)
    if os.system("python training.py TRACES %d %s" % (cell_size, cfg)):
        sys.exit
    # Step 3: Generate results for your paper...
    if os.system("python generator.py VAE %d %s" % (cell_size, cfg)):
        sys.exit(1)
    
    if os.system("python generator.py TRACES %d %s" % (cell_size, cfg)):
        sys.exit(1)
    # Step 4: Evaluate your performance...
    #for m in [0, 1, 5, 10, 25, 50, 100, 150]: 
    #	if os.system("python evaluate.py %d %s %d" % (cell_size, cfg, m)):
    #        sys.exit(1)


if __name__ == "__main__":
    print("======================== ", cnf.INPUT_DIR, "=================================")
    print("======================== CELL SIZE: ", cnf.CELL_SIZE, "=================================")
    named_tuple = time.localtime() # get struct_time
    time_string = time.strftime("%m/%d/%Y, %H:%M:%S", named_tuple)
    print("STARTING TIME: ", time_string)

    # # Step 1: Map taxi GPS data to a grid
    #if os.system("python create_mapped_data_Simra.py %f" % cnf.CELL_SIZE):
    #if os.system("python create_mapped_data_SF_Porto.py %f" % cnf.CELL_SIZE):
    #    sys.exit(1)

    #print("=================================================================== EPS = None ==================================================================")
    #run_sim("cfg/cfg_epsNone.json", cell_size=cnf.CELL_SIZE)
    run_sim("cfg/cfg_eps2.json", cell_size=cnf.CELL_SIZE)

    #print("=================================================================== EPS = 5 ==================================================================")
    #run_sim("cfg/cfg_eps5.json", cell_size=cnf.CELL_SIZE)
    
    named_tuple = time.localtime() # get struct_time
    time_string = time.strftime("%m/%d/%Y, %H:%M:%S", named_tuple)
    print("FINISH TIME: ", time_string)

# LA FIN
