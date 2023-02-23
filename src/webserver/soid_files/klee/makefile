BC1=./inter1.bc

BC2=./inter2.bc

BC3=./inter3.bc

BC=./inter.bc

symbolic:
	$(cc) -Dsymbolic -I $(SOIDLIB) -I $(KLEE) -emit-llvm -c -g -O0 ../../../gym_duckietown/decision_logic/types.c -o - | $(opt) -mem2reg -simplifycfg -S -o $(BC1)
	$(cc) -Dsymbolic -I $(SOIDLIB) -I $(KLEE) -emit-llvm -c -g -O0 ../../../gym_duckietown/decision_logic/decision_logic.c -o - | $(opt) -mem2reg -simplifycfg -S -o $(BC2)
	$(cc) -Dsymbolic -I $(SOIDLIB) -I $(KLEE) -emit-llvm -c -g -O0 ./klee_file.c -o - | $(opt) -mem2reg -simplifycfg -S -o $(BC3)
	$(link) $(BC1) $(BC2) $(BC3) -o $(BC) 
	$(KEXEC) -silent-klee-assume -write-smt2s -use-merge $(BC)

clean:
	rm -f ./inter1.bc
	rm -f ./inter2.bc
	rm -f ./inter3.bc
	rm -f ./inter.bc
	rm -rf ./klee-out-*
	rm -rf ./klee-last
