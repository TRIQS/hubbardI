triqs_build_f2py_module( triqs_HubbardI hubbard_I hubbard_I.pyf hubbard_I.f90)
install (FILES ${CMAKE_CURRENT_BINARY_DIR}/hubbard_I.so DESTINATION ${TRIQS_PYTHON_LIB_DEST}/applications/impurity_solvers/hubbard_I)
