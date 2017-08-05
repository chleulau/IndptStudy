# IndptStudy
Independent study in learning about program verification
This repository is used for providing code and data for a general-purpose program verifier. Code is written in Python 2.7

# Usage
In terminal, just run 'python parser1.py' where a prompt will ask you which llvm IR file to run. I provided two: examplels.ll (linear search) and exampleprime.ll (prime checker) Thus far, the parser will generate lines of 'boolean sentences' corresponding to the basic paths. (Each basic path is a sentence)

# TODO
I still need to provide the framework to run z3py for the basic paths, and tweak the parser to allow it to run the LLVM IR for fibonacci generator, where return value (rv) is not either true (1) or false (0).
