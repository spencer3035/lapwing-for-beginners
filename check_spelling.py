import json
import os
import requests

def load_lapwing_dict():
    """Loads the Lapwing stenography dictionary from a JSON file."""
    # Try to get local dictionary (linux). This will work assuming the user has installed plover and the plover-lapwig-aio plugin
    home_dir = os.path.expanduser("~")
    lapwig_dict_path = os.path.join(home_dir, ".config/plover/lapwing-base.json")
    if os.path.exists(lapwig_dict_path): 
        with open(lapwig_dict_path, 'r', encoding='utf-8') as file:
            return json.load(file)

    # Fall back to download dictionary from github
    url = "https://raw.githubusercontent.com/aerickt/plover-lapwing-aio/refs/heads/main/plover_lapwing/dictionaries/lapwing-base.json"
    response = requests.get(url)
    response.raise_for_status()
    return response.json()

def load_stroke_to_outline(file_path):
    """Loads the stroke-to-outline mappings from a practice '.txt' file."""
    stroke_to_outline = {}
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            parts = line.strip().split()
            if len(parts) == 2:
                outline, stroke = parts
                stroke_to_outline[stroke] = outline
    return stroke_to_outline

def check_syllable_mappings(lapwing_dict, stroke_to_outline):
    """Checks if the given words have correct mappings in the dictionary."""
    incorrect_mappings = {}

    # Note that this only checks direct mappings, not suffixes and prefixes. So
    # any tests that use those as mappings will report as errors when they are
    # not.
    for given_stroke, given_outline in stroke_to_outline.items():
        lapwing_outline = lapwing_dict.get(given_stroke)
        lapwing_strokes = [key for key, val in lapwing_dict.items() if val == given_outline]
        if lapwing_outline != given_outline:
            msg = f"\"{given_outline} => {given_stroke}\" should be one of \"{lapwing_strokes}\""
            incorrect_mappings[given_outline] = msg

    return incorrect_mappings

def check_spelling(file, lapwig_dict):
    """Checks mappings are correct and prints results"""
    stroke_to_outline = load_stroke_to_outline(file)
    incorrect_mappings = check_syllable_mappings(lapwig_dict, stroke_to_outline)

    if incorrect_mappings:
        print(f"Found incorrect mapping in {file}")
        for _, message in incorrect_mappings.items():
            print(f"{message}")

        print()

    return

def main(): 
    lapwig_dictonary = load_lapwing_dict()
    practice_directory = "./src/practice/"

    # finds all files ending in .txt in the target directory
    for f in os.listdir(practice_directory):
        if f.endswith('.txt'):
            words_to_check_filename = practice_directory + f;
            check_spelling(words_to_check_filename, lapwig_dictonary)

    return

if __name__ == "__main__":
    main()
