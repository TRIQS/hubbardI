###############################################################################
#
# hubbardI: A TRIQS based hubbardI solver
#
# Copyright (c) 2019-2020 Malte Schueler
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
from triqs.gf import *
from triqs.atom_diag import *
from itertools import *
import numpy as np
from triqs.operators import Operator, c, c_dag, n
import triqs.utility.mpi as mpi

class Solver():
    """Class providing initialization and solve function. Contains all relevant Greensfunctions and self energy."""

    def __init__(self, beta, gf_struct, n_iw=1025, n_tau=10001, n_l=30, n_w=500,w_min=-15,w_max=15,idelta=0.01):
        """

        Initialise the solver.

        Parameters
        ----------
        beta : scalar
               Inverse temperature.
        gf_struct : list of pairs [ (str,int), ...]
                    Structure of the Green's functions. It must be a
                    list of pairs, each containing the name of the
                    Green's function block and its linear size.
                    For example: ``[ ('up', 3), ('down', 3) ]``.
        n_iw : integer, optional
               Number of Matsubara frequencies used for the Green's functions.
        n_tau : integer, optional
                Number of imaginary time points used for the Green's functions.
        n_l : integer, optional
                Number of legendre polynomials used for the Green's functions.
        n_w : integer, optional
                Number of real frequency points used for the Green's functions.
        w_min : integer, optional
                Lower limit of the range of real frequencies
        w_max : integer, optional
                Upper limit of the range of real frequencies
        idelta : float, optional
                Broadening of Green's function on real frequencies

        """

        gf_struct = fix_gf_struct_type(gf_struct)

        g_w_list = []
        g_iw_list = []
        g_tau_list = []
        g_l_list = []

        name_list = [block for block, block_size in gf_struct]
        for block, block_size in gf_struct:
            g_w_list.append(GfReFreq(window = (w_min, w_max), n_points = n_w, target_shape = (block_size, block_size)))
            g_iw_list.append(GfImFreq(beta = beta, n_points = n_iw, target_shape = (block_size, block_size)))
            g_tau_list.append(GfImTime(beta = beta, n_points = n_tau, target_shape = (block_size, block_size)))
            g_l_list.append(GfLegendre(beta = beta, n_points = n_l, target_shape = (block_size, block_size)))

        self.G0_w = BlockGf(name_list = name_list, block_list = g_w_list)
        self.G0_iw = BlockGf(name_list = name_list, block_list = g_iw_list)
        self.G_tau = BlockGf(name_list = name_list, block_list = g_tau_list)
        self.G_l = BlockGf(name_list = name_list, block_list = g_l_list)

        self.Sigma_iw = self.G0_iw.copy()
        self.Sigma_iw.zero()

        self.G_iw = self.G0_iw.copy()
        self.G_iw.zero()

        self.Sigma_w = self.G0_w.copy()
        self.Sigma_w.zero()

        self.G_w = self.G0_w.copy()
        self.G_w.zero()

        self.gf_struct = gf_struct

        self.n_iw = n_iw
        self.n_tau = n_tau
        self.n_l = n_l
        self.beta = beta

        self.n_w = n_w
        self.w_min = w_min
        self.w_max = w_max
        self.idelta = idelta

        self.fops = []
        for block, block_size in gf_struct:
            for ii in range(block_size):
                self.fops.append((block,ii))

        self.eal = dict()
        for block, block_size in self.gf_struct:
            self.eal[block]= np.zeros((block_size,block_size))

    def solve(self, **params_kw):
        """
        Solve the impurity problem: calculate G(iw) and Sigma(iw)

        Parameters
        ----------
        params_kw : dict {'param':value} that is passed to the core solver.
                    Only required parameter is
                        * `h_int` (:ref:`Operator object <triqslibs:operators>`): the local Hamiltonian of the impurity problem to be solved,
                    Other parameters are
                        * `calc_gtau` (bool): calculate G(tau)
                        * `calc_gw` (bool): calculate G(w) and Sigma(w)
                        * `calc_gl` (bool): calculate G(legendre)
                        * `calc_dm` (bool): calculate density matrix

        """

        mpi.report('TRIQS: HubbardI solver')


        h_int = params_kw['h_int']
        try:
            calc_gtau = params_kw['calc_gtau']
        except KeyError:
            calc_gtau = False

        try:
            calc_gw = params_kw['calc_gw']
        except KeyError:
            calc_gw = False

        try:
            calc_gl = params_kw['calc_gl']
        except KeyError:
            calc_gl = False

        try:
            calc_dm = params_kw['calc_dm']
        except KeyError:
            calc_dm = False

        Delta_iw = 0*self.G0_iw
        Delta_iw << iOmega_n
        Delta_iw -= inverse(self.G0_iw)


        for block, block_size in self.gf_struct:
            a = Delta_iw[block].fit_tail()
            self.eal[block] = a[0][0]

        G0_iw_F = 0*self.G_iw
        if calc_gw:
            G0_w_F = 0*self.G_w

        G0_iw_F << iOmega_n
        if calc_gw:
            G0_w_F << Omega

        for block, block_size in self.gf_struct:
            G0_iw_F[block] -= self.eal[block]
            if calc_gw:
                G0_w_F[block] -= self.eal[block]

        G0_iw_F = inverse(G0_iw_F)
        if calc_gw:
            G0_w_F = inverse(G0_w_F)

        H_loc = 1.0*h_int
        for block, block_size in self.gf_struct:
            for ii in range(block_size):
                for jj in range(block_size):
                    H_loc += self.eal[block][ii,jj]*c_dag(block,ii)*c(block,jj)

        mpi.report('\n')
        mpi.report('The local Hamiltonian of the problem:')
        mpi.report(H_loc)
        mpi.report('\n')

        self.ad = AtomDiag(H_loc, self.fops)

        self.G_iw = atomic_g_iw(self.ad, self.beta, self.gf_struct, self.n_iw )
        if calc_gw:
            self.G_w = atomic_g_w(self.ad, self.beta, self.gf_struct, (self.w_min,self.w_max), self.n_w, self.idelta)
        if calc_gtau:
            self.G_tau = atomic_g_tau(self.ad, self.beta, self.gf_struct, self.n_tau )
        if calc_gl:
            self.G_l = atomic_g_l(self.ad, self.beta, self.gf_struct, self.n_l )
        if calc_dm:
            self.dm = atomic_density_matrix(self.ad, self.beta)

        self.Sigma_iw = inverse(G0_iw_F) - inverse(self.G_iw)
        if calc_gw:
            self.Sigma_w = inverse(G0_w_F) - inverse(self.G_w)




    def __reduce_to_dict__(self):
        store_dict = {'G0_w': self.G0_w, 'G0_iw': self.G0_iw,'G_tau': self.G_tau,
                      'G_l': self.G_l, 'Sigma_iw': self.Sigma_iw, 'G_iw': self.G_iw,
                      'Sigma_w': self.Sigma_w, 'G_w': self.G_w,
                      'gf_struct': self.gf_struct, 'n_iw': self.n_iw, 'n_w': self.n_w,
                      'n_tau': self.n_tau, 'n_l': self.n_l,'beta': self.beta,
                      'w_min': self.w_min,'w_max': self.w_max,
                      'idelta': self.idelta,'fops': self.fops,'eal':self.eal}
        if hasattr(self, 'ad'):
            store_dict['ad'] = self.ad

        return store_dict

    @classmethod
    def __factory_from_dict__(cls,name,D) :

        instance = cls(D['beta'], D['gf_struct'], D['n_iw'], D['n_tau'],
                       D['n_l'], D['n_w'], D['w_min'], D['w_max'], D['idelta'])

        instance.G0_w = D['G0_w']
        instance.G0_iw = D['G0_iw']
        instance.G_tau = D['G_tau']
        instance.G_l = D['G_l']
        instance.Sigma_iw = D['Sigma_iw']
        instance.G_iw = D['G_iw']
        instance.Sigma_w = D['Sigma_w']
        instance.G_w = D['G_w']
        instance.gf_struct = fix_gf_struct_type(D['gf_struct'])
        instance.fops = D['fops']
        instance.eal = D['eal']
        instance.ad = D['ad']

        return instance

# registering my class
from h5.formats import register_class
register_class(Solver)
