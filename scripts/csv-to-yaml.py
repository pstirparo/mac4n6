#!/usr/bin/python

#########################################################################
#																		#
#	This script is meant to convert the csv file containg the OSX/iOS	#
#	artifacts into a yaml artifact page									#
#																		#
#	Author: Pasquale Stirparo (@pstirparo)								#
#																		#
#	This work is licensed under the GNU General Public licensed			#
#																		#
#																		#
#########################################################################

import sys
import os
import csv
from datetime import date

__author__ = '@pstirparo'
__version__ = '0.1'
__location__ = 'https://github.com/pstirparo/mac4n6'


flag_openrow = False


def write_artifact(artifact, fh):
	print >> fh, "name: " + artifact["name"]
	print >> fh, "doc: " + artifact["doc"]
	print >> fh, "sources:"
	print >> fh, "- type: FILE"
	print >> fh, "  attributes:"
	tmp = artifact["paths"].split(',')
	if int(len(tmp)) > 1:
		print >> fh, "    paths: "
		for path in tmp:
			print >> fh, "      - \'" + path + "\'"
	else:
		print >> fh, "    paths: [\'" + artifact["paths"] + "\']"
	print >> fh, "labels: [" + artifact["labels"] + "]"
	print >> fh, "supported_os: [Darwin]"
	
	if int(len(artifact["urls"])) > 0:
		print >> fh, "urls: [\'" + artifact["urls"] + "\']"
	
	print >> fh, "---"


def main():
	global flag_openrow
	artifact = {}
	artifacts_counter, locations_counter = 0, 0

	if len(sys.argv) != 2:	
		print '[ERROR]: wrong input parameter'
		print 'Usage:'
		print 'csv-to-yaml.py <csv_file_to_parse>'

	else:
		csv_file = sys.argv[1]
		yaml_file = os.path.splitext(csv_file)[0] + ".yaml"
		
		fh = open(yaml_file, 'w')
		print >> fh, "# Mac OS X (Darwin) specific artifacts."
		print >> fh, "# URL: " + __location__
		print >> fh, "# Last update: " + date.today().isoformat() + "\n"

		with open(csv_file, 'rU') as file: 
		    reader = csv.reader(file, delimiter=',')
		    for row in reader:
		    	if len(row) > 0:
			    	if int(len(row[0])) > 1 and int(len(row[1])) > 1:
			    		if flag_openrow == True:
			    			write_artifact(artifact, fh)
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
		    write_artifact(artifact, fh)

		print >> fh, "# Total Artifacts: ", artifacts_counter
		print >> fh, "# Total Locations: ", locations_counter
		fh.close()


if __name__ == '__main__':
    main()