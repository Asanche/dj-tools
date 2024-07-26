import os
import re
import argparse
from mutagen.easyid3 import EasyID3
from mutagen.id3 import ID3NoHeaderError

# Define the alias lookup dictionary with regular expressions for wildcards
alias_lookup = {
    ('liquid dnb', 'liquid drum and bass'): ['liquid funk'],  # Multiple aliases example
    ('filthstep', 'neurofunk', 'neurostep', 'darkstep', 'liquid funk', 'drum funk', 'drumfunk', 'chill breakcore', 'jump up', 'tech step'): ['drum and bass'],
    ('deep liquid bass', 'deep rai', 'charva'): ['deep dnb', 'liquid funk', 'drum and bass'],
    ('bassline', 'boston electronic', 'wonky', 'experimental bass'): ['dub', 'halftime dnb'],
    'breakbeat': ['breaks'],
    'raggatek': ['hardcore', 'drum and bass', 'tekno'],
    ('speedcore', 'tekno', 'tek'): ['hardcore'],
    r'.*dnb.*$': ['drum and bass'],  # Regex wildcard example ("uk dnb" or "dnb xyz" => "drum and bass")
    r'.*techno.*$': ['techno'],
    r'.*jungle.*$': ['jungle'],
    r'.*ukg.*$': ['garage', 'ukg'],
    r'.*house.*$': ['house'],
    r'.*trap.*$': ['trap'],
    r'.*hardcore.*$': ['hardcore'],
    r'.*dub.*$': ['dub'],  # This will do "deep dub", "dubstep" or even "minimal dub" => dub
    # Add more aliases as needed
}

# Define genres to exclude from the unmatched genres output
excluded_genres = {'breaks', 'drum and bass'}

# Define specific artist/genre pairing rules
artist_genre_rules = {
    ('harmony', 'musical advocacy'): ['jungle'],
    ('sound in noise', 'estonian electronic'): ['drum and bass', 'neurofunk'],
    ('missin', 'serbian electronic'): ['drum and bass', 'neurofunk'],
    ('jon casey', 'south african electronic'): ['halftime dnb', 'drum and bass'],
    ('jon casey', 'miami electronic'): ['halftime dnb', 'drum and bass'],
    ('jon casey', 'gauze pop'): ['halftime dnb', 'drum and bass'],
    ('baby t', 'munich electronic'): ['breaks', 'techno'],
    ('billain', 'croatian electronic'): ['drum and bass', 'neurofunk', 'darkstep'],
    ('viers', 'experimental club'): ['breaks', 'techno'],
    ('fourward', 'electronica'): ['drum and bass', 'neurofunk'],
    ('hybrid minds', 'neo mellow'): ['drum and bass', 'liquid funk'],
    ('hybrid minds', 'uk pop'): ['drum and bass', 'liquid funk'],
    ('hybrid minds', 'viral pop'): ['drum and bass', 'liquid funk'],
    ('phibes', 'bass house'): ['drum and bass', 'jump up', 'dancefloor dnb'],  # A tonne of their music is mislabeled as house. They make basshouse, but most of this is DnB...
    # Add more specific artist/genre pairing rules as needed
}

def extract_artists(audio):
    """Extract artists from the audio metadata, including featuring and remix artists from the title."""
    artists = set()

    # Extract main artists
    if 'artist' in audio:
        for artist in audio['artist'][0].split(','):
            artists.add(artist.strip().lower())

    # Extract featuring artists from the title
    if 'title' in audio:
        feature_matches = re.findall(r'\(featuring ([^)]+)\)', audio['title'][0], re.IGNORECASE)
        for match in feature_matches:
            feature_artist = match.strip().lower()
            artists.add(feature_artist)
        
        # Extract remix artists from the title
        remix_matches = re.findall(r'\(([^)]+ remix)\)', audio['title'][0], re.IGNORECASE)
        for match in remix_matches:
            remix_artist = match.lower().replace(' remix', '').strip()
            artists.add(remix_artist)
    
    return artists

