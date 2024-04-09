HallRober is a program that was designed to help measure the Planar Hall Effect (PHE) in the laboratory. It automatizes the V vs angle, V vs Field and sensitivity measurements in a user-friendly interface created 100% with Python.
The equipment used in my laboratory (and consequently in this program) consists of a Keithley 6620/6621 current source, a Keithley 2010 multimeter, a Keithley 2260-B DC source and an arduino. These pieces of equiment are used respectively to inject an electrical current onto the sample, to measure its Hall voltage, to power a set of Helmholtz coils, and to control a relay module and a 28byj-48 driver module.
HallRober requires the following Python libraries to run:
-Numpy
-PyQt5
-PyQtGraph
-csv
-Pyvisa
-Pyserial
-Pyfirmata2
-configparser

Before a measurement starts, HallRober can auto-detect the instruments that are connected and automatically assign their addresses (no manual tweaking required) stress-free.

