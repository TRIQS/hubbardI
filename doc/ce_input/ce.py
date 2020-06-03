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
import numpy as np
import triqs.utility.mpi as mpi
from h5 import *
from triqs.gf import *
import sys, triqs.version as triqs_version
from triqs_dft_tools.sumk_dft import *
from triqs_dft_tools.sumk_dft_tools import *
from triqs.operators.util.hamiltonians import *
from triqs.operators.util.U_matrix import *
import triqs_dft_tools.version as dft_tools_version
from triqs_hubbardI import *
import triqs_hubbardI.version as hubbardI_version

import warnings
warnings.filterwarnings("ignore", category=FutureWarning)

filename = 'ce'

SK = SumkDFT(hdf_file = filename+'.h5', use_dft_blocks = False)

beta = 100.0 
 
Sigma = SK.block_structure.create_gf(beta=beta)
SK.put_Sigma([Sigma])
G = SK.extract_G_loc()
SK.analyse_block_structure_from_gf(G, threshold = 1e-2)
for i_sh in range(len(SK.deg_shells)):
    num_block_deg_orbs = len(SK.deg_shells[i_sh])
    mpi.report('found {0:d} blocks of degenerate orbitals in shell {1:d}'.format(num_block_deg_orbs, i_sh))
    for iblock in range(num_block_deg_orbs):
        mpi.report('block {0:d} consists of orbitals:'.format(iblock))
        for keys in SK.deg_shells[i_sh][iblock].keys():
            mpi.report('  '+keys)

# Setup CTQMC Solver

n_orb = SK.corr_shells[0]['dim']
spin_names = ['up','down']
orb_names = [i for i in range(0,n_orb)]

gf_struct = SK.gf_struct_solver[0]
mpi.report('Sumk to Solver: %s'%SK.sumk_to_solver)
mpi.report('GF struct sumk: %s'%SK.gf_struct_sumk)
mpi.report('GF struct solver: %s'%SK.gf_struct_solver)

S = Solver(beta=beta, gf_struct=gf_struct)

# Construct the Hamiltonian and save it in Hamiltonian_store.txt
H = Operator() 
U = 6.0
J = 0.7

U_sph = U_matrix(l=3, U_int=U, J_hund=J)
U_cubic = transform_U_matrix(U_sph, spherical_to_cubic(l=3, convention=''))

H = h_int_slater(spin_names, orb_names, U_cubic, map_operator_structure=SK.sumk_to_solver[0])

# Print some information on the master node
mpi.report('Greens function structure is: %s '%gf_struct)

# Double Counting: 0 FLL, 1 Held, 2 AMF
DC_type = 0

# Prepare hdf file and and check for previous iterations
n_iterations = 10

iteration_offset = 0
if mpi.is_master_node():
    ar = HDFArchive(filename+'.h5','a')
    if not 'DMFT_results' in ar: ar.create_group('DMFT_results')
    if not 'Iterations' in ar['DMFT_results']: ar['DMFT_results'].create_group('Iterations')
    if not 'DMFT_input' in ar: ar.create_group('DMFT_input')
    if not 'Iterations' in ar['DMFT_input']: ar['DMFT_input'].create_group('Iterations')

    if 'iteration_count' in ar['DMFT_results']: 
        iteration_offset = ar['DMFT_results']['iteration_count']+1
        S.Sigma_iw = ar['DMFT_results']['Iterations']['Sigma_it'+str(iteration_offset-1)]
        SK.dc_imp = ar['DMFT_results']['Iterations']['dc_imp'+str(iteration_offset-1)]
        SK.dc_energ = ar['DMFT_results']['Iterations']['dc_energ'+str(iteration_offset-1)]
        SK.chemical_potential = ar['DMFT_results']['Iterations']['chemical_potential'+str(iteration_offset-1)].real

iteration_offset = mpi.bcast(iteration_offset)
S.Sigma_iw = mpi.bcast(S.Sigma_iw)
SK.dc_imp = mpi.bcast(SK.dc_imp)
SK.dc_energ = mpi.bcast(SK.dc_energ)
SK.chemical_potential = mpi.bcast(SK.chemical_potential)

# Calc the first G0
SK.symm_deg_gf(S.Sigma_iw,orb=0)
SK.put_Sigma(Sigma_imp = [S.Sigma_iw])
SK.calc_mu(precision=0.01)
S.G_iw << SK.extract_G_loc()[0]
SK.symm_deg_gf(S.G_iw, orb=0)

#Init the DC term and the self-energy if no previous iteration was found
if iteration_offset == 0:
    dm = S.G_iw.density()
    SK.calc_dc(dm, U_interact=U, J_hund=J, orb=0, use_dc_formula=DC_type)
    S.Sigma_iw << SK.dc_imp[0]['up'][0,0]

mpi.report('%s DMFT cycles requested. Starting with iteration %s.'%(n_iterations,iteration_offset))

# The infamous DMFT self consistency cycle
for it in range(iteration_offset, iteration_offset + n_iterations):
    
    mpi.report('Doing iteration: %s'%it)
    
    # Get G0
    S.G0_iw << inverse(S.Sigma_iw + inverse(S.G_iw))

    # Solve the impurity problem
    S.solve(h_int = H, calc_gw=True )

    # Calculate double counting
    dm = S.G_iw.density()
    SK.calc_dc(dm, U_interact=U, J_hund=J, orb=0, use_dc_formula=DC_type)

    # Get new G
    SK.symm_deg_gf(S.Sigma_iw,orb=0)
    SK.put_Sigma(Sigma_imp=[S.Sigma_iw])
    SK.calc_mu(precision=0.01)
    S.G_iw << SK.extract_G_loc()[0]
    
    # print densities
    for sig,gf in S.G_iw:
        mpi.report("Orbital %s density: %.6f"%(sig,dm[sig][0,0]))
    mpi.report('Total charge of Gloc : %.6f'%S.G_iw.total_density())

    if mpi.is_master_node(): 
        ar['DMFT_results']['iteration_count'] = it
        ar['DMFT_results']['Iterations']['Sigma_it'+str(it)] = S.Sigma_iw
        ar['DMFT_results']['Iterations']['Sigma_w_it'+str(it)] = S.Sigma_w
        ar['DMFT_results']['Iterations']['Gloc_it'+str(it)] = S.G_iw
        ar['DMFT_results']['Iterations']['Gloc_w_it'+str(it)] = S.G_w
        ar['DMFT_results']['Iterations']['G0loc_it'+str(it)] = S.G0_iw
        ar['DMFT_results']['Iterations']['dc_imp'+str(it)] = SK.dc_imp
        ar['DMFT_results']['Iterations']['dc_energ'+str(it)] = SK.dc_energ
        ar['DMFT_results']['Iterations']['chemical_potential'+str(it)] = SK.chemical_potential

if mpi.is_master_node(): del ar
