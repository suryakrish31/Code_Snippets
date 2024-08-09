import numpy as np
from matplotlib import pyplot as plt
from srrcDesign import srrcDesign
from numpy import fft


def bytes_to_bitarray(bytes_sequence):
    return [int(b) for byte in bytes_sequence for b in f"{byte:08b}"]


def rrc_filtering(taps, I, Q, mod_type):
    num_delay = taps.size - 1
    num_taps = int(((taps.size - 1) / 2 + 1))

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
        for i in range(num_taps - 1):
            if i == 0:
                acc_I[i] = mul_I[i] + mul_I[i + 1]
            else:
                acc_I[i] = acc_I[i - 1] + mul_I[i + 1]
        I_list += [acc_I[num_taps - 2]]
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
            for i in range(num_taps - 1):
                if i == 0:
                    acc_Q[i] = mul_Q[i] + mul_Q[i + 1]
                else:
                    acc_Q[i] = acc_Q[i - 1] + mul_Q[i + 1]
            Q_list += [acc_Q[num_taps - 2]]
            # Buffer the input:-
            for i in range(len(buff_Q) - 1, -1, -1):
                if i != 0:
                    buff_Q[i] = buff_Q[i - 1]
                else:
                    buff_Q[i] = inp

    return I_list, Q_list


def rrc_imp(mod_type, sps, taps, in_IQ_file, out_IQ_file, filter_times):
    num_delay = taps.size-1
    num_taps = int(((taps.size-1)/2 + 1))
    print(f"num_delay={num_delay}\tnum_taps={num_taps}")
    
    # Read I and Q from input IQ file
    if mod_type != 2:
        with open(in_IQ_file, "rb") as fi:
            in_IQ_bytes = fi.read()
            print(f"Total bytes read:- {len(in_IQ_bytes)}")
        input_uint8 = np.array(bytes_to_bitarray(in_IQ_bytes), dtype=np.uint8)
    else:
        f_I = in_IQ_file[0]
        f_Q = in_IQ_file[1]
        f_Z = in_IQ_file[2]
        with open(f_I, "rb") as fi:
            in_I_bytes = fi.read()
            print(f"Total I bytes read:- {len(in_I_bytes)}")
        with open(f_Q, "rb") as fi:
            in_Q_bytes = fi.read()
            print(f"Total Q bytes read:- {len(in_Q_bytes)}")
        with open(f_Z, "rb") as fi:
            in_Z_bytes = fi.read()
            print(f"Total Z bytes read:- {len(in_Z_bytes)}")
        if len(in_I_bytes) % 3 != 0:
            print("Total number of I bytes is not a multiple of 3")
            print(f"No of padding bytes:- {(3 - len(in_I_bytes) % 3)}")
            in_I_bytes += b'\x00' * (3 - len(in_I_bytes) % 3)
        if len(in_Q_bytes) % 3 != 0:
            print("Total number of Q bytes is not a multiple of 3")
            print(f"No of padding bytes:- {(3 - len(in_Q_bytes) % 3)}")
            in_Q_bytes += b'\x00' * (3 - len(in_Q_bytes) % 3)
        if len(in_Z_bytes) % 3 != 0:
            print("Total number of Z bytes is not a multiple of 3")
            print(f"No of padding bytes:- {(3 - len(in_Z_bytes) % 3)}")
            in_Z_bytes += b'\x00' * (3 - len(in_Z_bytes) % 3)
        input_I_uint8 = np.array(bytes_to_bitarray(in_I_bytes), dtype=np.uint8)
        input_Q_uint8 = np.array(bytes_to_bitarray(in_Q_bytes), dtype=np.uint8)
        input_Z_uint8 = np.array(bytes_to_bitarray(in_Z_bytes), dtype=np.uint8)

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
        sym_str = lambda i,q,z: str(i) + str(q) + str(z)
        sym = [sym_str(input_I_uint8[k], input_Q_uint8[k], input_Z_uint8[k])
               for k in range(min(input_I_uint8.size, input_Q_uint8.size, input_Z_uint8.size))]
        in_I = []
        in_Q = []
        for s in sym:
            if s == '000':
                in_I += [1 / np.sqrt(2)]
                in_Q += [1 / np.sqrt(2)]
            elif s == '001':
                in_I += [0]
                in_Q += [1 / np.sqrt(2)]
            elif s == '011':
                in_I += [-1 / np.sqrt(2)]
                in_Q += [1 / np.sqrt(2)]
            elif s == '010':
                in_I += [-1 / np.sqrt(2)]
                in_Q += [0]
            elif s == '110':
                in_I += [-1 / np.sqrt(2)]
                in_Q += [-1 / np.sqrt(2)]
            elif s == '111':
                in_I += [0]
                in_Q += [-1 / np.sqrt(2)]
            elif s == '101':
                in_I += [1 / np.sqrt(2)]
                in_Q += [-1 / np.sqrt(2)]
            elif s == '100':
                in_I += [1 / np.sqrt(2)]
                in_Q += [0]
            else:
                print(f"Nani??? There is another hidden combination?\t\t{s}")

    # Repeat Symbols - sps times
    in_I = np.repeat(in_I, sps)
    in_Q = np.repeat(in_Q, sps)
    # return in_I + 1j*in_Q

    print(f"Length of I:- {in_I.size}\nLength of Q:- {in_Q.size}\n")
    # Filter n times
    I, Q = rrc_filtering(taps, in_I, in_Q, mod_type)
    if filter_times > 1:
        for i in range(filter_times-1):
            I, Q = rrc_filtering(taps, I, Q, mod_type)

    # Format output I and Q
    out_I = np.array(I, dtype=np.float32)
    out_Q = np.array(Q, dtype=np.float32)
    out_IQ = out_I + 1j * out_Q
    
    # Read I and Q from input IQ file
    with open(out_IQ_file, 'wb') as fo:
        fo.write(out_IQ.tobytes())
    
    # Return the IQ values
    return out_IQ, 1


