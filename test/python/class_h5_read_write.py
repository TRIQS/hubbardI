###############################################################################
#
# hubbardI: A TRIQS based hubbardI solver
#
# Copyright (c) 2020 Malte Schueler
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
from triqs_hubbardI import *
from h5 import *
from triqs.gf import *
from triqs.operators import *
from h5 import HDFArchive
import numpy as np

# registering my class
#from h5.formats import register_class
#register_class (Solver)
D, V, U = 1.0, 0.2, 4.0
e_f, beta = -U/2.0, 50

# initialize the solver
S = Solver(beta = beta, gf_struct = [ ('up',[0]), ('down',[0]) ],idelta=0.5,n_iw=20,n_tau=2,n_w=2)

# set the non-interacting Green's function
for name, g0 in S.G0_iw: g0 << inverse(iOmega_n - e_f - V**2 * Wilson(D))

# solve the atomic problem
S.solve( h_int = U * n('up',0) * n('down',0) )

# Save the results in an HDF5 file (only on the master node)
with HDFArchive("class.h5",'w') as Results:
     Results["Solver"] = S
     
# Read the results from the reference HDF5 file 
with HDFArchive("class.ref.h5",'r') as Results:
     S_ref = Results["Solver"]


for key in dir(S):
    if 'G' in key or 'Sigma' in key:
        print('comparing', key)
        
        val = getattr(S, key)
        val_ref = getattr(S_ref, key)

        if isinstance(val, BlockGf):
            for (n1, g1), (n1, g2) in zip(val, val_ref):
                np.testing.assert_array_almost_equal(g1.data, g2.data)
        elif val == None or isinstance(val, list):
            assert(val == val_ref)
        else:
            raise Exception("Invalid type in comparison")
    elif '__' not in key and 'ad' not in key and 'solve' not in key and 'eal' not in key:
        print('comparing', key)
        val = getattr(S, key)
        val_ref = getattr(S_ref, key)
        assert val == val_ref
    elif 'eal' in key:
        print('comparing', key)
        val = getattr(S, key)
        val_ref = getattr(S_ref, key)
        for name in val.keys():
            np.testing.assert_array_almost_equal(val[name], val_ref[name])
    else:
        val = getattr(S, key)
        val_ref = getattr(S_ref, key)
        # comparisons of the objects left seem not too easy to implement
        # wait for some simple h5diff scheme!
        # for now we just test if all the objects exist.
