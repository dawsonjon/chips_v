![build status](https://travis-ci.org/dawsonjon/chips_v.svg?branch=master)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)

# RISC-V System on Chip Builder

> The easy way to embed software in your FPGA project

Chips-V is easy to use. The `c2verilog` tool works like a compiler, pass in you C code and c2verilog will generate a single verilog file that you can drop into your FPGA design using your usual toolchain. 

```
c2verilog hello_world.v hello_world.c

```

Behind the scenes, this Python utility creates System on Chip (SoC) based on on a simple RISC-V RV32I(M) implementation. The SoC has a small footprint, ideally suited to FPGA implementation. The source code is compiled using the RISC-V port of the GNU toolchain, and is embedded into block-RAMS in the verilog file. A customised libc implementation provides a light-weight libc implementation ideally suited to targets with small RAMs. 


## Installation

### Install the Chips-V

The latest code can be obtained from [github](https://github.com/dawsonjon/chips_v).

To install:

``` bash

$ git clone --recursive https://github.com/dawsonjon/chips_v.git
$ cd chips_v
$ sudo python3 setup.py

```


### Install GNU Toolchain

Chips-V needs the riscv GNU toolchain, which may be obtained from
[github](https://github.com/riscv/riscv-gnu-toolchain). You can check there 
for the latest versions, instructions etc.

A script is provided to automate the installation process. Edit the
install_toolchain script to suite your system. Then run:

``` bash

$ ./install_toolchain

```
