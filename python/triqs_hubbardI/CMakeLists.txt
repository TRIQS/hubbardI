###############################################################################
#
# hubbardI: A TRIQS based hubbardI solver
#
# Copyright (c) 2019-2020 Malte Schueler
# Copyright (c) 2019-2020 The Simons Foundation
# 	author: N. Wentzell
#
# hubbardI is free software: you can redistribute it and/or modify it under the
# terms of the GNU General Public License as published by the Free Software
# Foundation, either version 3 of the License, or (at your option) any later
# version.
#
# hubbardI is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See the GNU General Public License for more
# details.
#
# You should have received a copy of the GNU General Public License along with
# hubbardI. If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
# Configure the version
configure_file(version.py.in version.py)

# All Python files. Copy them in the build dir to have a complete package for the tests.
file(GLOB_RECURSE python_sources RELATIVE ${CMAKE_CURRENT_SOURCE_DIR} *.py)
foreach(file ${python_sources})
  configure_file(${file} ${file} COPYONLY)
endforeach()

# Install python modules to proper location
set(PYTHON_LIB_DEST ${TRIQS_PYTHON_LIB_DEST_ROOT}/${PROJECT_NAME})
install(FILES ${python_sources} ${CMAKE_CURRENT_BINARY_DIR}/version.py DESTINATION ${PYTHON_LIB_DEST})
