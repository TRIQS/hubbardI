###############################################################################
#
# hubbardI: A TRIQS based hubbardI solver
#
# Copyright (c) 2020 Malte Schueler
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
from triqs_dft_tools.converters.vasp_converter import *
Converter = VaspConverter(filename = 'ce')
Converter.convert_dft_input()
