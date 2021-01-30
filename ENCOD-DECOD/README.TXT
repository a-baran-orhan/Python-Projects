I develop an encryption method that uses matrix multiplication and
matrix inversions. Procedure for using matrices when encoding and decoding hidden messages is
as follows.

First convert the secret message into a string of numbers by arbitrarily assigning a number to each letter
of the message. Next, convert this string of numbers into a new set of numbers by multiplying the string by a square matrix of our choice that has an inverse.This new set of numbers represents the coded message.
To decode the message, take the string of coded numbers and multiply it by the inverse of the matrix to get the original string of numbers. 
Finally, by associating the numbers with their corresponding letters, obtain the original message. You will use the correspondence shown in following Table where letters A to Z correspond to the numbers 1 to 26 and a space is represented by the number 27.

EXECUTION
python3 assingment4.py [operation type: enc / dec] "key file path" "input file path" "output file name"