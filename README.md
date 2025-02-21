# Grammar-Based Fuzzing

## Introduction
Grammar-based fuzzing is a commonly used method to test programs that consume structured inputs, particularly input parsers.

# Objectives
A grammar-based fuzzer to generate structured inputs for testing.
Explore various grammar structures to hit or exceed a coverage threshold.

This program is a grammar-based fuzzer capable of generating structured inputs based on a specified grammar.
The goal is to hit or exceed a coverage threshold by generating a test suite that effectively tests the target program.

The algorithms interprets grammar specifications and generate inputs accordingly.
Explore different paths and options within the grammar to maximise code coverage.
Test the generated inputs on the target program to assess its coverage.
Implement mechanisms to adjust the generation process to hit or exceed the coverage threshold.

## Input Specifications
The program takes 3 command-line arguments:
The path to a Python script
The path to a single Python (.py) script containing the grammar specifications using the syntax.
The number of strings your program should generate for the test suite.

It should be called using the following command:
python grammar_fuzzer.py <python_program> <grammar_file> <num_strings>
The grammar file should define the structure of the inputs using a specified syntax.

# Output Specifications
The program generates structured inputs based on the grammar specifications provided and write them to an output .in file with the same name as the program itself.
The output file contains the specified number of strings each on a new line, where each string represents a test input. 
The generated inputs cover various paths and options within the grammar, aiming to hit or exceed the coverage threshold defined for the target program.
