import telebot
import config
import logging
import time
from telebot import types
from bs4 import BeautifulSoup
import sys, requests
from config import (
    TOKEN
)

bot = telebot.TeleBot(config.bot_token)
telebot.logger.setLevel(logging.DEBUG)

defaults = {
    'request': {
        'token': TOKEN,
        'base_url': 'https://api.genius.com'
    },
    'message': {
        'search_fail': 'The lyrics for this song were not found!',
        'wrong_input': 'Wrong number of arguments.\n' \
                       'Use two parameters to perform a custom search ' \
                       'or none to get the song currently playing on Spotify.'
    }
}
def request_song_info(song_title, artist_name):
    base_url = defaults['request']['base_url']
    headers = {'Authorization': 'Bearer ' + defaults['request']['token']}
    search_url = base_url + '/search'
    data = {'q': song_title + ' ' + artist_name}
    response = requests.get(search_url, data=data, headers=headers)

    return response

def scrap_song_url(url):
    page = requests.get(url)
    html = BeautifulSoup(page.text, 'html.parser')
    [h.extract() for h in html('script')]
    lyrics = html.find('div', class_='lyrics').get_text()

    return lyrics

# def get_current_song_info():
#     return {'artist': 'halsey', 'title': 'Nightmare'}



# def main():
#     args_length = len(sys.argv)
#     if args_length == 1:
#         # Get info about song currently playing on Spotify
#         current_song_info = get_current_song_info()
#         song_title = current_song_info['title']
#         artist_name = current_song_info['artist']
#     elif args_length == 3:
#         # Use input as song title and artist name
#         song_info = sys.argv
#         song_title, artist_name = song_info[1], song_info[2]
#     else:
#         print(defaults['message']['wrong_input'])
#         return
#
#     print('{} by {}'.format(song_title, artist_name))
#
#     # Search for matches in request response
#     response = request_song_info(song_title, artist_name)
#     json = response.json()
#     remote_song_info = None
#
#     for hit in json['response']['hits']:
#         if artist_name.lower() in hit['result']['primary_artist']['name'].lower():
#             remote_song_info = hit
#             break
#
#     # Extract lyrics from URL if song was found
#     if remote_song_info:
#         song_url = remote_song_info['result']['url']
#         lyrics = scrap_song_url(song_url)
#
#         #write_lyrics_to_file(lyrics, song_title, artist_name)
#
#         print(lyrics)
#     else:
#         print(defaults['message']['search_fail'])

@bot.inline_handler(lambda query: len(query.query.split()) == 2)
def query_text(inline_query):
    text = inline_query.query
    artist = inline_query.query.split()[0]
    song = inline_query.query.split()[1]
    current_song_info = {'artist': '{}'.format(artist), 'title': '{}'.format(song)}
    song_title = current_song_info['title']
    artist_name = current_song_info['artist']
   #bot.send_message(message.chat.id, "{} by {}".format(song_title, artist_name))

    # Search for matches in request response

    response = request_song_info(song_title, artist_name)
    json = response.json()
    remote_song_info = None

    for hit in json['response']['hits']:
        if artist_name.lower() in hit['result']['primary_artist']['name'].lower():
            remote_song_info = hit
            break
    if remote_song_info:
        song_url = remote_song_info['result']['url']
        lyrics = scrap_song_url(song_url)
        #bot.send_message(message.chat.id, lyrics)
        info = "{} by {}".format(song_title, artist_name)
        try:
            r = types.InlineQueryResultArticle('1', '{}'.format(info), types.InputTextMessageContent('{}'.format(lyrics)))
           # r2 = types.InlineQueryResultArticle('2', 'Result2', types.InputTextMessageContent('hi'))
            bot.answer_inline_query(inline_query.id, [r])
        except Exception as e:
            print(e)
    else:
        try:
            r = types.InlineQueryResultArticle('1', 'could not find that song', types.InputTextMessageContent('!!!!!!!'))
            bot.answer_inline_query(inline_query.id, [r])
        except Exception as e:
            print(e)
            #bot.send_message(message.chat.id, "i couldnt find this song!")
    # try:
    #     r = types.InlineQueryResultArticle('1', '{}'.format(text), types.InputTextMessageContent('hi'))
    #     r2 = types.InlineQueryResultArticle('2', 'Result2', types.InputTextMessageContent('hi'))
    #     bot.answer_inline_query(inline_query.id, [r, r2])
    # except Exception as e:
    #     print(e)

@bot.message_handler(commands=['lyric'])
def send(message):
    lyricss = message.text.split()
    if len(lyricss) == 3:
        artist = message.text.split()[1]
        song = message.text.split()[2]
        current_song_info = {'artist': '{}'.format(artist), 'title': '{}'.format(song)}
        song_title = current_song_info['title']
        artist_name = current_song_info['artist']
        bot.send_message(message.chat.id, "{} by {}".format(song_title, artist_name))
        # Search for matches in request response
        response = request_song_info(song_title, artist_name)
        json = response.json()
        remote_song_info = None

        for hit in json['response']['hits']:
            if artist_name.lower() in hit['result']['primary_artist']['name'].lower():
                remote_song_info = hit
                break
        if remote_song_info:
            song_url = remote_song_info['result']['url']
            lyrics = scrap_song_url(song_url)
            bot.send_message(message.chat.id, lyrics)
        else:
            bot.send_message(message.chat.id, "i couldnt find this song!")
    else:
        bot.send_message(message.chat.id, "wrong format")




print("-------------------")
print("-------------------")
print("-------------------")
print("bot run successfuly")
print("-------------------")
print("-------------------")
print("-------------------")

#bot.polling(none_stop=True, interval=0, timeout=3)

def main_loop():
    bot.polling(True)
    while 1:
        time.sleep(3)


if __name__ == '__main__':
    try:
        main_loop()
    except KeyboardInterrupt:
        print('\nExiting by user request.\n')
        sys.exit(0)


# if __name__ == '__main__':
#     main()