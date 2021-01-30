import sys
import itertools
import os

encryption_table = {chr(i+96):i for i in range(1,27)}
encryption_table[" "] = 27 #for space character

def transposeMatrix(m):
    return list(map(list,zip(*m)))

def getMatrixMinor(m,i,j):
    return [row[:j] + row[j+1:] for row in (m[:i]+m[i+1:])]

def getMatrixDeternminant(m):
    #base case for 2x2 matrix
    if len(m) == 2:
        return m[0][0]*m[1][1]-m[0][1]*m[1][0]

    determinant = 0
    for c in range(len(m)):
        determinant += ((-1)**c)*m[0][c]*getMatrixDeternminant(getMatrixMinor(m,0,c))
    return determinant

def getMatrixInverse(m):
    determinant = getMatrixDeternminant(m)
    #special case for 2x2 matrix:
    if len(m) == 2:
        return [[m[1][1]/determinant, -1*m[0][1]/determinant],
                [-1*m[1][0]/determinant, m[0][0]/determinant]]

    #find matrix of cofactors
    cofactors = []
    for r in range(len(m)):
        cofactorRow = []
        for c in range(len(m)):
            minor = getMatrixMinor(m,r,c)
            cofactorRow.append(((-1)**(r+c)) * getMatrixDeternminant(minor))
        cofactors.append(cofactorRow)
    cofactors = transposeMatrix(cofactors)
    for r in range(len(cofactors)):
        for c in range(len(cofactors)):
            cofactors[r][c] = cofactors[r][c]/determinant
    return cofactors

def convert_to_number(string):
    encrypt_list = []
    for i in range(len(string)):
        try:
            encrypt_list.append(encryption_table[string[i]])
        except:
            pass
    return encrypt_list

def convert_to_char(number):
    try:
        for char,number_1 in encryption_table.items():
            if number_1 == number:
                return char
    except:
        return None

def openfile_enc(directory):
    with open(directory) as f:
        output = f.read().lower()
        return output
def openfile(directory):
    with open(directory) as f:
        output = f.read()
        return output
def write_file(directory, data):
    with open(directory,"w+") as f:
        f.write(data)
def read_keys(directory):

    with open(directory) as f:
        keys= f.read()
        f.seek(0)

        key_matrix_len = len(f.readlines())
        keys = keys.replace(',', '')
        keys = keys.replace('\n', '')

        arr = [[0 for i in range(key_matrix_len)] for j in range(key_matrix_len)]
        counter = 0
        for i in range(key_matrix_len):
            for j in range(key_matrix_len):
                arr[i][j] = keys[counter]
                counter += 1

    for i in range(len(arr)):
        arr[i] = [int(i) for i in arr[i]]
    return arr

def split(a, n):
    k, m = divmod(len(a), n)
    return list(a[i * k + min(i, m):(i + 1) * k + min(i + 1, m)] for i in range(n))

def encrypt_with_key(data,key):
    data = convert_to_number(data)
    left = len(data) % len(key)
    if not left == 0:
        row = (int(len(data)/len(key))) +1
    else:
        row = (int(len(data)/len(key)))
    result= [[0 for i in range(row)] for j in range(len(key))]

    if not (left == 0 ):
        for i in range(len(key) -left):
            data.append("27")    #used 27 instead of 0 for empty pair

    new_data_matrix = list(zip(*(split(data,int(len(data)/len(key))))))

    for i in range(len(new_data_matrix)):
        new_data_matrix[i] = [int(i) for i in new_data_matrix[i]]

    for i in range(len(key)):
        for j in range(len(new_data_matrix[0])):
            for k in range(len(new_data_matrix)):
                result[i][j] += key[i][k] * new_data_matrix[k][j]
    list_1 =[]

    result = transposeMatrix(result)
    for i in range(len(result)):
        string_ints = [str(int) for int in result[i]]
        list_1.append(string_ints)
    s = ",".join(itertools.chain(*list_1))
    return s

def decrypt_with_key(data,key):
    left = len(data) % len(key)
    if not left == 0:
        row = (int(len(data)/len(key))) +1
    else:
        row = (int(len(data)/len(key)))
    result= [[0 for i in range(row)] for j in range(len(key))]

    data = list(zip(*(split(data,int(len(data)/len(key))))))

    for i in range(len(key)):
        for j in range(len(data[0])):
            for k in range(len(data)):
                result[i][j] += round(key[i][k] * int(data[k][j]))

    result = list(map(list,zip(*result)))

    list_1=[]
    for i in range(len(result)):
        for j in range(len(result[i])):
            list_1.append(result[i][j])
    string_array = []
    for k in range(len(list_1)):
        string_array.append(convert_to_char(list_1[k]))

    string_array = [i for i in string_array if i]

    string_result = ''.join(string_array)
    return string_result

def main():
    if len(sys.argv) > 5:
        assert False, "Parameter number error"

    if not (sys.argv[1] == "enc" or sys.argv[1] == "dec"):
        assert False, "Undefined parameter error"

    nameKey = sys.argv[2] #controls for the file type
    nameKey = nameKey.split('.')
    if nameKey[1] != 'txt':
        assert False, "Key file could not be read error"

    if sys.argv[1] == "enc":
        try:
            keys = read_keys(sys.argv[2])
        except ValueError:
            assert False, "Invalid character in key file error"
        except:
            assert False, "Key file not found error"
        if not os.path.getsize(sys.argv[2]):
                assert False, "Key file is empty error"
        
        for i in range(len(keys)):
            for j in range(len(keys[i])):
                if not ((type(keys[i][j])==int) or (keys[i][j] == "\n") or (keys[i][j] == "," )) or keys[i][j] == 0: #control for key items
                    assert False, "Invalid character in key file error"

        namePlain = sys.argv[3]
        namePlain = namePlain.split('.')
        if namePlain[1] != 'txt':
            assert False, "The input file could not be read error"

        try:
            plain_text = openfile_enc(sys.argv[3])
        except:
            assert False, "Input file not found error"
        if not os.path.getsize(sys.argv[3]):
                assert False, "Input file is empty error"

        control_1 =all(elem in  encryption_table.keys() for elem in plain_text.replace('\n', ''))
        if not control_1:
            assert False, "Invalid character in input file error"

        output = encrypt_with_key(plain_text,keys)
        write_file(sys.argv[4], output)

    elif sys.argv[1] == "dec": #if or elif
        try:
            keys = read_keys(sys.argv[2])
        except ValueError:
            assert False, "Invalid character in key file error"
        except:
            assert False, "Key file not found error"
        if not os.path.getsize(sys.argv[2]):
                assert False, "Key file is empty error"

        for i in range(len(keys)):
            for j in range(len(keys[i])):
                if not ((type(keys[i][j])==int) or (keys[i][j] == "\n") or (keys[i][j] == "," )) or keys[i][j] == 0:
                    assert False, "Invalid character in key file error"

        keys = getMatrixInverse(keys)
        try:
            cipher_text = openfile(sys.argv[3])
        except:
            assert False, "Input file not found error"
        if not os.path.getsize(sys.argv[3]):
            assert False, "Input file is empty error"

        cipher_copy = list(map(int,cipher_text.split(',')))
        for i in cipher_copy: #looking for non positive integers in cipher_text
            if i <= 0:
                assert False, "Invalid character in input file error"
        cipher_text = cipher_text.replace('\n', '')
        cipher_data = cipher_text.split(',')
        output = decrypt_with_key(cipher_data,keys)
        write_file(sys.argv[4], output)

if __name__ == "__main__":
    try:
        main()
    except AssertionError as e:
        print(e)
