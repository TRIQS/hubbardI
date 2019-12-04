#!/usr/bin/env python

from triqs_hubbardi import *
from pytriqs.archive import *
from pytriqs.gf import *
from pytriqs.operators import *
from pytriqs.utility.h5diff import h5diff

D, V, U = 1.0, 0.2, 4.0
e_f, beta = -U/2.0, 50
S = Solver(beta = beta, gf_struct = [ ('up',[0]), ('down',[0]) ],n_iw=5,n_tau=2,n_w=2,n_l=5)
for name, g0 in S.G0_iw: g0 << inverse(iOmega_n - e_f - V**2 * Wilson(D))
 
S.solve(h_int = U * n('up',0) * n('down',0), calc_gl=True )

with HDFArchive("aim_l.h5",'w') as A:
    A["G_l"] = S.G_l
h5diff('aim_l.h5', 'aim_l.ref.h5')
        