def normalize_genre(artists, genres):
    """Normalize genres based on alias lookup and specific artist/genre pairing rules."""
    updated_genres = set(genres)
    for genre in genres:
        genre_lower = genre.lower().strip()  # Trim whitespace and convert to lowercase
        matched = False

        # Check artist/genre specific rules first
        for artist in artists:
            if (artist, genre_lower) in artist_genre_rules:
                updated_genres.update(artist_genre_rules[(artist, genre_lower)])
                matched = True

        # Check general alias lookup if no match in artist/genre specific rules
        if not matched:
            for key, normalized_genres in alias_lookup.items():
                if isinstance(key, tuple):
                    if genre_lower in [k.lower() for k in key]:
                        updated_genres.update(normalized_genres)
                        matched = True
                elif isinstance(key, str) and re.match(key, genre_lower):
                    updated_genres.update(normalized_genres)
                    matched = True
                if matched:
                    break
    return list(updated_genres)

def process_files(folder_path):
    """Process files in the given folder to normalize genre tags based on alias lookup."""
    alias_found_count = 0
    no_genre_count = 0
    unmatched_genres = {}  # To track genres not matched by alias lookup
    no_genre_files = []    # To track files with no genre tags

    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.endswith(('.mp3', '.flac', '.m4a', '.ogg', '.wav')):
                file_path = os.path.join(root, file)
                try:
                    audio = EasyID3(file_path)
                except ID3NoHeaderError:
                    audio = EasyID3()

                artists = extract_artists(audio)
                if 'genre' in audio:
                    # Trim whitespace from genre tags
                    genres = [genre.strip() for genre in audio['genre'][0].split(', ')]
                    updated_genres = normalize_genre(artists, genres)
                    updated_genres_str = ', '.join(updated_genres)
                    
                    if set(genres) != set(updated_genres):
                        alias_found_count += 1
                        print(f"Updating genres for file: {file_path} (was '{audio['genre'][0]}', now '{updated_genres_str}')")
                        audio['genre'] = updated_genres_str
                        audio.save()
                        # Skip adding to unmatched_genres as it has been updated
                        continue
                    
                    # Check for unmatched genres
                    genres_lower = [genre.lower() for genre in genres]
                    matched_genres = set()
                    for genre in genres_lower:
                        if any(
                            (isinstance(key, tuple) and genre in [k.lower() for k in key]) or
                            (isinstance(key, str) and re.match(key, genre))
                            for key in alias_lookup.keys()
                        ):
                            matched_genres.add(genre)
                        for normalized_genres in alias_lookup.values():
                            if genre in [g.lower() for g in normalized_genres]:
                                matched_genres.add(genre)
                    
                    # Add to unmatched_genres if no genres in the file are matched and not in excluded genres
                    if not matched_genres:
                        for genre in genres_lower:
                            if genre not in excluded_genres:
                                if genre not in unmatched_genres:
                                    unmatched_genres[genre] = []
                                unmatched_genres[genre].append((artists, file_path))
                else:
                    no_genre_count += 1
                    no_genre_files.append((audio.get('title', ['Unknown Title'])[0], file_path))
                    print(f"No genre tag found in file: {file_path}")

    print(f"\nSummary:")
    print(f"Songs found with aliases: {alias_found_count}")
    print(f"Songs found with no genre tag: {no_genre_count}")
    if no_genre_files:
        for title, path in no_genre_files:
            print(f" - {title} ({path})")

    if unmatched_genres:
        print("\nUnmatched genres that might need new rules:")
        for genre in sorted(unmatched_genres):
            print(f" - {genre}")
            for artists, song in unmatched_genres[genre]:
                artist_str = ', '.join(artists) if artists else 'Unknown Artist'
                print(f"    * {artist_str} - {song}")

def main():
    parser = argparse.ArgumentParser(description='Normalize genre tags based on alias lookup.')
    parser.add_argument('-path', type=str, help='Relative path to the folder', required=True)
    args = parser.parse_args()

    folder_path = args.path
    process_files(folder_path)

if __name__ == '__main__':
    main()
