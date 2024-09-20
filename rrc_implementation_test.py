import numpy as np
from matplotlib import pyplot as plt
from srrcDesign import srrcDesign
from numpy import fft
from float_to_Q31 import float_to_q31
from float_to_Q15 import float_to_q15
import random


def bytes_to_bitarray(bytes_sequence):
    return [int(b) for byte in bytes_sequence for b in f"{byte:08b}"]


def rrc_filtering(taps, I, Q, mod_type):
    num_delay = taps.size - 1
    num_taps = int(((taps.size - 1) / 2 + 1))
    counter = 0

    # Buffer - taps-1
    buff_I = np.zeros(taps.size - 1, dtype=np.float32)
    buff_Q = np.zeros(taps.size - 1, dtype=np.float32)

    # Declare empty add, mult and acc arrays
    add_I = np.zeros(num_taps - 1, dtype=np.float32)
    mul_I = np.zeros(num_taps, dtype=np.float32)
    acc_I = np.zeros(num_taps - 1, dtype=np.float32)
    I_list = []

    # Core Logic - I:-
    for inp in I:
        # Pre-Multiplication Addition:-
        for i in range(num_taps - 1):
            if i == 0:
                add_I[i] = inp + buff_I[num_delay - 1 - i]
            else:
                add_I[i] = buff_I[i - 1] + buff_I[num_delay - 1 - i]
        # Multiplication:-
        for i in range(num_taps):
            if i != num_taps - 1:
                mul_I[i] = taps[i] * add_I[i]
            else:
                mul_I[i] = taps[i] * buff_I[i]
        # Accumulation:-
        # New Architecture:-
        for i in range(16):
            acc_I[i] = mul_I[2*i] + mul_I[2*i + 1]
        for i in range(8):
            acc_I[i+16] = acc_I[2 * i] + acc_I[2 * i + 1]
        for i in range(4):
            acc_I[i+16+8] = acc_I[2 * i + 16] + acc_I[2 * i + 16 + 1]
        for i in range(2):
            acc_I[i + 16 + 8 + 4] = acc_I[2 * i + 16 + 8] + acc_I[2 * i + 16 + 8 + 1]
        acc_I[16 + 8 + 4 + 2] = acc_I[16 + 8 + 4] + acc_I[16 + 8 + 4 + 1]
        acc_I[num_taps-2] = acc_I[16 + 8 + 4 + 2] + mul_I[num_taps-1]

        # Old Architecture:-
        # for i in range(num_taps - 1):
        #     if i == 0:
        #         acc_I[i] = mul_I[i] + mul_I[i + 1]
        #     else:
        #         acc_I[i] = acc_I[i - 1] + mul_I[i + 1]
        I_list += [acc_I[num_taps - 2]]
        # if(counter > 2048):
        #     break
        # counter += 1
        # Buffer the input:-
        for i in range(len(buff_I) - 1, -1, -1):
            if i != 0:
                buff_I[i] = buff_I[i - 1]
            else:
                buff_I[i] = inp

    add_Q = np.zeros(num_taps - 1, dtype=np.float32)
    mul_Q = np.zeros(num_taps, dtype=np.float32)
    acc_Q = np.zeros(num_taps - 1, dtype=np.float32)
    Q_list = []

    if mod_type != 0:
        # Core Logic - Q:-
        for inp in Q:
            # Pre-Multiplication Addition:-
            for i in range(num_taps - 1):
                if i == 0:
                    add_Q[i] = inp + buff_Q[num_delay - 1 - i]
                else:
                    add_Q[i] = buff_Q[i - 1] + buff_Q[num_delay - 1 - i]
            # Multiplication:-
            for i in range(num_taps):
                if i != num_taps - 1:
                    mul_Q[i] = taps[i] * add_Q[i]
                else:
                    mul_Q[i] = taps[i] * buff_Q[i]
            # Accumulation:-
            # New Architecture:-
            for i in range(16):
                acc_Q[i] = mul_Q[2 * i] + mul_Q[2 * i + 1]
            for i in range(8):
                acc_Q[i + 16] = acc_Q[2 * i] + acc_Q[2 * i + 1]
            for i in range(4):
                acc_Q[i + 16 + 8] = acc_Q[2 * i + 16] + acc_Q[2 * i + 16 + 1]
            for i in range(2):
                acc_Q[i + 16 + 8 + 4] = acc_Q[2 * i + 16 + 8] + acc_Q[2 * i + 16 + 8 + 1]
            acc_Q[16 + 8 + 4 + 2] = acc_Q[16 + 8 + 4] + acc_Q[16 + 8 + 4 + 1]
            acc_Q[num_taps - 2] = acc_Q[16 + 8 + 4 + 2] + mul_Q[num_taps - 1]

            # Old Architecture:-
            # for i in range(num_taps - 1):
            #     if i == 0:
            #         acc_Q[i] = mul_Q[i] + mul_Q[i + 1]
            #     else:
            #         acc_Q[i] = acc_Q[i - 1] + mul_Q[i + 1]
            Q_list += [acc_Q[num_taps - 2]]
            if len(Q_list) >= 4094:
                pass
            # Buffer the input:-
            for i in range(len(buff_Q) - 1, -1, -1):
                if i != 0:
                    buff_Q[i] = buff_Q[i - 1]
                else:
                    buff_Q[i] = inp
    else:
        Q_list = [0]*len(I_list)

    return I_list, Q_list


