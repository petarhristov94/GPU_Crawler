from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from datetime import datetime
import os
import requests
import pandas

chrome_profile_path = r'C:\Users\phris\AppData\Local\Google\Chrome\User Data'
folder_path = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')

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
    'https://www.notebooksbilliger.de/pc+hardware/grafikkarten/nvidia/geforce+rtx+3070+nvidia/page/1?sort=price&order=asc&availability=alle',
    'https://www.notebooksbilliger.de/pc+hardware/grafikkarten/nvidia/geforce+rtx+3080+nvidia/page/1?sort=price&order=asc&availability=alle',
    'https://www.notebooksbilliger.de/pc+hardware/grafikkarten/nvidia/geforce+rtx+3090+nvidia/page/1?sort=price&order=asc&availability=alle',
    'https://www.notebooksbilliger.de/pc+hardware/grafikkarten+pc+hardware/amdati/rx+6800/page/1?sort=price&order=asc&availability=alle',
    'https://www.notebooksbilliger.de/pc+hardware/grafikkarten+pc+hardware/amdati/rx+6800+xt/page/1?sort=price&order=asc&availability=alle',
    'https://www.notebooksbilliger.de/pc+hardware/grafikkarten+pc+hardware/amdati/rx+6900+xt/page/1?sort=price&order=asc&availability=alle',
    'https://www.mindfactory.de/Hardware/Grafikkarten+(VGA)/GeForce+RTX+fuer+Gaming/RTX+3070.html',
    'https://www.mindfactory.de/Hardware/Grafikkarten+(VGA)/GeForce+RTX+fuer+Gaming/RTX+3080.html',
    'https://www.mindfactory.de/Hardware/Grafikkarten+(VGA)/GeForce+RTX+fuer+Gaming/RTX+3090.html',
    'https://www.caseking.de/pc-komponenten/grafikkarten/nvidia?sSort=3&sTemplate=list&ckFilters=13917&ckTab=0&sPage=1&sPerPage=48',
    'https://www.caseking.de/pc-komponenten/grafikkarten/nvidia?sSort=3&sTemplate=list&ckFilters=13915&ckTab=0&sPage=1&sPerPage=48',
    'https://www.caseking.de/pc-komponenten/grafikkarten/nvidia?sSort=3&sTemplate=list&ckFilters=13916&ckTab=0&sPage=1&sPerPage=48',
    'https://www.cyberport.de/pc-und-zubehoer/komponenten/grafikkarten/nvidia-fuer-gaming.html?productsPerPage=120&sort=popularity&2E_Grafikchip=GeForce%20RTX%203070,GeForce%20RTX%203080,GeForce%20RTX%203090&page=1',
    'https://www.cyberport.de/pc-und-zubehoer/komponenten/grafikkarten/amd-fuer-gaming.html?productsPerPage=120&sort=price_asc&2E_Grafikchip=Radeon%206800,Radeon%206800%20XT,Radeon%206900%20XT&page=1',
    'https://www.conrad.de/de/o/grafikkarten-amd-chipsatz-0414055.html?sort=Price-asc&tfo_ATT_LOV_GRAPHIC_CARD_MODELS=RX%206800%20XT~~~RX%206800~~~RX%206900%20XT',
    'https://www.conrad.de/de/o/grafikkarten-nvidia-chipsatz-0414054.html?sort=Price-asc&tfo_ATT_LOV_GRAPHIC_CARD_MODELS=RTX%203070~~~RTX%203080~~~RTX%203090'
    ]

STRING_ALTERNATE = 'alternate.de'
STRING_MINDFACTORY = 'mindfactory.de'
STRING_NOTEBOOKSBILLIGER = 'notebooksbilliger.de'
STRING_CYBERPORT = 'cyberport.de'
STRING_CONRAD = 'conrad.de'
STRING_CASEKING = 'caseking.de'


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
            'Maker': self.maker,
            'Name': self.name,
            'Chip': self.chip,
            'Price': self.price,
            'Location': self.location,
            'Buy Link': self.buyLink,
            'Availability': self.available
        }


