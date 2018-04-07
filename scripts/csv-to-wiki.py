#!/usr/bin/python

#########################################################################
#                                                                       #
#    This script is meant to convert the csv file containg the OSX/iOS  #
#    artifacts into a forensicswiki page                                #
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

#__description__ = ''
__author__ = '@pstirparo'
__version__ = '0.3.1'
__location__ = 'https://github.com/pstirparo/mac4n6'


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input', dest="csv_input", default=False, help='CSV Artifacts file to be converted into ForensicsWiki', metavar='')
    
    if len(sys.argv) == 1:
       parser.print_help()
       sys.exit(1)
    try:
       args = parser.parse_args()
    except:
       parser.print_help()
       sys.exit(0) 
    
    flag_openrow = False
    artifacts_counter, locations_counter = 0, 0
    csv_file = args.csv_input
    wiki_file = os.path.splitext(csv_file)[0] + ".txt"
    
    with open(wiki_file, 'w') as wikiF:
        wikiF.write("The content of this page is automatically generated from the \"Mac OS X artifacts location\" of the [" + __location__ + " mac4n6 project]. Please refer to that for any mistake/correction or if you wish to contribute.\n\n")
        
        with open(csv_file, 'r', encoding='latin-1') as csvF:
            reader = csv.reader(csvF, delimiter=',')
            for i in range(3):
                next(reader)
            for row in reader:
                #Check if current row is the intermediate section header and skip
                if row[0] == "Artifact" and row[1] == "Name":
                    continue

                elif row[0] == "SYSTEM ARTIFACTS" or row[0] == "USER ARTIFACTS" or row[0] == "APPLICATIONS ARTIFACTS":
                    wikiF.write("\n== " + row[0] + " ==\n")
                
                elif len(row[0]) > 0 and row[1] == "":
                    print("CAT: " + row[0])
                    wikiF.write("\n=== " + row[0] + " ===\n")
                    wikiF.write("----\n")
                
                elif int(len(row[0])) > 1 and int(len(row[1])) > 1:
                    if flag_openrow == True:
                        wikiF.write("</pre>\n")
                        flag_openrow = False
                
                    wikiF.write("\n;" + row[0] + "\n")
                    #wikiF.write("\n==== " + row[0] + " ====\n")
                    wikiF.write(row[4] + "\n")
                    wikiF.write("<pre>\n")
                    wikiF.write(row[3] + "\n")
                    artifacts_counter+=1
                    locations_counter+=1
                    flag_openrow = True
            
                elif row[0] == "\"":
                    wikiF.write(row[3] + "\n")
                    locations_counter+=1
        
                elif int(len(row[0])) == 0:
                    if flag_openrow == True:
                        wikiF.write("</pre>\n")
                        flag_openrow = False
        
        if flag_openrow == True:
            wikiF.write("</pre>\n")

        wikiF.write("\n== Other Informations ==\n")
        wikiF.write("Total Artifacts: " + str(artifacts_counter) + "\n\n")
        wikiF.write("Total Locations/Paths: " + str(locations_counter) + "\n\n")
    
        wikiF.write("\n== External Links ==\n")
        wikiF.write("The mac4n6 project: \n\n")
        wikiF.write(__location__ + "\n")
    
        wikiF.write("\n" + "[[Category:Mac OS X]]")
        wikiF.write("\n" + "[[Category:Operating systems]]")

    print("Aritfacts Counter: ", artifacts_counter)
    print("Locations Counter: ", locations_counter)

    
if __name__ == "__main__":
    main()