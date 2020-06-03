[![Build Status](https://travis-ci.org/TRIQS/hubbardI.svg?branch=unstable)](https://travis-ci.org/TRIQS/hubbardI)

# hubbardI - A Hubbard-I solver based on triqs atom_diag


This application implements the Hubbard-I solver in pytriqs using the lightweight diagonalization routine which come with triqs/atom_diag.

### Usage ###
The Solver comes with the same usage as, e.g., the [cthyb solver](https://triqs.github.io/cthyb/latest/index.html).

* Run the following commands in order after replacing **appname** accordingly

```bash
git clone https://github.com/triqs/app4triqs --branch python_only appname
cd appname
./share/squash_history.sh
./share/replace_and_rename.py appname
git add -A && git commit -m "Adjust app4triqs skeleton for appname"
```
and initializing the non_interacting Green's function
```python
G.G0_iw = ...
```

If you prefer to use the [SSH interface](https://help.github.com/en/articles/connecting-to-github-with-ssh)
to the remote repository, replace the http link with e.g. `git@github.com:username/appname`.

### Merging app4triqs skeleton updates ###

You can merge future changes to the app4triqs skeleton into your project with the following commands

```bash
git remote update
git merge app4triqs_remote/python_only -m "Merge latest app4triqs skeleton changes"
```
With optional parameters in the `solve` function `calc_gtau = True`, `calc_gw = True`, and `calc_gl = True` the solver also additionally calculates the interacting Green's function on the real axis, imaginary time and legendre. For the real and Matsubara axis, also the self energy is calculated. By using `calc_dm = True` the density matrix (stored in S.dm) is also calculated which enables the calculation of local observables. For further details refer to the documentation of atom_diag on the triqs homepage.

The mesh for the Green function is defined in the first step, e.g., by 
```python
Solver(beta = beta, gf_struct, n_iw= 512, n_tau = 200, n_w = 1001, w_min=-10, w_max=10, idelta=0.1, n_l=30)
```
where `n_w, w_min, w_max, idelta` define the real axis and broadening by an imaginary offset.

Getting Started
---------------

After setting up your application as described above you should customize the following files and directories
according to your needs (replace app4triqs in the following by the name of your application)

* Adjust or remove the `README.md` and `doc/ChangeLog.md` file
* In the `python/app4triqs` subdirectory add your Python source files.
* In the `test/python` subdirectory adjust the example test `Basic.py` or add your own tests.
* Adjust any documentation examples given as `*.rst` files in the doc directory.
* Adjust the sphinx configuration in `doc/conf.py.in` as necessary.
* The build and install process is identical to the one outline [here](https://triqs.github.io/app4triqs/unstable/install.html).

### Optional ###
----------------

* Add your email address to the bottom section of `Jenkinsfile` for Jenkins CI notification emails
```
End of build log:
\${BUILD_LOG,maxLines=60}
    """,
    to: 'user@domain.org',
```
