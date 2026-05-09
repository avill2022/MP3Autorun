import os
import json
import random
import time
from typing import List

# Assume Sound is imported from scanner if needed for type hinting, 
# but we can use 'any' or forward reference if not directly imported here.
from scanner import Sound

class Selecter:
    """Class containing rules for selecting a song by folder."""

    @staticmethod
    def get_song_ramdomply(sounds: List[Sound], folder_path: str, use_random_offset: bool = True) -> Sound:
        """
        Selects a song from a list of sounds based on history stored in a JSON file
        in the specified folder.

        Args:
            sounds: List of Sound objects available in the folder.
            folder_path: The path to the folder.

        Returns:
            The selected Sound object.
        """
        if not sounds:
            return None

        # Extract the base folder name
        folder_name = os.path.basename(os.path.normpath(folder_path))
        if not folder_name or folder_name == ".":
            # Fallback if folder_path is somehow the root directory
            folder_name = "root"

        # Define path for the history json file
        json_file_path = os.path.join(folder_path, f"{folder_name}.json")

        data = {
            "current": {
                "song": "",
                "time": ""
            },
            "selected": []
        }

        # Check if history file exists
        if os.path.exists(json_file_path):
            try:
                with open(json_file_path, 'r', encoding='utf-8') as f:
                    file_data = json.load(f)
                    if "selected" in file_data:
                        data["selected"] = file_data["selected"]
                    if "current" in file_data:
                        data["current"] = file_data["current"]
            except (json.JSONDecodeError, IOError):
                # If there's an error reading it, we'll just start fresh
                pass

        # Filter out songs that have already been played
        available_sounds = [s for s in sounds if s.file_name not in data["selected"]]

        # 1. If all sounds were selected (or no sounds are available), restart the JSON history
        if not available_sounds:
            data["selected"] = []
            available_sounds = sounds.copy()

        # 2. Select one random song from the available (not selected) songs
        chosen_sound = random.choice(available_sounds)

        # Generate a random offset between 0 and half of the duration
        random_offset_ms = 0
        if use_random_offset and chosen_sound.duration:
            random_offset_ms = random.randint(0, int(chosen_sound.duration * 1000 / 2))

        # Update the JSON data
        data["selected"].append(chosen_sound.file_name)
        data["current"] = {
            "song": chosen_sound.file_name,
            # Subtract the offset so when the diff is calculated it acts as elapsed time
            "time": str(int(time.time() * 1000) - random_offset_ms)
        }

        # Save the updated data back to the JSON file
        try:
            with open(json_file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=4, ensure_ascii=False)
        except IOError as e:
            print(f"Warning: Could not save selection history to {json_file_path}: {e}")

        # Set the erapse_time to the random offset instead of the current epoch time
        chosen_sound.erapse_time = random_offset_ms
        return chosen_sound

    @staticmethod
    def get_current_song(sounds: List[Sound], folder_path: str) -> Sound:
        """
        Gets the current song from the folder's JSON history. 
        If not found, falls back to get_song_ramdomply.
        """
        if not sounds:
            return None

        folder_name = os.path.basename(os.path.normpath(folder_path))
        if not folder_name or folder_name == ".":
            folder_name = "root"

        json_file_path = os.path.join(folder_path, f"{folder_name}.json")

        if os.path.exists(json_file_path):
            try:
                with open(json_file_path, 'r', encoding='utf-8') as f:
                    file_data = json.load(f)
                    if "current" in file_data:
                        current_song_name = file_data["current"].get("song")
                        song_played_at = file_data["current"].get("time")
                        
                        if current_song_name:
                            for sound in sounds:
                                if sound.file_name == current_song_name:
                                    if song_played_at:
                                        try:
                                            #the time when the song was played is allways less than the current time so..
                                            diff = int(time.time() * 1000) - int(song_played_at)
                                            sound.erapse_time = diff
                                            dur = int(sound.duration * 1000)
                                            if(diff > dur):
                                                if((diff - dur)>15000):
                                                    return Selecter.get_song_ramdomply(sounds, folder_path, use_random_offset=True)
                                                else:
                                                    return Selecter.get_song_ramdomply(sounds, folder_path ,use_random_offset=False)
                                        except ValueError:
                                            sound.erapse_time = int(time.time() * 1000)
                                    else:
                                        sound.erapse_time = int(time.time() * 1000)
                                    return sound
            except (json.JSONDecodeError, IOError):
                pass
                
        return Selecter.get_song_ramdomply(sounds, folder_path)

    @staticmethod
    def get_folder_ramdomly(folders: List[str]) -> str:
        """
        Selects a folder randomly from a list, tracking history in folder.json.
        """
        if not folders:
            return ""

        json_file_path = "folder.json"

        data = {
            "current folder": "",
            "folders selected": []
        }

        if os.path.exists(json_file_path):
            try:
                with open(json_file_path, 'r', encoding='utf-8') as f:
                    file_data = json.load(f)
                    if "folders selected" in file_data:
                        data["folders selected"] = file_data["folders selected"]
                    if "current folder" in file_data:
                        data["current folder"] = file_data["current folder"]
            except (json.JSONDecodeError, IOError):
                pass

        available_folders = [f for f in folders if f not in data["folders selected"]]

        if not available_folders:
            data["folders selected"] = []
            available_folders = folders.copy()

        chosen_folder = random.choice(available_folders)

        data["folders selected"].append(chosen_folder)
        data["current folder"] = chosen_folder

        try:
            with open(json_file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=4, ensure_ascii=False)
        except IOError as e:
            print(f"Warning: Could not save folder selection history to {json_file_path}: {e}")

        return chosen_folder

    @staticmethod
    def get_current_folder(folders: List[str]) -> str:
        """
        Returns the current folder from folder.json if it exists,
        otherwise selects one randomly.
        """
        json_file_path = "folder.json"
        
        if os.path.exists(json_file_path):
            try:
                with open(json_file_path, 'r', encoding='utf-8') as f:
                    file_data = json.load(f)
                    current_folder = file_data.get("current folder", "")
                    if current_folder and current_folder in folders:
                        return current_folder
            except (json.JSONDecodeError, IOError):
                pass
                
        return Selecter.get_folder_ramdomly(folders)
