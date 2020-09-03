
test.elf:     file format elf32-littleriscv


Disassembly of section .text:

00000000 <_start>:
   0:	00004137          	lui	sp,0x4
   4:	00010113          	mv	sp,sp
   8:	008000ef          	jal	ra,10 <end>

0000000c <_end>:
   c:	0000006f          	j	c <_end>

Disassembly of section .text.startup:

00000010 <main>:
  10:	00002023          	sw	zero,0(zero) # 0 <_start>
  14:	00400713          	li	a4,4
  18:	00100793          	li	a5,1
  1c:	00f72023          	sw	a5,0(a4)
  20:	00200693          	li	a3,2
  24:	00800793          	li	a5,8
  28:	00d7a023          	sw	a3,0(a5)
  2c:	00e02823          	sw	a4,16(zero) # 10 <main>
  30:	00500713          	li	a4,5
  34:	00e02a23          	sw	a4,20(zero) # 14 <main+0x4>
  38:	00600713          	li	a4,6
  3c:	00300693          	li	a3,3
  40:	00e02c23          	sw	a4,24(zero) # 18 <main+0x8>
  44:	02f02023          	sw	a5,32(zero) # 20 <main+0x10>
  48:	00700713          	li	a4,7
  4c:	00900793          	li	a5,9
  50:	00d02623          	sw	a3,12(zero) # c <_end>
  54:	00e02e23          	sw	a4,28(zero) # 1c <main+0xc>
  58:	02f02223          	sw	a5,36(zero) # 24 <main+0x14>
  5c:	02400513          	li	a0,36
  60:	00008067          	ret
