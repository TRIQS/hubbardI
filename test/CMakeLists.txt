# load triqs helper to set up tests
find_package(TriqsTest)

file(COPY ${CMAKE_CURRENT_SOURCE_DIR}/hubbard.ref.h5 DESTINATION ${CMAKE_CURRENT_BINARY_DIR})

triqs_add_python_test(hubbard)
