import numpy as np
import Ofpp
import os
import matplotlib.pyplot as plt
from scipy.interpolate import griddata
import argparse
from dataFoam.utilities.MLDatasetFromFoamCase import MLDatasetFromFoamCase
from dataFoam.utilities.foamIO.readFoam import get_endtime

parser = argparse.ArgumentParser()
case_type = parser.add_argument("-case_type", "--case_type", help="case type, e.g. komega, komegasst, LES")
args = parser.parse_args()

RANS_case = MLDatasetFromFoamCase('','','',args.case_type,'','')


RANS_foam_folder = os.path.join(os.getenv('ML_FOAM_DATASET'),args.case_type,'fp/writeFields/flatplate/')
RANS_numpy_folder = os.path.join(os.getenv('ML_NUMPY_DATASET'),args.case_type)
DNS_orig_folder = os.path.join(os.getenv('ML_FLATPLATE_DATA'),'data')
DNS_numpy_folder = os.path.join(os.getenv('ML_NUMPY_DATASET'),'REF')

endtime = str(get_endtime(RANS_foam_folder))
nu = 1.388e-05
U_infty = 69.4*0.99
interp_method = 'linear'

rans_field_list = RANS_case.foam_field_list

DNS_Re_theta_list = ['0670', '1000', '1410', '2000', '2540', '3030', '3270', '3630', '3970', '4060']


def v_line(wall_index):
    ind = np.where(abs(C[:,0] - C_bottom[wall_index])<1E-5)[0]
    return RANS_U[ind,:],C[:,1][ind], ind

def get_ind_wall(Re_theta, Re_theta_match):
    return np.nanargmin(np.abs(Re_theta-Re_theta_match))

def get_ind_volume(ind_wall, C, C_bottom, theta_i):
    return np.where((abs(C[:,0] - C_bottom[ind_wall])<1E-5) & (abs(C[:,1])<5*theta_i))[0]

# Loop 1: calculate RANS wall-normalized quantities
C_bottom = Ofpp.parse_boundary_field(os.path.join(RANS_foam_folder,endtime,'C'))[b'bottomWall'][b'value'][:,0]
C = np.load(os.path.join(RANS_numpy_folder,f'{args.case_type}_flatplate_C.npy'))
wss = Ofpp.parse_boundary_field(os.path.join(RANS_foam_folder,endtime,'wallShearStress'))[b'bottomWall'][b'value'][:,0]
RANS_U = np.load(os.path.join(RANS_numpy_folder,f'{args.case_type}_flatplate_U.npy'))
RANS_k = np.load(os.path.join(RANS_numpy_folder,f'{args.case_type}_flatplate_k.npy'))
RANS_y = C[:,1]
RANS_U_plus = np.empty(RANS_U.shape)
RANS_k_plus = np.empty(RANS_k.shape)
RANS_y_plus = np.empty(C[:,1].shape)
utau = np.sqrt(np.abs(wss))
theta = np.empty(wss.shape)
Re_theta = np.empty(wss.shape)

def lagrange_polynomial_derivative(x,fx):
    x0 = np.concatenate(([x[0]],x[0:-2],[x[-3]]))
    x1 = np.concatenate(([x[1]],x[1:-1],[x[-2]]))
    x2 = np.concatenate(([x[2]],x[2:],[x[-1]]))
    fx0 = np.concatenate(([fx[0]],fx[0:-2],[fx[-3]]))
    fx1 = np.concatenate(([fx[1]],fx[1:-1],[fx[-2]]))
    fx2 = np.concatenate(([fx[2]],fx[2:],[fx[-1]]))
    xq = x
    derivative = fx0*(2*xq - x1 - x2)/((x0-x1)*(x0-x2)) + fx1*(2*xq - x0 - x2)/((x1-x0)*(x1-x2)) + fx2*(2*xq - x0 - x1)/((x2-x0)*(x2-x1))
    return derivative

def interpolate(C_fine, field_fine, C_coarse, method=interp_method):
    interp_field = griddata(C_fine,
                            field_fine,
                            C_coarse,
                            method=method)

    if interp_method != 'nearest':
        ind_nan = np.argwhere(np.isnan(interp_field))
        if len(ind_nan) >0:
            print('Interpolation found '+ str(len(ind_nan))+' nans, using nearest to fill these nans in')
        interp_field[ind_nan] = griddata(C_fine,
                                         field_fine,
                                         C_coarse[ind_nan], method='nearest')
    return interp_field
                
