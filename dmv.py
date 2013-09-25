import argparse
import sys

from bs4 import BeautifulSoup
import requests

OFFICES = {
    'DALY CITY': '599',
    'SAN MATEO': '593',
    'SAN FRANCISCO': '503',
    'SANTA CLARA': '632',
}

def main(args):
    args = parse_args(args)
    post_data = build_post_data(args)
    try:
        for oname, oid in OFFICES.iteritems():
            post_data['officeId'] = oid
            earliest = get_earliest_appointment(post_data)
            if earliest:
                print 'The earliest appointment in %s is on %s' % (oname, earliest)
        return 0
    except:
        return 1


def parse_args(args):
    parser = argparse.ArgumentParser()
    parser.add_argument('--firstname', required=True, type=lambda s: s.upper())
    parser.add_argument('--lastname', required=True, type=lambda s: s.upper())
    parser.add_argument('--phone', required=True, type=telephone)
    return parser.parse_args(args)


def telephone(arg):
    """
    Parses the telephone number
    """
    if arg.startswith('+1'):
        arg = arg[2:]
    if len(arg) == 10:
        return arg[:3], arg[3:6], arg[6:10]

def build_post_data(args):
    return {'numberItems': '1', 'taskDL': 'true', 'firstName': args.firstname, 'lastName': args.lastname, 'telArea': args.phone[0], 'telPrefix': args.phone[1], 'telSuffix': args.phone[2], 'resetCheckFields': 'true'}


def get_earliest_appointment(data):
    r = requests.post('https://www.dmv.ca.gov/wasapp/foa/findOfficeVisit.do', data = data)
    soup = BeautifulSoup(r.content)
    #print soup.prettify()
    for p in soup.find_all('p', 'alert'):
        if not p.text.startswith('The first available appointment'):
            return p.text


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
