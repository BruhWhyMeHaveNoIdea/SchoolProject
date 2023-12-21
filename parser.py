from bs4 import BeautifulSoup
from requests import Session, get
from pprint import pprint
from functools import lru_cache

url = "https://www.litres.ru/new/"

headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'cookie': 'srv_id=FSVPYwPzW1hvnD6M.M4DmMrRZStCeH21imC5CjoM4kcDwpv_TGIK4-LSRcmKptTHP54qL_ufSMyhiAfpm57tv.YqFroUCgDqV2OvYJOgwA0B6LIyX39_xqirao2tQ_CT8=.web; gMltIuegZN2COuSe=EOFGWsm50bhh17prLqaIgdir1V0kgrvN; u=2y7ucglv.1dm13g7.1a5aivjc49f00; v=1702483643; buyer_laas_location=650520; luri=nizhnekamsk; buyer_location_id=650520; dfp_group=90; _gcl_au=1.1.1283238480.1702483645; _ga=GA1.1.771937517.1702483645; tmr_lvid=54e5d4a72068e923e860e6ab433547e0; tmr_lvidTS=1702483644976; advcake_track_id=c3ff8738-326c-b27c-2b60-9db1d675f1b5; advcake_session_id=ed5cdd3c-9a5b-5d03-c012-f7693ff4bef2; adrdel=1; adrcid=AO5epW5VV2BURegPXy7pvGg; _ym_uid=1702483647569517202; _ym_d=1702483647; f=5.32e32548b6f3e9784b5abdd419952845a68643d4d8df96e9a68643d4d8df96e9a68643d4d8df96e9a68643d4d8df96e94f9572e6986d0c624f9572e6986d0c624f9572e6986d0c62ba029cd346349f36c1e8912fd5a48d02c1e8912fd5a48d0246b8ae4e81acb9fa1a2a574992f83a9246b8ae4e81acb9fa46b8ae4e81acb9fae992ad2cc54b8aa8cad08e7e7eb412c8fa4d7ea84258c63d59c9621b2c0fa58f915ac1de0d034112ad09145d3e31a56946b8ae4e81acb9fae2415097439d4047fb0fb526bb39450a46b8ae4e81acb9fa34d62295fceb188dd99271d186dc1cd03de19da9ed218fe2d50b96489ab264edd50b96489ab264edd50b96489ab264ed46b8ae4e81acb9fa38e6a683f47425a8352c31daf983fa077a7b6c33f74d335c03d3f0af72d633b5db6aace19274a12602c730c0109b9fbb5e0290f4d67fb7ea796f2673db70edd529aa4cecca288d6b0205265a0636534ac772035eab81f5e146b8ae4e81acb9fa46b8ae4e81acb9faf5b8e78c6f0f62a3b4d34b548795e658dd9be0d84df7cccc2da10fb74cac1eab2da10fb74cac1eabc98d1c3ab1f148dc193cc3161054d47da6ef565a9fc26059; yandex_monthly_cookie=true; _ym_isad=2; ft="8ZU/TxvEXkGIISQn5lMn4g1Xon8+45EjDbv4avMh+oc7HWIV/9XRRPoa2AvZH6+MA74DQzyAQcPQx7TG7YsKQ3xmbErt5gHyyvdpjLSc2t/mQwo6Z1pb+dDLy1uxEthruRFYIXikQ3B3Qdlt6NUv/Dv6yaYTcts1yyWGz1HojG4n5lJa0ZrJITRmEkwfjPkq"; _ym_visorc=b; uxs_uid=b890b550-99d1-11ee-ab27-77c21e451cc9; sx=H4sIAAAAAAAC%2F1zOSW7CMBQA0Lt4zcLTn7iN823TACXBEEKCcveqCyrRCzy9l4HM7Jg0JBVFCJ11IWtRkJRRQMz%2BZR5mb2YmW%2FWSYFhH0WX8Ppxd%2ByKNxzs%2B6tHsTDF7R9YDWQu07QwiombCKiiAEaVQV4JkAqtK%2BU%2BO0pbjmgAttH48zHG63vw0nRpWGWT5lGPYdiZ552tgV5ECU1cL%2B0CeyUnB3CV9yznH8UIj3OIqvfLqn9iP5dnP58lds%2F0n%2F54TESUCqTlkiBQKl%2BI1VpCqUX19y3RY1hlOnodHxH6goSB3nkOXbq3d8UN21m%2FbTwAAAP%2F%2FFjT8IWkBAAA%3D; abp=0; _ga_M29JC28873=GS1.1.1702483644.1.1.1702483705.60.0.0; SEARCH_HISTORY_IDS=0; uuid=3e39248c25184af2%3A2; __upin=Yr7SbhBBUBD5OtKdyhvE2w; tmr_detect=0%7C1702483712403; _buzz_fpc=JTdCJTIycGF0aCUyMiUzQSUyMiUyRiUyMiUyQyUyMmRvbWFpbiUyMiUzQSUyMi53d3cuYXZpdG8ucnUlMjIlMkMlMjJleHBpcmVzJTIyJTNBJTIyRnJpJTJDJTIwMTMlMjBEZWMlMjAyMDI0JTIwMTYlM0EwOCUzQTMzJTIwR01UJTIyJTJDJTIyU2FtZVNpdGUlMjIlM0ElMjJMYXglMjIlMkMlMjJ2YWx1ZSUyMiUzQSUyMiU3QiU1QyUyMnVmcCU1QyUyMiUzQSU1QyUyMmIwYzRkNTQ5YmFlZmVhZmY4NzY4NjAxZTk5ZTRhZTY1JTVDJTIyJTJDJTVDJTIyYnJvd3NlclZlcnNpb24lNUMlMjIlM0ElNUMlMjIxMjAuMCU1QyUyMiU3RCUyMiU3RA==; _buzz_aidata=JTdCJTIycGF0aCUyMiUzQSUyMiUyRiUyMiUyQyUyMmRvbWFpbiUyMiUzQSUyMi53d3cuYXZpdG8ucnUlMjIlMkMlMjJleHBpcmVzJTIyJTNBJTIyRnJpJTJDJTIwMTMlMjBEZWMlMjAyMDI0JTIwMTYlM0EwOCUzQTMzJTIwR01UJTIyJTJDJTIyU2FtZVNpdGUlMjIlM0ElMjJMYXglMjIlMkMlMjJ2YWx1ZSUyMiUzQSUyMiU3QiU1QyUyMnVmcCU1QyUyMiUzQSU1QyUyMllyN1NiaEJCVUJENU90S2R5aHZFMnclNUMlMjIlMkMlNUMlMjJicm93c2VyVmVyc2lvbiU1QyUyMiUzQSU1QyUyMjEyMC4wJTVDJTIyJTdEJTIyJTdE; buyer_from_page=catalog'
}


