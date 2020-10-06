#converts a string and converts it to a 5x5 playfair grid
def create_playfair_grid(key):

    # empty 5x5 list to store our playfair gird on
    grid = [[], [], [], [], []]
    # list of alphabet, used later for making grid
    playfairChars = list('abcdefghiklmnopqrstuvwxyz')
    # dictionary used to keep track of which characters we have used
    characterCount = {}
    # a place to store our cleaned up text the user passed in
    filteredInput = ""

    # replace j with i and remove whitespaces
    # also checks to see if a charcter exists in our dictionary
    # if  a character not in it yet, add it in characterCount
    for char in key:
        if char == "j":
            char = "i"
        if char == " ":
            continue
        if char not in characterCount:
            characterCount[char] = 1
            filteredInput += char

    # check our dictionary of non-duplicated characters not used in filtered input
    # and then adds them
    for char in playfairChars:
        if char not in filteredInput:
            filteredInput += char

    # slices 5 letters of text from the filtered text at a time
    # and then attaches it to one of the empty lists within
    # the playfair grid
    # also cleans the filtered input to lowercase.
    currSlice = 5
    previousSlice = 0
    filteredInput = filteredInput.lower()
    for i in range(1, 6):
        currSlice = i*5
        previousSlice = currSlice-5
        grid[i-1] = list(filteredInput[previousSlice:currSlice])

    return grid

# This only prepares text for encryption, doesn't apply the
# playfair cipher besides removing whitespaces and adding x's in spots
def playfair_polish(text):

    # remove whitespaces and convert text to lower
    encrypted_plaintext = text.replace(" ", "")
    encrypted_plaintext = encrypted_plaintext.lower()

    # total_ch_len is used for avoiding out of bound and counting error with enumerating the string
    # since if we just add a letter during enumeration, it will never reach the end of
    # the string to check for more repeated letters and adds it to our counter
    total_ch_len = len(encrypted_plaintext)
    for ch in range(len(encrypted_plaintext)):
        if ch != len(encrypted_plaintext)-1 and encrypted_plaintext[ch] != "x" and (encrypted_plaintext[ch] == encrypted_plaintext[ch+1]):
            total_ch_len += 1

    # enumerates through the text, if a letter follows another
    # add an x inbetween them
    for ch in range(total_ch_len):
        if ch != total_ch_len-1 and encrypted_plaintext[ch] != "x" and (encrypted_plaintext[ch] == encrypted_plaintext[ch+1]):
            encrypted_plaintext = encrypted_plaintext[:ch +
                                                      1] + "x" + encrypted_plaintext[ch+1:]

    # if the text is uneven in lengh, add an x at the end
    if len(encrypted_plaintext) % 2 != 0:
        encrypted_plaintext += "x"
    return encrypted_plaintext

#helper function to convert text into lists of two letters
def _text_pair_list(text):
    # Go through the encrypted text two letters at a time, make a list of them
    # and then add it to a larger list to reference later
    pair_grid = []
    for ch in range(0, len(text), 2):
        pair = []
        pair.append(text[ch])
        pair.append(text[ch+1])

        pair_grid.append(pair)

    return pair_grid

#cleans the text before encrypting it by doing the following:
# 1.remove whitespace
# 2.add an "x" between repeated words
# 3. if the text length is odd, add an x at the end
def encrypt_polished_message(text, playfair_grid):
    encrypted_message = ""
    pair_grid = _text_pair_list(polished_messaged)
    #go through all pairs of letters in the message
    for i, pair in enumerate(pair_grid):
        ch1 = pair[0]
        ch2 = pair[1]
        sub_ch = ""
        sub_ch2 = ""
        x_cord1 = 0
        y_cord1 = 0
        x_cord2 = 0
        y_cord2 = 0 
        #grab the coordinates of the characters in the grid by x and y
        for i, row in enumerate(playfair_grid):
            for col in row:
                if col == ch1:
                    x_cord1 = i
                    y_cord1 = row.index(col)
                if col == ch2:
                    x_cord2 = i
                    y_cord2 = row.index(col)
        #if the pair is in the same row, shift right 
        #includes edge cases for numbers on the edge to 
        #go to toe beggining
        if y_cord1 == y_cord2:
            if x_cord1 == 4:
                encrypted_message += playfair_grid[0][y_cord1] + playfair_grid[x_cord2+1][y_cord2]
            elif x_cord2 == 4:
                encrypted_message += playfair_grid[x_cord1+1][y_cord1] + playfair_grid[0][y_cord2]
            else:
                encrypted_message += playfair_grid[x_cord1+1][y_cord1] + playfair_grid[x_cord2+1][y_cord2]
        #if the pair is in the same col, shift down
        #includes edge cases for numbers on the edge to 
        #go to toe beggining
        elif x_cord1 == x_cord2:
            if y_cord1 == 4:
                encrypted_message += playfair_grid[x_cord1][0] + playfair_grid[x_cord2][y_cord2+1]
            elif y_cord2 == 4:
                encrypted_message += playfair_grid[x_cord1][y_cord1+1] + playfair_grid[x_cord2][0]
            else:
                encrypted_message += playfair_grid[x_cord1][y_cord1+1] + playfair_grid[x_cord2][y_cord2+1]
        #swap the y coordinates to swap the corners.
        else:
            encrypted_message += playfair_grid[x_cord1][y_cord2] + playfair_grid[x_cord2][y_cord1]
    return encrypted_message

