def binToDec(inNum):
    numberx=inNum
    dec_number= int(numberx, 2)
    return (dec_number)
    #print('The decimal conversion is:', dec_number)
    #print(type(dec_number))
print(binToDec(input("Enter binary number: ")))