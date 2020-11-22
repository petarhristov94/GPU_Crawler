from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from datetime import datetime
from playsound import playsound
import time
import os
import requests
import pandas
import subprocess

CHROME_PROFILE_PATH = r'C:\Users\phris\AppData\Local\Google\Chrome\User Data'
DESKTOP_PATH = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')
XLSX_FILE_DATE = datetime.now().strftime("%d-%m-%Y_%H-%M-%S")
XLSX_FILE_NAME = 'products_' + XLSX_FILE_DATE + '_.xlsx'
XLSX_PATH = DESKTOP_PATH + '\\' + XLSX_FILE_NAME
CRAWLER_DRIVER_PATH = r'D:\OMG\Custom WebDriver' + '\\' + 'chromedriver_first.exe'
SOUND_CHEAP_ITEM = "cheap_item.wav"
SCRIPT_START_TIME = datetime.now().strftime("%d.%m.%Y at %H:%M:%S")
# crawl Websites every 300 seconds
CRAWL_WEBSITES_SCHEDULE = 300.0

loop = False


DATAFRAME_COLUMNS = ['Availability', 'Maker', 'Name', 'Chip', 'Price', 'Location', 'Buy Link']

CHIP_NAME_3060 = 'NVIDIA GeForce RTX 3060'
CHIP_NAME_3060Ti = 'NVIDIA GeForce RTX 3060 Ti'
CHIP_NAME_3070 = 'NVIDIA GeForce RTX 3070'
CHIP_NAME_3080 = 'NVIDIA GeForce RTX 3080'
CHIP_NAME_3090 = 'NVIDIA GeForce RTX 3090'
CHIP_NAME_6800 = 'AMD Radeon RX 6800'
CHIP_NAME_6800XT = 'AMD Radeon RX 6800 XT'
CHIP_NAME_6900 = 'AMD Radeon RX 6900'
CHIP_NAME_6900XT = 'AMD Radeon RX 6900 XT'

PRICE_CHIP_DICT = {CHIP_NAME_3060: 0.0,
                   CHIP_NAME_3060Ti: 0.0,
                   CHIP_NAME_3070: 560.0,
                   CHIP_NAME_3080: 750.0,
                   CHIP_NAME_3090: 1510.0,
                   CHIP_NAME_6800: 600.0,
                   CHIP_NAME_6800XT: 750.0,
                   CHIP_NAME_6900: 0.0,
                   CHIP_NAME_6900XT: 1100.0}

