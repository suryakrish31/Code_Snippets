import numpy as np
from asm_and_randomizer_validation import randomLut

def asmr_encoding(src_file, frame_len):
    with open(src_file, 'rb') as f_src:
        read_bytes = f_src.read()
    src = np.frombuffer(read_bytes, dtype=np.uint8)
    no_of_frames = len(src)/frame_len
    frames = np.empty((0,frame_len),dtype=np.uint8)
    frames_randomized = np.empty((0,frame_len),dtype=np.uint8)
    for i in range(no_of_frames):
        temp_frame = np.array([0x1a, 0xcf, 0xfc, 0x1d], dtype=np.uint8)
        frames = np.append(frames, temp_frame, axis=0)

    i = 0
    for frame_index in range(len(frames)-1):
        temp_bytearray = b''
        for byte_index in range(frame_index*frame_len, frame_len, 2):
            #if 895 < byte_index < 1023 or 1915 < byte_index <
            temp_value = (src[byte_index] << 8 | src[byte_index+1]) & 0xffff
            if i == 0xff:
                i = 0
            temp_value = temp_value ^ randomLut(i)
            temp_bytearray += bytes([(temp_value >> 8) & 0xff])
            temp_bytearray += bytes([temp_value & 0xff])
            i += 1
        frames_derandomized = np.append(frames_derandomized, np.array([x for x in temp_bytearray], dtype=np.uint8))

    with open(r"C:\Users\Admin\Documents\gnu_sinks\asmr_decoded.bin", 'wb') as f_w:
        for i in frames_derandomized:
            f_w.write(i.tobytes())


if __name__ == '__main__':
    file_path = r"C:\Users\Admin\Documents\gnu_sources\\"
    file = file_path + input(f"Enter the input file to be asm and randomized.\nPlease note that the file should be in path {file_path}")
    frame_len = int(input("Please enter the TF length\n").strip())
    asmr_encoding(file, frame_len)