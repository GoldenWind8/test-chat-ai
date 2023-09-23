# Finalizing the original function as it appears to be working correctly based on the available information.
def solution(s):
    # Braille encoding dictionary for lowercase letters
    braille_dict = {
        'a': '100000',
        'b': '101000',
        'c': '110000',
        'd': '110100',
        'e': '100100',
        'f': '111000',
        'g': '111100',
        'h': '101100',
        'i': '011000',
        'j': '011100',
        'k': '100010',
        'l': '101010',
        'm': '110010',
        'n': '110110',
        'o': '100110',
        'p': '111010',
        'q': '111110',
        'r': '101110',
        's': '011010',
        't': '011110',
        'u': '100011',
        'v': '101011',
        'w': '011101',
        'x': '110011',
        'y': '110111',
        'z': '100111',
        ' ': '000000'
    }

    # Initialize an empty string to store the Braille output
    braille_output = ""

    # Iterate through the input string
    for char in s:
        # Handle spaces
        if char == ' ':
            braille_output += braille_dict[' ']
        # Handle capital letters
        elif char.isupper():
            braille_output += '000001'  # Capitalization mark
            braille_output += braille_dict[char.lower()]  # Braille encoding of the lowercase character
        # Handle lowercase letters
        else:
            braille_output += braille_dict[char]

    return braille_output

print()