urls = [
    'https://www.alternate.de/Outlet/Grafikkarten/RTX-3070',
    'https://www.alternate.de/Outlet/Grafikkarten/RTX-3080',
    'https://www.alternate.de/Outlet/Grafikkarten/RTX-3090',
    'https://www.alternate.de/Outlet/Grafikkarten/AMD-Grafikkarten',
    'https://www.alternate.de/Grafikkarten/RTX-3070',
    'https://www.alternate.de/Grafikkarten/RTX-3080',
    'https://www.alternate.de/Grafikkarten/RTX-3090',
    'https://www.alternate.de/Grafikkarten/RX-6800',
    'https://www.alternate.de/Grafikkarten/RX-6800-XT',
    'https://www.alternate.de/Grafikkarten/RX-6900-XT',
    'https://www.alternate.be/Hardware/Grafische-kaarten/AMD/Radeon-RX/RX-6800',
    'https://www.alternate.be/Hardware/Grafische-kaarten/AMD/Radeon-RX/RX-6800-XT',
    'https://www.alternate.be/Hardware/Grafische-kaarten/AMD/Radeon-RX/RX-6900-XT',
    'https://www.alternate.be/Hardware/Grafische-kaarten/NVIDIA/RTX-3070',
    'https://www.alternate.be/Hardware/Grafische-kaarten/NVIDIA/RTX-3080',
    'https://www.alternate.be/Hardware/Grafische-kaarten/NVIDIA/RTX-3090',
    'https://www.alternate.be/Outlet/Hardware/Grafische-kaarten',
    'https://www.alternate.nl/Outlet/Grafische-kaarten',
    'https://www.alternate.nl/Grafische-kaarten/RX-6800',
    'https://www.alternate.nl/Grafische-kaarten/RX-6800-XT',
    'https://www.alternate.nl/Grafische-kaarten/RX-6900-XT',
    'https://www.alternate.nl/Grafische-kaarten/RTX-3070',
    'https://www.alternate.nl/Grafische-kaarten/RTX-3080',
    'https://www.alternate.nl/Grafische-kaarten/RTX-3090',
    'https://www.notebooksbilliger.de/pc+hardware/grafikkarten/nvidia/geforce+rtx+3070+nvidia/page/1?sort=price&order=asc&availability=alle',
    'https://www.notebooksbilliger.de/pc+hardware/grafikkarten/nvidia/geforce+rtx+3080+nvidia/page/1?sort=price&order=asc&availability=alle',
    'https://www.notebooksbilliger.de/pc+hardware/grafikkarten/nvidia/geforce+rtx+3090+nvidia/page/1?sort=price&order=asc&availability=alle',
    'https://www.notebooksbilliger.de/pc+hardware/grafikkarten+pc+hardware/amdati/rx+6800/page/1?sort=price&order=asc&availability=alle',
    'https://www.notebooksbilliger.de/pc+hardware/grafikkarten+pc+hardware/amdati/rx+6800+xt/page/1?sort=price&order=asc&availability=alle',
    'https://www.notebooksbilliger.de/pc+hardware/grafikkarten+pc+hardware/amdati/rx+6900+xt/page/1?sort=price&order=asc&availability=alle',
    'https://www.mindfactory.de/Hardware/Grafikkarten+(VGA)/GeForce+RTX+fuer+Gaming/RTX+3070.html/listing_sort/6',
    'https://www.mindfactory.de/Hardware/Grafikkarten+(VGA)/GeForce+RTX+fuer+Gaming/RTX+3080.html/listing_sort/6',
    'https://www.mindfactory.de/Hardware/Grafikkarten+(VGA)/GeForce+RTX+fuer+Gaming/RTX+3090.html/listing_sort/6',
    'https://www.mindfactory.de/Hardware/Grafikkarten+(VGA)/Radeon+RX+Serie/RX+6800.html/listing_sort/6',
    'https://www.mindfactory.de/Hardware/Grafikkarten+(VGA)/Radeon+RX+Serie/RX+6800+XT.html/listing_sort/6',
    'https://www.mindfactory.de/Hardware/Grafikkarten+(VGA)/Radeon+RX+Serie/RX+6900+XT.html/listing_sort/6',
    'https://www.caseking.de/pc-komponenten/grafikkarten/nvidia/geforce-rtx-3070?p=1&l=list&sSort=3&n=48',
    'https://www.caseking.de/pc-komponenten/grafikkarten/nvidia/geforce-rtx-3080?p=1&l=list&sSort=3&n=48',
    'https://www.caseking.de/pc-komponenten/grafikkarten/nvidia/geforce-rtx-3090?p=1&l=list&sSort=3&n=48',
    'https://www.caseking.de/pc-komponenten/grafikkarten/amd/radeon-rx-6800?sPerPage=48&sPage=1&sSort=3',
    'https://www.caseking.de/pc-komponenten/grafikkarten/amd/radeon-rx-6800-xt?sPerPage=48&sPage=1&sSort=3',
    'https://www.caseking.de/pc-komponenten/grafikkarten/amd/radeon-rx-6900-xt?sPerPage=48&sPage=1&sSort=3',
    'https://www.cyberport.de/pc-und-zubehoer/komponenten/grafikkarten/nvidia-fuer-gaming.html?productsPerPage=120&sort=popularity&2E_Grafikchip=GeForce%20RTX%203070,GeForce%20RTX%203080,GeForce%20RTX%203090&page=1',
    'https://www.cyberport.de/pc-und-zubehoer/komponenten/grafikkarten/amd-fuer-gaming.html?productsPerPage=120&sort=price_asc&2E_Grafikchip=Radeon%206800,Radeon%206800%20XT,Radeon%206900%20XT&page=1',
    'https://www.conrad.de/de/o/grafikkarten-amd-chipsatz-0414055.html?sort=Price-asc&tfo_ATT_LOV_GRAPHIC_CARD_MODELS=RX%206800%20XT~~~RX%206800~~~RX%206900%20XT',
    'https://www.conrad.de/de/o/grafikkarten-nvidia-chipsatz-0414054.html?sort=Price-asc&tfo_ATT_LOV_GRAPHIC_CARD_MODELS=RTX%203070~~~RTX%203080~~~RTX%203090'
]

STRING_ALTERNATE_NL = 'alternate.nl'
STRING_ALTERNATE_BE = 'alternate.be'
STRING_ALTERNATE = 'alternate.de'
STRING_MINDFACTORY = 'mindfactory.de'
STRING_NOTEBOOKSBILLIGER = 'notebooksbilliger.de'
STRING_CYBERPORT = 'cyberport.de'
STRING_CONRAD = 'conrad.de'
STRING_CASEKING = 'caseking.de'

global SCRIPT_LAST_RUN_TIME
global sub_driver


class Product:
    def __init__(self, maker, name, chip, price, location, buyLink, available):
        self.maker = maker
        self.name = name
        self.chip = chip
        self.price = price
        self.location = location
        self.buyLink = buyLink
        self.available = available

    def to_dict(self):
        return {
            'Availability': self.available,
            'Maker': self.maker,
            'Name': self.name,
            'Chip': self.chip,
            'Price': self.price,
            'Location': self.location,
            'Buy Link': self.buyLink
        }


def crawlWebsite(url):
    products = []
    response = requests.get(url)
    if url.__contains__(STRING_ALTERNATE):
        products = alternate(response, url)
    elif url.__contains__(STRING_ALTERNATE_BE):
        products = alternate_be(response, url)
    elif url.__contains__(STRING_ALTERNATE_NL):
        products = alternate_nl(response, url)
    elif url.__contains__(STRING_MINDFACTORY):
        products = mindfactory(response, url)
    elif url.__contains__(STRING_NOTEBOOKSBILLIGER):
        products = notebooksbilliger(response, url)
    elif url.__contains__(STRING_CYBERPORT):
        products = cyberport(response, url)
    elif url.__contains__(STRING_CONRAD):
        products = conrad(response, url)
    elif url.__contains__(STRING_CASEKING):
        products = caseking(response, url)
    return products