if __name__ == '__main__':
    # Constants
    file_path = r"C:\Users\Admin\Documents\gnu_sources\\"
    out_IQ_file = file_path + 'out.bin'

    # User Input
    mod_type = int(input("Enter Modulation Type:\n\t0 - BPSK\n\t1 - QPSK\n\t2 - 8PSK\n").strip())
    if mod_type not in [0, 1, 2]:
        print("Mod Type not in the list: [0,1,2].\nPlease enter the correct mod type.")
        print("0 - BPSK\n1 - QPSK\n2 - 8PSK")
    if mod_type == 2:
        file_I = file_path + input("Enter the input I file including path:-\n").strip()
        file_Q = file_path + input("Enter the input Q file including path:-\n").strip()
        file_Z = file_path + input("Enter the input Z file including path:-\n").strip()
        in_IQ_file = [file_I, file_Q, file_Z]
    else:
        in_IQ_file = file_path + input("Enter the input IQ file including path:-\n").strip()
    SPS = int(input("Enter SPS (Samples per Symbol):\n").strip())
    span = int(input("Enter the span of the filter:\n").strip())
    beta = float(input("Enter the rolling factor (beta):\n").strip())
    filter_times = int(input("Enter the number of times to filter:\n").strip())

    # Call the logic core
    taps = srrcDesign(SPS, span, beta)
    # taps = np.fromfile('rct_coeffs.txt', sep=' ')
    print(f"Number of rrc Taps:- {taps.size}\n")
    out_IQ, valid_token = rrc_imp(mod_type, SPS, taps, in_IQ_file, out_IQ_file, filter_times)

    if valid_token != 0:
        # Separate I and Q
        I = np.real(out_IQ)
        Q = np.imag(out_IQ)

        # Plot the impulse and frequency response
        fs = 4e6
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