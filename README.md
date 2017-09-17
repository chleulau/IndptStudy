# Introduction
Independent study in learning about program verification
This repository is used for providing code and data for a general-purpose program verifier. The code for this parser is named indptparser.py. It is written in Python 2.7, using the Z3py SMT-solver, clang for c to LLVM IR translation, and llvmpy for retrieving information about the LLVM IR (via LLVM 3.3).

# Update (9/17/17)
The new file pverifier.py is the program verifier that can also handle asserts. It takes an LLVM IR text, and verifies the program using "basic path" traversal and z3. This program verifier can handle loops and recursion. Usage of pverifier.py is provided in the "Usage" section. The old files containing pverifier.py without the assert handler and the old supply files are in the folder "Finished_Old2".

## Usage
In terminal, just run 'python pverifier.py' where a prompt will ask you which llvm IR file to run. I provided four: examplels.ll (linear search), exampleprime.ll (prime checker (True means not a prime, False means it is a prime)), examplefib.ll (Fibonacci generator), and examplebs.ll (binary search (Recursion)). Thus far, the parser will generate lines of 'boolean sentences' corresponding to the basic paths. (Each basic path is a sentence.) Then it checks each basic path for validity using Z3. It will now also generate and check the z3-friendly eval paths for a provided supply file, (specifically the first line consists of pre-condition, second line the loop invariant, and third line the post-condition). Theory of arrays are handled in the usual z3 way. For an array A and index i, 'A[i] == e' is simply 'Select(A, i) == e'. Supply files are corresponding to the example IR files. For instance, exampleprime.ll has the corresponding supplyprime.txt as a supply file.

## TODO
* I need to add more comments to pverifier.py.