def alternate(response, url):
    products = []
    print("▶ Working on: " + STRING_ALTERNATE + "   🌎 " + url)
    class_to_search = "listRow"

    if response.status_code == 404 or response.status_code == 502:
        print("☠ Page Not Found.\n")
    else:
        domain = response.request.url.replace(response.request.path_url, "")
        try:
            linkSortList = BeautifulSoup(response.text, features="html.parser").find(class_="list").attrs['href']
            response = requests.get(domain + linkSortList)
        except:
            pass
        # Check if REQUEST is being blocked
        if BeautifulSoup(response.text, features="html.parser").findAll(class_=class_to_search).__len__() == 0:
            print("⚡ Request blocked. Trying with Selenium...")
            options = webdriver.ChromeOptions()
            options.add_argument('--no-proxy-server')
            options.add_argument("--window-position=-700,0")
            options.add_argument("--window-size=576,1024")
            options.add_argument('--blink-settings=imagesEnabled=false')
            # options.add_argument('user-data-dir=' + chrome_profile_path)
            driver = webdriver.Chrome(options=options)
            try:
                driver.get(url)
            except Exception as e:
                print("☠ Non existent URL: " + url)
                driver.close()
                return products
            # Sort in a list
            try:
                driver.find_element_by_xpath('//*[@id="pageContent"]/div[4]/div[1]/div[2]/a[1]').click()
            except Exception as e:
                print("Sorting Button couldn't be clicked. Continue like that.")

            soup = BeautifulSoup(driver.page_source, features="html.parser")
        else:
            soup = BeautifulSoup(response.text, features="html.parser")
        try:
            for a in soup.findAll('div', attrs={'class': class_to_search}):
                maker = a.find(class_='name').findAll('span')[0].text.strip()
                name = a.find(class_='name').findAll('span')[1].text.strip().split(',', 1)[0]
                maker = 'ZOTAC GAMING' if maker.upper().__contains__('ZOTAC') else maker
                chip = getChipName(name)
                price = float(a.find(class_='price right right10').text
                              .replace('-', '00').strip('€').strip('*').strip()
                              .replace('.', '').replace(',', '.'))
                location = getDomainFromURL(url) + ' Outlet' if url.__contains__('Outlet') else getDomainFromURL(url)
                buy = domain + a.find(class_='productLink').attrs['href']
                tmp_avlb = a.find(class_='stockStatus').text
                if tmp_avlb.__contains__("Auf Lager"):
                    available = 'YES'
                elif tmp_avlb.__contains__("Liefertermin"):
                    available = 'NO'
                elif tmp_avlb.__contains__("neu eingetroffen"):
                    available = 'SOON'
                else:
                    available = 'UNKNOWN'
                product = Product(maker.upper(), name, chip, price, location, buy, available)
                products.append(product)
            try:
                driver.close()
            except UnboundLocalError as e:
                pass
            print('☑ Done.\n')
        except Exception as e:
            print("ⓧ Failed.\n")
    return products


def alternate_nl(response, url):
    products = []
    print("▶ Working on: " + STRING_ALTERNATE_NL + "   🌎 " + url)
    class_to_search = "listRow"

    if response.status_code == 404 or response.status_code == 502:
        print("☠ Page Not Found.\n")
    else:
        domain = response.request.url.replace(response.request.path_url, "")
        try:
            linkSortList = BeautifulSoup(response.text, features="html.parser").find(class_="list").attrs['href']
            response = requests.get(domain + linkSortList)
        except:
            pass
        # Check if REQUEST is being blocked
        if BeautifulSoup(response.text, features="html.parser").findAll(class_=class_to_search).__len__() == 0:
            print("⚡ Request blocked. Trying with Selenium...")
            options = webdriver.ChromeOptions()
            options.add_argument('--no-proxy-server')
            options.add_argument("--window-position=-700,0")
            options.add_argument("--window-size=576,1024")
            options.add_argument('--blink-settings=imagesEnabled=false')
            # options.add_argument('user-data-dir=' + chrome_profile_path)
            driver = webdriver.Chrome(options=options)
            try:
                driver.get(url)
            except Exception as e:
                print("☠ Non existent URL: " + url)
                driver.close()
                return products
            # Sort in a list
            try:
                driver.find_element_by_xpath('//*[@id="pageContent"]/div[4]/div[1]/div[2]/a[1]').click()
            except Exception as e:
                print("Sorting Button couldn't be clicked. Continue like that.")

            soup = BeautifulSoup(driver.page_source, features="html.parser")
        else:
            soup = BeautifulSoup(response.text, features="html.parser")
        try:
            for a in soup.findAll('div', attrs={'class': class_to_search}):
                maker = a.find(class_='name').findAll('span')[0].text.strip()
                maker = 'ZOTAC GAMING' if maker.upper().__contains__('ZOTAC') else maker
                name = a.find(class_='name').findAll('span')[1].text.strip().split(',', 1)[0].replace('grafische kaart',
                                                                                                      '').strip()
                chip = getChipName(name)
                price = float(a.find(class_='price right right10').text
                              .replace('-', '00').strip('€').strip('*').strip()
                              .replace('.', '').replace(',', '.'))
                location = getDomainFromURL(url) + ' Outlet' if url.__contains__('Outlet') else getDomainFromURL(url)
                buy = domain + a.find(class_='productLink').attrs['href']
                tmp_avlb = a.find(class_='stockStatus').text
                if tmp_avlb.__contains__("Direct leverbaar"):
                    available = 'YES'
                elif tmp_avlb.__contains__("Pre-order") or tmp_avlb.__contains__("Preorder"):
                    available = 'NO'
                elif tmp_avlb.__contains__("Verwachte levertermijn") or tmp_avlb.__contains__("werkdagen"):
                    available = 'SOON'
                else:
                    available = 'UNKNOWN'
                product = Product(maker.upper(), name, chip, price, location, buy, available)
                products.append(product)
            try:
                driver.close()
            except UnboundLocalError as e:
                pass
            print('☑ Done.\n')
        except Exception as e:
            print("ⓧ Failed.\n")
    return products


