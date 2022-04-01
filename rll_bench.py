import argparse
import random

parser = argparse.ArgumentParser(description="Add RLL to a bench circuit")
parser.add_argument("input_file", help="The input bench file")
parser.add_argument("num_keys", help="The number of locking keys")
parser.add_argument("num_gates", help="The number of gates in the unlocked circuit")
parser.add_argument("output_file", help="The output file name for obfuscated circuit")
parser.add_argument("key_file", help="File to store secret key")
args = parser.parse_args()

# parse args
num_keys = int(args.num_keys)
num_gates = int(args.num_gates)

# select nodes to obfuscate and generate key
selected_gates = []
key = []
for i in range(0, num_keys):
    x = random.randint(1, num_gates)
    if x not in selected_gates:
        selected_gates.append(x)
    y = random.randint(0, 1)
    key.append(y)

selected_gates.sort()
# check that correct number of lines were added with no duplicates
# print(selected_gates)

# add obfuscation
fileout = open(args.output_file, 'w')
filein = open(args.input_file, 'r')
gate_counter = 1
key_counter = 0

# Print name of module as comment on top line of file
module_name = filein.readline()
# funky substring notation to remove \n
module_name = module_name[:-1]
fileout.write(module_name + '_rll_' + str(args.num_keys) + '\n')
# print extra new line for cleanliness
fileout.write('\n')

# print key inputs
for i in range(0, num_keys):
    fileout.write('INPUT(keyInput' + str(i) + ')\n')

for line in filein:
    lowercase_line = line.lower()
    if "input" in lowercase_line:
        fileout.write(line)
    elif "output" in lowercase_line:
        fileout.write(line)
    elif ' = ' in lowercase_line:
        if gate_counter in selected_gates:
            # take current gate and add key gate to output
            split_line = line.split(' = ')
            print(split_line)
            # line is now split into gate output and gate. First, set gate output to a key wire
            fileout.write('keyWire' + str(key_counter) + ' = ' + str(split_line[1]))
            # now, make key gate that outputs to original gate output
            # Choose to insert xor or xnor gate. Key = 0 insert xor, Key = 1 insert xnor
            if key[key_counter] == 0:
                fileout.write(
                    str(split_line[0]) + ' = XOR(keyWire' + str(key_counter) + ', keyInput' + str(key_counter) + ')\n')
            else:
                fileout.write(
                    str(split_line[0]) + ' = XNOR(keyWire' + str(key_counter) + ', keyInput' + str(key_counter) + ')\n')
            key_counter += 1
        else:
            fileout.write(line)
        gate_counter += 1
    else:
        fileout.write(line)

filein.close()
fileout.close()

with open(args.key_file, 'w') as keyfile:
    for j in range(0, num_keys):
        keyfile.write('keyInput' + str(j) + ' = ' + str(key[j]) + '\n')

