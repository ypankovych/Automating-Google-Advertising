import subprocess
import time

from bs4 import BeautifulSoup

from settings import alpha_path, alpha_time, target


def detect_url(element):
    # check for equality of domains
    result = BeautifulSoup(str(element), 'html.parser').find('div', class_='ads-visurl')
    return target in result.cite.text


def find_ads(html_content):
    # find ads on the page
    soup = BeautifulSoup(html_content, 'html.parser')
    ad = [x for x in soup.find_all('li', class_='ads-ad') if detect_url(x)]
    return ad[0] if ad else False


def run_alpha():
    with subprocess.Popen(alpha_path) as alpha:
        time.sleep(alpha_time)
        alpha.terminate()
