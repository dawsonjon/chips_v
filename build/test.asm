
test.elf:     file format elf32-littleriscv


Disassembly of section .text:

00000000 <_start>:
   0:	3fc00113          	li	sp,1020
   4:	008000ef          	jal	ra,c <main>

00000008 <_end>:
   8:	0000006f          	j	8 <_end>

0000000c <main>:
   c:	fd010113          	addi	sp,sp,-48
  10:	02812623          	sw	s0,44(sp)
  14:	03010413          	addi	s0,sp,48
  18:	123457b7          	lui	a5,0x12345
  1c:	67878793          	addi	a5,a5,1656 # 12345678 <end+0x123455d7>
  20:	fef42423          	sw	a5,-24(s0)
  24:	09400793          	li	a5,148
  28:	0007a603          	lw	a2,0(a5)
  2c:	0047a683          	lw	a3,4(a5)
  30:	0087a703          	lw	a4,8(a5)
  34:	fcc42c23          	sw	a2,-40(s0)
  38:	fcd42e23          	sw	a3,-36(s0)
  3c:	fee42023          	sw	a4,-32(s0)
  40:	00c7c783          	lbu	a5,12(a5)
  44:	fef40223          	sb	a5,-28(s0)
  48:	0240006f          	j	6c <main+0x60>
  4c:	fec42783          	lw	a5,-20(s0)
  50:	00178713          	addi	a4,a5,1
  54:	fee42623          	sw	a4,-20(s0)
  58:	ff040713          	addi	a4,s0,-16
  5c:	00f707b3          	add	a5,a4,a5
  60:	fe87c703          	lbu	a4,-24(a5)
  64:	fe842783          	lw	a5,-24(s0)
  68:	00e78023          	sb	a4,0(a5)
  6c:	fec42783          	lw	a5,-20(s0)
  70:	ff040713          	addi	a4,s0,-16
  74:	00f707b3          	add	a5,a4,a5
  78:	fe87c783          	lbu	a5,-24(a5)
  7c:	fc0798e3          	bnez	a5,4c <main+0x40>
  80:	00000013          	nop
  84:	00000013          	nop
  88:	02c12403          	lw	s0,44(sp)
  8c:	03010113          	addi	sp,sp,48
  90:	00008067          	ret
  94:	6568                	flw	fa0,76(a0)
  96:	6c6c                	flw	fa1,92(s0)
  98:	6f77206f          	j	72f8e <end+0x72eed>
  9c:	6c72                	flw	fs8,28(sp)
  9e:	2164                	fld	fs1,192(a0)
	...