print(RANS_U.shape)
for i_wall, x_wall in enumerate(C_bottom):
    utau_i = utau[i_wall]
    v_U, v_y, v_ind = v_line(i_wall)
    RANS_U_plus[v_ind] = np.divide(v_U,utau_i)
    RANS_y_plus[v_ind] = np.divide(utau_i*v_y,nu)
    RANS_k_plus[v_ind] = np.divide(RANS_k[v_ind],np.square(utau_i))
    U_inf_i = np.mean(v_U[-65:,0])
    v_U_Uinf = v_U[:,0]/U_inf_i
    theta[i_wall] = np.sum((v_y[1:]-v_y[0:-1])*(v_U_Uinf[0:-1]*(1-v_U_Uinf[0:-1])+v_U_Uinf[1:]*(1-v_U_Uinf[1:]))/2)
    Re_theta[i_wall] = np.divide(U_inf_i*theta[i_wall],nu)

fig, ax = plt.subplots(1,1,figsize=(6,6))
nasa_Retheta = np.genfromtxt(os.path.join(os.getenv('ML_FLATPLATE_DATA'),'nasa_retheta_variation_typical.dat'),skip_header=3)
ax.plot(C_bottom,Re_theta,'b',label=f'{args.case_type}')
ax.plot(nasa_Retheta[:,0],nasa_Retheta[:,1],'k',label=f'NASA $Re_\theta$')

np.save(os.path.join(RANS_numpy_folder,f'{args.case_type}_x_Retheta_flatplate_RANS.npy'),np.column_stack((C_bottom, Re_theta)))
np.save(os.path.join(RANS_numpy_folder,f'{args.case_type}_x_Retheta_flatplate_ref.npy'),np.column_stack((nasa_Retheta[:,0],nasa_Retheta[:,1])))

ax.set_xlabel('$x$')
ax.set_ylabel('$Re_\theta$')
ax.legend(loc='lower right')
fig.savefig(os.path.join(RANS_numpy_folder,f'{args.case_type}_x_Retheta_flatplate.png'),dpi=300)

