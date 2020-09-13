import runpy
import os

def generate_header(spec_path):
    settings = runpy.run_path(spec_path)

    address = 0x80000008
    header = ["//Auto Generated Machine Description Header\n"]
    header = ["const unsigned int CLOCKS_PER_SEC = %u;\n"%settings["clocks_per_sec"]]

    #Add memory locations of outputs
    for output in settings["outputs"]:
        header.append("const unsigned int %s = 0x%x;\n"%(output, address));
        address += 4

    #Add memory locations of inputs
    for output in settings["inputs"]:
        header.append("const unsigned int %s = 0x%x;\n"%(output, address));
        address += 4

    directory = os.path.abspath(__file__)
    directory = os.path.dirname(directory)
    machine_h = os.path.join(directory, "include", "machine.h")
    with open(machine_h, "w") as f:
        f.write("".join(header))


generate_header("spec.py")
