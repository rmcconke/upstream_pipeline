import argparse
import numpy as np
import os
import Ofpp
from scipy.interpolate import griddata
import matplotlib.pyplot as plt

from dataFoam.preprocessing.calculate_extra_fields import calc_k_b_a

parser = argparse.ArgumentParser(description='write .txt files to numpy binaries.')
parser.add_argument("-case", "--case",  help="case")
parser.add_argument("-REF_data_dir", "--REF_data_dir",  help="storage location of .txt files")
parser.add_argument("-REF_numpy_dir", "--REF_numpy_dir",  help="storage location of numpy files")
args = parser.parse_args()

um = np.genfromtxt(os.path.join(args.REF_data_dir, f'{args.case}_um.txt'),skip_header=1)
vm = np.genfromtxt(os.path.join(args.REF_data_dir, f'{args.case}_vm.txt'),skip_header=1)
wm = np.genfromtxt(os.path.join(args.REF_data_dir, f'{args.case}_wm.txt'),skip_header=1)

REF_U = np.column_stack((um,vm,wm))

uu = np.genfromtxt(os.path.join(args.REF_data_dir, f'{args.case}_uu.txt'),skip_header=1)
uv = np.genfromtxt(os.path.join(args.REF_data_dir, f'{args.case}_uv.txt'),skip_header=1)
uw = np.genfromtxt(os.path.join(args.REF_data_dir, f'{args.case}_uw.txt'),skip_header=1)
vv = np.genfromtxt(os.path.join(args.REF_data_dir, f'{args.case}_vv.txt'),skip_header=1)
vw = np.genfromtxt(os.path.join(args.REF_data_dir, f'{args.case}_vw.txt'),skip_header=1)
ww = np.genfromtxt(os.path.join(args.REF_data_dir, f'{args.case}_ww.txt'),skip_header=1)

REF_tau = np.empty((len(uu),3,3))
REF_tau[:,0,0] = uu
REF_tau[:,0,1] = uv
REF_tau[:,0,2] = uw
REF_tau[:,1,1] = vv
REF_tau[:,1,2] = vw
REF_tau[:,2,2] = ww

REF_tau[:,1,0] = REF_tau[:,0,1]
REF_tau[:,2,0] = REF_tau[:,0,2]
REF_tau[:,2,1] = REF_tau[:,1,2]

REF_x = np.genfromtxt(os.path.join(args.REF_data_dir, f'{args.case}_x.txt'),skip_header=1)
REF_y = np.genfromtxt(os.path.join(args.REF_data_dir, f'{args.case}_y.txt'),skip_header=1)
REF_z = np.genfromtxt(os.path.join(args.REF_data_dir, f'{args.case}_z.txt'),skip_header=1)

REF_C = np.column_stack((REF_x,REF_y,REF_z))

np.save(os.path.join(args.REF_numpy_dir,f'REF_{args.case}_tau.npy'),REF_tau)
np.save(os.path.join(args.REF_numpy_dir,f'REF_{args.case}_U.npy'),REF_U)
np.save(os.path.join(args.REF_numpy_dir,f'REF_{args.case}_C.npy'),REF_C)
calc_k_b_a(args.REF_numpy_dir,f'REF_{args.case}')