for Re_theta_i in DNS_Re_theta_list:
    print(f'Case: {Re_theta_i}')
    ind_wall = get_ind_wall(Re_theta, float(Re_theta_i))
    ind_vol = get_ind_volume(ind_wall, C, C_bottom, theta[ind_wall])
    utau_i = utau[ind_wall]
    DNS_data = np.genfromtxt(os.path.join(DNS_orig_folder, f'vel_{Re_theta_i}_dns.prof'),skip_header=14)
    DNS_U_plus = np.column_stack((DNS_data[:,2],DNS_data[:,13],np.zeros(len(DNS_data))))
    DNS_y_plus = DNS_data[:,1]
    DNS_tau_plus = np.zeros((len(DNS_data),3,3))
    DNS_tau_plus[:,0,0] = np.square(DNS_data[:,3])
    DNS_tau_plus[:,1,1] = np.square(DNS_data[:,4])
    DNS_tau_plus[:,2,2] = np.square(DNS_data[:,5])
    DNS_tau_plus[:,0,1] = DNS_data[:,6]
    DNS_tau_plus[:,1,0] = DNS_tau_plus[:,0,1]
    
    DNS_U = DNS_U_plus*utau_i
    DNS_y = DNS_y_plus*nu/utau_i
    DNS_tau = DNS_tau_plus*np.square(utau_i)
    
    DNS_dUdy = lagrange_polynomial_derivative(DNS_y,DNS_U[:,0]) 
    DNS_dVdy = lagrange_polynomial_derivative(DNS_y,DNS_U[:,1]) 
    DNS_dUdx = -DNS_dVdy
    DNS_gradU = np.zeros((len(DNS_data),3,3))
    DNS_gradU[:,0,0] = DNS_dUdx
    DNS_gradU[:,0,1] = DNS_dUdy
    DNS_gradU[:,1,1] = DNS_dVdy

    DNS_dTauxydy = lagrange_polynomial_derivative(DNS_y,DNS_tau[:,0,1])
    DNS_dTauyydy = lagrange_polynomial_derivative(DNS_y,DNS_tau[:,1,1])
    DNS_dTauzydy = lagrange_polynomial_derivative(DNS_y,DNS_tau[:,1,2])
    DNS_divTau = np.zeros((len(DNS_data),3))
    DNS_divTau[:,0] = DNS_dTauxydy
    DNS_divTau[:,1] = DNS_dTauyydy
    DNS_divTau[:,2] = DNS_dTauzydy

    # Interpolate to RANS first to avoid divide by zero (the remainder are all algebraic operations)
    print('Interpolating fields using method '+interp_method)
    C_coarse = C[ind_vol,1]
    C_fine = DNS_y
    print('Fine field: '+str(len(C_fine))+ ' points')
    print('Coarse field: '+str(len(C_coarse))+ ' points')

    DNS_U = interpolate(C_fine,DNS_U,C_coarse,method=interp_method)
    DNS_tau = interpolate(C_fine,DNS_tau,C_coarse,method=interp_method)
    DNS_gradU = interpolate(C_fine,DNS_gradU,C_coarse,method=interp_method)
    DNS_divTau = interpolate(C_fine,DNS_divTau,C_coarse,method=interp_method)
    DNS_y_plus = interpolate(C_fine,DNS_y_plus,C_coarse,method=interp_method)
    DNS_U_plus = interpolate(C_fine,DNS_U_plus,C_coarse,method=interp_method)
    DNS_tau_plus = interpolate(C_fine,DNS_tau_plus,C_coarse,method=interp_method)

    # Calculating extra DNS fields
    DNS_k = 0.5*np.trace(DNS_tau,axis1=1,axis2=2)
    DNS_a = DNS_tau - 2/3 * DNS_k[:,None,None] * np.identity(3)
    DNS_b = DNS_a/(2*DNS_k[:,None,None])
    DNS_S = 0.5*(DNS_gradU + np.transpose(DNS_gradU,(0,2,1)))
    DNS_R = 0.5*(DNS_gradU - np.transpose(DNS_gradU,(0,2,1)))
    C_save = np.column_stack((np.zeros(len(C_coarse)),C_coarse,np.zeros(len(C_coarse))))
    # Saving DNS fields
    np.save(os.path.join(DNS_numpy_folder,f'REF_fp_{Re_theta_i}_a.npy'), DNS_a)
    np.save(os.path.join(DNS_numpy_folder,f'REF_fp_{Re_theta_i}_b.npy'), DNS_b)
    np.save(os.path.join(DNS_numpy_folder,f'REF_fp_{Re_theta_i}_C.npy'), C_save)
    np.save(os.path.join(DNS_numpy_folder,f'REF_fp_{Re_theta_i}_gradU.npy'), DNS_gradU)
    np.save(os.path.join(DNS_numpy_folder,f'REF_fp_{Re_theta_i}_divtau.npy'), DNS_divTau)

    np.save(os.path.join(DNS_numpy_folder,f'REF_fp_{Re_theta_i}_k.npy'), DNS_k)
    np.save(os.path.join(DNS_numpy_folder,f'REF_fp_{Re_theta_i}_R.npy'), DNS_R)
    np.save(os.path.join(DNS_numpy_folder,f'REF_fp_{Re_theta_i}_S.npy'), DNS_S)
    np.save(os.path.join(DNS_numpy_folder,f'REF_fp_{Re_theta_i}_tau.npy'), DNS_tau)
    np.save(os.path.join(DNS_numpy_folder,f'REF_fp_{Re_theta_i}_U.npy'), DNS_U)
    
    np.save(os.path.join(DNS_numpy_folder,f'REF_fp_{Re_theta_i}_yplus.npy'), DNS_y_plus)
    np.save(os.path.join(DNS_numpy_folder,f'REF_fp_{Re_theta_i}_Uplus.npy'), DNS_U_plus)
    np.save(os.path.join(DNS_numpy_folder,f'REF_fp_{Re_theta_i}_tauplus.npy'), DNS_tau_plus)

    print('Saving RANS fields....')
    for rans_field in rans_field_list:
        print(rans_field)
        field = np.load(os.path.join(RANS_numpy_folder,f'{args.case_type}_flatplate_{rans_field}.npy'))[ind_vol]
        np.save(os.path.join(RANS_numpy_folder,f'{args.case_type}_fp_{Re_theta_i}_{rans_field}.npy'), field)
    np.save(os.path.join(RANS_numpy_folder,f'{args.case_type}_fp_{Re_theta_i}_C.npy'), C_save)
    np.save(os.path.join(RANS_numpy_folder,f'{args.case_type}_fp_{Re_theta_i}_yplus.npy'), RANS_y_plus[ind_vol])
    np.save(os.path.join(RANS_numpy_folder,f'{args.case_type}_fp_{Re_theta_i}_Uplus.npy'), RANS_U_plus[ind_vol])
    np.save(os.path.join(RANS_numpy_folder,f'{args.case_type}_fp_{Re_theta_i}_kplus.npy'), RANS_k_plus[ind_vol])
    fig, ax = plt.subplots(1,1,figsize=(6,6))
    ax.plot(DNS_y_plus,DNS_U_plus[:,0],'b',label='DNS')
    ax.plot(RANS_y_plus[ind_vol],RANS_U_plus[ind_vol][:,0],'r',label=f'{args.case_type}')
    ax.semilogx()
    ax.set_ylabel('$U^+$')
    ax.set_xlabel('log($y^+$)')
    fig.savefig(os.path.join(RANS_numpy_folder,f'{args.case_type}_uplus_yplus_fp_{Re_theta_i}.png'),dpi=300)

