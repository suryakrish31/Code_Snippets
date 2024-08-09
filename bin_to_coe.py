import numpy as np


def bin_to_coe_file(bin_file, filename):
    """Generates a COE file from the given binary file.

    Args:
    bin_file: The name of the binary file.
    filename: The name of the COE file to generate.
    """


    with open(bin_file, "rb") as f0:
        data_buf = f0.read()
        data = np.frombuffer(data_buf, dtype=np.uint8)

    with open(filename, "w") as f:
        f.write("memory_initialization_radix=10;\n")
        f.write("memory_initialization_vector=\n")
        for value in data:
            f.write(f"{value},\n")

    byte_count = len(data)
    print(f"No of bytes written:- {byte_count}")


if __name__ == '__main__':
    filepath = r"C:\Users\Admin\Documents\gnu_sources\\"
    bin_file = filepath + input('Please enter the binary file name.\n'
                                f'Note that the file should be in the following path:- {filepath}\n').strip()

    output_path = input("Enter the coe file path:\n").strip()
    filename = output_path + "\\ram_init.coe"
    bin_to_coe_file(bin_file, filename)
