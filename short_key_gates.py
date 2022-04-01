import argparse

parser = argparse.ArgumentParser(description="Make two copies of locked circuit that replace key gate under test with "
                                             "a buffer or inverter")
parser.add_argument("input_file", help="The input bench file")
parser.add_argument("key_input", help="The key input under test")
parser.add_argument("output_file", help="The beginning of the output file name for the new files. Output files will be "
                                        "output_file_key_input_0 and output_file_key_input_1")

args = parser.parse_args()

filein = open(args.input_file, 'r')
fileout_0_name = args.output_file + args.key_input + "_0.bench"
fileout_1_name = args.output_file + args.key_input + "_1.bench"

# output file for key input being tested as a value of 0
fileout_0 = open(fileout_0_name, 'w')
# output file for key input being tested as a value of 1
fileout_1 = open(fileout_1_name, 'w')

# construct string for floating input to remove from file
floating_input = 'INPUT(' + args.key_input + ')'

# parse input file and create copies
for line in filein:
    if floating_input not in line:
        if args.key_input in line:
            # key gate identified. replace with buffer or inverter
            split_line = line.split(' = ')
            # split_line[0] is output, split_line[1] is gate. extract non-key input from gate
            inputs = split_line[1].split(',')
            buffer_input = ''
            if args.key_input in inputs[0]:
                # remove parantheses from gate
                buffer_input = inputs[1][:-2]
            else:
                # split again to remove gate name and parantheses
                find_input = inputs[0].split('(')
                buffer_input = find_input[1]
            if 'XOR' in line:
                # replacing with buffer is testing 0, replacing with inverter is testing 1
                fileout_0.write(split_line[0] + ' = BUF(' + buffer_input + ')\n')
                fileout_1.write(split_line[0] + ' = NOT(' + buffer_input + ')\n')
            else:
                # replacing with inverter is testing 0, replacing with buffer is testing 1
                fileout_0.write(split_line[0] + ' = NOT(' + buffer_input + ')\n')
                fileout_1.write(split_line[0] + ' = BUF(' + buffer_input + ')\n')
        else:
            fileout_0.write(line)
            fileout_1.write(line)

filein.close()
fileout_0.close()
fileout_1.close()



