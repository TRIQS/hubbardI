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
from h5 import HDFArchive
import matplotlib.pyplot as plt
import numpy as np
from triqs_dft_tools.sumk_dft import *
from triqs.gf import *

ar = HDFArchive('ce.h5', 'r')
out = ar['DMFT_results']
iteration_offset = out['iteration_count']+1

DOS = out['Iterations']['DOS_it'+str(iteration_offset-1)]['down']
DOSproj_orb = out['Iterations']['DOSproj_orb_it'+str(iteration_offset-1)][0]['down']

DOS0 = out['Iterations']['DOS0_it'+str(iteration_offset-1)]['down']
DOSproj0_orb = out['Iterations']['DOSproj0_orb_it'+str(iteration_offset-1)][0]['down']

w = np.array([ii.value.real for ii in out['Iterations']['Gloc_w_it'+str(iteration_offset-1)].mesh])

plt.figure(1,figsize=(8,8))
plt.plot(w,DOS,'k',label='total')
plt.plot(w,np.sum(np.diagonal(DOSproj_orb[:,:,:],axis1=1,axis2=2),axis=1),'C0',label='orbsum')

plt.plot(w,DOS0,'--k',label='total')
plt.plot(w,np.sum(np.diagonal(DOSproj0_orb[:,:,:],axis1=1,axis2=2),axis=1),'--C0',label='orbsum')
plt.xlim(-4,6)

plt.show()
