def float_to_q15(number):
    q15_max = 32767  # Maximum value for Q15 format
    q15_min = -32768  # Minimum value for Q15 format
    q15_resolution = 1 / 2 ** 15  # Resolution of Q15 format

    # print(f"Transformed number:- {number:0.16f}\n")
    # Scale the number and round to the nearest integer
    q15_number = round(number / q15_resolution)

    # Clip the number within the range of Q15 format
    q15_number = max(min(q15_number, q15_max), q15_min)

    return q15_number

if __name__ == '__main__':
    # Example usage
    float_number = float(input("Enter the floating number:-\n").strip())
    q15_number = float_to_q15(float_number)
    print(f"Float number: {float_number:0.16f}")
    print("Q15 number:", q15_number)
    print(f"Q15 number in hex: {q15_number & 0xffff:04x}")
