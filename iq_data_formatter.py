import numpy as np
from IEEE754_single import ieee754_hexStr_to_float
from matplotlib import pyplot as plt

with open("C:\\Users\\Admin\\Documents\\gnu_sources\\rrc_AXI_bpsk_out_synth.txt", 'r') as fi:
    read_str = fi.read().strip()
    hex_list = [x for x in read_str.split('\n')]
    i = [ieee754_hexStr_to_float(x.split(' ')[0]) for x in hex_list]
    q = [ieee754_hexStr_to_float(x.split(' ')[1]) for x in hex_list]
    i = np.array(i)
    q = np.array(q)


with open("C:\\Users\\Admin\\Documents\\gnu_sources\\rrc_AXI_bpsk_out_synth.bin", "wb") as fo:
    I_arr = np.array(i, dtype=np.float32)
    Q_arr = np.array(q, dtype=np.float32)
    IQ_arr = I_arr + Q_arr * 1j
    write_bytes = IQ_arr.tobytes()
    fo.write(write_bytes)

print(f"Number of samples:- {i.size}")
print(f"Hex list length:- {len(hex_list)}")

# fig = plt.figure(layout='tight')
# ax1 = fig.add_subplot(211)
# ax2 = fig.add_subplot(212)
# ax1.plot(i/(2**14))
# ax2.plot(q/(2**14))
# ax1.set_title('I-Data')
# ax2.set_title('Q-Data')
# plt.show()
