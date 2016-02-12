# where will the python end up in triqs?
set(python_destination pytriqs/applications/impurity_solvers/hubbard_I)

# site_customize for build
set(package_name "pytriqs.applications.impurity_solvers")
configure_file(${CMAKE_SOURCE_DIR}/cmake/sitecustomize.py ${CMAKE_CURRENT_BINARY_DIR}/sitecustomize.py @ONLY)

# make a local pytriqs copy
triqs_prepare_local_pytriqs(${python_destination})

# to be able to run from toplevel
execute_process(COMMAND ln -fs ${CMAKE_CURRENT_BINARY_DIR}/../fortran/hubbard_I.so ${CMAKE_BINARY_DIR}/python/hubbard_I)
