import csv
import re
import sys


def read_csv(*argv):
    for filename in argv[0]:
        filename = filename.strip()
    csv_reader = csv.reader(open(filename))
    for row in csv_reader:
        mask_bit = get_cidr_ip_range(row[0], row[1])
        print(row[0] + ' to ' + row[1] + ' => ' + row[0] + '/' + str(mask_bit))


def get_cidr_ip_range(ip1, ip2):
    range_dictionary = {0: 0, 1: 1, 3: 2, 7: 3, 15: 4, 31: 5, 63: 6, 127: 7, 255: 8}
    cl = [0, 0, 0, 0]

    a1, a2 = split_ip_address(ip1, ip2)
    for i in range(len(cl)):
        if difference_list(a2, a1, i) in range_dictionary:
            cl[i] = 8 - range_dictionary[difference_list(a2, a1, i)]
        else:
            print('Error in converting to CIDR notation')
            sys.exit()

    mask_bit = sum_list(cl)
    return mask_bit


def sum_list(list):
    s = 0
    for v in list:
        s += v
    return s


def difference_list(la, lb, idx):
    if not len(la) == len(lb):
        print('Invalid list size')
        return None

    if len(la) < idx:
        print('Invalid index')
        return None

    return int(la[idx]) - int(lb[idx])


def split_ip_address(ip1, ip2):
    if not check_ip_address(ip1):
        print('First IP address is invalid ' + ip1)

    if not check_ip_address(ip2):
        print('Second IP address is invalid ' + ip2)

    li1 = ip1.split('.')
    li2 = ip2.split('.')

    return (li1, li2)


def check_ip_address(ip):
    ip_regex = r'^(([1-9]?[0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5]).){3}'
    ip_regex = ip_regex + r'([1-9]?[0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])$'
    ipaddressregex = re.compile(ip_regex)
    match = ipaddressregex.match(ip)
    if match is not None:
        return True
    else:
        return False


if __name__ == "__main__":
    param = sys.argv
    read_csv(param)
