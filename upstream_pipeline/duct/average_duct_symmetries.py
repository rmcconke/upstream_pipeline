"""
This script is deprecated, since rather than averaging duct quadrants, the select_single_duct_quadrant script is used.
"""
#from dataFoam.utilities.MLDatasetFromFoamCase import MLDatasetFromFoamCase
import argparse
import numpy as np
import os
import Ofpp
from scipy.interpolate import griddata
import matplotlib.pyplot as plt

#from dataFoam.utilities.foamIO.writeFoam_DUCT import writeFoam_U_DUCT, writeFoam_TauDNS_DUCT

parser = argparse.ArgumentParser(description='Average RANS fields along the duct x direction, so RANS data is in an averaged duct cross-section plane like DNS data')
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
                    #'C'
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
T_1 = np.eye(3)
#T_2 = np.array([[1,0,0],[0,0,1],[0,-1,0]])
#T_3 = np.array([[1,0,0],[0,-1,0],[0,0,-1]])
#T_4 = np.array([[1,0,0],[0,0,-1],[0,1,0]])

#T_2 = np.array([[1,0,0],[0,1,0],[0,0,-1]])
#T_3 = np.array([[1,0,0],[0,-1,0],[0,0,-1]])
#T_4 = np.array([[1,0,0],[0,-1,0],[0,0,1]])
T_1 = np.array([[1,1,1],[1,1,1],[1,1,1]])

T_2 = np.array([[1,-1,1],[-1,1,1],[1,-1,1]])

T_3 = np.array([[1,-1,-1],[-1,1,1],[-1,1,1]])

T_4 = np.array([[1,1,-1],[1,1,-1],[-1,-1,1]])

print(T_1.shape)
for fieldname in fields:
    print(fieldname)
    field = np.load(os.path.join(args.numpy_dir,'komegasst', f'komegasst_squareDuctAve_Re_{args.Re}_{fieldname}.npy'))
    n_cells_plane = len(np.unique(ind_avg))
    if field.ndim == 1:
        avg_field = np.empty((n_cells_plane))
    elif field.ndim == 2:
        avg_field = np.empty((n_cells_plane,field.shape[1]))
    elif field.ndim == 3:
        avg_field = np.empty((n_cells_plane,field.shape[1],field.shape[2]))

    field_transformed = np.empty(field.shape)
    if field.ndim == 2:
        field_transformed[quadrant == 1] = (T_1@field[quadrant==1].reshape(-1,3,1)).reshape(-1,3)
        field_transformed[quadrant == 2] = (T_2@field[quadrant==2].reshape(-1,3,1)).reshape(-1,3)
        field_transformed[quadrant == 3] = (T_3@field[quadrant==3].reshape(-1,3,1)).reshape(-1,3)
        field_transformed[quadrant == 4] = (T_4@field[quadrant==4].reshape(-1,3,1)).reshape(-1,3)
    if field.ndim == 3:
        field_transformed[quadrant == 1] = T_1*field[quadrant==1]
        field_transformed[quadrant == 2] = T_2*field[quadrant==2]
        field_transformed[quadrant == 3] = T_3*field[quadrant==3]
        field_transformed[quadrant == 4] = T_4*field[quadrant==4]
    else:
        field_transformed = field

    for i in range(len(avg_field)):
        avg_field[i] = np.mean(field_transformed[ind_avg==i],axis=0)
    print(avg_field.shape)
    np.save(os.path.join(args.numpy_dir,'komegasst', f'komegasst_squareDuctQuadAve_Re_{args.Re}_{fieldname}.npy'),avg_field)

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
        avg_field = np.empty((n_cells_plane))
    elif field.ndim == 2:
        avg_field = np.empty((n_cells_plane,field.shape[1]))
    elif field.ndim == 3:
        avg_field = np.empty((n_cells_plane,field.shape[1],field.shape[2]))

    field_transformed = np.empty(field.shape)
    if field.ndim > 1:
        field_transformed[quadrant == 1] = field[quadrant==1]@T_1
        field_transformed[quadrant == 2] = field[quadrant==2]@T_2
        field_transformed[quadrant == 3] = field[quadrant==3]@T_3
        field_transformed[quadrant == 4] = field[quadrant==4]@T_4
    else:
        field_transformed = field

    for i in range(len(avg_field)):
        avg_field[i] = np.mean(field_transformed[ind_avg==i],axis=0)
    print(avg_field.shape)
    np.save(os.path.join(args.numpy_dir,'DNS', f'DNS_squareDuctQuadAve_Re_{args.Re}_{fieldname}.npy'),avg_field)