import os
import sys
import argparse
from mutagen.easyid3 import EasyID3
from mutagen.id3 import ID3NoHeaderError

def clear_genre_if_capitalized(folder_path):
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.endswith(('.mp3', '.flac', '.m4a', '.ogg', '.wav')):
                file_path = os.path.join(root, file)
                try:
                    audio = EasyID3(file_path)
                except ID3NoHeaderError:
                    audio = EasyID3()
                
                if 'genre' in audio:
                    genre = audio['genre'][0]
                    if genre and genre[0].isupper():
                        print(f"Clearing genre for file: {file_path} (was '{genre}')")
                        del audio['genre']
                        audio.save()
                else:
                    print(f"No genre tag found in file: {file_path}")

def main():
    parser = argparse.ArgumentParser(description='Clear genre tags that start with a capital letter.')
    parser.add_argument('-path', type=str, help='Relative path to the folder', required=True)
    args = parser.parse_args()

    folder_path = args.path
    clear_genre_if_capitalized(folder_path)

if __name__ == '__main__':
    main()