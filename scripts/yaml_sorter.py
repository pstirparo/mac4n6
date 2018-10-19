#!/usr/bin/python

import sys
import argparse
import ruamel.yaml

yaml = ruamel.yaml.YAML()

def main():
  parser = argparse.ArgumentParser()
  requiredArgs = parser.add_argument_group('required arguments')
  requiredArgs.add_argument('-i', '--input', dest="input_yaml", default=False,
      help='YAML file to be sorted', required=True, metavar='INPUT_YAML_FILE')
  parser.add_argument('-o', '--output', dest="output_yaml",
      default=False, help='Sorted YAML output file',
      metavar='OUTPUT_YAML_FILE')

  if len(sys.argv) < 3:
    parser.print_help()
    sys.exit(1)

  try:
    args = parser.parse_args()
  except:
    parser.print_help()
    sys.exit(0)

  try:
    f_input = open(args.input_yaml, 'r')
    yaml_tmp = list(
        ruamel.yaml.round_trip_load_all(f_input, preserve_quotes=True))

    if not yaml_tmp[-1]:
      yaml_tmp = yaml_tmp[:-1]

    sorted_yaml = sorted(yaml_tmp, key=lambda i: i['name'])
    if args.output_yaml:
      f_output = open(args.output_yaml, 'w')
    else:
      f_output = open(args.input_yaml + "_sorted.yaml", 'w')
    yaml.dump_all(sorted_yaml, f_output)
    f_output.write("...")

    f_input.close()
    f_output.close()
    print("[INFO] - Sorting completed.")
    print("[INFO] - Number of Artifacts: " + str(len(yaml_tmp)))
  except Exception as exc:
    print(exc)


if __name__ == '__main__':
  main()