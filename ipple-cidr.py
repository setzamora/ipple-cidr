import csv
import re
import sys


def readcsv(*argv):
    for filename in argv[0]:
        filename = filename.strip()
    csvreader = csv.reader(open(filename))
    for row in csvreader:
        maskbit = getcidriprange(row[0], row[1])
        print(row[0] + ' to ' + row[1] + ' => ' + row[0] + '/' + str(maskbit))


def getcidriprange(ip1, ip2):
    rangedictionary = {0: 0, 1: 1, 3: 2, 7: 3, 15: 4, 31: 5, 63: 6, 127: 7, 255: 8}
    cl = [0, 0, 0, 0]

    a1, a2 = splitipaddress(ip1, ip2)
    for i in range(len(cl)):
        if differencelist(a2, a1, i) in rangedictionary:
            cl[i] = 8 - rangedictionary[differencelist(a2, a1, i)]
        else:
            print('Error in converting to CIDR notation')
            sys.exit()

    maskbit = sumlist(cl)
    return maskbit


def sumlist(list):
    s = 0
    for v in list:
        s += v
    return s


def differencelist(la, lb, idx):
    if not len(la) == len(lb):
        print('Invalid list size')
        return None

    if len(la) < idx:
        print('Invalid index')
        return None

    return int(la[idx]) - int(lb[idx])


def splitipaddress(ip1, ip2):
    if not checkipaddress(ip1):
        print('First IP address is invalid ' + ip1)

    if not checkipaddress(ip2):
        print('Second IP address is invalid ' + ip2)

    li1 = ip1.split('.')
    li2 = ip2.split('.')

    return (li1, li2)


def checkipaddress(ip):
    ipregex = r'^(([1-9]?[0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5]).){3}'
    ipregex = ipregex + r'([1-9]?[0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])$'
    ipaddressregex = re.compile(ipregex)
    match = ipaddressregex.match(ip)
    if match is not None:
        return True
    else:
        return False


if __name__ == "__main__":
    param = sys.argv
    readcsv(param)
