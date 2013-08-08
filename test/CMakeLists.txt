# load triqs helper to set up tests
find_package(TriqsTest)
triqs_add_test_hdf(hubbard " -d 1.e-6" )

