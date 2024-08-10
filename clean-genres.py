import os
import shutil
import argparse
from mutagen.easyid3 import EasyID3
from mutagen.id3 import ID3NoHeaderError

def log_error(message):
    with open("error_log.txt", "a") as log_file:
        log_file.write(message + "\n")

def clear_genre_if_capitalized_or_special(folder_path, move_to_processed):    
    processed_folder = os.path.join(folder_path, 'processed')
    if move_to_processed and not os.path.exists(processed_folder):
        os.makedirs(processed_folder)

    for root, dirs, files in os.walk(folder_path):
        for file in files:
            print(f"Processing {file}")
            if file.endswith(('.mp3', '.flac', '.m4a', '.ogg', '.wav')):
                file_path = os.path.join(root, file)
                try:
                    try:
                        audio = EasyID3(file_path)
                    except ID3NoHeaderError:
                        audio = EasyID3()
                    
                    if 'genre' in audio:
                        genre_list = audio['genre']
                        if genre_list:  # Check if the genre list is not empty
                            new_genres = []
                            move_file = False
                            for genre in genre_list:
                                genre = genre.strip()  # Remove leading and trailing spaces
                                if genre and (genre[0].isupper() or not genre[0].isalpha()):
                                    print(f"Clearing genre '{genre}' for file: {file_path}")
                                    continue
                                else:
                                    new_genres.append(genre)
                                    if genre and genre[0].islower():
                                        move_file = True
                            
                            if new_genres:
                                audio['genre'] = new_genres
                                audio.save()
                            else:
                                print(f"All genres cleared for file: {file_path}")
                                del audio['genre']
                                audio.save()

                            if move_to_processed and move_file:
                                try:
                                    new_file_path = os.path.join(processed_folder, file)
                                    base, ext = os.path.splitext(file)
                                    counter = 1
                                    while os.path.exists(new_file_path):
                                        new_file_path = os.path.join(processed_folder, f"{base}_{counter}{ext}")
                                        counter += 1
                                    
                                    print(f"Moving file to processed folder: {file_path} -> {new_file_path}")
                                    shutil.move(file_path, new_file_path)
                                except Exception as e:
                                    log_error(f"Error moving file {file_path}: {e}")
                        else:
                            print(f"No genre tag found in file: {file_path}")
                except Exception as e:
                    log_error(f"Error processing file {file_path}: {e}")

def main():
    parser = argparse.ArgumentParser(description='Clear genre tags that start with a capital letter, number, or symbol, and handle comma-separated genres.')
    parser.add_argument('-path', type=str, help='Relative path to the folder', required=True)
    parser.add_argument('--move', action='store_true', help='Move files with lowercase genre tags to a "processed" sub-folder')
    args = parser.parse_args()

    folder_path = args.path
    move_to_processed = args.move
    clear_genre_if_capitalized_or_special(folder_path, move_to_processed)

if __name__ == '__main__':
    main()
