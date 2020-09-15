number_of_runs = 10
clock_frequency_MHz = 100e6
number_of_clocks = 3178 #with compiler optimisation set to O3

seconds = number_of_clocks/clock_frequency_MHz
dhrystones_per_second = number_of_runs/seconds
dhrystone_mips = dhrystones_per_second/1757 #speed of VAX 11/780

print ("dhrystone MIPS", dhrystone_mips)
