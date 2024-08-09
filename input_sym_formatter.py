import numpy as np

def bitstring_to_bytes(s):
    return int(s, 2).to_bytes(len(s) // 8, byteorder='big')
    
with open(r"D:\Vivado_Workarea\rrc_filter\rrc_filter.sim\sim_3\behav\xsim\input_sym.txt", 'r') as fi:
    read_list = fi.readlines
    bitstring_list = []
    

with open(r"input_sym.bin", "wb") as fo:
    write_bytes = [bitstring_to_bytes(s) for s in read_list]
    for i in write_bytes:
        fo.write(i)

print(f"Number of samples:- {len(read_list)}")