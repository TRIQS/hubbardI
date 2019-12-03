[![Build Status](https://travis-ci.org/TRIQS/triqs_hubbardi.svg?branch=unstable)](https://travis-ci.org/TRIQS/triqs_hubbardi)

# triqs_hubbardi - A Hubbard-I solver based on triqs atom_diag


This application implements the Hubbard-I solver in pytriqs using the lightweight diagonalization routine which come with triqs/atom_diag.

### Usage ###
The Solver comes with the same usage as, e.g., the [cthyb solver](https://triqs.github.io/cthyb/latest/index.html).

After constructing the impurity solver instance by
```python
S = Solver(beta = beta, gf_struct)
```
and initializing the non_interacting Green's function
```python
G.G0_iw = ...
```
we can solve the impurity problem by
```python
S.solve(h_int = h_int)
```
With optional parameters in the `solve` function like `calc_gtau = True` and `calc_gw = True` the solver also calculates the interacting Green's function on the real axis and imaginary time. For the real and Matsubara axis, also the self energy is calculated.

### Installation ###
----------------

The only thing you need is a working triqs installation. If you have sourced the `triqsvars.sh` file everything works automatically.

```bash
git clone https://github.com/malte-schueler/triqs_hubbardI triqs_hubbardI.src
mkdir cthyb.build && cd cthyb.build
cmake ../cthyb.src
make
make test
make install
```