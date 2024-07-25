# Description
This repository contains some tools I use for aiding with DJing.

This is currently intended to be used on macOS

## Normalize Genres

This scipt contains a bunch of rules for normalizing song genre tagging. This currently includes:
- specifying genres that are an alias for other genres. It will look for, e.g. "liquid dnb" and add the tag "liquid funk". This can be a "one to many", "many to many", "many to one", or "wildcard to many" relationship (with the use of regex). Currently it will also, for example, look for any genres containg "dub" and add the "dub" tag to it. This could be "deep dub", "dubstep", "minimal dub", "experimental dub" etc... There are many rules, custom to my library, that are easy to expand upon.
- specifying artist/genre pairings that are an alias for other genres. I found some artists use wonly genres regularly that are non-specific, but no one else really uses. e.g. the artist "Sound In Noise" labels all of his music "estonian electronic" despite it basically being neurofunk. This supports remixing artists.

This script also will output a summary of genres you may want to add rules to.
- This mostly consistes of genres that do not contain rules for them that appear in your library for which there are songs that only contain a combination of genres with no rules. 
- It will also report the "Artist - Song File Path" pairing to make it easier to add rules for a genre or artist/genre pairing.
- There is a spot for exclusions to clean up the output as well. Say you have a small library of "Breaks", and don't have any rules around it as your tags for that genre are clean and useful. Just add it to the list!

* note: the current rules are built around Spotify's genre-tagging system. You would ideally add new implementations, or edit the current script to meet your needs with your specific tags and genres. I tend to have DnB in my library, and Beatport basically just labels every "Drum & Bass" regardless of neuro, liquid, dancefloor, etc... but it may be a better option for other genres.

### Setup:
chmod +x setup_env.sh
sh ./setup_env.sh

### Use
python3 normalizeGenres -path <relative_path_to_music_library>

## Clear Beatport Tags
A very dumb script that just iterates your library and clears the genre tags for anything that starts with a capital letter. It is not perfect and misses stuff that starts with a number (140). I will have to fix this later.