#The algorithm that does the work:
#goes through all pairs in the polished text and identifies their location in the playfair grid and stores it for later
#based off the values stored from the location it will do one of three things:
#   1. If the letters are on the same row, move them to the right one
#   2. IF the letters are on the same column, move them down one
#   3. Otherwise swap the corners of the letters (maintain row poistion)
def decrypt_message(text, playfair_grid):
    # W A R N I N G!!!

    #I realize after finishing the algorithm that I had mislabeled the x and y variables
    #in this function but thats a lot of rearranging of variables I would have to do which
    #I know I will mess up somewhere in this equation
    decrypted_message = ""
    pair_grid = _text_pair_list(text)
    for i, pair in enumerate(pair_grid):
        ch1 = pair[0]
        ch2 = pair[1]
        sub_ch = ""
        sub_ch2 = ""
        x_cord1 = 0
        y_cord1 = 0
        x_cord2 = 0
        y_cord2 = 0 
        for i, row in enumerate(playfair_grid):
            for col in row:
                if col == ch1:
                    x_cord1 = i
                    y_cord1 = row.index(col)
                if col == ch2:
                    x_cord2 = i
                    y_cord2 = row.index(col)
        #if same row move left
        if y_cord1 == y_cord2:
            if x_cord1 == 0:
                decrypted_message += playfair_grid[4][y_cord1] + playfair_grid[x_cord2-1][y_cord2]
            elif x_cord2 == 0:
                decrypted_message += playfair_grid[x_cord1-1][y_cord1] + playfair_grid[4][y_cord2]
            else:
                decrypted_message += playfair_grid[x_cord1-1][y_cord1] + playfair_grid[x_cord2-1][y_cord2]
        #if same col
        elif x_cord1 == x_cord2:
            if y_cord1 == 0:
                decrypted_message += playfair_grid[x_cord1][4] + playfair_grid[x_cord2][y_cord2-1]
            elif y_cord2 == 0:
                decrypted_message += playfair_grid[x_cord1][y_cord1-1] + playfair_grid[x_cord2][4]
            else:
                decrypted_message += playfair_grid[x_cord1][y_cord1-1] + playfair_grid[x_cord2][y_cord2-1]
        #corners 
        else:
            decrypted_message += playfair_grid[x_cord1][y_cord2] + playfair_grid[x_cord2][y_cord1]
    if len(decrypted_message) %2 == 0 and decrypted_message[-1] == "x":
        decrypted_message = decrypted_message[:len(decrypted_message)-1]
    fully_decrypted_message = ""
    for ch in range(len(decrypted_message)):
        if not (decrypted_message[ch] == "x" and decrypted_message[ch-1] == decrypted_message[ch+1]):
            fully_decrypted_message += decrypted_message[ch].lower()

    return fully_decrypted_message






key = "playfair example"

plaintext = "Hide the gold in the tree stump"

polished_messaged = playfair_polish(plaintext)

playfair_grid = create_playfair_grid(key)

encrypted_message = encrypt_polished_message(polished_messaged, playfair_grid)

decrypted_message = decrypt_message(encrypted_message, playfair_grid)
print(encrypted_message)
print(decrypted_message)

for i, row in enumerate(playfair_grid):
    print(row)