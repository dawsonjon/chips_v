# RISCV System on Chip Builder

This is a python utility to create System on Chip (SoC) HDL code. The SoC is based on a simple RISC-V RV32IM implemenation. The SoC uses block RAM for instruction and data memory and is ideally suited to FPGA implementation. 

The tool is written in baremetal, a simple Python library to create and simulate harware designs using a very low level of abstraction (gates/registers). Baremetal has a capability to output verilog for implementation in FPGA.


Chips-V provides a convenience function `c2verilog` to go straight from C code to verilog. The process take a C file as input, compiles to binary, embeds into a System on Chip with RISC-V rv32i CPU, and gnerates a single verilog output.

```
c2verilog hello_world.v hello_world.c

```

A second convenience function `csim` can take the same C input, and run a simulation of the resulting system on chip.

```
csim hello_world.c

```
