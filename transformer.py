"""
CSAPX Lab 1: Secret Messages

A program that encodes/decodes a message by applying a set of transformation operations.
The transformation operations are:
    shift - Sa[,n] changes letter at index a by moving it n letters fwd in the alphabet. A negative
        value for n shifts the letter backward in the alphabet.
    rotate - R[n] rotates the string n positions to the right. A negative value for n rotates the string
        to the left.
    duplicate - Da[,n] follows character at index a with n copies of itself.
    trade - Ta,n replaces character at index a with former character at index n, and replaces character
        at index n with former character at index a.

All indices numbers (the subscript parameters) are 0-based.
All input messages must be capital letters with no spaces.
All transformation operations are seporated by a ;.

author: Miles Sopchak
"""


def main() -> None:
    """
    Encripts or Decrypts a message based on a string of transformation opperations supplied by the user.
    :return: None
    """
    print("Welcome to Secret Messages!") #opening statement
    while True:  #loop for entire transformer
        inp = input("What do you want to do: (E)ncrypt, (D)ecrypt or (Q)uit?  ")
        if (inp == 'Q'):  #quits program
            print('And awaaaaaaay I go!')
            break
        elif (inp == 'E' or inp == 'D'):
            msg = input('Enter the message:  ')  #msg stands for message
            ops = input('Enter the encrypting transformation operations:  ').split(';')  #ops stands for operations
            if (inp == 'E'):  #prepares to encrypt a message
                encrypt(msg,ops)
            elif (inp == 'D'):  #prepares to decrypt
                decrypt(msg,ops[::-1])
        else:  #catch for invalid inputs
            print('Please use a valid input')

def encrypt(msg,ops) -> None:
    """
    Encrypts msg based on ops
    :param msg: A string of uppercase characters that will be encrypted.
    :param ops: A string of operations to be preformed on msg to encrypt it.
    :return: None
    """
    for x in ops:
        if (x[0] == 'S'):  #split call
            if (x.find(',') != -1):
                x = x[1:].split(',')
                msg = shift(msg,x[0],x[1])
            else:
                msg = shift(msg,x[1:],1)
        elif (x[0] == 'R'):  #rotate call
            if (len(x) > 1):
                msg = rotate(msg,x[1:])
            else:
                msg = rotate(msg,1)
        elif (x[0] == 'D'):  #duplicate call
            if (x.find(',') != -1):
                x = x[1:].split(',')
                msg = duplicate(msg,x[0],x[1])
            else:
                msg = duplicate(msg,x[1:],1)
        elif (x[0] == 'T'): #trade call
            x = x[1:].split(',')
            msg = trade(msg,x[0],x[1])
        else:
            print('Please use propper encrypting transformation operations')
            return None
    print('Done.\n' + str(msg))

def decrypt(msg,ops) -> None:
    """
    Decrypts msg based on ops
    :param msg: A string of uppercase characters that will be decrypted.
    :param ops: The string of operations that were preformed on msg to encrypt it.
    :return: None
    """
    for x in ops:
        if (x[0] == 'S'):  #split call
            if (x.find(',') != -1):
                x = x[1:].split(',')
                msg = shift(msg,x[0],-int(x[1]))
            else:
                msg = shift(msg,x[1:],-1)
        elif (x[0] == 'R'):  #rotate call
            if (len(x) > 1):
                msg = rotate(msg,-int(x[1:]))
            else:
                msg = rotate(msg,-1)
        elif (x[0] == 'D'):  #duplicate call
            if (x.find(',') != -1):
                x = x[1:].split(',')
                msg = unduplicate(msg,x[0],x[1])
            else:
                msg = unduplicate(msg,x[1:],1)
        elif (x[0] == 'T'): #trade call
            x = x[1:].split(',')
            msg = trade(msg,x[0],x[1])
        else:
            print('Please use propper encrypting transformation operations')
            return None
    print('Done.\n' + str(msg))

def shift(msg,i,k):
    """
    Shifts character i in msg, k letters forward in the alphabet. If the letter 'Z' is surpassed it will loop back
        to 'A' at the beginning of the alphabet. If k is negative is will move backwards.
    :param msg: A string of uppercase characters that will have a character shifted.
    :param i: The index of the character to be shifted.
    :param k: The number of letters to shift by.
    :return: msg
    """
    i = int(i) % len(msg)
    k = int(k)
    msg = msg[:i] + chr(((ord(msg[i]) - ord('A') + k) % 26) + ord('A')) + msg[i + 1:]
    return msg

def rotate(msg,i):
    """
    Rotates the characters in msg by i places to the right. Ex: rotate(TRANSFORM,5) -> SFORMTRAN.
        If i is negative then it rotates left.
    :param msg: A string of uppercase characters that will be rotated.
    :param i: The number of places to rotate by.
    :return: msg
    """
    i = int(i) % len(msg)
    if (i > 0):
        return msg[-i:] + msg[:-i]
    else:
        return msg[i:] + msg[:i] 

def duplicate(msg,i,k):
    """
    Duplicates a character in msg at index i, k times.
    :param msg: A string of uppercase characters that will have a character duplicated.
    :param i: The index of the character to be duplicated.
    :param k: The number of times the character will be duplicated.
    :return: msg
    """
    i = int(i) % len(msg)
    k = abs(int(k))
    for x in range(k):
        msg = msg[:i + 1] + msg[i] + msg[i + 1:]
    return msg

def unduplicate(msg,i,k):
    """
    Attempts to unduplicate a character in msg at index i, that had been duplicated k times.
    :param msg: A string of uppercase characters that will have a character unduplicated.
    :param i: The index of the character that was previously duplicated.
    :param k: The number of times the character was duplicated.
    :return: If sucessful return msg. Else returns an error message.
    """
    i = int(i) % len(msg)
    k = abs(int(k))
    str = msg  #using str as msg so if unduplicate is unsucessful it will return the original string
    if (len(msg) == i + 1):  #catch in case i is the last chr ins msg
        print('Could not preform duplication decryption')
        return msg
    for x in range(k):
        if (str[i] == str[i + 1]):
            str = str[:i + 1] + str[i + 2:]
        else:
            print('Could not preform duplication decryption')
            return msg
    return str

def trade(msg,i,j):
    """
    Trades the positions of two characters in msg located at indexes i and j.
    :param msg: A string of uppercase characters that will have two characters traded.
    :param i: The index of the first character to be traded.
    :param j: The index of the second character to be traded.
    :return: msg
    """
    i = int(i) % len(msg)
    j = int(j) % len(msg)
    if (i < j):
        return msg[:i] + msg[j] + msg[i + 1:j] + msg[i] + msg[j + 1:]
    else:
        return msg[:j] + msg[i] + msg[j + 1:i] + msg[j] + msg[i + 1:]


        



if __name__ == '__main__':
    main()