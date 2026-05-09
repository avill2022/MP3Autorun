# MP3 Autorun Player

A modern, recursive Python music player with a two-panel UI for easy folder navigation and playback. It organizes your music collection by directory, parses embedded metadata (like album covers and lyrics), and remembers what you've played to offer a smart rotation of your tracks.

## Features

- **Modern Two-Panel UI**: A clean split-view interface prioritizing folder navigation on the left and song selection on the right.
- **Recursive Directory Scanning**: Accurately maps your music folders, allowing playback of all audio files nested within any selected directory hierarchy.
- **Smart Rotation & Randomizer**: Stateful folder and song tracking ensures balanced rotation. It keeps track of previously visited directories and tracks, ensuring a fresh mix until all options are exhausted.
- **Embedded Metadata Support**: Automatically extracts and displays album cover art and lyrics from supported audio formats (MP3, FLAC, etc.).
- **Automatic Playback**: Remembers playback state and automatically plays the next song/folder based on intelligent selection logic.

## Prerequisites

- Python 3.8+
- Required dependencies listed in `requirements.txt`.

## Installation

1. Clone the repository or download the source code.
2. Install the required dependencies using pip:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. Run the application:
   ```bash
   python main.py
   ```
2. **First Run**: Select your root music folder when prompted (or configure it in the UI/code).
3. **Left Panel**: Browse through the recursive folder structure of your music collection.
4. **Right Panel**: View and select songs from the highlighted folder.
5. **Playback**: Use the bottom control bar for play/pause, next, previous, and to view current song metadata and album art.

## Technologies Used

- **Tkinter**: Standard Python interface to the Tk GUI toolkit.
- **Pygame**: Used for robust audio playback control.
- **Mutagen**: For reading metadata (album art, lyrics, titles) from various audio formats.
- **Pillow (PIL)**: For image processing and displaying album cover art in the UI.
