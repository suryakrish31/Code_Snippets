def float_to_q31(number):
    q31_max = 2147483647  # Maximum value for Q15 format
    q31_min = -2147483648  # Minimum value for Q15 format
    q31_resolution = 1 / 2 ** 31  # Resolution of Q15 format

    #print(f"Transformed number:- {number:0.16f}\n")
    # Scale the number and round to the nearest integer
    q31_number = round(number / q31_resolution)

    # Clip the number within the range of Q15 format
    q31_number = max(min(q31_number, q31_max), q31_min)

    return q31_number

if __name__ == '__main__':
    # Example usage
    float_number = float(input("Enter the floating number:-\n").strip())
    q31_number = float_to_q31(float_number)
    print(f"Float number: {float_number:0.16f}")
    print("Q15 number:", q31_number)
    print(f"Q15 number in hex: {q31_number & 0xffffffff:08x}")
