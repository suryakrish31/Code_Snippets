class LSFR:
    def __init__(self, polynomial, seed):
        self.polynomial = polynomial
        self.state = seed

    def shift(self):
        feedback_bit = 0
        for term in self.polynomial:
            feedback_bit ^= self.state >> term & 1
        self.state = (self.state >> 1) | (feedback_bit << (self.polynomial[0] - 1))

    def generate(self, num_bits):
        random_numbers = []
        for _ in range(num_bits):
            random_numbers.append(self.state & 1)
            self.shift()
        return random_numbers

# Example usage
if __name__ == "__main__":
    polynomial = [8, 7, 5, 3, 0]  # Coefficients of the polynomial
    seed = 0b11111111  # Example seed
    lfsr = LSFR(polynomial, seed)
    random_bits = lfsr.generate(4096)  # Generate 10 random bits
    print("Generated pseudo-random sequence:")
    for i in range(0, len(random_bits), 16):
        print(f"when x\"{int(i/16):02x}\" => temp1 := x\"{int(''.join([str(x) for x in random_bits[i:i+16]]), 2):04x}\";")
    print("Last bits: ", random_bits[i+16:])
    #print("Generated pseudo-random sequence:", random_bits)