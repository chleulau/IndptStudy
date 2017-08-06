# Introduction
Independent study in learning about program verification
This repository is used for providing code and data for a general-purpose program verifier. Code is written in Python 2.7

## Usage
In terminal, just run 'python indptparser.py' where a prompt will ask you which llvm IR file to run. I provided three: examplels.ll (linear search), exampleprime.ll (prime checker), and examplefib.ll (Fibonacci generator). Thus far, the parser will generate lines of 'boolean sentences' corresponding to the basic paths. (Each basic path is a sentence)

### Update (8/5/17)
It will now also generate the z3-friendly eval paths for a provided supply file, (specifically the first line consists of pre-condition, second line the loop invariant, and third line the post-condition). Theory of arrays are handled in the usual z3 way. For an array A and index i, 'A[i] == e' is simply 'Select(A, i) == e'

## TODO
* Tweak the parser to allow it to run the LLVM IR for fibonacci generator, where return value (rv) is not either true (1) or false (0). 
* I also need to add more comments to indptparser.py.
