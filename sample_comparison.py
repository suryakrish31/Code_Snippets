import numpy as np
from IEEE754_single import float_to_ieee754
import struct


def samp_comp(file1, file2):
    with open(file1, 'rb') as f1:
        f1_buf = f1.read()
        print(f"f1_buf size:- {len(f1_buf)}")
        # f1_data = np.frombuffer(f1_buf, dtype=np.uint32)
        f1_data = [struct.unpack('<I', f1_buf[x:x+4])[0] for x in range(0,int(len(f1_buf)/4), 4)]
        # f1_data = f1_data[0::2]
        print(f"f1_data size:- {len(f1_data)}")
        print(f"Sample data of File-1:- {(f1_data[0]):08x}, {(f1_data[1]):08x}, {(f1_data[2]):08x}, {(f1_data[3]):08x}")

    with open(file2, 'rb') as f2:
        f2_buf = f2.read()
        print(f"f2_buf size:- {len(f2_buf)}")
        f2_data = [struct.unpack('<I', f2_buf[x:x+4])[0] for x in range(0, int(len(f1_buf)/4), 4)]
        #f2_data = f2_data[::2]
        print(f"f2_data size:- {len(f2_data)}")
        print(f"Sample data of File-2:- {(f2_data[0]):08x}, {(f2_data[1]):08x}, {(f2_data[2]):08x}, {(f2_data[3]):08x}")

    print("Word:\tf1_value:\tf2_value:\t")
    for i in range(min(len(f1_data), len(f2_data))):
        if i > 40000:
          break
        if (f1_data[i]>>16) & 0xffff != (f2_data[i]>>16) & 0xffff:
            print(f"{i}\t\t{f1_data[i]:08x}\t{f2_data[i]:08x}")


if __name__ == '__main__':
    file_path = r"C:\Users\Admin\Documents\gnu_sources\\"
    # file1 = file_path + "rrc_impl_qpsk_out_inv.bin"
   # file1 = file_path + "Mode1_Q_sample_50MHZ.bin"
    file2= file_path + "SDR_EM_FI_200MHZ_ps_200MHZ.bin"
    file1 = file_path + "SDR_Integration_Final.bin"
    # file2 = file_path + "rrc_verilog_bpsk_out_synth.bin"
    # file2 = file_path + "rrc_AXI_bpsk_out_synth.bin"
    # file2 = file_path + input(f"Enter the input IQ file; which is at path:- {file_path}\n").strip()
    samp_comp(file1, file2)

