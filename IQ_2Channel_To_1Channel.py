
def combine_files(file1_path, file2_path, output_path):
    chunk_size = 4  # 32 bits = 4 bytes

    try:
        with open(file1_path, 'rb') as file1, open(file2_path, 'rb') as file2, open(output_path, 'wb') as output_file:
            while True:
                # Read a 32-bit chunk from file 1
                chunk1 = file1.read(chunk_size)
                if chunk1:
                    output_file.write(chunk1)
                else:
                    break
                # Read a 32-bit chunk from file 2
                chunk2 = file2.read(chunk_size)
                if chunk2:
                    output_file.write(chunk2)
                else:
                    break

        print(f"Files combined and saved to {output_path}")

    except FileNotFoundError as e:
        print(f"Error: {e.strerror}. File not found: {e.filename}")
    except IOError as e:
        print(f"IO error occurred: {e.strerror}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


if __name__ == '__main__':
    # Example usage
    file_path = r"C:\Users\Admin\Documents\gnu_sources\\"
    out_file = file_path + 'rrc_qpsk_200MHZ.bin'

    file1 = file_path + input(f"Enter the input I file; which is at path:- {file_path}\n").strip()
    file2 = file_path + input(f"Enter the input Q file; which is at path:- {file_path}\n").strip()

    combine_files(file1, file2, out_file)
