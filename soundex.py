def get_soundex_code(word):
    """creates a 4-character code for a word based on how it sounds."""
    if not word:
        return "0000"

    word = word.upper()        # soundex works with uppercase letters
    first_letter = word[0]
    
    # a map of letters to their soundex number
    sound_map = {
        'B': '1', 'F': '1', 'P': '1', 'V': '1',
        'C': '2', 'G': '2', 'J': '2', 'K': '2', 'Q': '2', 'S': '2', 'X': '2', 'Z': '2',
        'D': '3', 'T': '3',
        'L': '4',
        'M': '5', 'N': '5',
        'R': '6'
    }

    result_code = first_letter
    last_code = sound_map.get(first_letter, '0')      # get the code for the very first letter

    for letter in word[1:]:
        code = sound_map.get(letter, '0')       # get the code for the current letter, or '0' for vowels
        if code != '0' and code != last_code:    # add the code if it's not a vowel and not a repeat
            result_code += code
        last_code = code

    result_code = (result_code + "000")[:4]       # make sure the code is exactly 4 characters long
    
    return result_code