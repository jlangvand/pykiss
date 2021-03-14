# pykiss Copyright © 2021 Orbit NTNU

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
Main init file
"""

import logging
import sys
from serial import Serial, SerialException

import kiss.constants as CONST

logger = logging.getLogger()
logger.setLevel(logging.INFO)
CONSOLE_FORMAT = '%(levelname)8s %(filename)14s:%(lineno)-4s %(message)s'
stream_handler = logging.StreamHandler(sys.stdout)
stream_formatter = logging.Formatter(CONSOLE_FORMAT)
stream_handler.setFormatter(stream_formatter)
logger.addHandler(stream_handler)


class Kiss:
    """
    Defines new KISS interface.
    """

    def __init__(self, port: str, baud: int = 115200, timeout: int = 0.1):
        self._interface = Serial(port=port, baudrate=baud, timeout=timeout)

    def read_frame(self) -> (bytes, bytes):
        """
        Read a single frame from interface.

        Returns (type, payload)
        """
        _bytes = b''
        _type: bytes = b''
        _payload: bytes = b''
        _escape = False

        while True:
            _byte = self._interface.read()

            if _byte is None:
                break
            if _byte == CONST.FEND:
                break
            if _byte == CONST.FESC:
                _escape = True
            elif _escape:
                if _byte == CONST.TFEND:
                    _bytes += CONST.FEND
                elif _byte == CONST.TFESC:
                    _bytes += CONST.FESC
                _escape = False
            else:
                _bytes += _byte

        if len(_bytes) > 0:
            _type = _bytes[:1]
            if len(_bytes) > 1:
                _payload = _bytes[1:]
        elif self.has_data():
            _type, _payload = self.read_frame()

        return _type, _payload

    def write(self, head: bytes = b'\x00', payload: bytes = b'') -> int:
        """
        Write a frame to the interface.
        """
        i = 0
        n = 0

        n += self._interface.write(CONST.FEND)
        n += self._interface.write(head)
        
        while i < len(payload):
            _b = payload[i:i+1]
            if _b == CONST.FEND:
                n += self._interface.write(CONST.FESC)
                n += self._interface.write(CONST.TFEND)
            elif _b == CONST.FESC:
                n += self._interface.write(CONST.FESC)
                n += self._interface.write(CONST.TFESC)
            else:
                n += self._interface.write(_b)
            i += 1

        n += self._interface.write(CONST.FEND)
        return n

    def has_data(self) -> int:
        """
        Returns the number of bytes waiting on the serial port.
        One frame is at least three bytes.

        :return: Number of bytes in input buffer (int)
        """
        try:
            # logger.debug('Request to get number of bytes in input buffer.')
            return self._interface.in_waiting
        except SerialException:
            logger.error(
                'Device not connected properly, could not get buffer size. ',
                exc_info=True)
