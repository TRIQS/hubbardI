#!/usr/bin/env python

from triqs_hubbardi import *
from pytriqs.archive import *
from pytriqs.gf import *
from pytriqs.utility.h5diff import h5diff
import pytriqs.operators.util as op


# General parameters
beta = 40.0                                  # Inverse temperature
l = 2                                        # Angular momentum
n_orbs = 2*l + 1                             # Number of orbitals
U = 4.0                                      # Screened Coulomb interaction
J = 1.0                                      # Hund's coupling
half_bandwidth = 1.0                         # Half bandwidth
mu = 25.0                                    # Chemical potential
spin_names = ['up','down']                   # Outer (non-hybridizing) blocks
orb_names = ['%s'%i for i in range(n_orbs)]  # Orbital indices
off_diag=True

gf_struct = op.set_operator_structure(spin_names,orb_names,off_diag=off_diag) 
U_mat = op.U_matrix(l=l, U_int=U, J_hund=J, basis='spherical')
H = op.h_int_slater(spin_names,orb_names,U_mat,off_diag=off_diag)

S = Solver(beta=beta, gf_struct=gf_struct, n_iw = 30)

delta_iw = GfImFreq(indices=[0], beta=beta, mesh=S.G_iw.mesh)
delta_iw << (half_bandwidth/2.0)**2 * SemiCircular(half_bandwidth)
for name, g0 in S.G0_iw: g0 << inverse(iOmega_n + mu - delta_iw)

g_iw = GfImFreq(indices=[0], beta=beta, mesh=S.G_iw.mesh)
for name, g0 in S.G0_iw: 
        g0 << inverse(iOmega_n + mu - (half_bandwidth/2.0)**2 * g_iw )

S.solve(h_int=H)
    
with HDFArchive("bethe5.h5",'w') as A:
    A["G_iw"] = S.G_iw
with HDFArchive("bethe5.ref.h5",'r') as A:
    Giw_read = A["G_iw"]
h5diff('bethe5.h5', 'bethe5.ref.h5')
