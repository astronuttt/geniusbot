import telebot
import config
import requests


bot = telebot.TeleBot(config.token)

client_id = '9QxQRJDvEwyKjpVn3JoHez7p8BsnPO7rpehzmwlKBdFZjN71BrKfLVzQnyXyvCih'
client_secret = 'tePSLljN6UBeanWG3zqqw60r0qkp6Us2uf2iaBDfHBRGFRmKIfipCGXbZi6EP4WMnP-f-FTAhPO_ExY01S6Aig'
access_token = 'zUKGnnzvuNhVS4s0LaafO09KaHgnxms1PO_pt1JH9H4Rs6tBRgMRksJNtDtgcBLw'

def request_song_info(song_title, artist_name):
    base_url = 'https://api.genius.com'
    headers = {'Authorization': 'Bearer' + access_token}
    search_url = base_url + '/search'
    data = {'q': song_title + ' ' + artist_name}
    response = requests.get(search_url, data=data, headers=headers)

    return response

title = "Nightmare"
artist = "halsey"

request_song_info(title, artist)