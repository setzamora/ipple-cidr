import csv
import re
import sys
from prettytable import PrettyTable

def read_csv(*argv):
    for filename in argv[0]:
        filename = filename.strip()
    table = PrettyTable(['FROM', 'TO', 'CIDR'])
    table.align = 'r'
    csv_reader = csv.reader(open(filename))
    for row in csv_reader:
        mask_bit = get_cidr_ip_range(row[0], row[1])
        table.add_row([row[0], row[1], row[0] + '/' + str(mask_bit)])
    print(table)


def get_cidr_ip_range(ip_address_1, ip_address_2):
    range_dictionary = {0: 0, 1: 1, 3: 2, 7: 3, 15: 4, 31: 5, 63: 6, 127: 7, 255: 8}
    cl = [0, 0, 0, 0]

    address_1, address_2 = split_ip_address(ip_address_1, ip_address_2)
    for i in range(len(cl)):
        if difference_list(address_2, address_1, i) in range_dictionary:
            cl[i] = 8 - range_dictionary[difference_list(address_2, address_1, i)]
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


def split_ip_address(ip_address_1, ip_address_2):
    if not check_ip_address(ip_address_1):
        print('First IP address is invalid ' + ip_address_1)

    if not check_ip_address(ip_address_2):
        print('Second IP address is invalid ' + ip_address_2)

    li_1 = ip_address_1.split('.')
    li_2 = ip_address_2.split('.')

    return (li_1, li_2)


def check_ip_address(ip):
    ip_regex = r'^(([1-9]?[0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5]).){3}'
    ip_regex = ip_regex + r'([1-9]?[0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])$'
    ip_address_regex = re.compile(ip_regex)
    match = ip_address_regex.match(ip)
    if match is not None:
        return True
    else:
        return False


if __name__ == "__main__":
    param = sys.argv
    read_csv(param)
