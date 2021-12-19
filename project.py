import numpy as np
import codecs
import os
from PIL import Image
import math
import cv2



def genData(data):


    newdata = []
#   Make a list called new data

    for i in data:
        newdata.append(format(ord(i), '08b'))

# putting sign at the end of data file
    end_of_data = 'endofdata'
    for i in end_of_data:
        newdata.append(format(ord(i), '08b'))

    print('data has been generated successfully ')
    return newdata


def create_image(data):
    num_of_images = math.ceil(len(data)/15000)
    print('num_of_images ', num_of_images)

    for n in range(num_of_images):
        a = np.random.rand(200, 200, 3) * 255
        im_out = Image.fromarray(a.astype('uint8')).convert('RGB')
        im_out.save('out%000d.jpg' % n)

    return num_of_images


def encode_enc(image, block):


    binaryFile = conversion(block)

    i = 0
    blocksLength = len(binaryFile)
    for cells in image:
        for pixel in cells:

            R, G, B = conversion(pixel)

            if i < blocksLength:
                pixel[0] = int(R[:-1] + binaryFile[i], 2)
                i += 1

            if i < blocksLength:
                pixel[1] = int(G[:-1] + binaryFile[i], 2)
                i += 1

            if i < blocksLength:
                pixel[2] = int(B[:-1] + binaryFile[i], 2)
                i += 1

            if i >= blocksLength:
                break

    return image


def conversion(message):

    if type(message) == str:
        return ''.join([format(ord(i), "08b") for i in message])

    elif type(message) == bytes or type(message) == np.ndarray:
        return [format(i, "08b") for i in message]

    elif type(message) == int or type(message) == np.uint8:
        return format(message, "08b")

    else:
        raise TypeError("NOT SUPPORTED")


def encodeText():
   

    inputFile = open("EP#1.pdf", "rb") #Here put the name of your file
    binaryFile = inputFile.read()
    inputFile.close()

    bytesArray = codecs.encode(binaryFile, 'base64')

    data = bytesArray.decode('utf-8')

    partial = []
    for i in range(39):  #This sould be changed depending of the number of needed picture
        partial.append(data[i*15000:(i+1)*15000])

    print('data datafile is opend ')



    print()
    x = True
    hiddenData = []
    create_image(data)
    i = 0
    while x:
        image = cv2.imread('./out%000d.jpg' % i)

        hiddenData.append(encode_enc(image, partial[i]))

        cv2.imwrite(os.path.join('hidden%000d.jpg' % i), image)
        print('hidden%000d.jpg' % i)

        i = i+1
        if not os.path.isfile('./out%000d.jpg' % i):
            x = False

    print('encodeText finshed and pictures are saved ')
    return hiddenData
# Finally save the new Image


def decode(image):
   

    data = ""
    for cells in image:
        for pixel in cells:
            R, G, B = conversion(pixel)
            data += R[-1]
            data += G[-1]
            data += B[-1]

    allBytes = [data[i: i+8] for i in range(0, len(data), 8)]
    extractData = ""
    end_of_data = "endofdata"
    for byte in allBytes:
        extractData += chr(int(byte, 2))
        if extractData[-9:] == end_of_data:
            break

    return extractData


def decode_file(encodedImages):
    messages = []
    blocksNumber = len(encodedImages)

    FileInString = ""

    for i in range(blocksNumber):
        messages.append(decode(encodedImages[i]))
        FileInString += messages[i]

    fileBytesArray = FileInString.encode('utf-8')
    fileAsBinary = codecs.decode(fileBytesArray, 'base64')
    return fileAsBinary


def main():

    hidden = encodeText()
    decodeFile = decode_file(hidden)

    datafile = open("Stegano.pdf", 'wb')
    datafile.write(decodeFile)
    datafile.close()
    print('decode file is saved as: Stegano.pdf')


if __name__ == '__main__':

    main()
