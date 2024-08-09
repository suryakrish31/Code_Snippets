from srrcDesign import srrcDesign
from float_to_Q15 import float_to_q15
from float_to_Q31 import float_to_q31
from float_to_Q17 import float_to_q17
from IEEE754_single import float_to_ieee754

def generate_coe_file(data, filename):
    """Generates a COE file from the given data.

    Args:
    data: A list of data values.
    filename: The name of the COE file to generate.
    """
  
    with open(filename, "w") as f:
        f.write("memory_initialization_radix=16;\n")
        f.write("memory_initialization_vector=\n")
        for value in data:
          #f.write(f"{value & 0xffff:04x},\n")
          #f.write(f"{value & 0xfffff:05x},\n")
          f.write(f"{value},\n")

 
def rrc_coe_gen(file_path, SPS, span, beta):
    filename = file_path + "\\rrc_taps.coe"
    weights = srrcDesign(SPS, span, beta)
    with open("rrc_taps.txt", 'w') as fo:
        for value in weights:
            fo.write(f"{value:0.16f}\n")
    print(f"Number of filter taps generated:- {weights.size}")
    taps = [0]*weights.size
    for i in range(weights.size):
        #taps[i] = int(float_to_q15(weights[i]))
        #taps[i] = int(float_to_q17(weights[i]))
        #taps[i] = int(float_to_q31(weights[i]))
        taps[i] = float_to_ieee754(weights[i])
    generate_coe_file(taps, filename)
    

if __name__ == '__main__':
    file_path = input("Enter the file path:\n").strip()
    SPS = int(input("Enter SPS (Samples per Symbol):\n").strip())
    span = int(input("Enter the span of the filter:\n").strip())
    beta = float(input("Enter the rolling factor (beta):\n").strip())
    rrc_coe_gen(file_path, SPS, span, beta)