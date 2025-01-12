from dataFoam.utilities.MLDatasetFromFoamCase import MLDatasetFromFoamCase
import argparse
import numpy as np
import os
import Ofpp
from scipy.interpolate import griddata
import matplotlib.pyplot as plt
import multiprocessing as mp
from itertools import repeat
from dataFoam.utilities.foamIO.writeFoam_DUCT import writeFoam_U_DUCT, writeFoam_TauDNS_DUCT

parser = argparse.ArgumentParser(description='Average RANS fields along the duct x direction, so RANS data is in an averaged duct cross-section plane like DNS data')
parser.add_argument("-Re", "--Re",  help="Reynolds number for the case")
parser.add_argument("-RANS_numpy_dir", "--RANS_numpy_dir",  help="storage location of numpy files")
case_type = parser.add_argument("-case_type", "--case_type", help="case type, e.g. komega, komegasst, LES")
args = parser.parse_args()

RANS_case = MLDatasetFromFoamCase('','','',args.case_type,'','')
fields = RANS_case.foam_field_list

def save_plane_averaging_index():
    C = np.load(os.path.join(args.RANS_numpy_dir, f'{args.case_type}_squareDuct_Re_{args.Re}_C.npy'))
    x = C[:,0]
    y = C[:,1]
    z = C[:,2]
    unique_y = np.sort(np.unique(y))
    unique_z = np.sort(np.unique(z))
    Y, Z = np.meshgrid(unique_y, unique_z)
    Y = Y.flatten()
    Z = Z.flatten()
    ind_avg = np.empty(y.shape)
    #ind_field = np.mean(field[(y == Y) & (z == Z)])
    for i, yi in enumerate(y):
        ind_avg[i] = np.argwhere((y[i]== Y) & (z[i] == Z))
    np.save(os.path.join(args.RANS_numpy_dir,f'{args.case_type}_squareDuct_allRe_plane_averaging_index_field.npy'),ind_avg)

if not os.path.isfile(os.path.join(args.RANS_numpy_dir,f'{args.case_type}_squareDuct_allRe_plane_averaging_index_field.npy')):
    save_plane_averaging_index()
ind_avg = np.load(os.path.join(args.RANS_numpy_dir,f'{args.case_type}_squareDuct_allRe_plane_averaging_index_field.npy'))

def average_field(field,ind_avg,i):
    avg_field = np.mean(field[ind_avg==i])
    return avg_field

for fieldname in fields:
    print(fieldname)
    field = np.load(os.path.join(args.RANS_numpy_dir, f'{args.case_type}_squareDuct_Re_{args.Re}_{fieldname}.npy'))
    n_cells_plane = len(np.unique(ind_avg))
    if field.ndim == 1:
        avg_field = np.empty((n_cells_plane))
    elif field.ndim == 2:
        avg_field = np.empty((n_cells_plane,field.shape[1]))
    elif field.ndim == 3:
        avg_field = np.empty((n_cells_plane,field.shape[1],field.shape[2]))

    #ncpus = int(os.environ.get('SLURM_CPUS_PER_TASK',default=2))
    #print(f'Parallel ncpus {ncpus}')
    #pool = mp.Pool(processes=ncpus)
    #result = pool.starmap(average_field, [(fieldi,ind_avgi,i) for fieldi,ind_avgi, i in zip(repeat(field),repeat(ind_avg),range(len(avg_field)))])
    #avg_field = np.array(result)
    for i in range(len(avg_field)):
        avg_field[i] = np.mean(field[ind_avg==i],axis=0)
    print(avg_field.shape)
    np.save(os.path.join(args.RANS_numpy_dir, f'{args.case_type}_squareDuctAve_Re_{args.Re}_{fieldname}.npy'),avg_field)

C = np.load(os.path.join(args.RANS_numpy_dir, f'{args.case_type}_squareDuctAve_Re_{args.Re}_C.npy'))
C[:,0] = np.zeros(len(C))
np.save(os.path.join(args.RANS_numpy_dir, f'{args.case_type}_squareDuctAve_Re_{args.Re}_C.npy'),C)