def rrc_imp(mod_type, const_sel, sps, taps, in_IQ_file, out_IQ_file, out_IQ_gay_file, filter_times, mod_IQ_file):
    num_delay = taps.size-1
    num_taps = int(((taps.size-1)/2 + 1))
    const_sel = 0
    print(f"Selected Constellation Model No :- {const_sel}")
    print(f"num_delay={num_delay}\tnum_taps={num_taps}")
    
    # Read I and Q from input IQ file
    with open(in_IQ_file, "rb") as fi:
        in_IQ_bytes = fi.read()
        print(f"Total bytes read:- {len(in_IQ_bytes)}")
    if mod_type == 2 and len(in_IQ_bytes) % 3 != 0:
        print("Total number of bytes is not a multiple of 3")
        print(f"No of padding bytes:- {(3 - len(in_IQ_bytes) % 3)}")
        in_IQ_bytes += b'\x00' * (3 - len(in_IQ_bytes) % 3)
    input_uint8 = np.array(bytes_to_bitarray(in_IQ_bytes), dtype=np.uint8)

    # Modulation:- 0-BPSK, 1-QPSK, 2-8PSK
    if mod_type == 0:
        mod = lambda b: -1 if b == 0 else 1
        in_Q = np.zeros(input_uint8.size, dtype=np.float32)
        in_I = np.array([mod(input_uint8[x]) for x in range(input_uint8.size)])
    elif mod_type == 1:
        mod = lambda b: 1/np.sqrt(2) if b==0 else -1/np.sqrt(2)
        in_I = np.array([mod(input_uint8[x]) for x in range(input_uint8.size) if x % 2 == 0])
        in_Q = np.array([mod(input_uint8[x]) for x in range(input_uint8.size) if x % 2 == 1])
    elif mod_type == 2:
        sym_str = lambda x: ''.join(str(i) for i in x)
        sym_dict0 = {'000': (1, 0),
                     '100': (0.707, 0.707),
                     '101': (0, 1),
                     '001': (-0.707, 0.707),
                     '011': (-1, 0),
                     '111': (-0.707, -0.707),
                     '110': (0, -1),
                     '010': (0.707, -0.707)
                     }
        sym_dict1 = {'000': (0.92, 0.38),
                     '100': (0.38, 0.92),
                     '101': (-0.38, 0.92),
                     '001': (-0.92, 0.38),
                     '011': (-0.92, -0.38),
                     '111': (-0.38, -0.92),
                     '110': (0.38, -0.92),
                     '010': (0.92, -0.38)
                     }

        sym = [sym_str(input_uint8[i:i + 3]) for i in range(0, input_uint8.size, 3)]
        in_I = []
        in_Q = []
        for s in sym:
            if const_sel == 0:
                in_I += [sym_dict0[s][0]]
                in_Q += [sym_dict0[s][1]]
            elif const_sel == 1:
                in_I += [sym_dict1[s][0]]
                in_Q += [sym_dict1[s][1]]

    else:
        print("Mod Type not in the list: [0,1,2].\nPlease enter the correct mod type.")
        print("0 - BPSK\n1 - QPSK\n2 - 8PSK")

    # Repeat Symbols - sps times
    in_I = np.repeat(in_I, sps)
    in_Q = np.repeat(in_Q, sps)
    # return in_I + 1j*in_Q

    with open(mod_IQ_file, 'wb') as f1:
        temp_i = np.array(in_I, dtype=np.float32)
        temp_q = np.array(in_Q, dtype=np.float32)
        temp_iq = temp_i + 1j*temp_q
        f1.write(temp_iq.tobytes())

    print(f"Length of I:- {in_I.size}\nLength of Q:- {in_Q.size}\n")
    # Filter n times
    I, Q = rrc_filtering(taps, in_I, in_Q, mod_type)
    if filter_times > 1:
        for i in range(filter_times-1):
            I, Q = rrc_filtering(taps, I, Q, mod_type)

    # Format output I and Q
    out_I = np.array(I, dtype=np.float32)
    out_Q = np.array(Q, dtype=np.float32)
    out_I_1 = np.array([float_to_q15(x) for x in out_I], dtype=np.int16)
    out_Q_1 = np.array([float_to_q15(x) for x in out_Q], dtype=np.int16)
    out_IQ = out_I + 1j * out_Q
    # out_IQ = out_Q + 1j * out_I #for debug. To be removed.
    out_IQ_gay = np.array([(out_I_1[i]<<16)|out_Q_1[i] for i in range(len(out_I_1))],dtype=np.int32)
    # out_IQ_gay = out_I_1 << 16 | out_Q_1
    # np.savetxt(out_IQ_gay_file,out_IQ_gay & 0xFFFFFFFF, fmt='0x%08x', delimiter=',', newline=',\n')

    # # write I and Q to output IQ file
    with open(out_IQ_file, 'wb') as fo:
        fo.write(out_IQ.tobytes())
    
    # Return the IQ values
    return out_IQ, 1


