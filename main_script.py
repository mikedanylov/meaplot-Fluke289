#!/usr/bin/env python

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

    return args

def main():
    
    args = argsParser()
    # print args.filePath
    # print args.serialPort
    # print args.graphLabel
    # print args.legendLabel
    # print args.samples
    # print args.duration

if __name__ == "__main__":
    main()