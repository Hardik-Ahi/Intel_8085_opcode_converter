import os

hex_mappings = {'A': 10, 'B': 11, 'C': 12, 'D': 13, 'E': 14, 'F': 15}
dec_mappings = {10: 'A', 11: 'B', 12: 'C', 13: 'D', 14: 'E', 15: 'F'}

program_name = input("Enter the program file name (path): ")
starting_address = input("Enter 4-digit starting address of the program in hexadecimal: ")
invalid = False

if not os.path.isfile(program_name):
    print("Input file does not exist.")
    input("Press any key to continue...")
    quit()
else:
    if len(starting_address) != 4:
        invalid = True
    else:
        for digit in starting_address:
            try:
                digit = int(digit)
            except ValueError:
                if digit not in hex_mappings.keys():
                    invalid = True
                    break
if invalid:
    print("Invalid starting address.")
    input("Press any key to continue...")
    quit()

def hexadecimal_to_decimal(hex_string):
    hex_string = hex_string[::-1]
    total = 0
    power = 0
    for digit in hex_string:
        try:
            total += int(digit) * (16**power)
        except ValueError:
            total += hex_mappings[digit.upper()] * (16**power)
        power += 1

    return total

def decimal_to_hexadecimal(decimal_number):
    result = []
    remainder = 0

    while True:
        remainder = decimal_number % 16
        if remainder in dec_mappings.keys():
            result.append(dec_mappings[remainder])
        else:
            result.append(str(remainder))
        if decimal_number // 16 == 0:
            break
        decimal_number //= 16

    result = result[::-1]
    return "".join(result)

program_file = open(program_name, "r")
output_file = open("".join(program_name.split(".")[0] + "_opcode.txt"), "w+")
opcode_file = open("opcode.txt", "r")

opcodes = opcode_file.readlines()
opcodes_line_count = 0
program_line = hexadecimal_to_decimal(starting_address)

incoming_labels = {}
outgoing_labels = {}

def insertLineNumber():
    global output_file
    global program_line
    output_file.write(decimal_to_hexadecimal(program_line)+" -> ")
    program_line += 1

def leave_space_for_labels():
    insertLineNumber()
    output_file.write("\n")
    insertLineNumber()
    output_file.write("\n")

for line in program_file.readlines():
    opcodes_line_count = 0
    line_list = line.split(" ")

    while 1:
        if opcodes_line_count > len(opcodes) - 1:
            break
        opcode_list = opcodes[opcodes_line_count].split(" ")

        if line_list[0].replace("\n", "") == opcode_list[0]:
            if opcode_list[1] == "-" or opcode_list[1] == "--":  # each opcode line has exactly 3 space-separated components
                insertLineNumber()
                output_file.write(opcode_list[-1])

                if opcode_list[1] == "--":
                    if line_list[1].islower():  # outgoing label found
                        outgoing_labels[decimal_to_hexadecimal(program_line)] = line_list[1].replace("\n", "")
                        leave_space_for_labels()
                        break
                    else:
                        insertLineNumber()
                        output_file.write(line_list[1][2:].replace("\n", "") + "\n")

                insertLineNumber()
                output_file.write(line_list[1][0:2].replace("\n", "") + "\n")
                break
            else:  # the opcode has (register), (register, register), (register, operand), (_)
                if not opcode_list[1] == "_":
                    if line_list[1].replace("\n", "") == opcode_list[1]:  # checking for (register)
                        insertLineNumber()
                        output_file.write(opcode_list[-1])
                        break

                    elif line_list[1] in opcode_list[1]:
                        if line_list[2].replace("\n", "") in opcode_list[1]:  # checking for (register, register)
                            insertLineNumber()
                            output_file.write(opcode_list[-1])
                            break

                        elif "--" in opcode_list[1]:
                            insertLineNumber()
                            output_file.write(opcode_list[-1])

                            insertLineNumber()
                            output_file.write(line_list[2][2:].replace("\n", "") + "\n")

                            insertLineNumber()
                            output_file.write(line_list[2][:2] + "\n")
                            break

                        elif "-" in opcode_list[1]:
                            insertLineNumber()
                            output_file.write(opcode_list[-1])

                            insertLineNumber()
                            output_file.write(line_list[2].replace("\n", "") + "\n")
                            break
                else:
                    insertLineNumber()
                    output_file.write(opcode_list[-1])
        elif ":" in line_list[0]:  # incoming label found
            incoming_labels[line_list[0].replace(":", "")] = decimal_to_hexadecimal(program_line)
            del line_list[0]
            continue
        opcodes_line_count += 1

output_file.seek(0, 0)
opcodes = output_file.readlines()
label_writer = False
line_index = 0
location = "0000"

for line in opcodes:
    line_list = line.split()

    if label_writer:
        opcodes[line_index] = "".join([opcodes[line_index].replace("\n", ""), location[:2], "\n"])
        label_writer = False
    elif len(line_list) < 3:  # found location for inserting label location
        location = str(incoming_labels[outgoing_labels[line_list[0]]])
        label_writer = True
        opcodes[line_index] = "".join([opcodes[line_index].replace("\n", ""), location[2:], "\n"])

    line_index += 1

output_file.seek(0, 0)
output_file.write("".join(opcodes))

print("Output file generated successfully.")
input("Press any key to continue...")

program_file.close()
output_file.close()
opcode_file.close()
