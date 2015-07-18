###!/usr/bin/env python
#!venv_meaplot/bin/python

import pylab
import time
import datetime
import serial
import argparse   

def argsParser():

    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--filePath', type=str,
        help="path to the file where measurements are saved")
    parser.add_argument('-p', '--serialPort', type=str,
        help="port on which Fluke 289 is connected")
    parser.add_argument('-g', '--graphLabel', type=str,
        help="name of the graph")
    parser.add_argument('-l', '--legendLabel', type=str,
        help="name of the plot in legend")
    parser.add_argument('-s', '--samples', type=int,
        help="N of measurements/second")
    parser.add_argument('-d', '--duration', type=int,
        help="duration of measurement in seconds [10; 86400]")
    args = parser.parse_args()

    if args.filePath == None:
        args.filePath = '/tmp/some.file'
        print 'File was not specified. Measurements are saved to /tmp/some.file'
    if args.serialPort == None:
        args.serialPort = '/dev/ttyUSB0'
        print 'Serial Port was not specified. Default is set to /dev/ttyUSB0'
    if args.samples == None:
        args.samples = 10
        print 'Number of samples/second is not given. Default set to 10 samples/second'
    if args.duration == None:
        args.duration = 10
        print 'Duration of measurements is not specified. Default set to 10 second'
    if args.graphLabel == None:
        args.graphLabel = 'New Graph'
        print 'Graph label is not specified. Default is set to New Graph'
    if args.legendLabel == None:
        args.legendLabel = 'New Legend Item'
        print 'Legend label is not specified. Default is set to New Legend Item'   

    return args


def serialRead(filePath='/tmp/some.file', port='/dev/ttyUSB0', readTime=10, samples=10):
    '''
    Read specified Serial port
    where Fluke 289 is connected
    '''

    if samples > 25: # can't handle more samles
        samples = 25
    elif samples < 1:
        samples = 1
    if readTime > 86400: # 24 hours restriction
        readTime
    elif readTime < 10:
        readTime = 10

    try:
        ser = serial.Serial(port, 115200, timeout = 1.0/samples)
        f = open(filePath, 'w')

        start_time = time.time()

        while (start_time + readTime) > time.time(): # code a timer here which will stop when readTime seconds is elapsed
            try:
                line_from_serial = ""
                ser.write("QM\r")
                line_from_serial += ser.read(32) 
                line_from_serial = line_from_serial[2:-1] # cut '0\n'
                # print line_from_serial
                line_splited = line_from_serial.split(',')
                value_amperes = float(line_splited[0])
                # print value_amperes
                f.write(str(value_amperes) + ',' + str(datetime.datetime.now()) + '\n')
            except serial.SerialException:
                print 'Error occured!\n'
                continue
            except ValueError:
                print 'Lost value!'
                continue
    except OSError:
        print 'ERROR: Multimeter is not connected!'
        print 'Check /dev/ folder for ttyUSBx port and do sudo chmod 777 /dev/ttyUSBx'
        print 'to allow not sudo user to read the port'
        print 'WARNING: plot might be outdated...'


def chargingRatePlot(filePath='/tmp/some.file', plotLabel = 'New Plot', legendLabel = 'Some charger'):
    '''
    Plots a graph A(t)
    where:
    A - current measured from multimeter
    t - time stamp
    Throws IOError exeption if file doesn't exist
    returns None
    '''
    try:
        # check if file exists, throws exeption otherwise
        times, measurements = getMeasurements(filePath)
        
        # plotting related stuff
        pylab.figure(str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")), figsize=(22.0, 9.0))
        pylab.title(plotLabel)
        pylab.xlabel('time, hour')
        pylab.ylabel('current, A')
        pylab.grid(True)
        pylab.plot(times, measurements, '-b', label=legendLabel)
        mng = pylab.get_current_fig_manager() # get figure manager for
        mng.resize(*mng.window.maxsize())     # setting window size to max
        # mng.full_screen_toggle()
        pylab.legend(loc='best') # should be placed after pylab.plot()
        pylab.savefig(plotLabel + '_' + legendLabel +  '_' + str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + '.png'), format='png', dpi=200)
        pylab.show()

    except IOError:
        print "File does not exist! Check file in " + str(filePath)

def getMeasurements(filePath):
    '''
    Get measurements from file
    Assumes:
        - measurements are already read from multimeter
        - measurements are stored as 'float,datetime\n' on each line
    returns two lists of measurements(float) and times(datetime)
    '''
    dataFile = open(filePath, 'r')
    times = []
    measurements = []
    counter = 0 # counter to keep track of lines
    PRESCALER = 1 # allows to read only N-th line from measurements
        
    for line in dataFile:
        # read only each N-th line
        if counter % PRESCALER == 0:
            line = line[:-1] # cut \n from the end of the line
            value, time = line.split(',')
            times.append(datetime.datetime.strptime(time, "%Y-%m-%d %H:%M:%S.%f"))
            measurements.append(value)
            counter += 1
    return (times, measurements)


def main():

    args = argsParser()
    # serialRead('/tmp/serial_data.txt', '/dev/ttyUSB0', 15, 10)
    # chargingRatePlot('/tmp/serial_data.txt', 'Tablet charging 1A', 'Phihong charger')
    serialRead(args.filePath, args.serialPort, args.duration, args.samples)
    chargingRatePlot(args.filePath, args.graphLabel, args.legendLabel)

if __name__ == "__main__":
    main()
