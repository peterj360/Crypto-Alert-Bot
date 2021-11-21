from bs4 import BeautifulSoup
import smtplib
from email.message import EmailMessage
import requests
import time

user_email = input('Please input your email: ')
msg = EmailMessage()
msg['Subject'] = 'Crypto Alert'
msg['To'] = user_email
bot_email = 'cryptoalertbot123@gmail.com'
bot_password = 'vitbeogeelzghelr'
msg['From'] = 'Crypto Alert'

low_price_list = []
high_price_list = []
percent_list = []
price_change_list = []
valid_coin_list = []
coin_list = []
valid_check = False
valid = False


url = 'https://crypto.com/price'

html_text = requests.get(url).text
soup = BeautifulSoup(html_text, 'lxml')
cryptocurrencies = soup.find_all('a', class_='css-ttxvk0')

for cryptocurrency in cryptocurrencies:
    valid_coin = cryptocurrency.find('span', class_='chakra-text css-1mrk1dy').text.replace(' ', '-')
    valid_coin_list.append(valid_coin)

while not valid:
    valid = True
    coin_list = [item for item in input('Please list the cryptocurrencies in your portfolio (separated by commas): ').replace(', ', ',').replace(' ', '-').split(',')]
    for i in coin_list:
        valid_check = False
        for x in valid_coin_list:
            if i.lower() == x.lower():
                valid_check = True
        if not valid_check:
            print('Invalid Input')
            valid = False
            break

for i, x in zip(range(len(coin_list)), coin_list):
    low_input = float(input(f'Please input your selling price for {x}: '))
    low_price_list.append(low_input)

    high_input = float(input(f'Please input your buying price for {x}: '))
    high_price_list.append(high_input)

    percent_input = float(input(f'Please input your wanted 24 hour percent change for {x}: '))
    percent_list.append(percent_input)

    price_input = float(input(f'Please input your wanted 24 hour price change for {x}: '))
    price_change_list.append(price_input)


def find_coins():
    for c, l, h, p, pr in zip(coin_list, low_price_list, high_price_list, percent_list, price_change_list):
        website = f'https://coinmarketcap.com/currencies/{c}/'

        html_text = requests.get(website).text
        soup = BeautifulSoup(html_text, 'lxml')
        coin = soup.tbody

        coin_name = coin.tr.th.text.replace(' Price', '')
        coin_price = coin.tr.td.text
        percent_change_24h = coin.tr.next_sibling.td.div.text
        price_change_24h = coin.tr.next_sibling.td.span.text

        float_price = float(coin_price.replace('$', '').replace(',', ''))

        if price_change_24h[1] == '-':
            float_percent_change = float(percent_change_24h.replace('%', '')) * -1
            percent_change_24h = '-' + percent_change_24h
            price_change_24h = '-' + price_change_24h.replace('-', '')
            float_price_change = float(price_change_24h.replace('$', '').replace(',', '').replace('+', '').replace('-', '')) * -1
        else:
            float_percent_change = float(percent_change_24h.replace('%', ''))
            percent_change_24h = '+' + percent_change_24h
            price_change_24h = '+' + price_change_24h
            float_price_change = float(price_change_24h.replace('$', '').replace(',', '').replace('+', '').replace('-', ''))

        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.ehlo('smtp.gmail.com')
        server.starttls()

        if float_price <= l or float_percent_change <= p * -1 or float_price_change <= pr * -1:
            print("Email Sent")
            msg.set_content(f'{coin_name} is priced at {coin_price} (USD)\nPercent Change (24h): {percent_change_24h} \nPrice Change (24h): {price_change_24h}')
            server.login(bot_email, bot_password)
            server.send_message(msg)
        elif float_price >= h or float_percent_change >= p or float_price_change >= pr:
            print('Email Sent')
            msg.set_content(f'{coin_name} is priced at {coin_price} (USD)\nPercent Change (24h): {percent_change_24h} \nPrice Change (24h): {price_change_24h}')
            server.login(bot_email, bot_password)
            server.send_message(msg)
        server.quit()


if __name__ == '__main__':

    wait_time = int(input('Please input your preferred wait time (minutes): '))

    while True:
        find_coins()
        print(f'Waiting {wait_time} minute(s)...')
        time.sleep(wait_time * 60)
