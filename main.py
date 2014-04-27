import sys
from bitwise import *

def osbytes(inFile):
    bytes = fileBytes(inFile, 4)
    if bytes[0] == 79 and bytes[1] == 83 and bytes[2] == 47 and bytes[3] == 50:
        return 1
    else:
        return 0

def readHeader():
    tabtag = array('c',[0,0,0,0,0])

    version = readBE4(fontfile)
    print ("- Fileformat version: hex: '" + str(version) + "'\n")
    if version != 0x00010000:
        print ("Error: Fileformat version must be '0x00010000'\n")
        return 1
    numtables = readBE2(fontfile)
    print ("- Number of Infotables: " + numtables + "\n")
    if numtables <= 9:
        print ("Error: numtables must be greater than '9'\n")
        return 1

    dummy = readBE2(fontfile)  # search range - not needed
    dummy = readBE2(fontfile)  # entry selector - not needed
    dummy = readBE2(fontfile)

    found_os2_table = 0
    tables_checked = 0

    while (tables_checked < numtables and found_os2_table == 0):
        found_os2_table = osbytes(fontfile)
        dummy = readBE4(fontfile)
        taboffset = readBE4(fontfile);  # we need THIS!
        dummy = readBE4(fontfile)
        tables_checked = tables_checked +1

    print ("- Tableoffset: hex:'" + taboffset + "'\n")

    fontfile.seek(taboffset)
    tabversion = readBE2(fontfile)

    if tabversion != 0x0001:
        if tabversion == 0x0000 or tabversion == 0x0002:
            print ("Warning: OS/2 tableversion is not '0x0001' but '0x0000'\n")
        else:
            print ("Error: OS/2 tableversion must be 0, 1 or 2 and is hex:" + tabversion + "\n")
            return 1

    dummy = readBE2(fontfile)  # average char width - not needed
    dummy = readBE2(fontfile)  # weight class - not needed
    dummy = readBE2(fontfile)  # widht class - not needed

    tab_fsType_pos = fontfile.tell()    # remember 0-based position of fsType (16 bit)

    tab_fsType = readBE2(fontfile)   # <<<--- We will change THIS !!!

    printf ("- Curret fsType: hex:'" + tab_fsType + "'\n")

    fontfile.seek(0, 2)
    ttf_filesize = fontfile.tell()

    return 0



argv = sys.argv
argc = len(argv)

try:
    filename = argv[1]
except:
    None

print "Pyttf by @haas85\n"

if (argc != 2 and argc != 3):
    print("Provides an easy way for font designers to set the 'embeddable' flags");
    print("of their own true type fonts. If you want to prohibit embedding of your");
    print("font e.g. in Acrobat PDF files, simply run: 'ttfpatch myfont.ttf 2'");
    print ("Usage: python main.py TrueTypeFontFile [NewFsTypeValue]\n");
    print ("fsType values:");
    print ("       0: embedding for permanent installation");
    print ("       1: reserved - do not use!");
    print ("       2: embedding restricted (not allowed!)");
    print ("       4: embedding for preview & printing allowed");
    print ("       8: embedding for editing allowed\n");
    exit()

fontfile = None

try:
    fontfile = open(filename, "r")
except:
    None

if not fontfile:
    print "Error: Could not open fontfile " + filename + " for reading"
    exit()

# import struct
# print struct.unpack(">I", ''.join([chr(x) for x in fontfile.read(4)[:-1]]))
# print struct.unpack("i", "\x00\x00\x00\x00")

bytes = [ord(b) for b in fontfile.read()]
for byte in bytes:
    if byte == 79:
        print byte
    if byte == 83:
        print byte
    if byte == 47:
        print byte
    if byte == 50:
        print byte

print "- Opened: " + filename + "\n"

if readHeader() == 1:
    fontfile.close()
    exit()