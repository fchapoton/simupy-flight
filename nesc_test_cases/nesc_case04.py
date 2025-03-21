from simupy.block_diagram import BlockDiagram
import simupy_flight
import numpy as np

from nesc_testcase_helper import plot_nesc_comparisons, int_opts, benchmark
from nesc_testcase_helper import ft_per_m, kg_per_slug

planet = simupy_flight.Planet(
    gravity=simupy_flight.get_spherical_gravity(simupy_flight.earth_spherical_gravity_constant),
    winds=simupy_flight.get_constant_winds(),
    atmosphere=simupy_flight.atmosphere_1976,
    planetodetics=simupy_flight.Planetodetic(a=20902255.199/ft_per_m, omega_p=0., f=0.)
)

Ixx = 3.6*kg_per_slug/(ft_per_m**2) #slug-ft2
Iyy = 3.6*kg_per_slug/(ft_per_m**2) #slug-ft2
Izz = 3.6*kg_per_slug/(ft_per_m**2) #slug-ft2
Ixy = 0.0*kg_per_slug/(ft_per_m**2) #slug-ft2
Iyz = 0.0*kg_per_slug/(ft_per_m**2) #slug-ft2
Izx = 0.0*kg_per_slug/(ft_per_m**2) #slug-ft2
m = 1.0*kg_per_slug #slug

x = 0.
y = 0.
z = 0.

S_A = 0.1963495/(ft_per_m**2)
b_l = 1.0
c_l = 1.0
a_l = b_l
vehicle = simupy_flight.Vehicle(base_aero_coeffs=simupy_flight.get_constant_aero(CD_b=0.1), m=m, I_xx=Ixx, I_yy=Iyy, I_zz=Izz, I_xy=Ixy, I_yz=Iyz, I_xz=Izx, x_com=x, y_com=y, z_com=z, x_mrc=x, y_mrc=y, z_mrc=z, S_A=S_A, a_l=a_l, b_l=b_l, c_l=c_l, d_l=0.,)

BD = BlockDiagram(planet, vehicle)
BD.connect(planet, vehicle, inputs=np.arange(planet.dim_output))
BD.connect(vehicle, planet, inputs=np.arange(vehicle.dim_output))

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

planet.initial_condition = planet.ic_from_planetodetic(long_ic, lat_ic, h_ic, V_N_ic, V_E_ic, V_D_ic, psi_ic, theta_ic, phi_ic)
planet.initial_condition[-3:] = omega_X_ic, omega_Y_ic, omega_Z_ic

with benchmark() as b:
    res = BD.simulate(30, integrator_options=int_opts)
    b.tfinal = res.t[-1]

plot_nesc_comparisons(res, '04')
