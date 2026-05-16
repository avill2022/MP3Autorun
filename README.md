# Yousawso Video Player

A modern, recursive Python video player with a two-panel UI for easy folder navigation and playback. It organizes your video collection by directory, parses embedded metadata, and remembers what you've played to offer a smart rotation of your videos.

## Features

- **Modern Two-Panel UI**: A clean split-view interface prioritizing folder navigation on the left and video selection on the right.
- **Recursive Directory Scanning**: Accurately maps your video folders, allowing playback of all video files nested within any selected directory hierarchy.
- **Smart Rotation & Randomizer**: Stateful folder and video tracking ensures balanced rotation. It keeps track of previously visited directories and tracks, ensuring a fresh mix until all options are exhausted.
- **Embedded Metadata Support**: Automatically extracts metadata from supported video formats.
- **Automatic Playback**: Remembers playback state and automatically plays the next video/folder based on intelligent selection logic.

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
3. **Left Panel**: Browse through the recursive folder structure of your video collection.
4. **Right Panel**: View and select videos from the highlighted folder.
5. **Playback**: Use the bottom control bar for play/pause, next, previous, and to view current video metadata.

## Technologies Used

- **Tkinter**: Standard Python interface to the Tk GUI toolkit.
- **python-vlc**: Used for robust video playback control.
- **tinytag**: For reading metadata (titles, duration) from various video formats.
- **Pillow (PIL)**: For image processing in the UI.
