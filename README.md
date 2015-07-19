# Power_Measurements_Fluke289
Automated power consumption measurements using Fluke 289

This simple peace of software allows to read current values from Fluke 289 multimeter using serial port and plot a corresponding graph.

Flow of operation is the following:

1. Send request to multimeter 'QM\r'
2. Receive a response '1.0327E0,ADC,NORMAL,NONE' (where the only thing we actually need is floating point number 1.0327E0 which represents current value in Amperes)
3. Add timestamps to each value
4. Save measurements one by one to a file
5. Read the file and plot a graph A(t)

Script can be called using python from CLI.
Help option contains short descriptions of all options. Also, they are quite self explanatory in the code but I will mention them here just for convenience so that all info is gathered here.

```bash
usage: meaplotter.py [-h] [-f FILEPATH] [-p SERIALPORT] [-g GRAPHLABEL]
                      [-l LEGENDLABEL] [-s SAMPLES] [-d DURATION]

optional arguments:
  -h, --help            show this help message and exit
  -f FILEPATH, --filePath FILEPATH
                        path to the file where measurements are saved
  -p SERIALPORT, --serialPort SERIALPORT
                        port on which Fluke 289 is connected
  -g GRAPHLABEL, --graphLabel GRAPHLABEL
                        name of the graph
  -l LEGENDLABEL, --legendLabel LEGENDLABEL
                        name of the plot in legend
  -s SAMPLES, --samples SAMPLES
                        N of measurements/second [0; 25]
  -d DURATION, --duration DURATION
                        duration of measurement in seconds [10; 86400]
```

**TODO**
- [ ] would be nice to be able to install this tool as rpm package which will install necessary python libraries as well
