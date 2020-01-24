from triqs_hubbardi import *
from pytriqs.archive import *
from pytriqs.gf import *
from pytriqs.operators import *
from pytriqs.archive import HDFArchive
import numpy as np

# registering my class
#from pytriqs.archive.hdf_archive_schemes import register_class
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
        print 'comparing', key
        
        val = getattr(S, key)
        val_ref = getattr(S_ref, key)

        if isinstance(val, BlockGf):
            for (n1, g1), (n1, g2) in zip(val, val_ref):
                np.testing.assert_array_almost_equal(g1.data, g2.data)
        elif val == None or isinstance(val, list):
            assert(val == val_ref)
        else:
            raise Exception("Invalid type in comparison")
    elif '__' not in key and 'ad' not in key and 'solve' not in key:
        print 'comparing', key
        val = getattr(S, key)
        val_ref = getattr(S_ref, key)
        
        print val, val_ref, val==val_ref
        assert val == val_ref
    else:
        val = getattr(S, key)
        val_ref = getattr(S_ref, key)
        # comparisons of the objects left seem not too easy to implement
        # wait for some simple h5diff scheme!
        # for now we just test if all the objects exist.