def alternate_be(response, url):
    products = []
    print("▶ Working on: " + STRING_ALTERNATE_BE + "   🌎 " + url)
    class_to_search = "listRow"

    if response.status_code == 404 or response.status_code == 502:
        print("☠ Page Not Found.\n")
    else:
        domain = response.request.url.replace(response.request.path_url, "")
        try:
            linkSortList = BeautifulSoup(response.text, features="html.parser").find(class_="list").attrs['href']
            response = requests.get(domain + linkSortList)
        except:
            pass
        # Check if REQUEST is being blocked
        if BeautifulSoup(response.text, features="html.parser").findAll(class_=class_to_search).__len__() == 0:
            print("⚡ Request blocked. Trying with Selenium...")
            options = webdriver.ChromeOptions()
            options.add_argument('--no-proxy-server')
            options.add_argument("--window-position=-700,0")
            options.add_argument("--window-size=576,1024")
            options.add_argument('--blink-settings=imagesEnabled=false')
            # options.add_argument('user-data-dir=' + chrome_profile_path)
            driver = webdriver.Chrome(options=options)
            try:
                driver.get(url)
            except Exception as e:
                print("☠ Non existent URL: " + url)
                driver.close()
                return products
            # Sort in a list
            try:
                driver.find_element_by_xpath('//*[@id="pageContent"]/div[4]/div[1]/div[2]/a[1]').click()
            except Exception as e:
                print("Sorting Button couldn't be clicked. Continue like that.")

            soup = BeautifulSoup(driver.page_source, features="html.parser")
        else:
            soup = BeautifulSoup(response.text, features="html.parser")
        try:
            for a in soup.findAll('div', attrs={'class': class_to_search}):
                maker = a.find(class_='name').findAll('span')[0].text.strip()
                maker = 'ZOTAC GAMING' if maker.upper().__contains__('ZOTAC') else maker
                name = a.find(class_='name').findAll('span')[1].text.strip().split(',', 1)[0].replace('grafische kaart',
                                                                                                      '').strip()
                chip = getChipName(name)
                price = float(a.find(class_='price right right10').text
                              .replace('-', '00').strip('€').strip('*').strip()
                              .replace('.', '').replace(',', '.'))
                location = getDomainFromURL(url) + ' Outlet' if url.__contains__('Outlet') else getDomainFromURL(url)
                buy = domain + a.find(class_='productLink').attrs['href']
                tmp_avlb = a.find(class_='stockStatus').text
                if tmp_avlb.__contains__("Direct leverbaar"):
                    available = 'YES'
                elif tmp_avlb.__contains__("Pre-order") or tmp_avlb.__contains__("Preorder"):
                    available = 'NO'
                elif tmp_avlb.__contains__("Verwachte levertermijn") or tmp_avlb.__contains__("werkdagen"):
                    available = 'SOON'
                else:
                    available = 'UNKNOWN'
                product = Product(maker.upper(), name, chip, price, location, buy, available)
                products.append(product)
            try:
                driver.close()
            except UnboundLocalError as e:
                pass
            print('☑ Done.\n')
        except Exception as e:
            print("ⓧ Failed.\n")
    return products


