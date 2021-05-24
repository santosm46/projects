
data = open('data.txt', 'r')
result = open('result.txt', 'w')
out_ascii = open('ascii.txt', 'w')

indice_do_campo = 0
separador = " "
binary_groups = []
converted = []

binario = "10011111 10100111 10111110 10111101 11011111 11111101 11011111 11011010 11111111 10010100 11001110 11011110 11111111 11111110 11101100 10111100 11110001 10011100 11001111 11111110 10010000 11111110"

hexa_in_binary = {
    "0": "0000",
    "1": "0001",
    "2": "0010",
    "3": "0011",
    "4": "0100",
    "5": "0101",
    "6": "0110",
    "7": "0111",
    "8": "1000",
    "9": "1001",
    "A": "1010",
    "B": "1011",
    "C": "1100",
    "D": "1101",
    "E": "1110",
    "F": "1111",
    " ": " "
}

def convertLineToBinary(line):
    convertedLine = ""

    for i in line:
        convertedLine = convertedLine + hexa_in_binary[i]

    return convertedLine

inInt = int('0b' + binario.replace(" ", ""), 2)
print(inInt.to_bytes((inInt.bit_length() + 7) // 8, 'big').decode())

for line in data.readlines():
    convertedLine = convertLineToBinary(line[:-1].upper())
    result.write(convertedLine + "\n")
    inInt = int('0b' + convertedLine.replace(" ", ""), 2)
    out_ascii.write(inInt.to_bytes((inInt.bit_length() + 7) // 8, 'big').decode())

    converted.append(
        convertedLine
    )

data.close()
result.close()
out_ascii.close()
