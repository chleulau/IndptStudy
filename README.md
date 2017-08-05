# Introduction
Independent study in learning about program verification
This repository is used for providing code and data for a general-purpose program verifier. Code is written in Python 2.7

## Usage
In terminal, just run 'python parser.py' where a prompt will ask you which llvm IR file to run. I provided three: examplels.ll (linear search), exampleprime.ll (prime checker), and examplefib.ll (Fibonacci generator). Thus far, the parser will generate lines of 'boolean sentences' corresponding to the basic paths. (Each basic path is a sentence)

### Update (8/5/17)
It will now also generate the z3-friendly eval paths (except for arrays like a[i]) for a provided supply file, (specifically the first line consists of pre-condition, second line the loop invariant, and third line the post-condition) 

## TODO
* Provide the framework to run z3py for the basic paths
* Tweak the parser to allow it to run the LLVM IR for fibonacci generator, where return value (rv) is not either true (1) or false (0). 
* I also need to add more comments to parser.py.
* I also need to allow the parser to handle arrays (Using theory of arrays)