def mindfactory(response, url):
    products = []
    print("▶ Working on: " + STRING_MINDFACTORY + "   🌎 " + url)
    class_to_search = "p"

    if response.status_code == 404 or response.status_code == 502:
        print("☠ Page Not Found.\n")
    else:
        domain = response.request.url.replace(response.request.path_url, "")
        # Check if REQUEST is being blocked
        if BeautifulSoup(response.text, features="html.parser").findAll(class_=class_to_search).__len__() == 0:
            print("⚡ Request blocked. Trying with Selenium...")
            options = webdriver.ChromeOptions()
            options.add_argument('--no-proxy-server')
            options.add_argument("--window-position=-700,0")
            options.add_argument("--window-size=576,1024")
            options.add_argument('--blink-settings=imagesEnabled=false')
            # options.add_argument('user-data-dir=' + chrome_profile_path)
            driver = webdriver.Chrome(options=options)
            try:
                driver.get(url)
            except Exception as e:
                print("☠ Non existent URL: " + url)
                driver.close()
                return products
            soup = BeautifulSoup(driver.page_source, features="html.parser")
        else:
            soup = BeautifulSoup(response.text, features="html.parser")
        try:
            for a in soup.findAll('div', attrs={'class': class_to_search}):
                maker = a.find(class_='pname').text.split('GB ', 1)[1].split('GeForce', 1)[0].strip()
                maker = 'ZOTAC GAMING' if maker.upper().__contains__('ZOTAC') else maker
                name = a.find(class_='pname').text.split(maker, 1)[1].split("GDDR")[0].strip()
                chip = getChipName(name)
                price = float(a.find(class_='pprice').text.replace('.', '')
                              .replace('€', '').replace('*', '')
                              .replace(',', '.').strip())
                location = getDomainFromURL(url)
                buy = a.find(class_='p-complete-link visible-xs visible-sm').attrs['href']
                tmp_avlb = a.find(class_='pshipping').text
                if tmp_avlb.__contains__("Lagernd") or tmp_avlb.__contains__("Verfügbar"):
                    available = 'YES'
                elif tmp_avlb.__contains__("Liefertermin"):
                    available = 'NO'
                elif tmp_avlb.__contains__("Bestellt") or tmp_avlb.__contains__("vorbestellen"):
                    available = 'SOON'
                else:
                    available = 'UNKNOWN'
                product = Product(maker.upper(), name, chip, price, location, buy, available)
                products.append(product)
            try:
                driver.close()
            except UnboundLocalError as e:
                pass
            print('☑ Done.\n')
        except Exception as e:
            print("ⓧ Failed.\n")
    return products


def notebooksbilliger(response, url):
    products = []
    print("▶ Working on: " + STRING_NOTEBOOKSBILLIGER + "   🌎 " + url)
    class_to_search = "js-ado-product-click"

    if response.status_code == 404 or response.status_code == 502:
        print("☠ Page Not Found.\n")
    else:
        domain = response.request.url.replace(response.request.path_url, "")
        # Check if REQUEST is being blocked
        if BeautifulSoup(response.text, features="html.parser").findAll(class_=class_to_search).__len__() == 0:
            print("⚡ Request blocked. Trying with Selenium...")
            options = webdriver.ChromeOptions()
            options.add_argument('--no-proxy-server')
            options.add_argument("--window-position=-700,0")
            options.add_argument("--window-size=576,1024")
            options.add_argument('--blink-settings=imagesEnabled=false')
            # options.add_argument('user-data-dir=' + chrome_profile_path)
            driver = webdriver.Chrome(options=options)
            try:
                driver.get(url)
            except Exception as e:
                print("☠ Non existent URL: " + url)
                driver.close()
                return products
            try:
                driver.find_element_by_xpath('/html/body/div[2]/div[4]/div[2]/div/div[2]/div[1]/button').click()

            except Exception as e:
                pass

            soup = BeautifulSoup(driver.page_source, features="html.parser")
        else:
            soup = BeautifulSoup(response.text, features="html.parser")
        try:
            for a in soup.findAll('div', attrs={'class': class_to_search}):
                maker = a.find(class_='short_description').find('li').text.strip().split('GeForce', 1)[0].strip()
                maker = 'ZOTAC GAMING' if maker.upper().__contains__('ZOTAC') else maker
                name = \
                a.find(class_='short_description').find('li').text.strip().split(maker)[1].split('-', 1)[0].split(
                    'GDDR', 1)[0].replace('Grafikkarte', '').strip()
                chip = getChipName(name)
                price = float(a.find(class_='product-price__regular').attrs['data-price'])
                location = getDomainFromURL(url)
                buy = a.find(class_='left').attrs['href']
                tmp_avlb = a.find(class_='availability').text
                if tmp_avlb.__contains__("sofort ab Lager"):
                    available = 'YES'
                elif tmp_avlb.__contains__("Liefertermin") or tmp_avlb.__contains__("vorbestellen"):
                    available = 'NO'
                elif tmp_avlb.__contains__("Verfügbarkeit"):
                    available = 'SOON'
                else:
                    available = 'UNKNOWN'
                product = Product(maker.upper(), name, chip, price, location, buy, available)
                products.append(product)
            try:
                driver.close()
            except UnboundLocalError as e:
                pass
            print('☑ Done.\n')
        except Exception as e:
            print("ⓧ Failed.\n")
    return products


