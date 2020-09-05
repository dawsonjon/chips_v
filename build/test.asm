
test.elf:     file format elf32-littleriscv


Disassembly of section .text:

00000000 <_start>:
   0:	00004137          	lui	sp,0x4
   4:	00010113          	mv	sp,sp
   8:	008000ef          	jal	ra,10 <main>

0000000c <_end>:
   c:	0000006f          	j	c <_end>

00000010 <main>:
  10:	fd010113          	addi	sp,sp,-48 # 3fd0 <end+0x3bc3>
  14:	02812623          	sw	s0,44(sp)
  18:	03010413          	addi	s0,sp,48
  1c:	123457b7          	lui	a5,0x12345
  20:	67878793          	addi	a5,a5,1656 # 12345678 <end+0x1234526b>
  24:	fef42423          	sw	a5,-24(s0)
  28:	40000793          	li	a5,1024
  2c:	0007a603          	lw	a2,0(a5)
  30:	0047a683          	lw	a3,4(a5)
  34:	0087a703          	lw	a4,8(a5)
  38:	fcc42c23          	sw	a2,-40(s0)
  3c:	fcd42e23          	sw	a3,-36(s0)
  40:	fee42023          	sw	a4,-32(s0)
  44:	00c7c783          	lbu	a5,12(a5)
  48:	fef40223          	sb	a5,-28(s0)
  4c:	0240006f          	j	70 <main+0x60>
  50:	fec42783          	lw	a5,-20(s0)
  54:	00178713          	addi	a4,a5,1
  58:	fee42623          	sw	a4,-20(s0)
  5c:	ff040713          	addi	a4,s0,-16
  60:	00f707b3          	add	a5,a4,a5
  64:	fe87c703          	lbu	a4,-24(a5)
  68:	fe842783          	lw	a5,-24(s0)
  6c:	00e78023          	sb	a4,0(a5)
  70:	fec42783          	lw	a5,-20(s0)
  74:	ff040713          	addi	a4,s0,-16
  78:	00f707b3          	add	a5,a4,a5
  7c:	fe87c783          	lbu	a5,-24(a5)
  80:	fc0798e3          	bnez	a5,50 <main+0x40>
  84:	00000013          	nop
  88:	00000013          	nop
  8c:	02c12403          	lw	s0,44(sp)
  90:	03010113          	addi	sp,sp,48
  94:	00008067          	ret