def crawlWebsite(url):
    products = []
    response = requests.get(url)
    if url.__contains__(STRING_ALTERNATE):
        products = alternate(response, url)
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

    # driver.close()
    return products


def alternate(response, url):
    driver = None
    products = []
    print("▶ Working on: " + STRING_ALTERNATE + "   🌎 " + url)
    class_to_search = "listRow"

    if response.status_code == 404:
        print("☠ Page Not Found.")
    else:
        domain = response.request.url.replace(response.request.path_url, "")
        linkSortList = BeautifulSoup(response.text, features="html.parser").find(class_="list").attrs['href']
        response = requests.get(domain + linkSortList)
        # Check if REQUEST is being blocked
        if BeautifulSoup(response.text, features="html.parser").findAll(class_=class_to_search).__len__() == 0:
            print("⚡ Request blocked. Trying with Selenium...")
            options = webdriver.ChromeOptions()
            options.add_argument('--no-proxy-server')
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
                chip = getChipName(name)
                price = float(a.find(class_='price right right10').text
                              .replace('-', '00').strip('€').strip('*').strip()
                              .replace('.', '').replace(',', '.'))
                location = STRING_ALTERNATE
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
            if driver is not None:
                driver.close()
            print('☑ Done.')
        except Exception as e:
            print("ⓧ Failed.")
    return products


def mindfactory(response, url):
    driver = None
    products = []
    print("▶ Working on: " + STRING_MINDFACTORY + "   🌎 " + url)
    class_to_search = "p"

    if response.status_code == 404:
        print("☠ Page Not Found.")
    else:
        domain = response.request.url.replace(response.request.path_url, "")
        # Check if REQUEST is being blocked
        if BeautifulSoup(response.text, features="html.parser").findAll(class_=class_to_search).__len__() == 0:
            print("⚡ Request blocked. Trying with Selenium...")
            options = webdriver.ChromeOptions()
            options.add_argument('--no-proxy-server')
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
                name = a.find(class_='pname').text.split(maker, 1)[1].split("GDDR")[0].strip()
                chip = getChipName(name)
                price = float(a.find(class_='pprice').text.replace('.', '')
                              .replace('€', '').replace('*', '')
                              .replace(',', '.').strip())
                location = STRING_MINDFACTORY
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
            if driver is not None:
                driver.close()
            print('☑ Done.')
        except Exception as e:
            print("ⓧ Failed.")
    return products


def notebooksbilliger(response, url):
    driver = None
    products = []
    print("▶ Working on: " + STRING_NOTEBOOKSBILLIGER + "   🌎 " + url)
    class_to_search = "js-ado-product-click"

    if response.status_code == 404:
        print("☠ Page Not Found.")
    else:
        domain = response.request.url.replace(response.request.path_url, "")
        # Check if REQUEST is being blocked
        if BeautifulSoup(response.text, features="html.parser").findAll(class_=class_to_search).__len__() == 0:
            print("⚡ Request blocked. Trying with Selenium...")
            options = webdriver.ChromeOptions()
            options.add_argument('--no-proxy-server')
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
                print("Couldn't bypass Cookies Message.")
            soup = BeautifulSoup(driver.page_source, features="html.parser")
        else:
            soup = BeautifulSoup(response.text, features="html.parser")
        try:
            for a in soup.findAll('div', attrs={'class': class_to_search}):
                maker = a.find(class_='short_description').find('li').text.strip().split('GeForce', 1)[0].strip()
                name = a.find(class_='short_description').find('li').text.strip().split(maker)[1].split('-', 1)[
                    0].replace(
                    'Grafikkarte', '').strip()
                chip = getChipName(name)
                price = float(a.find(class_='product-price__regular').attrs['data-price'])
                location = STRING_NOTEBOOKSBILLIGER
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
            if driver is not None:
                driver.close()
            print('☑ Done.')
        except Exception as e:
            print("ⓧ Failed.")
    return products


