###############################################################################
#
# hubbardI: A TRIQS based hubbardI solver
#
# Copyright (c) 2019-2020 Malte Schueler
# Copyright (c) 2019-2020 The Simons foundation
#   authors: N. Wentzell
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
# Generate the sphinx config file
configure_file(${CMAKE_CURRENT_SOURCE_DIR}/conf.py.in ${CMAKE_CURRENT_BINARY_DIR}/conf.py @ONLY)

# ---------------------------------
# Top Sphinx target
# ---------------------------------
if(NOT DEFINED SPHINXBUILD_EXECUTABLE)
  find_package(Sphinx)
endif()

# Sphinx has internal caching, always run it
add_custom_target(${PROJECT_NAME}_docs_sphinx ALL)
add_custom_command(
  TARGET ${PROJECT_NAME}_docs_sphinx
  COMMAND PYTHONPATH=${PROJECT_BINARY_DIR}/python:$ENV{PYTHONPATH} ${SPHINXBUILD_EXECUTABLE} -c . -j8 -b html ${CMAKE_CURRENT_SOURCE_DIR} html
)

# ---------------------------------
# Install
# ---------------------------------
install(DIRECTORY ${CMAKE_CURRENT_BINARY_DIR}/html/ COMPONENT documentation DESTINATION share/doc/${PROJECT_NAME}
  FILES_MATCHING
  REGEX "\\.(html|pdf|png|gif|jpg|svg|js|xsl|css|py|txt|inv|bib|cfg)$"
  PATTERN "_*"
)
