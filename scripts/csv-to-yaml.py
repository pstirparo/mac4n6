#!/usr/bin/python

#########################################################################
#                                                                       #
#    This script is meant to convert the csv file containg the OSX/iOS  #
#    artifacts into a yaml artifact page                                #
#                                                                       #
#    Author: Pasquale Stirparo (@pstirparo)                             #
#                                                                       #
#    This work is licensed under the GNU General Public licensed        #
#                                                                       #
#########################################################################

import sys
import os
import csv
import argparse
from datetime import date

__author__ = '@pstirparo'
__version__ = '0.2'
__location__ = 'https://github.com/pstirparo/mac4n6'
__ref1__ = 'http://forensicswiki.org/wiki/Mac_OS_X'
__ref2__ = 'http://forensicswiki.org/wiki/Mac_OS_X_10.9_-_Artifacts_Location'


flag_openrow = False


def write_artifact(artifact, yamlF):
    yamlF.write("name: " + artifact["name"] + "\n")
    yamlF.write("doc: " + artifact["doc"] + "\n")
    yamlF.write("sources:\n")
    yamlF.write("- type: FILE\n")
    #yamlF.write("  attributes:\n")
    tmp = artifact["paths"].split(',')
    if int(len(tmp)) > 1:
        yamlF.write("  attributes:\n")
        yamlF.write("    paths: \n")
        for path in tmp:
            yamlF.write("      - \'" + path + "\'\n")
    else:
        yamlF.write("  attributes: ")
        yamlF.write("{paths: [\'" + artifact["paths"] + "\']}\n")
    yamlF.write("labels: [" + artifact["labels"] + "]\n")
    yamlF.write("supported_os: [Darwin]\n")
    
    if int(len(artifact["urls"])) > 0:
        yamlF.write("urls: [\'" + artifact["urls"] + "\']\n")
    
    yamlF.write("---\n")


def main():
    global flag_openrow
    artifact = {}
    artifacts_counter, locations_counter = 0, 0

    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input', dest="csv_input", default=False, help='CSV Artifacts file to be converted into YAML', metavar='')
    
    if len(sys.argv) == 1:
       parser.print_help()
       sys.exit(1)
    try:
       args = parser.parse_args()
    except:
       parser.print_help()
       sys.exit(0) 

    csv_file = args.csv_input
    yaml_file = os.path.splitext(csv_file)[0] + ".yaml"
        
    with open(yaml_file, 'w+') as yamlF:
        yamlF.write("# Mac OS X (Darwin) specific artifacts.\n")
        yamlF.write("# mac4n6: " + __location__ + "\n")
        yamlF.write("# Reference: " + __ref1__ + "\n")
        yamlF.write("# Reference: " + __ref2__ + "\n")
        yamlF.write("# Last update: " + date.today().isoformat() + "\n\n")

        with open(csv_file, 'rU') as file: 
            reader = csv.reader(file, delimiter=',')
            #skip the first 3 lines of the csv file
            for i in range(3):
                next(reader)
            for row in reader:
                if len(row) > 0:
                    if int(len(row[0])) > 1 and int(len(row[1])) > 1:
                        #Check if current row is the intermediate section header and skip
                        if row[0] == "Artifact" and row[1] == "Name":
                            continue
                        if flag_openrow == True:
                            write_artifact(artifact, yamlF)
                            flag_openrow = False

                        artifact["name"] = row[1]
                        artifact["doc"] = row[0]
                        artifact["paths"] = row[3]
                        artifact["labels"] = row[2]
                        artifact["urls"] = row[5]
                        flag_openrow = True
                        artifacts_counter+=1
                        locations_counter+=1

                    elif int(len(row[0])) == 1:
                        artifact["paths"] = artifact["paths"] + "," + row[3]
                        locations_counter+=1

        if flag_openrow == True:
            write_artifact(artifact, yamlF)

        yamlF.write("# Total Artifacts: " + str(artifacts_counter) + "\n")
        yamlF.write("# Total Locations: " + str(locations_counter) + "\n")


if __name__ == '__main__':
    main()
