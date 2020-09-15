#!/usr/bin/env python3

from distutils.core import Extension, setup

version = open("version").read()
long_description = open("README.md").read()

setup(name="Chips-V",
      version=version,
      description="Easy RISC-V SoC for FPGAs",
      long_description=long_description,

      author="Jon Dawson",
      author_email="chips@jondawson.org.uk",
      url="http://pyandchips.org",
      download_url="http://github.com/dawsonjon/Chips-V",
      keywords=["Verilog", "FPGA", "C", "HDL", "Synthesis", "RISC V", "Simulation"],
      classifiers = [
          "Programming Language :: Python",
          "License :: OSI Approved :: MIT License",
          "Operating System :: OS Independent",
          "Intended Audience :: Science/Research",
          "Intended Audience :: Developers",
          "Development Status :: 3 - Alpha",
          "Topic :: Scientific/Engineering :: Electronic Design Automation (EDA)",
          "Topic :: Software Development :: Embedded Systems",
          "Topic :: Software Development :: Code Generators",
      ],
      package_dir={
          "chips_v":"chips_v",
          "baremetal":"baremetal/baremetal"
      },
      packages=[
          "chips_v",
          "baremetal",
      ],
      package_data = {
          "chips_v":[
              "libs/*",
              "include/*",
          ],
      },
      scripts=[
          "c2verilog",
          "csim"
      ]
)
