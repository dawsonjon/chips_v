.section .init
.global main
.global _start

_start:
	/* set stack pointer */
	//lui sp, %hi(1023)
	//addi sp, sp, %lo(1023)
	addi sp, zero, 1020

	/* call main */
	jal ra, main

	/* break */
_end:
	j _end	
