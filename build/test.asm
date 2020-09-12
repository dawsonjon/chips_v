
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
  7c:	7fc00113          	li	sp,2044
  80:	008000ef          	jal	ra,88 <_end>

00000084 <_end>:
  84:	0000006f          	j	84 <_end>

Disassembly of section .text.startup.main:

00000088 <main>:
  88:	14c02703          	lw	a4,332(zero) # 14c <stdout>
  8c:	bf010113          	addi	sp,sp,-1040
  90:	07800693          	li	a3,120
  94:	00d72023          	sw	a3,0(a4)
  98:	01010613          	addi	a2,sp,16
  9c:	21010693          	addi	a3,sp,528
  a0:	00000713          	li	a4,0
  a4:	14c00793          	li	a5,332
  a8:	00060893          	mv	a7,a2
  ac:	00068813          	mv	a6,a3
  b0:	04000593          	li	a1,64
  b4:	0007a503          	lw	a0,0(a5)
  b8:	03070313          	addi	t1,a4,48
  bc:	00e62023          	sw	a4,0(a2)
  c0:	00e6a023          	sw	a4,0(a3)
  c4:	00652023          	sw	t1,0(a0)
  c8:	00170713          	addi	a4,a4,1
  cc:	00460613          	addi	a2,a2,4
  d0:	00468693          	addi	a3,a3,4
  d4:	feb710e3          	bne	a4,a1,b4 <main+0x2c>
  d8:	0007a703          	lw	a4,0(a5)
  dc:	06100693          	li	a3,97
  e0:	10000613          	li	a2,256
  e4:	00d72023          	sw	a3,0(a4)
  e8:	80000737          	lui	a4,0x80000
  ec:	00072683          	lw	a3,0(a4) # 80000000 <stdout+0x7ffffeb4>
  f0:	0007a703          	lw	a4,0(a5)
  f4:	00d72023          	sw	a3,0(a4)
  f8:	00012623          	sw	zero,12(sp)
  fc:	00000713          	li	a4,0
 100:	00e886b3          	add	a3,a7,a4
 104:	00e80533          	add	a0,a6,a4
 108:	0006a683          	lw	a3,0(a3)
 10c:	00052503          	lw	a0,0(a0)
 110:	00c12583          	lw	a1,12(sp)
 114:	00470713          	addi	a4,a4,4
 118:	02a686b3          	mul	a3,a3,a0
 11c:	00b686b3          	add	a3,a3,a1
 120:	00d12623          	sw	a3,12(sp)
 124:	fcc71ee3          	bne	a4,a2,100 <main+0x78>
 128:	80000737          	lui	a4,0x80000
 12c:	00072683          	lw	a3,0(a4) # 80000000 <stdout+0x7ffffeb4>
 130:	0007a703          	lw	a4,0(a5)
 134:	00d72023          	sw	a3,0(a4)
 138:	0007a783          	lw	a5,0(a5)
 13c:	06200713          	li	a4,98
 140:	00e7a023          	sw	a4,0(a5)
 144:	41010113          	addi	sp,sp,1040
 148:	00008067          	ret
