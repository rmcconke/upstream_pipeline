import argparse
import numpy as np
import os
import Ofpp
from scipy.interpolate import griddata
import matplotlib.pyplot as plt

from dataFoam.utilities.foamIO.writeFoam_DUCT import writeFoam_U_DUCT, writeFoam_TauDNS_DUCT

parser = argparse.ArgumentParser(description='write DUCT DNS data as .txt to an OpenFOAM grid for gradient computations and further processing.')
parser.add_argument("-Re", "--Re",  help="Reynolds number for the case")
parser.add_argument("-DNS_data_dir", "--DNS_data_dir",  help="storage location of .txt files")
parser.add_argument("-DNS_foam_dir", "--DNS_foam_dir",  help="storage location of DNS foam cases. Should contain a template case with a mesh.")
args = parser.parse_args()

#print(f'No overwrite:{args.no_overwrite}')

# Read duct fields: U, TauDNS, Cell Centres_
um = np.genfromtxt(os.path.join(args.DNS_data_dir, f'DUCT_{args.Re}_um.txt'),skip_header=1)
vm = np.genfromtxt(os.path.join(args.DNS_data_dir, f'DUCT_{args.Re}_vm.txt'),skip_header=1)
wm = np.genfromtxt(os.path.join(args.DNS_data_dir, f'DUCT_{args.Re}_wm.txt'),skip_header=1)

DNS_U = np.column_stack((um,vm,wm))

uu = np.genfromtxt(os.path.join(args.DNS_data_dir, f'DUCT_{args.Re}_uu.txt'),skip_header=1)
uv = np.genfromtxt(os.path.join(args.DNS_data_dir, f'DUCT_{args.Re}_uv.txt'),skip_header=1)
uw = np.genfromtxt(os.path.join(args.DNS_data_dir, f'DUCT_{args.Re}_uw.txt'),skip_header=1)
vv = np.genfromtxt(os.path.join(args.DNS_data_dir, f'DUCT_{args.Re}_vv.txt'),skip_header=1)
vw = np.genfromtxt(os.path.join(args.DNS_data_dir, f'DUCT_{args.Re}_vw.txt'),skip_header=1)
ww = np.genfromtxt(os.path.join(args.DNS_data_dir, f'DUCT_{args.Re}_ww.txt'),skip_header=1)

DNS_tau = np.column_stack((uu,uv,uw,vv,vw,ww))

DNS_x = np.genfromtxt(os.path.join(args.DNS_data_dir, f'DUCT_{args.Re}_x.txt'),skip_header=1)
DNS_y = np.genfromtxt(os.path.join(args.DNS_data_dir, f'DUCT_{args.Re}_y.txt'),skip_header=1)
DNS_z = np.genfromtxt(os.path.join(args.DNS_data_dir, f'DUCT_{args.Re}_z.txt'),skip_header=1)

DNS_C = np.column_stack((DNS_y,DNS_z))

# Read OpenFOAM cell centres
Cx = Ofpp.parse_internal_field(os.path.join(args.DNS_foam_dir,'squareDuct_template','0/Cx'))
Cy = Ofpp.parse_internal_field(os.path.join(args.DNS_foam_dir,'squareDuct_template','0/Cy'))
Cz = Ofpp.parse_internal_field(os.path.join(args.DNS_foam_dir,'squareDuct_template','0/Cz'))
MESH_C = np.column_stack((Cy,Cz)) 

# Interpolate duct fields to OpenFOAM cell centres
MESH_U = griddata(DNS_C,
                    DNS_U,
                    MESH_C,
                    method='linear')

MESH_TauDNS = griddata(DNS_C,
                    DNS_tau,
                    MESH_C,
                    method='linear')

# Write Duct fields to OpenFOAM: U and TauDNS
foamdir = os.path.join(args.DNS_foam_dir,f'squareDuct_Re_{args.Re}')
if os.path.exists(foamdir):
    os.system(f'rm -r {foamdir}')
template = os.path.join(args.DNS_foam_dir,'squareDuct_template')
os.system(f'cp -r {template} {foamdir}')
writeFoam_U_DUCT(os.path.join(foamdir,'0/U'),MESH_U)
writeFoam_TauDNS_DUCT(os.path.join(foamdir,'0/tau'),MESH_TauDNS)