triqs_make_target_to_copy_all_py_files_from_python_dir_to_build_dir()

execute_process(COMMAND ln -fs ${CMAKE_CURRENT_BINARY_DIR}/../fortran/hubbard_I.so ${CMAKE_CURRENT_BINARY_DIR})

#installation 
SET(PYTHON_SOURCES 
 ${CMAKE_CURRENT_SOURCE_DIR}/__init__.py 
 ${CMAKE_CURRENT_SOURCE_DIR}/hubbard_solver.py 
 ${CMAKE_CURRENT_SOURCE_DIR}/old_solver.py 
 )
install (FILES ${PYTHON_SOURCES} DESTINATION ${TRIQS_PYTHON_LIB_DEST}/applications/impurity_solvers/hubbard_I)

#make sure that the __init__.py empty files are present ...
file (WRITE __init__.py.all_empty  "__all__=[]")
install (FILES __init__.py.all_empty DESTINATION ${TRIQS_PYTHON_LIB_DEST}/applications/impurity_solvers/ RENAME __init__.py)
install (FILES __init__.py.all_empty DESTINATION ${TRIQS_PYTHON_LIB_DEST}/applications/                  RENAME __init__.py)