def caseking(response, url):
    products = []
    print("▶ Working on: " + STRING_CASEKING + "   🌎 " + url)
    class_to_search = "artbox"

    if response.status_code == 404 or response.status_code == 502:
        print("☠ Page Not Found. \n")
    else:
        domain = response.request.url.replace(response.request.path_url, "")
        # Check if REQUEST is being blocked
        if BeautifulSoup(response.text, features="html.parser").findAll(class_=class_to_search).__len__() == 0:
            print("⚡ Request blocked. Trying with Selenium...")
            options = webdriver.ChromeOptions()
            options.add_argument('--no-proxy-server')
            options.add_argument("--window-position=-700,0")
            options.add_argument("--window-size=576,1024")
            options.add_argument('--blink-settings=imagesEnabled=false')
            # options.add_argument('user-data-dir=' + chrome_profile_path)
            driver = webdriver.Chrome(options=options)
            try:
                driver.get(url)
            except Exception as e:
                print("☠ Non existent URL: " + url)
                driver.close()
                return products
            soup = BeautifulSoup(driver.page_source, features="html.parser")
        else:
            soup = BeautifulSoup(response.text, features="html.parser")

        try:
            for a in soup.findAll('div', attrs={'class': class_to_search}):
                maker = soup.find(class_='ProductSubTitle').text.strip()
                maker = 'ZOTAC GAMING' if maker.upper().__contains__('ZOTAC') else maker
                name = a.find(class_='ProductTitle').text.replace(maker, '').split(',', 1)[0].strip()
                chip = getChipName(name)
                price = float(a.find(class_='price').text.replace('.', '')
                              .replace('€', '').replace('*', '')
                              .replace(',', '.').strip())
                location = getDomainFromURL(url)
                buy = a.find(class_='producttitles').attrs['href']
                tmp_avlb = a.find(class_='delivery_container').text
                if tmp_avlb.__contains__("lagernd"):
                    available = 'YES'
                elif tmp_avlb.__contains__("ab ") or tmp_avlb.__contains__("Zulauf"):
                    available = 'SOON'
                else:
                    available = 'UNKNOWN'
                product = Product(maker.upper(), name, chip, price, location, buy, available)
                products.append(product)
            try:
                driver.close()
            except UnboundLocalError as e:
                pass
            print('☑ Done.\n')
        except Exception as e:
            print("ⓧ Failed.\n")
    return products


def cyberport(response, url):
    products = []
    print("▶ Working on: " + STRING_CYBERPORT + "   🌎 " + url)
    class_to_search = "productArticle"

    if response.status_code == 404 or response.status_code == 502:
        print("☠ Page Not Found.\n")
    else:
        domain = response.request.url.replace(response.request.path_url, "")
        # Check if REQUEST is being blocked
        if BeautifulSoup(response.text, features="html.parser").findAll(class_=class_to_search).__len__() == 0:
            print("⚡ Request blocked. Trying with Selenium...")
            options = webdriver.ChromeOptions()
            options.add_argument('--no-proxy-server')
            options.add_argument("--window-position=-700,0")
            options.add_argument("--window-size=576,1024")
            options.add_argument('--blink-settings=imagesEnabled=false')
            # options.add_argument('user-data-dir=' + chrome_profile_path)
            driver = webdriver.Chrome(options=options)
            try:
                driver.get(url)
            except Exception as e:
                print("☠ Non existent URL: " + url)
                driver.close()
                return products
            soup = BeautifulSoup(driver.page_source, features="html.parser")
        else:
            soup = BeautifulSoup(response.text, features="html.parser")

        try:
            for a in soup.findAll(class_=class_to_search):
                maker = \
                    a.find(class_='productTitleName').text.replace('GeForce', '*').replace('AMD Radeon', '*').split('*',
                                                                                                                    1)[
                        0].strip().replace('.', '')
                maker = 'ZOTAC GAMING' if maker.upper().__contains__('ZOTAC') else maker
                name = a.find(class_='productTitleName').text.split(maker, 1)[1].split(
                    a.find('ul', class_='hidden-xs').findAll('li')[1].text[0:5].strip().replace(' ', ''))[0].strip()
                chip = getChipName(name)
                price = float(a.find(class_='price').text.replace('.', '')
                              .replace('€', '').replace('*', '')
                              .replace(',', '.').strip())
                location = getDomainFromURL(url)
                buy = domain + a.find(class_='head').attrs['href']
                tmp_avlb = a.find(class_='tooltipAppend').text
                if tmp_avlb.__contains__("Sofort"):
                    available = 'YES'
                elif tmp_avlb.__contains__("ab ") or tmp_avlb.__contains__("Zulauf"):
                    available = 'SOON'
                elif tmp_avlb.__contains__("nicht verfügbar"):
                    available = 'NO'
                else:
                    available = 'UNKNOWN'
                product = Product(maker.upper(), name, chip, price, location, buy, available)
                products.append(product)
            try:
                driver.close()
            except UnboundLocalError as e:
                pass
            print('☑ Done.\n')
        except Exception as e:
            print("ⓧ Failed.\n")
    return products


