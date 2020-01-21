Version 2.2
----------------

This is a complete rewrite which is compatible to triqs 2.2. For solving the atomic problem the atom_diag function of triqs is used. The solve function now works completely similar to the cthyb solve function which ensures exchangeability between both solvers.

If you are moving from 1.4 to 2.2 this might help: The parts of a script in version 1.4

 .. code-block:: python

	from pytriqs.applications.impurity_solvers.hubbard_I.hubbard_solver import Solver

	# Init the Hubbard-I solver:
	S = Solver( beta, l )

	# set the atomic levels explicitly by matrix eal
	S.set_atomic_levels( eal )

	# solve and specify the interaction via U and J paramters
	S.solve( U_int, J_hund )

transitions to the following in version 2.2
 .. code-block:: python

	from triqs_hubbardi import *

	# Init the Hubbard-I solver:
	S = Solver( beta, gf_struct )

	# set the interaction via an interaction Hamiltonian
	U_sph = U_matrix( l, U_int, J_hund )
	U_cubic = transform_U_matrix( U_sph, spherical_to_cubic(l, convention='') )
	H = h_int_slater( spin_names, orb_names, U_cubic, map_operator_structure )

	# set the non-interacting Green's function
	S.G0_iw << inverse( S.Sigma_iw + inverse( S.G_iw ) )

	# Solve the impurity problem specifiying the interaction Hamiltonian
	# the atomic levels are automatically set by the high frequency behavior of S.G0_iw
	S.solve( h_int = H )

For a more detailed comparison compare the Ce example in the tutorial section of the dft_tools app and the Ce example in the example section here: :ref:`ce`

Version 1.4
-------------

This version is only compatible to triqs 1.4. It comes with a fortran solver for the atomic problem.
