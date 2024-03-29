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

from triqs_hubbardI import *
from h5 import *
from triqs.gf import *
from triqs.operators import *
from triqs.utility.h5diff import h5diff

D, V, U = 1.0, 0.2, 4.0
e_f, beta = -U/2.0, 50
S = Solver(beta = beta, gf_struct = [ ('up',1), ('down',1) ],n_iw=5,n_tau=2,n_w=20)
for name, g0 in S.G0_iw: g0 << inverse(iOmega_n - e_f - V**2 * Wilson(D))
 
    
S.solve(h_int = U * n('up',0) * n('down',0),calc_gw=True )
with HDFArchive("aim_w.h5",'w') as A:
    A["G_w"] = S.G_w
h5diff('aim_w.h5', 'aim_w.ref.h5')
