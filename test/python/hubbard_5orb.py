###############################################################################
#
# hubbardI: A TRIQS based hubbardI solver
#
# Copyright (c) 2019 Malte Schueler
#
# hubbardI is free software: you can redistribute it and/or modify it under the
# terms of the GNU General Public License as published by the Free Software
# Foundation, either version 3 of the License, or (at your option) any later
# version.
#
# hubbardI is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See the GNU General Public License for more
# details.
#
# You should have received a copy of the GNU General Public License along with
# hubbardI. If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
#!/usr/bin/env python

# this test implements exactly the same test included in the old Hubbard-I solver, see
# (https://github.com/TRIQS/hubbardI, git commit  d919676f472bd5855751159bb91d1737ee9a46ea)
# the reference hubbard.ref.h5 s actually taken from there!
# so this test is also a nice benchmark

from triqs_hubbardI import *
from h5 import *
from pytriqs.gf import *
from pytriqs.utility.h5diff import h5diff
import pytriqs.operators.util as op

# General parameters
beta = 200.0                                  # Inverse temperature
l = 2                                        # Angular momentum
n_orbs = 2*l + 1                             # Number of orbitals
U = 6.0                                      # Screened Coulomb interaction
J = 0.6                                      # Hund's coupling
half_bandwidth = 1.0                         # Half bandwidth
mu = 1.0                                    # Chemical potential
spin_names = ['up','down']                   # Outer (non-hybridizing) blocks
orb_names = ['%s'%i for i in range(n_orbs)]  # Orbital indices
off_diag=True

gf_struct = op.set_operator_structure(spin_names,orb_names,off_diag=off_diag) 
U_mat = op.U_matrix(l=l, U_int=U, J_hund=J, basis='spherical')
H = op.h_int_slater(spin_names,orb_names,U_mat,off_diag=off_diag)

S = Solver(beta=beta, gf_struct=gf_struct, n_iw = 1025)

for name, g0 in S.G0_iw: g0 << inverse(iOmega_n + mu)

S.solve(h_int=H)

with HDFArchive("hubbard.h5",'w') as A:
    A["G"] = S.G_iw
    A["Sigma"] = S.Sigma_iw

print(h5diff("hubbard.h5", "hubbard.ref.h5"))
