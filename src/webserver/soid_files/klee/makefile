cc=/tools/soid/soid/llvm-project/release/bin/clang -std=c99
opt=/tools/soid/soid/llvm-project/release/bin/opt
link=/tools/soid/soid/llvm-project/release/bin/llvm-link
BC=./inter.bc

KLEE=/tools/soid/soid/klee-float/include/klee
KEXEC=/tools/soid/soid/klee-float/build/bin/klee
PRE-LIB-KLEE=-L /tools/soid/soid/klee-float/build/lib/
POST-LIB-KLEE=-lkleeRuntest

SOIDLIB=/tools/soid/soid/soid/soidlib

symbolic:
	$(cc) -Dsymbolic -I $(SOIDLIB) -I $(KLEE) -emit-llvm -c -g -O0 ./klee_file.c -o $(BC)
	$(KEXEC) -silent-klee-assume -write-smt2s -use-merge $(BC)

#clean:
#	rm -f ./inter.bc
#	rm -rf ./klee-out-*
#	rm -rf ./klee-last
