HallRober is a program designed to easily carry out and standardize measurements on Planar Hall Effect and Anisotropic Magnetoresistance (AMR) sensors. Three different type of measurements are available, which are the most common ones used to assess the performance of these type of sensors, given a fixed current J applied on the sensor:

(1) The Angular dependence of the output voltage, measured between the applied magnetic field and J.

(2) The Magnetic Field dependence of the output voltage, measured at a fixed angle between the magnetic field and the sensor.

(3) The Magnetic Field dependence of the output voltage for very small magnetic fields (< 1G), measured at a fixed angle between the magnetic field and the sensor. This is usually done to provide a measurement of the sensitivity at small magnetic fields. 

In order to carry out these measurements, four lab instruments are required, and an additional one is required for small magnetic field measurements:
- An Arduino board is required to control a 28byj-48 motor to rotate the sample holder, and a relay module to switch the output current supplied from a DC power source to the magnetic coils. 
- A Bench multimeter is used to measure the output voltage of the sensor.
- A DC Power source is used to supply current to the Helmholtz coils that generate the magnetic field. 
- A precision current source is used to supply current to the sample. In the case of very small magnetic field measurements (3), an additional current source is used to supply small currents to the Helmholtz coils in place of the DC power source. 

HallRober was designed to work with the following lab instruments; however, other instruments from the same company might also work.
- Bench Multimeter: Keithley 2010
  
- DC Power Source: Keithley 2260b (though other models might also work)
  
- Precision Current Source: Keithley 6200 series


Library requirements:
-Pyfirmata2
-Pyvisa
-PyQT5
-serial
-configparser


How to use:
----
In a terminal, run ./main.py.

Before starting a measurement or setting the sensor holder's angle, the instruments need to be initialized. To do so, go to File > Initialize Instruments. Before doing so, make sure all the instruments are connected to the computer and turned on.

In this new window, all the instruments available are listed. If less than four instruments are found, check the instruments' connection to the PC. 

It is recommended to run the "Auto-Guess" button: the program will automatically try to find each instrument and assign it to its corresponding function. If this program is being run from Windows, it might not auto recognize the Arduino, but it can be assigned manually through the drop-down menus next to each instrument.

After each instrument is initialized, measurements can be carried out. Make sure to fill in your sample's name and to choose the path to save your measurements.
From the "Type of Measurement" drop down menu, each type of measurement can be selected. Every type of measurement includes different options that can be changed, and are discussed below.

(Angle, Field and Sensitivity measurements)

*Current (in uA): The current supplied to the sample (measured in uA). 

*Number of Measurements: For each step (angle or field), how many voltage samples are used to calculate the mean and std.

*Angle (deg): the initial angular position of the sample holder. Can be set instead from the "Set Angle" window from the "File" menu.

(Angle Sweep: Measuring the angular dependence of the output voltage)

Start, End Angle: The angle position at the start & end of the measurement.

Angle Step: the rotation step (in deg) taken during the measurement. It is recommended that, for this type of motor, a 2 deg step is used. 

Applied Field: The field (in G) applied during the whole measurement. It is recommended that a field equal or higher than the saturation field of the sample is selected.

(Field Sweep: Measuring the magnetic field dependence of the output voltage)

Start, end Field: The starting and ending magnetic fields of the measurement. It is recommended that both fields are equal or higher than the saturation field.

Field Step: the field step taken during measurements. 

Angle: the angular position of the substrate holder. Can be set instead from the "Set Angle" window from the "File" menu.

(Sensitivity: Measuring the magnetic field dependence of the output voltage at small magnetic fields)

Saturation Field: The magnetic field applied with the DC Power Source to reset the sensor's magnetic status. It is recommended that this field is higher than the saturation field of the sample.

Start, End field: The starting and ending magnetic fields. 

Field Step: the field step taken during measurements.

- Starting the measurement:
To start, simply click the "Start" button on the desired measurement. The measurement can be stopped at any time with the "Stop" button. Only one measurement can be started at any time.

- Saving the measurement:
To save the measurement's data, go to File > "Save ...". Make sure to update the filename for each measurement you carry out. The file is saved in a .csv format containing both the measured data and the measurement's parameters.









