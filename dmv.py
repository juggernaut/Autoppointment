import sys

from bs4 import BeautifulSoup
import requests

OFFICES = {
    'DALY CITY': '599',
    'SAN MATEO': '593',
    'SAN FRANCISCO': '503',
    'SANTA CLARA': '632',
}

def main():
    for oname, oid in OFFICES.iteritems():
        earliest = get_earliest_appointment(oid)
        if earliest:
            print 'The earliest appointment in %s is on %s' % (oname, earliest)
    return 0


def get_earliest_appointment(city_id):
    data = {'officeId': str(city_id), 'numberItems': '1', 'taskDL': 'true', 'firstName': 'AMEYA', 'lastName': 'LOKARE', 'telArea': '900', 'telPrefix':'310', 'telSuffix': '0000', 'resetCheckFields': 'true'}
    r = requests.post('https://www.dmv.ca.gov/wasapp/foa/findOfficeVisit.do', data = data)
    soup = BeautifulSoup(r.content)
    #print soup.prettify()
    for p in soup.find_all('p', 'alert'):
        if not p.text.startswith('The first available appointment'):
            return p.text


if __name__ == '__main__':
    sys.exit(main())
