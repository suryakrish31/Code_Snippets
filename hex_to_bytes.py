with open("TM_EPS_Jan9_decoded.txt" , 'r') as fi:
	hex_string = fi.read().strip('\n')

hex_values = [int(i, 16) for i in hex_string.split() if i != '0x']
byte_values = bytes(hex_values)

with open("TCP_IP.dat", 'wb') as fo:
	fo.write(byte_values)
