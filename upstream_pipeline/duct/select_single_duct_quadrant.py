#from dataFoam.utilities.MLDatasetFromFoamCase import MLDatasetFromFoamCase
import argparse
import numpy as np
import os
import Ofpp
from scipy.interpolate import griddata
import matplotlib.pyplot as plt

#from dataFoam.utilities.foamIO.writeFoam_DUCT import writeFoam_U_DUCT, writeFoam_TauDNS_DUCT

parser = argparse.ArgumentParser(description='')
parser.add_argument("-Re", "--Re",  help="Reynolds number for the case")
parser.add_argument("-numpy_dir", "--numpy_dir",  help="base numpy e.g. /home/dataset/numpy...")

args = parser.parse_args()

#def save_plane_averaging_index():
def save_quadrant_averaging_index():
    C = np.load(os.path.join(args.numpy_dir,'komegasst', f'komegasst_squareDuctAve_Re_{args.Re}_C.npy'))
    x = C[:,0]
    y = C[:,1]
    z = C[:,2]

    yabs = abs(y).round(decimals=4)
    zabs = abs(z).round(decimals=4)


    print(np.unique(y,return_counts=True))
    print(len(np.unique(y,return_counts=True)))

    unique_y = np.sort(np.unique(yabs))
    unique_z = np.sort(np.unique(zabs))
    Y, Z = np.meshgrid(unique_y, unique_z)
    Y = Y.flatten()
    Z = Z.flatten()

    print(len(Y))
    ind_avg = np.empty(yabs.shape)
    quadrant = np.empty(yabs.shape)

    #ind_field = np.mean(field[(y == Y) & (z == Z)])
    for i, yi in enumerate(yabs):
        ind_avg[i] = np.argwhere((yabs[i]== Y) & (zabs[i] == Z))
        if (y[i] < 0) & (z[i] > 0):
            quadrant[i] = 2
        elif (y[i] < 0) & (z[i] < 0):
            quadrant[i] = 3
        elif (y[i] > 0) & (z[i] < 0):
            quadrant[i] = 4
        else:
            quadrant[i] = 1
    np.save(os.path.join(args.numpy_dir,'komegasst','komegasst_squareDuct_allRe_quadrant_averaging_index_field.npy'),ind_avg)
    np.save(os.path.join(args.numpy_dir,'komegasst','komegasst_squareDuct_allRe_quadrant_index_field.npy'),quadrant)
    np.save(os.path.join(args.numpy_dir,'komegasst', f'komegasst_squareDuctQuadAve_Re_{args.Re}_C.npy'),np.column_stack((np.zeros(len(Y)),Y,Z)))



#if not os.path.isfile(os.path.join(args.numpy_dir,'komegasst','komegasst_squareDuct_allRe_quadrant_averaging_index_field.npy')):
save_quadrant_averaging_index()
ind_avg = np.load(os.path.join(args.numpy_dir,'komegasst','komegasst_squareDuct_allRe_quadrant_averaging_index_field.npy'))
quadrant = np.load(os.path.join(args.numpy_dir,'komegasst','komegasst_squareDuct_allRe_quadrant_index_field.npy'))
rans_field_list = ['k',
                    'omega',
                    'epsilon',
                    'T_t_ke',
                    'T_t_nut',
                    'T_k',
                    'U',
                    'gradp',
                    'gradk',
                    'gradomega',
                    'p',
                    'DUDt',
                    'wallDistance',
                    'nut',
                    'S',
                    'Shat',
                    'R',
                    'Rhat',
                    'Ao',
                    'Ak',
                    'Aohat',
                    'Akhat',
                    'gradU',
                    'skewness',
                    'C'
                    ]

def assemble_rans_field_list(rans_field_list):
    for i in range(47):
        rans_field_list.append(f'I1_{i+1}')
        rans_field_list.append(f'I2_{i+1}')
    for i in range(10):
        rans_field_list.append(f'T{i+1}')
    for i in range(9):
        rans_field_list.append(f'q{i+1}')
    for i in range(5):
        rans_field_list.append(f'lambda{i+1}')
    print('Assembled full foam field list: ')
    print(rans_field_list)
    return rans_field_list

fields = assemble_rans_field_list(rans_field_list)

for fieldname in fields:
    print(fieldname)
    field = np.load(os.path.join(args.numpy_dir,'komegasst', f'komegasst_squareDuctAve_Re_{args.Re}_{fieldname}.npy'))
    n_cells_plane = len(np.unique(ind_avg))
    if field.ndim == 1:
        quad1_field = np.empty((n_cells_plane))
    elif field.ndim == 2:
        quad1_field = np.empty((n_cells_plane,field.shape[1]))
    elif field.ndim == 3:
        quad1_field = np.empty((n_cells_plane,field.shape[1],field.shape[2]))

    quad1_field = field[quadrant == 1]
    np.save(os.path.join(args.numpy_dir,'komegasst', f'komegasst_squareDuctQuad1_Re_{args.Re}_{fieldname}.npy'),quad1_field)

fields = ['U',
        'gradU',
        'TauDNS',
        'S',
        'R',
        'k',
        'a',
        'b',
        ]

for fieldname in fields:
    print(fieldname)
    field = np.load(os.path.join(args.numpy_dir,'DNS', f'DNS_mappedSquareDuct_Re_{args.Re}_{fieldname}.npy'))
    n_cells_plane = len(np.unique(ind_avg))
    if field.ndim == 1:
        quad1_field = np.empty((n_cells_plane))
    elif field.ndim == 2:
        quad1_field = np.empty((n_cells_plane,field.shape[1]))
    elif field.ndim == 3:
        quad1_field = np.empty((n_cells_plane,field.shape[1],field.shape[2]))

    quad1_field = field[quadrant == 1]
    np.save(os.path.join(args.numpy_dir,'DNS', f'DNS_squareDuctQuad1_Re_{args.Re}_{fieldname}.npy'),quad1_field)