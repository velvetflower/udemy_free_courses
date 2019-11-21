import discord
import requests
from time import sleep
from bs4 import BeautifulSoup
from random import randint
import webbrowser

headers = {
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36 OPR/63.0.3368.58152',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-User': '?1',
    'DNT': '1',
}

# fill this with your udemy cookies

cookies = {
    '__cfduid': '',
    'ud_firstvisit': '',
    '__udmy_2_v57r': '',
    '_pxhd': '',
    'EUCookieMessageShown': 'true',
    'ud_locale': 'ru_RU',
    'muxData': '',
    '__cfruid': '',
    'ud_cache_version': '1',
    'ud_cache_modern_browser': '1',
    'ud_cache_marketplace_country': 'RU',
    'ud_cache_price_country': 'RU',
    'ud_cache_language': 'ru',
    'ud_cache_brand': 'RUru_RU',
    'csrftoken': '',
    'ud_last_auth_information': '',
    'ud_credit_last_seen': 'None',
    'ud_cache_user': '',
    'ud_cache_logged_in': '1',
    'dj_session_id': '',
    'client_id': '',
    'access_token': '',
    'ud_cache_release': '',
    'ud_credit_unseen': '0',
    'seen': '1',
    'ud_cache_campaign_code': 'LEARNNOW',
    'ud_cache_device': 'desktop',
    'evi': '',
    'ud_rule_vars': '',
    'eventing_session_id': ''
}

udemyHeaders = {
    'authority': 'www.udemy.com',
    'cache-control': 'max-age=0',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36 OPR/63.0.3368.58152',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-user': '?1',
    'dnt': '1',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'sec-fetch-site': 'none',
    'referer': 'https://google.com/',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
}

newsess = requests.Session()

APPROVED_LINKS = []

def main():
    global APPROVED_LINKS
    with open("links.txt", 'w') as file: # clean file
        file.write("")
    pageNum = 0
    position = 0
    name = ""
    while True:
        response = newsess.get(f'https://onehack.us/tags/udemycoupons?page={pageNum}', headers=headers)
        soup = BeautifulSoup(response.text, "html.parser")
        trs = soup.findAll('table')[0].findAll('tr')
        for i in trs:
            print (f'Status: position {position}; page {pageNum}; {name}')
            if len(APPROVED_LINKS) != 0:
                for i in APPROVED_LINKS:
                    webbrowser.open(i, new=2) # open link in webbrowser
                    with open("links.txt", 'a') as file: # write new links to file
                        file.write(i + "\n") 
                APPROVED_LINKS.clear()
                print ("Writed to file")
            try:
                position = i.contents[1].contents[1].attrs["content"]
                name = i.contents[1].contents[5].attrs["content"]
                url = i.contents[1].contents[3].attrs["content"]
            except:
                continue
            sleep(3)
            coupons = getUdemyLinks(url) # load coupon links to list
            sleep(3)
            if coupons != 0:
                for link in coupons:
                    print (f"Checking {link}")
                    checkLink = checkInUdemy(link) # check link in udemy
                    if checkLink == 1:
                        print ("Allowed to sign in for free!")
                        APPROVED_LINKS.append(link) # if we can sign in so add link
                        sleep(5)
                    else:
                        print ("Not allowed to sign in!")
                        sleep(5)
            else:
                sleep(5)

        pageNum += 1
        print ("Page increased")
        if pageNum == 65:
            exit()

def getUdemyLinks(urlink):
    # collect links with coupons
    listWithCoupons = []
    response2 = newsess.get(urlink, headers=headers)
    soup = BeautifulSoup(response2.text, "html.parser")
    try:
        posts = soup.contents[2].contents[3].contents[1].contents[3].contents[9].contents[3] # huehuhue
        for i in posts.contents:
            if i != "\n":
                listWithCoupons.append(i.contents[0].attrs["href"])
            else:
                continue
    except:
        if len(listWithCoupons) == 0:
            return 0

    if len(listWithCoupons) != 0:
        return listWithCoupons
    else:
        return 0

def checkInUdemy(urlink):
    # checking if corse available to sign up for your account
    try:
        udemyResponse = requests.get(urlink, headers=headers, cookies=cookies)
        soup = BeautifulSoup(udemyResponse.text, "html.parser")
        udemyButtonDiv = soup.findAll("div", {"class": "ud-component--clp--buy-button"})[0].contents[1].contents[0].replace("\n","")
        if udemyButtonDiv == "Зарегистрироваться": # change to your language
            return 1
        else:
            return 0
    except:
        return 0

main()