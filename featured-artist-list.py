import os
import re
from datetime import datetime

def extract_artist_data(file: str) -> str:
    lines = ''
    with open(file, mode='r', encoding='utf-8') as handler:
        lines = handler.readlines()

    name = ''
    link = ''
    for line in lines:
        if name == '':
            pos = line.find('title: "New Featured Artist: ')
            if pos != -1:
                parts = line.split('"\n')
                name = parts[0][29:]

        match = re.search('\'s Featured Artist (listing|library)\]\(https:\/\/osu\.ppy\.sh\/beatmaps\/artists\/[\w]+', line)
        if match is not None:
            artist_base_link = 'https://osu.ppy.sh/beatmaps/artists/'
            parts = match.string.split(artist_base_link)
            link = artist_base_link + line[line.index(artist_base_link)+len(artist_base_link):match.end()]
            break

    return '[' + name + '](' + link + ')'

def get_featured_artists(wiki_link: str) -> list:
    artists = [[] for x in range(12)]
    for root, dirs, files in os.walk(wiki_link):
        for file in files:
            if file.find('-new-featured-artist-') != -1:
                artist = extract_artist_data(root + '\\' + file)
                date = file[:10]
                date_obj = datetime.strptime(date, '%Y-%m-%d')
                artists[date_obj.month-1].append(artist)
    return artists

def list_featured_artists() -> None:
    wiki_link = r'osu-wiki\\news\\2022'
    artists = get_featured_artists(wiki_link)

    for i, month in enumerate(artists):
        print('Month: ' + str(i) + '\n')
        for artist in month:
            print(artist)
        print('')

def main() -> None:
    list_featured_artists()

if __name__ == '__main__':
        main()