def conrad(response, url):
    products = []
    print("▶ Working on: " + STRING_CONRAD + "   🌎 " + url)
    class_to_search = "searchResult"

    if response.status_code == 404 or response.status_code == 502:
        print("☠ Page Not Found.\n")
    else:
        domain = response.request.url.replace(response.request.path_url, "")
        # Check if REQUEST is being blocked
        if BeautifulSoup(response.text, features="html.parser").findAll(class_=class_to_search).__len__() == 0:
            response = None
            print("⚡ Request blocked. Trying with Selenium...")
            options = webdriver.ChromeOptions()
            options.add_argument('--headless')
            options.add_argument('--no-proxy-server')
            options.add_argument("--window-position=-700,0")
            options.add_argument("--window-size=576,1024")
            options.add_argument('--blink-settings=imagesEnabled=false')
            # options.add_argument('user-data-dir=' + chrome_profile_path)
            driver = webdriver.Chrome(options=options)
            try:
                driver.get(url)
            except Exception as e:
                print("☠ Non existent URL: " + url)
                driver.close()
                return products
            try:
                driver.find_element_by_xpath('/html/body/div[2]/div[2]/div/div[2]/div[2]').click()
            except Exception as e:
                pass
            try:
                element_present = ec.presence_of_element_located((By.CLASS_NAME, 'productAvailability__status'))
                WebDriverWait(driver, 10).until(element_present)
            except Exception as e:
                pass
            soup = BeautifulSoup(driver.page_source, features="html.parser")
        else:
            soup = BeautifulSoup(response.text, features="html.parser")

        try:
            for a in soup.findAll(class_=class_to_search):
                maker = a.find(class_='searchResult__header').text.split('Grafikkarte', 1)[0].strip()
                maker = 'ZOTAC GAMING' if maker.upper().__contains__('ZOTAC') else maker
                name = \
                    a.find(class_='product__title').text.split(maker)[1].replace('Grafikkarte Nvidia ', '').replace(
                        'Grafikkarte AMD Radeon ', '').strip()
                chip = getChipName(name)
                price = float(a.find(class_='product__currentPrice').text.replace('.', '').replace('€', '').replace('*',
                                                                                                                    '').replace(
                    ',', '.').strip())
                location = getDomainFromURL(url)
                buy = domain + a.find(class_='product__title').attrs['href']
                tmp_avlb = a.find(class_='productAvailability__status').text
                if tmp_avlb.__contains__("Online verfügbar") or tmp_avlb.__contains__("Vorrat reicht"):
                    available = 'YES'
                elif tmp_avlb.__contains__("Lieferung in"):
                    available = 'SOON'
                elif tmp_avlb.__contains__("sobald verfügbar"):
                    available = 'NO'
                else:
                    available = 'UNKNOWN'
                product = Product(maker.upper(), name, chip, price, location, buy, available)
                products.append(product)
            try:
                driver.close()
            except UnboundLocalError as e:
                pass
            print('☑ Done.\n')
        except Exception as e:
            print("ⓧ Failed.\n")
    return products


def createFirstDataFrame(products):
    df = pandas.DataFrame.from_records([product.to_dict() for product in products])
    return df


def createDataFrame(products, df_tmp):
    df = pandas.DataFrame.from_records([product.to_dict() for product in products])
    df.append(df_tmp, ignore_index=True)
    if df.__len__() != 0:
        df = df.sort_values(by=['Availability', 'Price'], ascending=[False, True])
        df = df[~df['Chip'].str.contains("N/A")]
    return df


def checkPrices(df):
    df_goodPrice = pandas.DataFrame(columns=DATAFRAME_COLUMNS)
    for CHIP in PRICE_CHIP_DICT.keys():
        df_goodTmp = df.loc[
            (df['Price'] < PRICE_CHIP_DICT.get(CHIP)) & df['Chip'].isin([CHIP]) & df['Availability'].isin(
                ['YES'])]  # & df['Buy Link'].str.contains(getDomainFromURL(url))
        if df_goodTmp.__len__() > 0:
            print(df_goodTmp.__len__().__str__() + 'x ' + CHIP + ' ARE AVAILABLE FOR LESS THAN ' + PRICE_CHIP_DICT.get(
                CHIP).__str__() + " €")  # ==> " + getDomainFromURL(url)
        df_goodPrice = df_goodPrice.append(df_goodTmp, ignore_index=True)
    return df_goodPrice


def getDomainFromURL(url):
    domain = ''
    if url.__contains__(STRING_ALTERNATE):
        domain = STRING_ALTERNATE
    elif url.__contains__(STRING_ALTERNATE_BE):
        domain = STRING_ALTERNATE_BE
    elif url.__contains__(STRING_ALTERNATE_NL):
        domain = STRING_ALTERNATE_NL
    elif url.__contains__(STRING_MINDFACTORY):
        domain = STRING_MINDFACTORY
    elif url.__contains__(STRING_NOTEBOOKSBILLIGER):
        domain = STRING_NOTEBOOKSBILLIGER
    elif url.__contains__(STRING_CYBERPORT):
        domain = STRING_CYBERPORT
    elif url.__contains__(STRING_CONRAD):
        domain = STRING_CONRAD
    elif url.__contains__(STRING_CASEKING):
        domain = STRING_CASEKING
    return domain


