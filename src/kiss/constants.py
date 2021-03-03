# pykiss Copyright © 2021  Orbit NTNU

# Authors:
# David Ferenc Bendiksen
# Joakim Skogø Langvand
# Sander Aakerholt

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


"""
Constants used in the Kiss class
"""

FEND = b'\xC0'  # Frame end, also used at beginning of frame to flush buffer
FESC = b'\xDB'  # Escape bytes
TFEND = b'\xDC'  # Transposed FEND (FESC TFEND)
TFESC = b'\xDD'  # Transposed FESC (FESC TFESC)
