def float_to_q17(number):
    q17_max = 65536  # Maximum value for Q15 format
    q17_min = -65536  # Minimum value for Q15 format
    q17_resolution = 1 / 2 ** 17  # Resolution of Q15 format
    
    # Clip the number within the range of Q15 format
    number = max(min(number, q17_max), q17_min)
    #print(f"Transformed number:- {number:0.16f}\n")
    # Scale the number and round to the nearest integer
    q17_number = round(number / q17_resolution)
    
    return q17_number

if __name__ == '__main__':
    # Example usage
    float_number = float(input("Enter the floating number:-\n").strip())
    q17_number = float_to_q17(float_number)
    print(f"Float number: {float_number:0.16f}")
    print("Q15 number:", q17_number)
    print(f"Q15 number in hex: {q17_number & 0xfffff:05x}")
