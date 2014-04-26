from array import array

def writeLE4(value, outFile):
    raw = array('B',[0,0,0,0])

    raw[0] = (value & 0xFF)
    value = value >> 8
    raw[1] = (value & 0xFF)
    value = value >> 8
    raw[2] = (value & 0xFF)
    value = value >> 8
    raw[3] = (value & 0xFF)

    # fwrite(raw, 1, 4, outFile)

def writeLE2(value, outFile):
    raw = array('B',[0,0])

    raw[0] = (value & 0xFF)
    value = value >> 8
    raw[1] = (value & 0xFF)

    # fwrite(raw, 1, 2, outFile)

def writeBE4(value, outFile):
    raw = array('B',[0,0,0,0])

    raw[3] = (value & 0xFF)
    value = value >> 8
    raw[2] = (value & 0xFF)
    value = value >> 8
    raw[1] = (value & 0xFF)
    value = value >> 8
    raw[0] = (value & 0xFF)

    # fwrite(raw, 1, 4, outFile)

def writeBE2(value, outFile):
    raw = array('B',[0,0])

    raw[1] = (value & 0xFF)
    value = value >> 8
    raw[0] = (value & 0xFF)

    # fwrite(raw, 1, 2, outFile)

def readLE4(inFile):
    retval = None
    fourbytes = fileBytes(inFile, 4)
    raw = array('B',fourbytes)

    retval = (raw[3]<<24) | (raw[2]<<16)  | (raw[1]<<8)  | (raw[0])
    return retval

def readLE2(inFile):
    retval = None
    twobytes = fileBytes(inFile, 2)
    raw = array('B',twobytes)

    retval = (raw[1]<<8) | (raw[0])
    return retval

def readBE4(inFile):
    retval = None
    fourbytes = fileBytes(inFile, 4)
    raw = array('B',fourbytes)

    retval = (raw[0]<<24) | (raw[1]<<16)  | (raw[2]<<8)  | (raw[3])
    return retval

def readBE2(inFile):
    retval = None
    twobytes = fileBytes(inFile, 2)
    raw = array('B',twobytes)

    retval = (raw[0]<<8) | (raw[1])
    return retval

def readFile():
    f = open("ttfpatch10/ttfpatch10_cpp_source/tako.ttf", "r")
    return f

def fileBytes(inFile, length):
    bytes = [ord(b) for b in inFile.read(length)]
    return bytes

inFile = readFile()
print readLE4(inFile)
print readLE2(inFile)
print readBE4(inFile)
print readBE2(inFile)
inFile.close()
