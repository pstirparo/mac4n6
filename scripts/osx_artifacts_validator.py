from pathlib import Path
import glob
import platform
from ruamel.yaml import YAML
import argparse
import sys
import os
from datetime import datetime

yaml = YAML()

__author__ = '@pstirparo'
__version__ = '0.1'
__location__ = 'https://github.com/pstirparo/mac4n6'
__ref1__ = 'http://forensicswiki.org/wiki/Mac_OS_X'
__ref2__ = 'http://forensicswiki.org/wiki/Mac_OS_X_10.9_-_Artifacts_Location'

# Defining '%%users.homedir%%' variable
homedir = str(Path.home())

valid_yaml = []
invalid_yaml = []
output_log = []

def validate(p):
    if '%%users.homedir%%' in p:
        p = p.replace("%%users.homedir%%", homedir)

    # If it's a DIR, remove the final * or glob fails if folder is empty
    if p[-2:] == '/*':
        p = p[:-1]     

    if '#' in p:
        if glob.glob(p.replace('#', "[0-9]")):
            return True
        else:
            return False
    elif "<name@address>" in p:
        if glob.glob(p.replace("<name@address>", "*")):
            return True
        else:
            return False
    else:
        if glob.glob(p):
            return True
        else:
            return False

# This function is to print only the artifacts paths that are missing in a txt/csv format
def print_log(output_log, file_name):
    with open(file_name, 'w') as fh:
        fh.write("--- MISSING OSX ARTIFACTS LOCATIONS ---\n")
        if os.getuid() == 0:
            fh.write("--- Executed as root ---\n")
        else:
            fh.write("--- Not executed as root ---\n")
        for log in output_log:
            fh.write(log + '\n')
    
def print_yaml(yaml_list, file_name):
    with open(file_name, 'w') as out:
        out.write("# MAC OSX ARTIFACTS REPORT\n")
        out.write("# System:   " + str(platform.system()) + '\n')
        #out.write("# Machine:  " + str(platform.machine()) + '\n')
        out.write("# Platform: " + str(platform.platform()) + '\n')
        out.write("# Version:  " + str(platform.mac_ver()[0]) + '\n')
        if os.getuid() == 0:
            out.write("# Executed as root\n")
        else:
            out.write("# Not executed as root\n")
        out.write(datetime.utcnow().strftime('# %Y-%m-%d %H:%M UTC\n\n'))
        yaml.dump_all(yaml_list, out)
        out.write("...")
    
def labels_to_string(labels):
    string = labels[0]
    for label in labels[1:]:
        string = string + "|" + label
    return string

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input', dest="yaml_input", default=False, help='YAML Artifacts file to be checked', metavar='')
    parser.add_argument('-o', '--output', dest="output_prefix", default="", help='Prefix for output files', metavar='')
    
    if len(sys.argv)==1:
       parser.print_help()
       sys.exit(1)
    try:
       args = parser.parse_args()
    except:
       parser.print_help()
       sys.exit(0) 
       
    with open(args.yaml_input, 'r') as stream:
        try:
            documents = yaml.load_all(stream)
            # "data" is the entire single yaml entry. It's a dict of dicts
            # while the field "sources" is a list of dict
            for data in documents:
                for sources in data["sources"]:
                    path_list = sources["attributes"]["paths"]
                    if(len(path_list) == 1):
                        if validate(path_list[0]):
                            valid_yaml.append(data)
                        else:
                            invalid_yaml.append(data)
                            output_log.append(labels_to_string(data["labels"]) + 
                                              "," + data["doc"] + "," + data["name"] + "," + path_list[0])
                    else:
                        invalid_flag = False
                        for path in path_list:
                            if validate(path) == False:
                                invalid_flag = True
                                output_log.append(labels_to_string(data["labels"]) + 
                                                  "," + data["doc"] + "," + data["name"] + "," + path)
                        if invalid_flag:
                            invalid_yaml.append(data)            
        except Exception as exc:
            print(exc)
    print_yaml(valid_yaml, args.output_prefix + "_valid_osx_artifacts.yaml")
    print_yaml(invalid_yaml, args.output_prefix + "_invalid_osx_artifacts.yaml")
    print_log(output_log, args.output_prefix + "_output_log.csv")
                
    
if __name__ == '__main__':
    main()