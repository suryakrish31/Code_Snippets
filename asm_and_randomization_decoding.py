import numpy as np
from asm_and_randomizer_validation import randomLut
from pattern_search_bitBybit import search_pattern_bit_by_bit


def asm_search(data):
    matches = search_pattern_bit_by_bit(data, b'\x1a\xcf\xfc\x1d')
    print(f"Total Number of frames found:- {len(matches)}")
    return len(matches), matches


def asmr_decoding(src_file, frame_len):
    with open(src_file, 'rb') as f_src:
        read_bytes = f_src.read()
    no_of_frames, frame_offsets = asm_search(read_bytes)
    frames = np.empty((0,frame_len),dtype=np.uint8)
    frames_derandomized = np.empty((0,frame_len),dtype=np.uint8)
    for offset in frame_offsets:
        try:
            temp_frame = np.array([[x for x in read_bytes[int(offset):frame_len+int(offset)]]], dtype=np.uint8)
            frames = np.append(frames, temp_frame, axis=0)
        except IndexError:
            pass
        except ValueError:
            pass
    i = 0
    for frame_index in range(len(frames)-1):
        temp_bytearray = b''
        for byte_index in range(0, len(frames[frame_index])-1, 2):
            #if 895 < byte_index < 1023 or 1915 < byte_index <
            temp_value = (frames[frame_index][byte_index] << 8 | frames[frame_index][byte_index+1]) & 0xffff
            if i == 0xff:
                i = 0
            if temp_value == 0x1acf or temp_value == 0xfc1d:
                temp_bytearray += bytes([(temp_value>>8) & 0xff])
                temp_bytearray += bytes([temp_value & 0xff])
                continue
            else:
                temp_value = temp_value ^ randomLut(i)
                temp_bytearray += bytes([(temp_value >> 8) & 0xff])
                temp_bytearray += bytes([temp_value & 0xff])
                i += 1
        frames_derandomized = np.append(frames_derandomized, np.array([x for x in temp_bytearray], dtype=np.uint8))

    with open(r"C:\Users\Admin\Documents\gnu_sinks\asmr_decoded.bin", 'wb') as f_w:
        for i in frames_derandomized:
            f_w.write(i.tobytes())



if __name__ == '__main__':
    file_path = r"C:\Users\Admin\Documents\gnu_sinks\\"
    file = file_path + "fec_decoded_output_bpsk.bin"
    frame_len = int(input("Please enter the TF length\n").strip())
    asmr_decoding(file, frame_len)