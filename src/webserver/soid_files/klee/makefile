cc=/tools/soid/soid/llvm-project/release/bin/clang -std=c99
opt=/tools/soid/soid/llvm-project/release/bin/opt
link=/tools/soid/soid/llvm-project/release/bin/llvm-link
BC1=./inter1.bc

BC2=./inter2.bc

BC3=./inter3.bc

BC=./inter.bc

KLEE=/tools/soid/soid/klee-float/include/klee
KEXEC=/tools/soid/soid/klee-float/build/bin/klee
PRE-LIB-KLEE=-L /tools/soid/soid/klee-float/build/lib/
POST-LIB-KLEE=-lkleeRuntest

SOIDLIB=/tools/soid/soid/soid/soidlib

symbolic:
	$(cc) -Dsymbolic -I $(SOIDLIB) -I $(KLEE) -emit-llvm -c -g -O0 /home/mje48/duckietown-soid/src/gym_duckietown/decision_logic/types.c -o - | $(opt) -mem2reg -simplifycfg -S -o $(BC1)
	$(cc) -Dsymbolic -I $(SOIDLIB) -I $(KLEE) -emit-llvm -c -g -O0 /home/mje48/duckietown-soid/src/gym_duckietown/decision_logic/decision_logic.c -o - | $(opt) -mem2reg -simplifycfg -S -o $(BC2)
	$(cc) -Dsymbolic -I $(SOIDLIB) -I $(KLEE) -emit-llvm -c -g -O0 ./klee_file.c -o - | $(opt) -mem2reg -simplifycfg -S -o $(BC3)
	$(link) $(BC1) $(BC2) $(BC3) -o $(BC) 
	$(KEXEC) -silent-klee-assume -write-smt2s -use-merge $(BC)

clean:
	rm -f ./inter1.bc
	rm -f ./inter2.bc
	rm -f ./inter3.bc
	rm -f ./inter.bc
