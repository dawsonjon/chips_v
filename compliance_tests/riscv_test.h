// See LICENSE for license details.

#ifndef _ENV_PHYSICAL_SINGLE_CORE_H
#define _ENV_PHYSICAL_SINGLE_CORE_H

#include "./encoding.h"

//-----------------------------------------------------------------------
// Begin Macro
//-----------------------------------------------------------------------

#define RVTEST_RV64U                                                    \
  .macro init;                                                          \
  .endm

#define RVTEST_RV64UF                                                   \
  .macro init;                                                          \
  RVTEST_FP_ENABLE;                                                     \
  .endm

#define RVTEST_RV32U                                                    \
  .macro init;                                                          \
  .endm

#define RVTEST_RV32UF                                                   \
  .macro init;                                                          \
  RVTEST_FP_ENABLE;                                                     \
  .endm

#define RVTEST_RV64M                                                    \
  .macro init;                                                          \
  RVTEST_ENABLE_MACHINE;                                                \
  .endm

#define RVTEST_RV64S                                                    \
  .macro init;                                                          \
  RVTEST_ENABLE_SUPERVISOR;                                             \
  .endm

#define RVTEST_RV32M                                                    \
  .macro init;                                                          \
  RVTEST_ENABLE_MACHINE;                                                \
  .endm

#define RVTEST_RV32S                                                    \
  .macro init;                                                          \
  RVTEST_ENABLE_SUPERVISOR;                                             \
  .endm

#if __riscv_xlen == 64
# define CHECK_XLEN li a0, 1; slli a0, a0, 31; bgez a0, 1f; RVTEST_PASS; 1:
#else
# define CHECK_XLEN li a0, 1; slli a0, a0, 31; bltz a0, 1f; RVTEST_PASS; 1:
#endif

#define INIT_PMP                                                        \
  la t0, 1f;                                                            \
  csrw mtvec, t0;                                                       \
  li t0, -1;        /* Set up a PMP to permit all accesses */           \
  csrw pmpaddr0, t0;                                                    \
  li t0, PMP_NAPOT | PMP_R | PMP_W | PMP_X;                             \
  csrw pmpcfg0, t0;                                                     \
  .align 2;                                                             \
1:

#define INIT_SPTBR                                                      \
  la t0, 1f;                                                            \
  csrw mtvec, t0;                                                       \
  csrwi sptbr, 0;                                                       \
  .align 2;                                                             \
1:

#define DELEGATE_NO_TRAPS                                               \
  la t0, 1f;                                                            \
  csrw mtvec, t0;                                                       \
  csrwi medeleg, 0;                                                     \
  csrwi mideleg, 0;                                                     \
  csrwi mie, 0;                                                         \
  .align 2;                                                             \
1:

#define RVTEST_ENABLE_SUPERVISOR                                        \
  li a0, MSTATUS_MPP & (MSTATUS_MPP >> 1);                              \
  csrs mstatus, a0;                                                     \
  li a0, SIP_SSIP | SIP_STIP;                                           \
  csrs mideleg, a0;                                                     \

#define RVTEST_ENABLE_MACHINE                                           \
  li a0, MSTATUS_MPP;                                                   \
  csrs mstatus, a0;                                                     \

#define RVTEST_FP_ENABLE                                                \
  li a0, MSTATUS_FS & (MSTATUS_FS >> 1);                                \
  csrs mstatus, a0;                                                     \
  csrwi fcsr, 0

#define RISCV_MULTICORE_DISABLE                                         \
  csrr a0, mhartid;                                                     \
  1: bnez a0, 1b

#define EXTRA_TVEC_USER
#define EXTRA_TVEC_MACHINE
#define EXTRA_INIT
#define EXTRA_INIT_TIMER

//
// undefine some unusable CSR Accesses if no PRIV Mode present
//
#if defined(PRIV_MISA_S)
#  if (PRIV_MISA_S==0)
#    undef  INIT_SPTBR
#    define INIT_SPTBR
#    undef  INIT_PMP
#    define INIT_PMP
#    undef  DELEGATE_NO_TRAPS
#    define DELEGATE_NO_TRAPS
#    undef  RVTEST_ENABLE_SUPERVISOR
#    define RVTEST_ENABLE_SUPERVISOR
#  endif
#endif
#if defined(PRIV_MISA_U)
#  if (PRIV_MISA_U==0)
#  endif
#endif
#if defined(TRAPHANDLER)
#include TRAPHANDLER
#endif

#define INTERRUPT_HANDLER j other_exception /* No interrupts should occur */

#define RVTEST_CODE_BEGIN                                               \
        .section .text.init;                                            \
        .align  6;                                                      \
        .weak stvec_handler;                                            \
        .weak mtvec_handler;                                            \
        .globl _start;                                                  \
_start:                                                                 \
        /* reset vector */                                              \
        j reset_vector;                                                 \
        .align 2;                                                       \
reset_vector:                                                           \
	li x1, 0;                                                       \
	li x2, 0;                                                       \
	li x3, 0;                                                       \
	li x4, 0;                                                       \
	li x5, 0;                                                       \
	li x6, 0;                                                       \
	li x7, 0;                                                       \
	li x8, 0;                                                       \
	li x9, 0;                                                       \
	li x10, 0;                                                       \
	li x11, 0;                                                       \
	li x12, 0;                                                       \
	li x13, 0;                                                       \
	li x14, 0;                                                       \
	li x15, 0;                                                       \
	li x16, 0;                                                       \
	li x17, 0;                                                       \
	li x18, 0;                                                       \
	li x19, 0;                                                       \
	li x20, 0;                                                       \
	li x21, 0;                                                       \
	li x22, 0;                                                       \
	li x23, 0;                                                       \
	li x24, 0;                                                       \
	li x25, 0;                                                       \
	li x26, 0;                                                       \
	li x27, 0;                                                       \
	li x28, 0;                                                       \
	li x29, 0;                                                       \
	li x30, 0;                                                       \
	li x31, 0;                                                       \
begin_testcode:                                                          \


//-----------------------------------------------------------------------
// End Macro
//-----------------------------------------------------------------------

#define RVTEST_CODE_END                                                 \
pass:                                                                   \
	li x1, 0x03000000;                                              \
        li x2, 0x0000600D;                                              \
	sw x2, 0(x1);                                                   \
        j end_testcode;                                                 \
fail:                                                                   \
	li x1, 0x03000000;                                              \
        li x2, 0x00000BAD;                                              \
	sw x2, 0(x1);                                                   \
end_testcode:                                                           \
        j end_testcode;

//-----------------------------------------------------------------------
// Pass/Fail Macro
//-----------------------------------------------------------------------
#define RVTEST_SYNC fence
//#define RVTEST_SYNC nop

#define RVTEST_PASS                                                     \
	j pass;

#define TESTNUM gp
#define RVTEST_FAIL                                                     \
        j fail;

//-----------------------------------------------------------------------
// Data Section Macro
//-----------------------------------------------------------------------

#define EXTRA_DATA

#define RVTEST_DATA_BEGIN

#define RVTEST_DATA_END                                                 

#endif
