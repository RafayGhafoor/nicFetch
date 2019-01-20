import os
import csv
import requests
import bs4


def get_cnic_from_csv(filepath, limit=10):
    '''Obtain CNIC's from file (csv) alongwith their names and returns a dictionary object.

    Example:

    {"Name": "CNIC"}
    '''
    with open(filepath, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        NICS = {nic['Name']: nic['NIC'] for num, nic in enumerate(reader) if num < limit}  # Maps CNICS to Names
    return NICS


def get_cnic_info(cnic):
    '''Obtain CNIC information from wanavisa site.
    
    Returns:

    Dictionary object containing key, value pairs as:-
    {'Gender': 'Gender_info', 'Province': "Punjab|Sindh|Punjab"...}
    '''
    categories = ['Gender', 'Province', 'Divison', 'District']

    try:
        cnic = cnic.replace('-', '').lower()
        int(cnic)
        
        if len(cnic) != 13:
            print("CNIC is invalid")
        
        else:
            r = requests.get('http://wanavisa.com/find-id-card-detail-nadra.php?number={}'.format(cnic))
            soup = bs4.BeautifulSoup(r.content, 'lxml')
            try:
                info = soup.find('table', class_='table table-striped').findAll('td')
                info_gathered = {category: user_info.text.strip() for category, user_info in zip(categories, info)}
            except:
                return

        return info_gathered    
   
    except ValueError:
        print("CNIC is invalid")
    

def main():
    cnic_dict = get_cnic_from_csv('/home/rafay/Downloads/Telegram Desktop/names.csv', 20)

    for username, cnic in cnic_dict.items():

        personal_info = get_cnic_info(cnic)

        if personal_info is not None:
            print("============Information for {}============\n".format(username))
            for category, user_info in personal_info.items():
                print("{}: {}\n".format(category, user_info))
            print()


if __name__ == '__main__':
    main()




