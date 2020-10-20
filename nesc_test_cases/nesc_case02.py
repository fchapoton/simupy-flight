from simupy.block_diagram import BlockDiagram
import simupy_flight
import pandas as pd
import numpy as np
import os
import glob
from nesc_testcase_helper import plot_nesc_comparisons, data_relative_path, int_opts, ft_per_m, kg_per_slug

kin_block = simupy_flight.KinematicsBlock(
    gravity=simupy_flight.earth_J2_gravity,
    winds=simupy_flight.get_constant_winds(),
    density=simupy_flight.get_constant_density(0.),
    speed_of_sound=simupy_flight.get_constant_speed_of_sound(),
    viscosity=simupy_flight.get_constant_viscosity(),
    a = simupy_flight.earth_equitorial_radius,
    omega_p=simupy_flight.earth_rotation_rate,
    f=simupy_flight.earth_f
)

Ixx = 0.001894220*kg_per_slug/(ft_per_m**2) #slug-ft2
Iyy = 0.006211019*kg_per_slug/(ft_per_m**2) #slug-ft2
Izz = 0.007194665*kg_per_slug/(ft_per_m**2) #slug-ft2
Ixy = 0.0*kg_per_slug/(ft_per_m**2) #slug-ft2
Iyz = 0.0*kg_per_slug/(ft_per_m**2) #slug-ft2
Izx = 0.0*kg_per_slug/(ft_per_m**2) #slug-ft2
m = 0.155404754*kg_per_slug #slug

x = 0.
y = 0.
z = 0.

dyn_block =  simupy_flight.DynamicsBlock(simupy_flight.get_constant_aero(), m, Ixx, Iyy, Izz, Ixy, Iyz, Izx, x,y,z, x,y,z, S_A=0., a_l=1., b_l=1., c_l=1., d_l=1.,)

BD = BlockDiagram(kin_block, dyn_block)
BD.connect(kin_block, dyn_block, inputs=np.arange(kin_block.dim_output))
BD.connect(dyn_block, kin_block, inputs=np.arange(dyn_block.dim_output))

lat_ic = 0.*np.pi/180
long_ic = 0.*np.pi/180
h_ic = 30_000/ft_per_m
V_N_ic = 0.
V_E_ic = 0.
V_D_ic = 0.
psi_ic = 0.*np.pi/180
theta_ic = 0.*np.pi/180
phi_ic = 0.*np.pi/180
omega_X_ic = 10.*np.pi/180
omega_Y_ic = 20.*np.pi/180
omega_Z_ic = 30.*np.pi/180

kin_block.initial_condition = kin_block.ic_from_geodetic(0, long_ic, lat_ic, h_ic, V_N_ic, V_E_ic, V_D_ic, psi_ic, theta_ic, phi_ic, omega_X_ic, omega_Y_ic, omega_Z_ic)
out_at_ic = kin_block.output_equation_function(0, kin_block.initial_condition)
check_pos = out_at_ic[13:16]
check_att = out_at_ic[16:19]
orig_pos = np.array([long_ic, lat_ic, h_ic])
orig_att = np.array([psi_ic, theta_ic, phi_ic])
print('position:', np.allclose(check_pos, orig_pos))
print('attitude:', np.allclose(check_att, orig_att))

res = BD.simulate(30, integrator_options=int_opts)

baseline_pds = []
for fname in glob.glob(os.path.join(data_relative_path, 'Atmospheric_checkcases', 'Atmos_02_TumblingBrickNoDamping', 'Atmos_02_sim_*.csv'),):
    baseline_pds.append(pd.read_csv(fname, index_col=0))
    
plot_nesc_comparisons(res, baseline_pds)