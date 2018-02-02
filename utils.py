from bs4 import BeautifulSoup, SoupStrainer
import requests
import csv
import os


def get_announcements(count=10):
    print('Getting announcements...')
    url = 'http://www.civil.upatras.gr/el/Tmima/Anouncements/'
    r = requests.get(url)
    data = r.content

    get_only_bullet = SoupStrainer(class_='bullet')

    soup = BeautifulSoup(data, 'html.parser', parse_only=get_only_bullet)

    announcements = soup.find_all(class_='bullet')

    announcements_list = []
    for item in announcements[:count]:
        date = item.text[:10]
        title = item.br.previous
        link = item.a.get('href')
        announcements_list.append({'date': date, 'title': title, 'link': link})

    try:
        dict_to_csv(announcements_list, 'announcements.csv')
        print('Announcements saved at: {}'.format("'announcements.csv'"))
    except IOError as e:
        print("I/O error({0}): {1}".format(e.errno, e.strerror))


def get_single_announcement(link):
    url = 'http://www.civil.upatras.gr' + link
    print('Getting announcement for {} \n'.format(url))
    output = ''
    d = {}

    r = requests.get(url)
    data = r.content

    soup = BeautifulSoup(data, 'html.parser')

    res = soup.find(class_='main_topic_text')
    for text in res.stripped_strings:
        if not text == 'Επιστροφή':
            output += text + '\n'

    output += '\nLinks:'
    links = res.findAll('a')
    for link in links:
        if not link.text == 'Επιστροφή':
            if not link.text == link.get('href'):
                d[link.text] = link.get('href')
            else:
                d[link.get('href')] = link.get('href')
    return output, d


def formatted_print(st, width=75):
    output = ''
    para = st.split("\n")
    for p in para:
        st = p.split()
        out = ""
        while True:
            while len(st) > 0 and len(out + st[0]) < width:
                out = " ".join([out, st.pop(0)])
            output += out + '\n'
            out = ""
            if len(st) == 0:
                break
    return output


def csv_to_dict(fname='announcements.csv'):
    try:
        dl = []
        infile = csv.DictReader(open(fname, mode='r'), delimiter=';')
        for row in infile:
            dl.append(row)
        return [dict(x) for x in dl]
    except:
        return []


def dict_to_csv(dl, fname='announcements.csv'):
    # αποθηκεύει μια λίστα από λεξικά dl σε ένα αρχείο csv με όνομα fname
    try:
        with open(fname, 'w', encoding='utf-8') as fout:
            w = csv.DictWriter(fout, fieldnames=dl[0].keys(), delimiter=';')
            w.writerow(dict((x, x) for x in dl[0].keys()))
            w.writerows(dl)
        return True
    except:
        return False


def print_to_screen(dlist):
    print('Announcements')
    for i, item in enumerate(dlist):
        date = item['date']
        title = item['title']
        if len(title) > 50:
            title = title[0:50] + "..."
        print('{no:3d} | {date} | {title}'.format(no=i + 1, date=date, title=title))
    print('')


def get_announcements(count=10):
    print('Getting announcements...')
    url = 'http://www.civil.upatras.gr/el/Tmima/Anouncements/'
    r = requests.get(url)
    data = r.content

    get_only_bullet = SoupStrainer(class_='bullet')

    soup = BeautifulSoup(data, 'html.parser', parse_only=get_only_bullet)

    announcements = soup.find_all(class_='bullet')

    announcements_list = []
    for item in announcements[:count]:
        date = item.text[:10]
        title = item.br.previous
        link = item.a.get('href')
        announcements_list.append({'date': date, 'title': title, 'link': link})

    dict_to_csv(announcements_list, 'announcements.csv')


def get_single_announcement(link):
    url = 'http://www.civil.upatras.gr' + link
    output = ''
    d = {}

    r = requests.get(url)
    data = r.content

    soup = BeautifulSoup(data, 'html.parser')

    res = soup.find(class_='main_topic_text')
    for text in res.stripped_strings:
        if not text == 'Επιστροφή':
            output += text + '\n'

    output += '\nLinks:'
    links = res.findAll('a')
    for link in links:
        if not link.text == 'Επιστροφή':
            if not link.text == link.get('href'):
                d[link.text] = link.get('href')
            else:
                d[link.get('href')] = link.get('href')
    return output, d


def cls_():
    os.system('cls' if os.name == 'nt' else 'clear')
