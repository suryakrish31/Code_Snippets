import numpy as np
import struct


def float_to_ieee754(f):
  return hex(struct.unpack('<I', struct.pack('<f', f))[0])[2:]



def ieee754_hexStr_to_float(f):
  try:
    return struct.unpack('!f', bytes.fromhex(f))[0]
  except ValueError:
    print(f)


def ieee754_to_float(file_name):
  with open(file_name, "rb") as fptr:
    read_bytes = fptr.read()



# Example usage:
if __name__ == '__main__':
  # f = np.float32(float(input('Please enter the float number:- \n')))
  f = 1/np.sqrt(2)
  print(f"Entered Number:- {f}")
  ieee754 = float_to_ieee754(f)
  print(f"IEEE754 Formated value:- {ieee754}")
  #print((f"{f:08x},\n"))