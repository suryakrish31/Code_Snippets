import struct
import numpy as np
def fixed_to_float(fixed_value, fractional_bits=15):
    """
    Convert a fixed-point value to a floating-point value.
    :param fixed_value: The fixed-point value to convert (in two's complement format).
    :param fractional_bits: The number of fractional bits in the fixed-point representation.
    :return: The converted floating-point value.
    """
    # Handle negative values for signed 16-bit integers
    if fixed_value > 0x7FFF:
        # Convert to signed integer
        fixed_value -= (1 << 16)
    return [fixed_value / (1 << fractional_bits)]

def convert_fixed_to_float(input_file, output_file):
    I_float = np.array([], dtype=np.float32)
    Q_float = np.array([], dtype=np.float32)
    with open(input_file, 'rb') as f_in, open(output_file, 'wb') as f_out:
        while True:
            # Read 4 bytes at a time (2 bytes for I and 2 bytes for Q)
            data = f_in.read(4)
            if len(data) == 0:
                # End of file reached
                break
            
            if len(data) == 4:
                # Unpack 16-bit I and Q values from the data (big-endian or little-endian based on your system)
                I_fixed, Q_fixed = struct.unpack('<hh', data)  # Little-endian format

                # Convert fixed-point values to float
                I_float = np.append(I_float, fixed_to_float(I_fixed))
                Q_float = np.append(Q_float, fixed_to_float(Q_fixed))

                # Pack the float values into 32-bit float format (little-endian) and write to output file
            else:
                # Handle the case where the final data chunk is incomplete
                print("Warning: Incomplete data chunk found. Skipping last chunk...")
                break
        IQ = I_float + 1j * Q_float
        f_out.write(IQ.tobytes())

if __name__ == "__main__":
    input_file = 'rx_jesd_data.bin'
    output_file = 'out_rx_jesd_data.bin'
    out = fixed_to_float(32768)
    print(out)
    # convert_fixed_to_float(input_file, output_file)
    # print(f"Conversion complete. Data written to {output_file}.")