def caseking(response, url):
    driver = None
    products = []
    print("▶ Working on: " + STRING_CASEKING + "   🌎 " + url)
    class_to_search = "artbox"

    if response.status_code == 404:
        print("☠ Page Not Found.")
    else:
        domain = response.request.url.replace(response.request.path_url, "")
        # Check if REQUEST is being blocked
        if BeautifulSoup(response.text, features="html.parser").findAll(class_=class_to_search).__len__() == 0:
            print("⚡ Request blocked. Trying with Selenium...")
            options = webdriver.ChromeOptions()
            options.add_argument('--no-proxy-server')
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
                maker = a.find(class_='ProductSubTitle').text.strip()
                name = a.find(class_='ProductTitle').text.split(',', 1)[0].strip()
                chip = getChipName(name)
                price = float(a.find(class_='price').text.replace('.', '')
                              .replace('€', '').replace('*', '')
                              .replace(',', '.').strip())
                location = STRING_CASEKING
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
            if driver is not None:
                driver.close()
            print('☑ Done.')
        except Exception as e:
            print("ⓧ Failed.")
    return products


def cyberport(response, url):
    driver = None
    products = []
    print("▶ Working on: " + STRING_CYBERPORT + "   🌎 " + url)
    class_to_search = "productArticle"

    if response.status_code == 404:
        print("☠ Page Not Found.")
    else:
        domain = response.request.url.replace(response.request.path_url, "")
        # Check if REQUEST is being blocked
        if BeautifulSoup(response.text, features="html.parser").findAll(class_=class_to_search).__len__() == 0:
            print("⚡ Request blocked. Trying with Selenium...")
            options = webdriver.ChromeOptions()
            options.add_argument('--no-proxy-server')
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
                maker = a.find(class_='productTitleName').text.replace('GeForce', '*').replace('AMD Radeon', '*').split('*', 1)[0].strip().replace('.', '')
                name = a.find(class_='productTitleName').text.split(maker, 1)[1].split(
                    a.find('ul', class_='hidden-xs').findAll('li')[1].text[0:5].strip().replace(' ', ''))[0].strip()
                chip = getChipName(name)
                price = float(a.find(class_='price').text.replace('.', '')
                              .replace('€', '').replace('*', '')
                              .replace(',', '.').strip())
                location = STRING_CYBERPORT
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
            if driver is not None:
                driver.close()
            print('☑ Done.')
        except Exception as e:
            print("ⓧ Failed.")
    return products


def conrad(response, url):
    driver = None
    products = []
    print("▶ Working on: " + STRING_CONRAD + "   🌎 " + url)
    class_to_search = "searchResult"

    if response.status_code == 404:
        print("☠ Page Not Found.")
    else:
        domain = response.request.url.replace(response.request.path_url, "")
        # Check if REQUEST is being blocked
        if BeautifulSoup(response.text, features="html.parser").findAll(class_=class_to_search).__len__() == 0:
            response = None
            print("⚡ Request blocked. Trying with Selenium...")
            options = webdriver.ChromeOptions()
            options.add_argument('--no-proxy-server')
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
                driver.find_element_by_xpath('/html/body/div[1]/div/header/header/div/div[1]/div/div/div[2]/div[2]').click()
            except Exception as e:
                print("Couldn't bypass Cookies Message.")
            element_present = ec.presence_of_element_located((By.CLASS_NAME, 'productAvailability__status'))
            WebDriverWait(driver, 10).until(element_present)
            soup = BeautifulSoup(driver.page_source, features="html.parser")
        else:
            soup = BeautifulSoup(response.text, features="html.parser")

        try:
            for a in soup.findAll(class_=class_to_search):
                maker = a.find(class_='searchResult__header').text.split('Grafikkarte', 1)[0].strip()
                name = a.find(class_='product__title').text.split(maker)[1].replace('8 GB', '*').replace('10 GB', '*').replace('12 GB', '*').replace('16 GB', '*').replace('24 GB', '*').split('*', 1)[0].replace('Grafikkarte Nvidia ', '').replace('Grafikkarte AMD Radeon ', '').strip()
                chip = getChipName(name)
                price = float(a.find(class_='product__currentPrice').text.replace('.', '').replace('€', '').replace('*', '').replace(',', '.').strip())
                location = STRING_CONRAD
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
            if driver is not None:
                driver.close()
            if products.__len__() == 0:
                print("ⓧ Failed.")
            else:
                print('☑ Done.')
        except Exception as e:
            print("ⓧ Failed.")
    return products


