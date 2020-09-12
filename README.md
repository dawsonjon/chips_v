# RISCV System on Chip Builder

This is a python utility to create System on Chip (SoC) HDL code. The SoC is based on a simple RISC-V RV32IM implemenation. The SoC uses block RAM for instruction and data memory and is ideally suited to FPGA implementation. 

The tool is written in baremetal, a simple Python library to create and simulate harware designs using a very low level of abstraction (gates/registers). Baremetal has a capability to output verilog for implementation in FPGA.