@lru_cache(maxsize=None)
def book_name(base_url):
    response = get(base_url)
    soup = BeautifulSoup(response.text, 'lxml')
    items = soup.find_all('div', class_="ArtsGrid-module__artWrapper_1j1xJ")
    ab = []
    for i in items:
        title = i.find("p", class_="ArtInfo-modules__title_1UysF").text
        ab.append(title)
    return ab


@lru_cache(maxsize=None)
def who_read(base_url):
    response = get(base_url)
    soup = BeautifulSoup(response.text, 'lxml')
    found = soup.find_all('div', class_='ArtsGrid-module__artWrapper_1j1xJ')
    lr = []
    for i in found:
        reader = i.find('a', class_='ArtInfo-modules__reader_4aV4e')
        if reader is not None:
            lr.append(reader.text)
        else:
            lr.append("Нет читающего")
    return lr


@lru_cache(maxsize=None)
def author_book(base_url):
    response = get(base_url)
    soup = BeautifulSoup(response.text, 'lxml')
    items = soup.find_all('div', class_='ArtsGrid-module__artWrapper_1j1xJ')
    am = []
    for j in items:
        author = j.find('a', class_='ArtInfo-modules__author_FTzMn').text
        am.append(author)
    return am


@lru_cache(maxsize=None)
def url_to_book(base_url):
    response = get(base_url)
    soup = BeautifulSoup(response.text, 'lxml')
    items = soup.find_all('div', class_='ArtsGrid-module__artWrapper_1j1xJ')
    urls = []
    for i in items:
        fou_url1 = i.find('div', class_='ArtInfo-modules__wrapper_2lOpZ')
        found = fou_url1.find('a')['href']
        urls.append('https://www.litres.ru' + found)
    return urls


@lru_cache(maxsize=None)
def finished_dict():
    full = {}
    for i in range(1, len(author_book(url))):
        full[i] = {"Название книги": book_name(url)[i], "Автор книги": author_book(url)[i], "Читает": who_read(url)[i]}
    return full

authors = author_book(url)
dictionary = finished_dict()

urls = url_to_book(url)