def createDataFrame(products):
    df = pandas.DataFrame.from_records([product.to_dict() for product in products])
    df = df.sort_values(by=['Availability', 'Price'], ascending=[False, True])
    df = df[~df['Chip'].str.contains("N/A")]
    return df


def getChipName(name):
    chip = "N/A"
    if name.__contains__("RTX 3070"):
        chip = "NVIDIA GeForce RTX 3070"
    elif name.__contains__("RTX 3080"):
        chip = "NVIDIA GeForce RTX 3080"
    elif name.__contains__("RTX 3090"):
        chip = "NVIDIA GeForce RTX 3090"
    elif name.__contains__("RX 6800 XT"):
        chip = "AMD Radeon RX 6800 XT"
    elif name.__contains__("RX 6800"):
        chip = "AMD Radeon RX 6800"
    elif name.__contains__("RX 6900 XT"):
        chip = "AMD Radeon RX 6900 XT"
    return chip


def exportAsXLSX(df):
    dt_string = datetime.now().strftime("%d-%m-%Y_%H-%M-%S")
    fileName = 'products_' + dt_string + '_.xlsx'
    sheetName = 'GPUs'
    excelWriter = pandas.ExcelWriter(folder_path + '\\' + fileName, engine='xlsxwriter')
    if not df.index.name:
        df.index.name = 'Index'
    df.to_excel(excelWriter, header=True, sheet_name=sheetName, encoding='utf-8')
    workbook = excelWriter.book
    worksheet = excelWriter.sheets[sheetName]
    # Get the dimensions of the dataframe.
    (max_row, max_col) = df.shape
    # Create a list of column headers, to use in add_table().
    column_settings = [{'header': 'Index'}]
    for header in df.columns:
        column_settings.append({'header': header})
    # Add the table.
    worksheet.add_table(0, 0, max_row, max_col, {'columns': column_settings})
    # Make the columns wider for clarity.
    for i, width in enumerate(get_col_widths(df)):
        worksheet.set_column(i, i, width + 5)
    # Close the Pandas Excel writer and output the Excel file.
    workbook.close()
    print('✔ Workbook exported')
    path = os.path.realpath(excelWriter.path)
    os.startfile(path)


def get_col_widths(dataframe):
    # First we find the maximum length of the index column
    idx_max = max([len(str(s)) for s in dataframe.index.values] + [len(str(dataframe.index.name))])
    # Then, we concatenate this to the max of the lengths of column name and its values for each column, left to right
    return [idx_max] + [max([len(str(s)) for s in dataframe[col].values] + [len(col)]) for col in dataframe.columns]


def main():
    products = []
    for url in urls:
        products_from_url = crawlWebsite(url)
        if products is None:
            print('✘ NO PRODUCTS FOUND IN ' + url)
        else:
            products += products_from_url

    df = createDataFrame(products)
    if df.__len__() != 0:
        exportAsXLSX(df)
    else:
        print("✘ DataFrame is empty.")


if __name__ == '__main__':
    main()
