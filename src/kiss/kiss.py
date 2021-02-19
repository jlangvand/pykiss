# Copyright (C) 2021  Orbit NTNU

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
Simple serial kiss implementation
"""

# Externalimport serial
import re
import serial
# Internal
import kiss.constants as CONST
from kiss import logger


class Kiss:
    """
    Defines new KISS interface.

    :return:
    """

    def __init__(self, interface: serial.Serial):
        self._interface = interface
        self._incoming_data = []
        self._incomplete_frame = b'', b''

    def read_frame(self) -> (bytes, bytes):
        """
        Read a single frame from interface.

        Returns (type, payload)
        """
        _bytes = b''
        _type: bytes = b''
        _payload: bytes = b''
        _escape = False

        while self._interface.in_waiting:
            _byte = self._interface.read()

            if _byte == CONST.FEND:
                break
            if _escape:
                if _byte == CONST.TFEND:
                    _bytes += CONST.FEND
                elif _byte == CONST.TFESC:
                    _bytes += CONST.FESC
                _escape = False
            else:
                _bytes += _byte

        if len(_bytes) > 0:
            _type = _bytes[0]
        if len(_bytes) > 1:
            _payload = _bytes[1:]

        return _type, _payload

    def write(self, head: bytes = b'\x00', payload: bytes = b'') -> int:
        """
        Write a frame to the interface.
        """
        _bytes = head  # TODO: Check if head is FEND or FESC

        for _b in payload:
            if _b == CONST.FEND:
                _bytes += CONST.FESC + CONST.TFEND
            elif _b == CONST.FESC:
                _bytes += CONST.FESC + CONST.TFESC
            else:
                _bytes += _b

        return self._interface.write(_bytes)

    def has_data(self) -> int:
        """
        Returns the number of bytes waiting on the serial port.
        One frame is at least three bytes.

        :return: Number of bytes in input buffer (int)
        """
        try:
            # logger.debug('Request to get number of bytes in input buffer.')
            return self._interface.in_waiting
        except serial.SerialException:
            logger.error(
                'Radio not connected properly, could not get buffer size. ',
                exc_info=True)
