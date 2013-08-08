# where will the python end up in triqs?
set(python_destination applications/impurity_solvers/hubbard_I)

# make a local pytriqs copy
triqs_prepare_local_pytriqs_merged_with_my_python(${python_destination})

# to be able to run from toplevel
execute_process(COMMAND ln -fs ${CMAKE_CURRENT_BINARY_DIR}/../fortran/hubbard_I.so ${CMAKE_BINARY_DIR}/pytriqs/${python_destination})

