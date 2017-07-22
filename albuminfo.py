#!/bin/python

import argparse, json, sys, urllib.request

### Global Variable Definitions ###
album_url = 'https://jsonplaceholder.typicode.com/photos?albumId=%d'

### Global Functions ###
def get_album_info(album_number):
    """Retrieves photo album information for a specific album.

       The function retrieves photo album information, filtered by a specified
       photo album number (album ID). While all album numbers, both positive
       and negative are valid, some album numbers may return no results.
       """

    with urllib.request.urlopen(album_url % album_number) as url:
        data = json.loads(url.read().decode())
        return data

def print_album_info(album_data_list):
    """Prints information about photos in a photo album.

       Function iterates through a list of photo data, each containing
       information about that photo, and prints out to the console the photo
       id and title text in the format '[id] title'.
    """

    for picture_info in album_data_list:
        print('[{id}] {title}'.format(id=picture_info['id'], title=picture_info['title']))

### Main Program ###

def main(sysargs):
    parser = argparse.ArgumentParser(description='Displays photo ids and title texts from a photo album')
    parser.add_argument('album_num', type=int, help='the album number to display')
    parsed_args = parser.parse_args(sysargs)

    album_json = get_album_info(parsed_args.album_num)
    print_album_info(album_json)

    return

if __name__ == '__main__':
    main(sys.argv[1:])
