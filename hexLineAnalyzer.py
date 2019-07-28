import tkinter as tk
import binascii
import codecs
import struct


# def qf(x):
#     b = binascii.a2b_uu(x)
#     b = binascii.hexlify(b)
#     y = str(b, 'ascii')
    #codecs.encode(x, "hex")
    #print(b, y)

def checLine(dataLine):
    #= ":106B5000762E332E322E300043453133303037001D"                    # Master hex line to change

    dataLine = dataLine.strip()                                         # Remove White Spaces
    dataLen = len(dataLine)                                             # get data length
    startByte = dataLine[:1]                                            # Get start Byte ":"
    byteCount = dataLine[1:3]                                           # Get byte count
    BCHexToDec = int(byteCount, 16)                                     # convert byte count from Hex to Dec
    addressCode = dataLine[3:7]                                         # get the address
    addressToDec = int(addressCode, 16)                                 # convert the address from Hex to Dec
    recordType = dataLine[7:9]                                          # get record type
    recordTypeToDec = int(recordType, 16)                               # convert record type to Dec
    dataFL = dataLine[9: 9 + 2 * BCHexToDec]                            # get data from line
    checksum = dataLine[9 + 2 * BCHexToDec: 9 + 2 * BCHexToDec + 2]     # get checksum from line data

    err = ""

    LenOk = (9 + (2 * BCHexToDec) + 2)                                  # Check if some bytes are missing
    checksumDec = "NULL"                                                # if no checksum in data provided, without if condition
    if dataLen ==  LenOk:                                               # checksumDec get some data out of the line which throw exception
        # print("----------------dataLine OK-------------------")
        checksumDec = int(checksum, 16)                                 # get the Dec checksum from Hex Value
    else:
        err += "Hex line too short! some bytes are missing! \n"
        # print(dataLen, LenOk)



    typeString = typeStringfunc(recordTypeToDec)                        # init Record type

    checksumVerify = 0
    for x in range(0, BCHexToDec + 4, 1):                               # Checksum verification
        res = int(dataLine[1+x*2:3+x*2], 16)
        checksumVerify += res

    checksumVerify = checksumVerify % 256                               # get the modulo
    if checksumVerify > 0:
        checksumVerify = 256 - checksumVerify                           # sub if modulo is greater than 256

                                                                # error management
    if startByte != ":" :
        err += "Start byte : missing \n"                                # check for ":" if missing
    if dataLen < (BCHexToDec * 2) + 9:
        err += "Hex line too short! some bytes are missing! \n"         # check if data is missing
    if checksumDec != checksumVerify:
        err += "checksum missmatch! \n"                                 # compare checksum from line and calculated

    checksumVerifyResult = (hex(checksumVerify).split('x')[-1]).upper() # convert checksum to Hex uppercase

    # print("Address: ", addressCode)
    # print("Byte count: ", byteCount)
    # print("Record type: ", recordType, typeString)
    # print("Checksum: ", checksum, "\n")

    if len(checksumVerifyResult) == 1:                                  # add a ignored leading 0 to checksum, example: 0E gives E with a missing 0 after convertion Dec->Hex
        # print("----------------",len(checksumVerifyResult), "----------------")
        # print("Calculated Checksum: ", checksumVerifyResult.zfill(2))
        checksumVerifyResult = checksumVerifyResult.zfill(2)
    # else:
    #     print("Calculated Checksum: ", checksumVerifyResult)


    # print(err)
    # print("**************************************************")
    LAR = (err ,addressCode, byteCount, recordType, typeString, checksum, checksumVerifyResult)
    return LAR              # Line Analysed Result


def typeStringfunc(argument):                                       # data type function
    switcher = {
        0:"Data",
        1:"End Of File",
        2:"Extended Segment Address",
        3:"Start Segment Address",
        4:"Extended Linear Address",
        5:"Start Linear Address",
    }
    return switcher.get(argument, "Unknown ")


# checLine(':106B5000762E332E322E30004345313330303700')
