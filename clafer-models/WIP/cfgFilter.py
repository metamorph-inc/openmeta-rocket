import csv
"""
with open('data-2018-05-08-01.csv', 'r') as data:
    startline = 1
    counter = 0
    csvfile = csv.reader(data, delimiter=",")
    passDict = dict()
    for line in csvfile:
        if counter < startline:
            counter += 1
        else:
            if float(line[0]) > 1500 and float(line[0]) < 1700:
                if float(line[5]) < 5:
                    if float(line[7]) > 2:
                        if float(line[9]) < 150:
                            if float(line[10]) < 343:
                                if float(line[14]) > 15:
                                    if '{}'.format(line[3]) in passDict.keys():
                                        passDict['{}'.format(line[3])] += 1
                                    else:
                                        passDict['{}'.format(line[3])] = 1
    with open('C:\\Users\\austin\\Desktop\\frequency1.txt','w') as testout:
        sortDict = dict()
        for k,v in passDict.iteritems():
            testout.write("{0}: {1}\n".format(k,v))
            sortDict['{}'.format(k)] = v
    testout.close()
    keys = sortDict.keys()
    keys.sort(key=lambda k:(k[0:2], int(k[3:])))
    with open('C:\\Users\\austin\\Desktop\\cfgs1.txt','w') as testout:
        for key in keys:
            testout.write("{0}\n".format(key))
    testout.close()
"""
with open('C:\\Users\\austin\\Desktop\\cfgs1.txt','r') as testout:
    with open('C:\\Users\\austin\\Desktop\\editcfgs1.txt','w') as test:
        for line in testout:
            line.replace(",","\n")
            test.write("{0}".format(line))
    test.close()
testout.close()
