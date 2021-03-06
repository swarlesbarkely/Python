    ##############################################################################
# Counts the number of programming bytes in a hex or s19 file
# Inputs: File, Size Limit (optional)
# Outputs: Byte count, % used of size limit (if given)
##############################################################################

import parser
import sys
import getopt

def PrintUsage ():
    print ("Usage: CountingBytes.py -f|--file InputFile [-s|--sizelimit SizeLimit]")
    print ("Ex. CountingBytes.py -f MyFile.hex -s 128k")
    return

def main (argv):

    sInputFile = ''
    SizeLimit = ''
    nByteCount = 0

    try:
        sOptions, sArgs = getopt.getopt (argv, 'hf:s:', ['help', 'file', 'sizelimit'])

    except getopt.GetoptError:
        PrintUsage ()
        sys.exit (-1)

    # Process command line arguments
    for sOpt, sArg in sOptions:
        if sOpt in ('-f', '--file'):
            sInputFile = sArg

        elif sOpt in ('-s', '--sizelimit'):
            SizeLimit = sArg

        elif sOpt in ('-h', '--help'):
            PrintUsage ()
            sys.exit (-1)


    try:
        FileToRead = open (sInputFile, 'r')

    except OSError:
        print ("Error opening file!")
        sys.exit (-1)

    sLine = FileToRead.readline ()

    if sLine[0] == ':':
        FileFormat = 'hex'

    elif sLine[0] == 'S':
        FileFormat = 's19'

    else:
        # Unknown file format
        print ("Unknown file format!")
        sys.exit (-1)

    if FileFormat == 'hex':
        # Read until we get an empty string (this does not include newlines)
        while not sLine == '':
            if sLine[7:9] == '00':
                # This line contains data --> add the byte count to our counter
                nByteCount += int (sLine[1:3], 16)

            sLine = FileToRead.readline ()

    elif FileFormat == 's19':
        # Read until we get an empty string (this does not include newlines)
        while not sLine == '':
            if sLine[1:2] == '1':
                # This line contains data and 3 non-data bytes --> add the data byte count to our counter
                nByteCount += (int (sLine[2:4], 16) - 3)
            elif sLine[1:2] == '2':
                # This line contains data and 4 non-data bytes --> add the data byte count to our counter
                nByteCount += (int (sLine[2:4], 16) - 4)
            elif sLine[1:2] == '3':
                # This line contains data and 5 non-data bytes --> add the data byte count to our counter
                nByteCount += (int (sLine[2:4], 16) - 5)

            sLine = FileToRead.readline ()

    # Print the results
    print ("Number of data bytes: " + str (nByteCount))

    if not SizeLimit == '':
        # Check for any suffixes on the size limit
        SizeLimit = str (SizeLimit).replace ('k', '* 1024')
        SizeLimit = str (SizeLimit).replace ('M', '* 1024**2')
        SizeLimit = str (SizeLimit).replace ('G', '* 1024**4')
        SizeLimit = eval (parser.expr(SizeLimit).compile())
        print ("Percent used: " + str (float (100 * nByteCount / SizeLimit)))

if __name__ == '__main__':
    main (sys.argv[1:])
