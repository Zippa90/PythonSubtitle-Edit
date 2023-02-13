#!/usr/bin/python3
 
import os
import subprocess
import re
 
def extract_subtitle(file):
 
    # First command: mkvmerge -i file
    mkvmerge_output = subprocess.run(["mkvmerge", "-i", file], capture_output=True, text=True)
    mkvmerge_output = mkvmerge_output.stdout
 
    # Check for HDMV PGS subtitles
    if not "HDMV PGS" in mkvmerge_output:
        print("Skipping file", os.path.dirname(file)[:30]+"/"+file[:30], "as it does not have HDMV PGS subtitles")
        return None
 
    # Show the available track IDs
    print(mkvmerge_output)
 
    # Ask the user for the track number
    track_num = input("Enter the track number (or X to skip):")
 
    # Skip the file if X was entered
    if track_num == "X":
        return None
 
    return file, track_num
 
tracks_to_extract = []
 
# Find all .mkv files in the current directory and subdirectories
for root, dirs, files in os.walk("."):
    for file in files:
        if not file.endswith(".mkv"):
            continue
 
        file = os.path.join(root, file)
 
        # Check if the file has a .sup or .srt file with the same name
        if os.path.isfile(file + ".sup") or os.path.isfile(file + ".srt"):
            print("Skipping file", os.path.dirname(file)[:30]+"/"+file[:30], "as it already has a .sup or .srt file")
            continue
 
        track = extract_subtitle(file)
        if track:
            tracks_to_extract.append(track)
 
# Extract the tracks
if tracks_to_extract:
    for file, track_num in tracks_to_extract:
        subprocess.run(["mkvextract", file, "tracks", f"{track_num}:{file}.sup"])
else:
    print("No tracks found to extract")
 
