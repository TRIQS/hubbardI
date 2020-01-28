###############################################################################
#
# hubbardI: A TRIQS based hubbardI solver
#
# Copyright (c) 2019-2020 Malte Schueler
# Copyright (c) 2019-2020 The Simons Foundation
#	author: N. Wentzell
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
configure_file(triqs_hubbardI-config.cmake.in triqs_hubbardI-config.cmake @ONLY)
configure_file(triqs_hubbardI-config-version.cmake.in triqs_hubbardI-config-version.cmake @ONLY)
install(
  FILES
    ${CMAKE_CURRENT_BINARY_DIR}/triqs_hubbardI-config.cmake
    ${CMAKE_CURRENT_BINARY_DIR}/triqs_hubbardI-config-version.cmake
  DESTINATION lib/cmake/triqs_hubbardI
)
