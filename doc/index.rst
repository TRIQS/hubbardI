.. _welcome:

hubbardI
********

.. sidebar:: hubbardI 3.0.0

   This is the homepage of hubbardI v3.0.0.
   For changes see the :ref:`changelog page <changelog>`.
      
      .. image:: _static/logo_github.png
         :width: 75%
         :align: center
         :target: https://github.com/triqs/hubbardI


An application using :ref:`TRIQS <triqslibs:welcome>` to implement a Hubbard-I solver.

Contrary to the hybridization-expansion algorithm, the Hubbard I solver does not solve the quantum impurity problem exactly. It provides an approximation in which the hybridization between the impurity and the electronic bath is neglected. Hence, solving the impurity problem is reduced to finding the “atomic” Green's function of an effective atomic Hamiltonian with a correlated impurity subject to a Coulomb repulsion. The advantage of this solver is that it is very fast and can provide a reasonable approximation of the Green’s function. It is mainly used in the LDA+DMFT framework.

Note that the Hubbard I approximation is only reasonable for strongly-localized systems, e.g. local moment rare-earth compounds. It is very fast and can be employed both on the Matsubara grid and on the real axis.

Learn how to use hubbardI in the :ref:`documentation`.

    
.. toctree::
   :maxdepth: 2
   :hidden:

   install
   documentation
   issues
   ChangeLog.md
   about
