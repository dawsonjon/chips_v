
test.elf:     file format elf32-littleriscv


Disassembly of section .text:

00000000 <_start>:
   0:	00000093          	li	ra,0
   4:	00000113          	li	sp,0
   8:	00000193          	li	gp,0
   c:	00000213          	li	tp,0
  10:	00000293          	li	t0,0
  14:	00000313          	li	t1,0
  18:	00000393          	li	t2,0
  1c:	00000413          	li	s0,0
  20:	00000493          	li	s1,0
  24:	00000513          	li	a0,0
  28:	00000593          	li	a1,0
  2c:	00000613          	li	a2,0
  30:	00000693          	li	a3,0
  34:	00000713          	li	a4,0
  38:	00000793          	li	a5,0
  3c:	00000813          	li	a6,0
  40:	00000893          	li	a7,0
  44:	00000913          	li	s2,0
  48:	00000993          	li	s3,0
  4c:	00000a13          	li	s4,0
  50:	00000a93          	li	s5,0
  54:	00000b13          	li	s6,0
  58:	00000b93          	li	s7,0
  5c:	00000c13          	li	s8,0
  60:	00000c93          	li	s9,0
  64:	00000d13          	li	s10,0
  68:	00000d93          	li	s11,0
  6c:	00000e13          	li	t3,0
  70:	00000e93          	li	t4,0
  74:	00000f13          	li	t5,0
  78:	00000f93          	li	t6,0
  7c:	3fc00113          	li	sp,1020
  80:	08c000ef          	jal	ra,10c <main>

00000084 <_end>:
  84:	0000006f          	j	84 <_end>

Disassembly of section .text.fprint_udecimal_full:

00000088 <fprint_udecimal_full>:
  88:	3b9ad7b7          	lui	a5,0x3b9ad
  8c:	00a00813          	li	a6,10
  90:	00000893          	li	a7,0
  94:	a0078793          	addi	a5,a5,-1536 # 3b9aca00 <stdout+0x3b9ac8a4>
  98:	00a00313          	li	t1,10
  9c:	02f55733          	divu	a4,a0,a5
  a0:	0ff77e13          	andi	t3,a4,255
  a4:	000e1463          	bnez	t3,ac <fprint_udecimal_full+0x24>
  a8:	02088463          	beqz	a7,d0 <fprint_udecimal_full+0x48>
  ac:	0ff77713          	andi	a4,a4,255
  b0:	03070713          	addi	a4,a4,48
  b4:	00e6a023          	sw	a4,0(a3)
  b8:	00100893          	li	a7,1
  bc:	fff80813          	addi	a6,a6,-1
  c0:	02f57533          	remu	a0,a0,a5
  c4:	0267d7b3          	divu	a5,a5,t1
  c8:	fc081ae3          	bnez	a6,9c <fprint_udecimal_full+0x14>
  cc:	00008067          	ret
  d0:	ff05e6e3          	bltu	a1,a6,bc <fprint_udecimal_full+0x34>
  d4:	00c6a023          	sw	a2,0(a3)
  d8:	fe5ff06f          	j	bc <fprint_udecimal_full+0x34>

Disassembly of section .text.fprint_udecimal:

000000dc <fprint_udecimal>:
  dc:	00058693          	mv	a3,a1
  e0:	02000613          	li	a2,32
  e4:	00000593          	li	a1,0
  e8:	fa1ff06f          	j	88 <fprint_udecimal_full>

Disassembly of section .text.fprint_decimal:

000000ec <fprint_decimal>:
  ec:	00054463          	bltz	a0,f4 <fprint_decimal+0x8>
  f0:	fedff06f          	j	dc <fprint_udecimal>
  f4:	02d00693          	li	a3,45
  f8:	00d5a023          	sw	a3,0(a1)
  fc:	40a00533          	neg	a0,a0
 100:	ff1ff06f          	j	f0 <fprint_decimal+0x4>

Disassembly of section .text.print_decimal:

00000104 <print_decimal>:
 104:	15c02583          	lw	a1,348(zero) # 15c <stdout>
 108:	fe5ff06f          	j	ec <fprint_decimal>

Disassembly of section .text.startup.main:

0000010c <main>:
 10c:	ff010113          	addi	sp,sp,-16
 110:	00812423          	sw	s0,8(sp)
 114:	00912223          	sw	s1,4(sp)
 118:	15c00413          	li	s0,348
 11c:	800004b7          	lui	s1,0x80000
 120:	0004a703          	lw	a4,0(s1) # 80000000 <stdout+0x7ffffea4>
 124:	00042783          	lw	a5,0(s0)
 128:	00112623          	sw	ra,12(sp)
 12c:	00003537          	lui	a0,0x3
 130:	00e7a023          	sw	a4,0(a5)
 134:	03950513          	addi	a0,a0,57 # 3039 <stdout+0x2edd>
 138:	fcdff0ef          	jal	ra,104 <print_decimal>
 13c:	0004a703          	lw	a4,0(s1)
 140:	00042783          	lw	a5,0(s0)
 144:	00c12083          	lw	ra,12(sp)
 148:	00812403          	lw	s0,8(sp)
 14c:	00e7a023          	sw	a4,0(a5)
 150:	00412483          	lw	s1,4(sp)
 154:	01010113          	addi	sp,sp,16
 158:	00008067          	ret
