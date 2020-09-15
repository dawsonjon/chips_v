# RISCV System on Chip Builder

This is a python utility to create System on Chip (SoC) HDL code. The SoC is based on a simple RISC-V RV32IM implementation. The SoC uses block RAM for instruction and data memory and is ideally suited to FPGA implementation. 

The tool is written in baremetal, a simple Python library to create and simulate hardware designs using a very low level of abstraction (gates/registers). Baremetal has a capability to output Verilog for implementation in FPGA.

Chips-V provides a convenience function `c2verilog` to go straight from C code to Verilog. The process take a C file as input, compiles to binary, embeds into a System on Chip with RISC-V rv32i CPU, and generates a single Verilog output.

```
c2verilog hello_world.v hello_world.c

```

A second convenience function `csim` can take the same C input, and run a simulation of the resulting system on chip.

```
csim hello_world.c

```

## Installation

### Install the Chips-V

The latest code can be obtained from [github](https://github.com/dawsonjon/chips_v).

To install:

``` bash

git clone --recursive https://github.com/dawsonjon/chips_v.git
cd chips-v
sudo python3 setup.py

```


### Install GNU Toolchain

Chips-V needs the riscv GNU toolchain, which may be obtained from
[github](https://github.com/riscv/riscv-gnu-toolchain). You can check there 
for the latest versions, instructions etc.

A script is provided to automate the installation process. Edit the
install_toolchain script to suite your system. Then run:

``` bash

./install_toolchain

```

