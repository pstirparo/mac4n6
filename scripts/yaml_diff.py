#!/usr/bin/python

import argparse
import sys

from ruamel.yaml import YAML
import ruamel.yaml
from deepdiff import DeepDiff

yaml = YAML()

__author__ = '@pstirparo'
__version__ = '0.1'
__location__ = 'https://github.com/pstirparo/mac4n6'


def main():
  parser = argparse.ArgumentParser()
  requiredArgs = parser.add_argument_group('required arguments')
  requiredArgs.add_argument('-f', '--first', dest="first_yaml", default=False,
      help='Original/Old YAML file to be compared', required=True,
      metavar='OLD_YAML_FILE')
  requiredArgs.add_argument('-s', '--second', dest="second_yaml", default=False,
      help='New YAML file to be compared', required=True,
      metavar='NEW_YAML_FILE')
  parser.add_argument('-o', '--output_dir', dest="output_directory",
      default=".", help='Prefix for output files',  metavar='prefix')

  if len(sys.argv) < 5:
    parser.print_help()
    sys.exit(1)

  try:
    args = parser.parse_args()
  except:
    parser.print_help()
    sys.exit(0)

  stream1 = open(args.first_yaml, 'r')
  stream2 = open(args.second_yaml, 'r')

  try:
    yaml1 = clear_urls(stream1)
    yaml2 = clear_urls(stream2)

    ddiff = DeepDiff(yaml1, yaml2, ignore_order=True)

    missing_file = open(args.output_directory + "/missing_in_" +
                        args.second_yaml.split("/")[-1], 'w')
    new_file_out = open(args.output_directory + "/new_from_" +
                        args.second_yaml.split("/")[-1], 'w')
    print("\nMISSING ARTIFACTS IN " + args.second_yaml + " FROM " +
          args.first_yaml + ":\n")
    if 'iterable_item_removed' in ddiff.keys():
      print_artifacts(ddiff['iterable_item_removed'], missing_file)
    else:
      print("None")
    print("\n\nNEW ARTIFACTS FROM " + args.second_yaml + ":\n")
    if 'iterable_item_added' in ddiff.keys():
      print_artifacts(ddiff['iterable_item_added'], new_file_out)
    else:
      print("None")

    stream1.close()
    stream2.close()
    missing_file.close()
    new_file_out.close()
  except Exception as exc:
    print(exc)


# This function removes the URL field from the entry to make
# proper 1:1 comparison on the artifacts content, and remove invalid
# entries (e.g. often closure trail is wrong, '---' instead of '...')
def clear_urls(stream):
  yaml_tmp = list(ruamel.yaml.round_trip_load_all(stream, preserve_quotes=True))
  for data in yaml_tmp:
    if data:
      del data['urls']
    else:
      yaml_tmp.remove(data)
  return yaml_tmp


def print_artifacts(d_diff_items, file_h):
  first_item = True
  tmp = []
  for key, value in d_diff_items.iteritems():
    tmp.append(value)

  for item in sorted(tmp, key = lambda i: i['name']):
    if not first_item:
      print("---")
      file_h.write("---\n")
    first_item = False
    yaml.dump(item, sys.stdout)
    yaml.dump(item, file_h)
  print("...")
  file_h.write("...")


if __name__ == '__main__':
  main()