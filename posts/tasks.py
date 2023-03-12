from meet.celery import app
from .models import Currency
import requests
from bs4 import BeautifulSoup


@app.task
def currency_value():
    DOLLAR_RUB = 'https://www.google.com/search?sxsrf=ALeKk01NWm6viYijAo3HXYOEQUyDEDtFEw%3A1584716087546&source=hp&ei=N9l0XtDXHs716QTcuaXoAg&q=%D0%B4%D0%BE%D0%BB%D0%BB%D0%B0%D1%80+%D0%BA+%D1%80%D1%83%D0%B1%D0%BB%D1%8E&oq=%D0%B4%D0%BE%D0%BB%D0%BB%D0%B0%D1%80+&gs_l=psy-ab.3.0.35i39i70i258j0i131l4j0j0i131l4.3044.4178..5294...1.0..0.83.544.7......0....1..gws-wiz.......35i39.5QL6Ev1Kfk4'
    DIRHAM = 'https://www.google.com/search?q=дирхам+к+рублю&ei=_G8HZOmzFJPbrgTozp6AAQ&oq=lbh%5Bfv+к+рублю&gs_lcp=Cgxnd3Mtd2l6LXNlcnAQARgAMgcIABCxAxBDMgcIABCABBAKMgcIABCABBAKMgcIABCABBAKMgcIABCABBAKMgcIABCABBAKMgcIABCABBAKMgcIABCABBAKMgcIABCABBAKMgcIABCABBAKOgoIABBHENYEELADOgcIABCwAxBDOgYIABAHEB46DQgAEAcQHhDxBBAKECo6CAgAEAcQHhAKOgoIABAHEB4QChAqOg0IABAIEAcQHhDxBBAKOgcIABANEIAEOggIABAeEA0QDzoICAAQBRAeEA06DAgAEA0QgAQQRhCCAjoKCAAQDRCABBCxA0oECEEYAFCGEFi1MmD1R2gCcAF4AIABigGIAcEJkgEDNy41mAEAoAEByAEKwAEB&sclient=gws-wiz-serp'
    EVRO = 'https://www.google.com/search?q=евро+к+рублю&ei=EHAHZIm6HM2GwPAP8pW82A0&ved=0ahUKEwiJgt3tp8r9AhVNAxAIHfIKD9sQ4dUDCA8&uact=5&oq=евро+к+рублю&gs_lcp=Cgxnd3Mtd2l6LXNlcnAQAzIMCAAQsQMQQxBGEIICMgUIABCABDIFCAAQgAQyBQgAEIAEMgUIABCABDIFCAAQgAQyBQgAEIAEMgUIABCABDIFCAAQgAQyBQgAEIAEOgoIABBHENYEELADOgcIABCwAxBDOgYIABAHEB46BAgAEEM6CAgAEAcQHhAKOgcIABANEIAEOggIABAFEB4QDToKCAAQgAQQDRCxAzoHCAAQgAQQDToGCAAQHhANSgQIQRgAUKAFWP4_YMhGaAVwAXgAgAHcAYgB2gqSAQYxMi4xLjGYAQCgAQHIAQrAAQE&sclient=gws-wiz-serp'
    CNY = 'https://www.google.com/search?q=юань+к+рублю&ei=dHIHZPD8KpS7rgSTwrWIAw&ved=0ahUKEwjwhtWRqsr9AhWUnYsKHRNhDTEQ4dUDCA8&uact=5&oq=юань+к+рублю&gs_lcp=Cgxnd3Mtd2l6LXNlcnAQAzIQCAAQgAQQsQMQgwEQRhCCAjIFCAAQgAQyBQgAEIAEMgUIABCABDIFCAAQgAQyBQgAEIAEMgUIABCABDIFCAAQgAQyBQgAEIAEMgUIABCABDoKCAAQRxDWBBCwAzoNCAAQRxDWBBDJAxCwAzoICAAQkgMQsAM6BwgAELADEEM6BAgAEEM6BwgAEIAEEAo6DAgAEOoCELQCEEMYAToOCAAQ6gIQtAIQChBDGAE6CggAELEDEIMBEEM6EQguEIAEELEDEIMBEMcBENEDOhEILhCDARDHARCxAxDRAxCABDoUCC4QgAQQsQMQgwEQxwEQ0QMQ1AI6CwgAEIAEELEDEIMBOggIABCABBCxAzoFCAAQsQM6DwgAELEDEIMBEEMQRhCCAkoECEEYAFDLBFi_NWDBOWgCcAF4BIABjQGIAeIRkgEFMTMuMTCYAQCgAQGwAQrIAQrAAQHaAQQIARgH&sclient=gws-wiz-serp'
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36'}
    full_page = requests.get(DOLLAR_RUB, headers=headers)
    full_page_dir = requests.get(DIRHAM, headers=headers)
    full_page_evro = requests.get(EVRO, headers=headers)
    full_page_cny = requests.get(CNY, headers=headers)
    soup = BeautifulSoup(full_page.content, 'html.parser')
    soup_dir = BeautifulSoup(full_page_dir.content, 'html.parser')
    soup_evro = BeautifulSoup(full_page_evro.content, 'html.parser')
    soup_cny = BeautifulSoup(full_page_cny.content, 'html.parser')
    convert = soup.findAll("span", {"class": "DFlfde", "class": "SwHCTb", "data-precision": 2})
    convert_dir = soup_dir.findAll("span", {"class": "DFlfde", "class": "SwHCTb", "data-precision": 2})
    convert_evro = soup_evro.findAll("span", {"class": "DFlfde", "class": "SwHCTb", "data-precision": 2})
    convert_cny = soup_cny.findAll("span", {"class": "DFlfde", "class": "SwHCTb", "data-precision": 2})
    return Currency.objects.create(
        currency_usd=convert[0].text,
        currency_aed=convert_dir[0].text,
        currency_eur=convert_evro[0].text,
        currency_cnr=convert_cny[0].text,
    )
