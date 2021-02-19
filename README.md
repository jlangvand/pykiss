# pykiss
Python serial KISS implementation.

This package is initially made for controlling the Nanoavionics Sat2RF1 satellite radio module, and in its current state it does not fully implement the full KISS spec, though this is planned for future releases.

It provides
* Reading data from interface, returned as a tuple (header, payload)
* Writing data to interface with a custom header, allows passing any command to the interface
* Escaping/restoring special characters as per the KISS spec

Currently it does not provide
* Anything else