if __name__ == '__main__':
    # Constants
    file_path = r"C:\Users\Admin\Documents\gnu_sources\\"
    out_IQ_file = file_path + 'rrc_impl_8psk_out.bin'
    out_IQ_gay_file = 'gayatri_bpsk.txt'
    mod_IQ_file = file_path + 'mod_psk_iq.bin'

    # User Input
    in_IQ_file = file_path + input(f"Enter the input IQ file; which is at path:- {file_path}\n").strip()
    mod_type = int(input("Enter Modulation Type:\n\t0 - BPSK\n\t1 - QPSK\n\t2 - 8PSK\n").strip())
    # const_sel = int(input("Enter Modulation Model No:\n").strip())
    const_sel = 1
    SPS = int(input("Enter SPS (Samples per Symbol):\n").strip())
    span = int(input("Enter the span of the filter:\n").strip())
    beta = float(input("Enter the rolling factor (beta):\n").strip())
    filter_times = int(input("Enter the number of times to filter:\n").strip())

    # # Generate Random numbers between 0 and 1 and write into in_IQ_file
    # in_bytes = b''
    # for i in range(2000):
    #     # in_bytes += random.getrandbits(1).to_bytes()
    #     in_bytes += random.randrange(0,1000).to_bytes(2, byteorder='little')
    # with open(in_IQ_file, 'wb') as fi:
    #     fi.write(in_bytes)

    # Call the logic core
    taps = srrcDesign(SPS, span, beta)
    # taps = np.fromfile('rct_coeffs.txt', sep=' ')
    print(f"Number of rrc Taps:- {taps.size}\n")
    out_IQ, valid_token = rrc_imp(mod_type, const_sel, SPS, taps, in_IQ_file, out_IQ_file, out_IQ_gay_file, filter_times, mod_IQ_file)

    if valid_token != 0:
        # Separate I and Q
        I = np.real(out_IQ)
        Q = np.imag(out_IQ)

        # Plot the impulse and frequency response
        fs = 1e6
        Ts = 1/fs
        N = 1024
        f = fft.fftfreq(N, Ts)
        f = fft.fftshift(f)
        t = np.arange(-span*SPS, span*SPS+1)
        taps_fft = fft.fftshift(fft.fft(out_IQ, n=N)*(1/N))
        taps_db = 20 * np.log10(np.abs(taps_fft))

        fig = plt.figure(layout='tight')
        ax1 = fig.add_subplot(311)
        ax2 = fig.add_subplot(312)
        ax3 = fig.add_subplot(313)
        ax1.set_title('Impulse response of RRC')
        ax2.set_title('Filter response')
        ax3.set_title('Frequency response of RRC')
        ax1.plot(t, taps, '-b', marker='*')
        ax2.plot(I, '-b', label='I', linewidth=0.5)
        ax2.plot(Q, '-r', label='Q', linewidth=0.5)
        ax3.plot(f, taps_db, '-r')
        ax1.set_xticks(t[::5])
        ax1.grid()
        ax2.grid()
        ax3.grid()
        ax2.legend()
        plt.show()