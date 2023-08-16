import argparse
import numpy as np
import os
import Ofpp
from scipy.interpolate import griddata
import matplotlib.pyplot as plt

from dataFoam.utilities.foamIO.writeFoam_DUCT import writeFoam_U_DUCT, writeFoam_TauDNS_DUCT

parser = argparse.ArgumentParser(description='write Pinelli DNS raw data to .txt')
parser.add_argument("-raw_filename", "--raw_filename",  help="Raw filename")
parser.add_argument("-Re", "--Re",  help="Reynolds number for the case")
parser.add_argument("-DNS_data_dir", "--DNS_data_dir",  help="storage location of .txt files")
args = parser.parse_args()


import numpy as np
import matplotlib.pyplot as plt
filename = args.raw_filename

ny = np.fromfile(filename,np.int32)[0]

data = np.fromfile(filename,np.float64)

um = np.empty(ny**2)
vm = np.empty(ny**2)
wm = np.empty(ny**2)
uu = np.empty(ny**2)
uv = np.empty(ny**2)
uw = np.empty(ny**2)
vv = np.empty(ny**2)
vw = np.empty(ny**2)
ww = np.empty(ny**2)

y = data[5:(5+ny)]
y = y/(max(y)-min(y)) - (max(y)+min(y))/2
z = data[(5+ny):(5+2*ny)]
z = z/(max(z)-min(z)) - (max(z)+min(z))/2

[Y,Z] = np.meshgrid(y,z)
y = Y.flatten()
z = Z.flatten()

fields = data[(5+2*ny):]
um = fields[0*ny*ny:((0+1)*ny*ny)]
vm = fields[1*ny*ny:((1+1)*ny*ny)]
wm = fields[2*ny*ny:((2+1)*ny*ny)]
uu = fields[3*ny*ny:((3+1)*ny*ny)]
uv = fields[4*ny*ny:((4+1)*ny*ny)]
uw = fields[5*ny*ny:((5+1)*ny*ny)]
vv = fields[6*ny*ny:((6+1)*ny*ny)]
vw = fields[7*ny*ny:((7+1)*ny*ny)]
ww = fields[8*ny*ny:((8+1)*ny*ny)]

np.savetxt(os.path.join(args.DNS_data_dir,f'DUCT_{args.Re}_x.txt'),np.zeros(y.shape),header='x')
np.savetxt(os.path.join(args.DNS_data_dir,f'DUCT_{args.Re}_y.txt'),y,header='y')
np.savetxt(os.path.join(args.DNS_data_dir,f'DUCT_{args.Re}_z.txt'),z,header='z')

np.savetxt(os.path.join(args.DNS_data_dir,f'DUCT_{args.Re}_um.txt'),um,header='um')
np.savetxt(os.path.join(args.DNS_data_dir,f'DUCT_{args.Re}_vm.txt'),vm,header='vm')
np.savetxt(os.path.join(args.DNS_data_dir,f'DUCT_{args.Re}_wm.txt'),wm,header='wm')
np.savetxt(os.path.join(args.DNS_data_dir,f'DUCT_{args.Re}_uu.txt'),uu,header='uu')
np.savetxt(os.path.join(args.DNS_data_dir,f'DUCT_{args.Re}_uv.txt'),uv,header='uv')
np.savetxt(os.path.join(args.DNS_data_dir,f'DUCT_{args.Re}_uw.txt'),uw,header='uw')
np.savetxt(os.path.join(args.DNS_data_dir,f'DUCT_{args.Re}_vv.txt'),vv,header='vv')
np.savetxt(os.path.join(args.DNS_data_dir,f'DUCT_{args.Re}_vw.txt'),vw,header='vw')
np.savetxt(os.path.join(args.DNS_data_dir,f'DUCT_{args.Re}_ww.txt'),ww,header='ww')


