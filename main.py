import sys
from bitwise import *

filename = ""
fontfile = None
tab_fsType_pos = 0
tab_fsType = 0
ttf_filesize = 0
ttf_allbytes = None

def osbytes(inFile):
    bytes = fileBytes(inFile, 4)
    if bytes[0] == 79 and bytes[1] == 83 and bytes[2] == 47 and bytes[3] == 50:
        return 1
    else:
        return 0

def readHeader():
    global tab_fsType_pos
    global tab_fsType
    global ttf_filesize

    version = readBE4(fontfile)
    print ("- Fileformat version: hex: '" + hex(version) + "'")
    if version != 0x00010000:
        print ("Error: Fileformat version must be '0x00010000'\n")
        return 1
    numtables = readBE2(fontfile)
    print ("- Number of Infotables: " + str(numtables) + "")
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
        if found_os2_table == 1:
            print "- Found 'OS/2' table"
        dummy = readBE4(fontfile)
        taboffset = readBE4(fontfile);  # we need THIS!
        dummy = readBE4(fontfile)
        tables_checked = tables_checked +1

    print ("- Tableoffset: hex:'" + hex(taboffset) + "'")

    fontfile.seek(taboffset)
    tabversion = readBE2(fontfile)

    if tabversion != 0x0001:
        if tabversion == 0x0000 or tabversion == 0x0002:
            print ("Warning: OS/2 tableversion is not '0x0001' but '0x0000'\n")
        else:
            print ("Error: OS/2 tableversion must be 0, 1 or 2 and is hex:" + str(tabversion) + "\n")
            return 1

    dummy = readBE2(fontfile)  # average char width - not needed
    dummy = readBE2(fontfile)  # weight class - not needed
    dummy = readBE2(fontfile)  # widht class - not needed

    tab_fsType_pos = fontfile.tell()    # remember 0-based position of fsType (16 bit)
    tab_fsType = readBE2(fontfile)   # <<<--- We will change THIS !!!

    print ("- Curret fsType: hex:'" + hex(tab_fsType) + "'")

    fontfile.seek(0, 2)

    ttf_filesize = fontfile.tell()

    return 0

def printlicencebits(fstype):
    if fstype == 0x0000:
        print ("       0: embedding for permanent installation allowed");

    if fstype & 0x0001 == 0x0001:
        print ("       1: reserved - not to be used, must be zero!");

    if fstype & 0x0002:
        print ("       2: embedding restricted (not allowed, at all!)");

    if fstype & 0x0004:
        print ("       4: embedding for preview & printing allowed");

    if fstype & 0x0008:
        print ("       8: embedding for editing allowed");



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
    fontfile = open(filename, "rb")
except:
    None

if not fontfile:
    print "Error: Could not open fontfile " + filename + " for reading"
    exit()

print "- Opened: " + filename + "\n"

if readHeader() == 1:
    fontfile.close()
    exit()

if argc == 3:
    wanted_fsType = int(argv[2])
    print ("- Wanted fsType: hex:'" + hex(wanted_fsType) + "'")
    printlicencebits(wanted_fsType)

    if wanted_fsType & 0x0001:
        print ("\nError: fsType & 0x0001 bit is reserved. must be zero!")
        fontfile.close()
        exit()

    if((wanted_fsType & 0x0002) and ((wanted_fsType & 0x0004) or (wanted_fsType & 0x0008))):
        print ("\nError: fsType & 0x0002 bit set, and (embedding allowed 0x0004 or 0x0008)")
        fontfile.close()
        exit()
    if(wanted_fsType == tab_fsType):
        print ("\nNothing to do... wanted fsType " + hex(wanted_fsType) + " already stored in TTF file!")
        fontfile.close()
        exit()

    print ("- TTF filesize: '" + str(ttf_filesize) + "' bytes")

    fontfile.seek(0)

    ttf_allbytes = fileBytes(fontfile, ttf_filesize)
    bytesread = len(ttf_allbytes)

    if bytesread != ttf_filesize:
        print ("\nError: Could not read " + ttf_filesize + " bytes from fontfile (read: " + bytesread + ")")
        fontfile.close()
        exit()

    print ("- OK: read: '" + str(bytesread) + "' bytes from file")

    ttf_allbytes[tab_fsType_pos] = 0
    ttf_allbytes[tab_fsType_pos + 1] = wanted_fsType

    fontfile.close()

    try:
        fontfile = open(filename, "wb")
    except:
        None

    if not fontfile:
        print "Error: Could not open fontfile " + filename + " for reading"
        exit()

    byte_string = ("".join(chr(b) for b in ttf_allbytes))
    byteswritten = len(byte_string)

    fontfile.write(byte_string)

    if byteswritten != ttf_filesize:
        print ("\nError: Could not write " + str(ttf_filesize) + " bytes to fontfile (written: " + str(byteswritten) + ")")
        fontfile.close()
        exit()

    print("- OK: written: '" + str(byteswritten) + "' bytes to file")

    fontfile.close()

else:
    print("\nNothing changed! - No new fsType value specified")
    print("Run program without any arguments to get usage hints")


