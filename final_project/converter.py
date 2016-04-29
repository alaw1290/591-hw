'''
Converter: takes in stock indicies data and reorders them and convert them to gmt time as well as
           two additional columns: percent change and absolute percent change
'''
import datetime
from time import mktime

data_folder = 'data/'

def converter(fileName):
    # print "Ordered" + fileName
    # return 1
    ordered = open(data_folder + "Ordered_" + fileName, 'w')
    previousPrice = 0
    for line in reversed(open(data_folder+fileName).readlines()):
        lin = line.split('\t')
        print lin
        cPrice = float(lin[1])
        example = lin[0]
        example = example.replace(":","-")
        example = example.replace(" ","-")
        example = example.split("-")
        start =datetime.datetime(int(example[0]),int(example[1]),int(example[2]),int(example[3]),int(example[4]),int(example[5]))
        uni = mktime(start.timetuple())
        if previousPrice == 0:
            pChange = 0
        elif previousPrice < cPrice:
            pChange = (cPrice/previousPrice - 1)*100
        elif previousPrice > cPrice:
            pChange = -(previousPrice/cPrice -1)*100
        elif previousPrice == cPrice:
            pChange = 0
        ordered.write(str(int(uni)) +" " + lin[1] +" "  + str(pChange)+" " + str(abs(pChange)) + "\n")
        previousPrice = cPrice
    
    ordered.close()