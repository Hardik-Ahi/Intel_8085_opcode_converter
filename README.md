# Intel 8085 Opcode Converter

A Python script for converting Intel 8085 assembly mnemonics into executable opcodes.

This program was written primarily for converting programs written on `sim8085.com` into their opcode equivalents, making it easier to load and test programs on real 8085 trainer kits.

[Watch Demo on YouTube](https://youtu.be/PcFSY1kE05s)

## Why This Exists

In many educational 8085 trainer kits, entering mnemonic instructions directly can be inconvenient. Some kits require restarting the entire program entry process if even a small mistake is made.

One alternative is to enter raw opcodes directly into memory addresses, since individual instructions can then be edited without losing all progress. However, manually converting every instruction using opcode reference sheets is repetitive and error-prone.

This script automates that conversion process so the focus can remain on the program logic itself rather than opcode lookup.

## Features

- Converts Intel 8085 mnemonics to opcodes
- Supports label handling
- Generates opcode output files automatically
- Designed specifically around the formatting used by `sim8085.com`

## Input File Conventions

The input assembly program must follow a few formatting rules:

1. Always place a space after a comma.

   Example:
   ```asm
   MOV A, B
   ```
2. Hexadecimal is the default number system.

    * Do not append H to hexadecimal values
    * Use uppercase letters for hexadecimal digits

    Example:
    ```asm
    LXI H, 205A
    ```
3. Labels:
    * Must contain at least one lowercase letter
    * Must not contain uppercase letters
    * Must not contain spaces or special characters
    * Digits are allowed

4. Labels must be written in the following format:
    ```asm
    label: mnemonic
    ```
5. A sample file named `8-bit-addition.txt` is included for reference.

## How to Use

1. Prepare your assembly input file. Example: `yourfile.txt`.
2. Run the Python script.
3. Enter the file name when prompted.
    * If the file is in the same directory: `yourfile.txt`
    * Otherwise, provide the absolute path: `C:\Users\user\Desktop\yourfile.txt`
4. Enter the starting memory address in hexadecimal. Example: `6100`
5. The program generates an output file named: `yourfile_opcode.txt`. This file will contain the opcode version of the input program.

## Example Workflow

* Input: `8-bit-addition.txt`
* Start Address: `6100`
* Output: `8-bit-addition_opcode.txt`