def getChipName(name):
    chip = "N/A"
    if name.__contains__("3600"):
        if name.__contains__("Ti "):
            chip = CHIP_NAME_3060Ti
        else:
            chip = CHIP_NAME_3060
    elif name.__contains__("3070"):
        chip = CHIP_NAME_3070
    elif name.__contains__("3080"):
        chip = CHIP_NAME_3080
    elif name.__contains__("3090"):
        chip = CHIP_NAME_3090
    elif name.__contains__("6800"):
        if name.__contains__("XT "):
            chip = CHIP_NAME_6800XT
        else:
            chip = CHIP_NAME_6800
    elif name.__contains__("6900"):
        if name.__contains__("XT "):
            chip = CHIP_NAME_6900XT
        else:
            chip = CHIP_NAME_6900
    return chip


def exportAsXLSX(df, url):
    notExported = True
    while notExported:
        sheetName = 'GPUs'
        try:
            excelWriter = pandas.ExcelWriter(XLSX_PATH, engine='xlsxwriter')
            # if not df.index.name:
            #    df.index.name = 'Index'
            df.to_excel(excelWriter, header=True, sheet_name=sheetName, encoding='utf-8')
            workbook = excelWriter.book
            worksheet = excelWriter.sheets[sheetName]
            # Get the dimensions of the dataframe.
            (max_row, max_col) = df.shape
            # Create a list of column headers, to use in add_table().
            column_settings = [{'header': datetime.now().strftime("%H:%M:%S")}]
            for header in df.columns:
                column_settings.append({'header': header})
            # Add the table.
            worksheet.add_table(0, 0, max_row, max_col, {'columns': column_settings})
            # Make the columns wider for clarity.
            for i, width in enumerate(get_col_widths(df)):
                worksheet.set_column(i, i, width + 2)
            # Close the Pandas Excel writer and output the Excel file.
            workbook.close()
            notExported = False
            if url is urls[urls.__len__() - 1] and excelWriter is not None:
                print('✔ Workbook exported')
                print('')
                # path = os.path.realpath(excelWriter.path)
                # os.startfile(path)

        except Exception as e:
            if url is not urls[urls.__len__() - 1]:
                notExported = False
                print('Workbook NOT exported. Continuing loop')
            else:
                print('Close Excel!')
                time.sleep(2)


def get_col_widths(dataframe):
    # First we find the maximum length of the index column
    idx_max = max([len(str(s)) for s in dataframe.index.values] + [len(str(dataframe.index.name))])
    # Then, we concatenate this to the max of the lengths of column name and its values for each column, left to right
    return [idx_max] + [max([len(str(s)) for s in dataframe[col].values] + [len(col)]) for col in dataframe.columns]


def notifyCheapItemAvailability(product_name, url):
    print(product_name + ' is AVAILABLE AT ' + getDomainFromURL(url).upper() + ' !!!!')
    print('OPENING BROWSER TO ' + url)
    openChrome(url)
    playsound(SOUND_CHEAP_ITEM)
    # os.startfile(DESKTOP_PATH + '\\' + XLSX_FILE_NAME)


def openChrome(url):
    global sub_driver
    options = webdriver.ChromeOptions()
    # options.add_argument('user-data-dir=' + chrome_profile_path)
    sub_driver = webdriver.Chrome(executable_path=CRAWLER_DRIVER_PATH, options=options)
    try:
        sub_driver.get(url)
    except Exception as e:
        print("☠ Non existent URL: " + url)
        sub_driver.close()


def examineProducts(goodPrices):
    for index, row in goodPrices.iterrows():
        print('')
        buyURL = row['Buy Link']
        productName = row['Maker'] + ' ' + row['Name']
        notifyCheapItemAvailability(productName, buyURL)


def main():
    global loop
    pointer_loop = True
    global SCRIPT_LAST_RUN_TIME
    SCRIPT_LAST_RUN_TIME = SCRIPT_START_TIME
    start = time.time()
    while pointer_loop:
        if not loop:
            pointer_loop = False
        products = []
        df_tmp = createFirstDataFrame(products)
        subprocess.Popen("cls", shell=True).communicate()
        print('== Started: ' + SCRIPT_START_TIME + ' | Last Check: ' + SCRIPT_LAST_RUN_TIME + ' ==')
        for url in urls:
            products_from_url = crawlWebsite(url)
            if products is None:
                print('✘ NO PRODUCTS FOUND IN ' + url)
            else:
                products += products_from_url
                df = createDataFrame(products, df_tmp)
                if df.__len__() != 0:
                    exportAsXLSX(df, url)
                else:
                    print("✘ DataFrame is empty.")
                df_tmp = df
        goodPrices = checkPrices(createDataFrame(products, None))
        examineProducts(goodPrices)
        SCRIPT_LAST_RUN_TIME = datetime.now().strftime("%d.%m.%Y at %H:%M:%S")
        if loop:
            print("======================= Checking every " + CRAWL_WEBSITES_SCHEDULE.__str__() + " seconds ======================= ")
            time.sleep(CRAWL_WEBSITES_SCHEDULE - ((time.time() - start) % CRAWL_WEBSITES_SCHEDULE))
        else:
            print("========================================================================= ")


if __name__ == '__main__':
    main()
