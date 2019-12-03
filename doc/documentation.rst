.. _documentation:

Documentation
=============

The Hubbard-I solver approximates the solution of the impurity model by neglecting any hybiridization and solcing an atomic problem. The atomic problem is defined by the local interaction Hamiltonian and the orbital dependent high-frequency behavior of the non-interacting bath Green's function.


Table of Contents
-----------------

.. toctree::
   :maxdepth: 5

   index
   install
   issues
   changelog
   about

Python reference manual
-----------------------

.. automodule:: triqs_hubbardi 
   :members:

.. autoclass:: triqs_hubbardi.Solver
   :members:

.. autofunction:: triqs_hubbardi.Solver.solve
