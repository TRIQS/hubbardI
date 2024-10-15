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
from itertools import *
import triqs.utility.mpi as mpi
from h5 import *
from triqs.gf import *
from triqs_dft_tools.sumk_dft import *
from triqs_dft_tools.sumk_dft_tools import *
from triqs_hubbardI import *
import warnings
warnings.filterwarnings("ignore", category=FutureWarning)

filename = 'ce'
beta = 100.0
mesh = MeshImFreq(beta=beta, n_iw=1025, S='Fermion')
SK_tools = SumkDFTTools(hdf_file = filename+'.h5', use_dft_blocks = False, mesh = mesh)

# We analyze the block structure of the Hamiltonian
Sigma = SK_tools.block_structure.create_gf(beta=beta)

SK_tools.put_Sigma([Sigma])
G = SK_tools.extract_G_loc(transform_to_solver_blocks=False)
SK_tools.analyse_block_structure_from_gf(G, threshold = 1e-2)
gf_struct = [(key,val) for key, val in SK_tools.gf_struct_solver[0].items()]

S = Solver(beta=beta, gf_struct=gf_struct)

# non-interacting chemical potential, interacting chemical potential, and double counting
chemical_potential0 = 0.0
chemical_potential = 0.0
dc_imp = None
if mpi.is_master_node():
    ar = HDFArchive(filename+'.h5','a')
    if 'iteration_count' in ar['DMFT_results']:
        previous_present = True
        iteration_offset = ar['DMFT_results']['iteration_count']+1
        print('reading iteration'+str(iteration_offset))
        dc_imp = ar['DMFT_results']['Iterations']['dc_imp'+str(iteration_offset-1)]
        S.Sigma_w = ar['DMFT_results']['Iterations']['Sigma_w_it'+str(iteration_offset-1)]
        dc_energ = ar['DMFT_results']['Iterations']['dc_energ'+str(iteration_offset-1)]
        chemical_potential = ar['DMFT_results']['Iterations']['chemical_potential'+str(iteration_offset-1)].real
        chemical_potential0 = ar['DMFT_results']['Iterations']['chemical_potential0'].real

mpi.barrier()
S.Sigma_w << mpi.bcast(S.Sigma_w)

# create new SumkTools with ReFreqMesh
SK_tools = SumkDFTTools(hdf_file = filename+'.h5', use_dft_blocks = False, mesh = S.Sigma_w.mesh)
SK_tools.analyse_block_structure_from_gf(G, threshold = 1e-2)

SK_tools.chemical_potential = mpi.bcast(chemical_potential)
chemical_potential0 = mpi.bcast(chemical_potential0)
SK_tools.dc_imp = mpi.bcast(dc_imp)
SK_tools.put_Sigma(Sigma_imp = [S.Sigma_w])

idelta = 0.1
DOS, DOSproj, DOSproj_orb = SK_tools.density_of_states(broadening=idelta, proj_type='wann', with_dc=True, with_Sigma=True, save_to_file=False)

SK_tools.chemical_potential = chemical_potential0
SK_tools.put_Sigma(Sigma_imp = [0.0*S.Sigma_w])
DOS0, DOSproj0, DOSproj0_orb = SK_tools.density_of_states(broadening=idelta, proj_type='wann', with_dc=False, with_Sigma=True, save_to_file=False)

if mpi.is_master_node(): 
    ar['DMFT_results']['Iterations']['DOS_it'+str(iteration_offset-1)] = DOS
    ar['DMFT_results']['Iterations']['DOSproj_orb_it'+str(iteration_offset-1)] = DOSproj_orb
    ar['DMFT_results']['Iterations']['DOS0_it'+str(iteration_offset-1)] = DOS0
    ar['DMFT_results']['Iterations']['DOSproj0_orb_it'+str(iteration_offset-1)] = DOSproj0_orb
if mpi.is_master_node(): del ar
if mpi.is_master_node(): print("done!")
