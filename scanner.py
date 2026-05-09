import os
import mutagen
from mutagen.mp3 import MP3
from mutagen.flac import FLAC
from mutagen.mp4 import MP4
from mutagen.oggvorbis import OggVorbis
from mutagen.wave import WAVE
from pathlib import Path
from typing import List, Dict, Optional
import json

class Sound:
    """Class representing a sound file with its metadata tags"""
    
    def __init__(self, file_path: str):
        self.src = file_path
        self.file_name = os.path.basename(file_path)
        self.file_extension = os.path.splitext(file_path)[1].lower()
        self.file_size = os.path.getsize(file_path)
        
        # Basic tags
        self.title = None
        self.artist = None
        self.album = None
        self.genre = None
        self.year = None
        self.track_number = None
        self.duration = None
        self.bitrate = None
        self.sample_rate = None
        
        # Additional metadata
        self.composer = None
        self.comment = None
        self.album_artist = None
        self.disc_number = None
        self.lyrics = None
        self.erapse_time = None
        self.cover_data = None
        self.cover_mime = None
        self.raw_tags = {}
        
        # Load tags based on file type
        self._load_tags()
    
    def _load_tags(self):
        """Load tags based on the file extension"""
        try:
            if self.file_extension == '.mp3':
                self._load_mp3_tags()
            elif self.file_extension == '.flac':
                self._load_flac_tags()
            elif self.file_extension == '.m4a':
                self._load_mp4_tags()
            elif self.file_extension == '.ogg':
                self._load_ogg_tags()
            elif self.file_extension == '.wav':
                self._load_wav_tags()
            else:
                print(f"Unsupported format: {self.file_extension}")
        except Exception as e:
            print(f"Error loading tags for {self.src}: {e}")
    
    def _load_mp3_tags(self):
        """Load tags from MP3 files"""
        audio = MP3(self.src)
        self.duration = audio.info.length
        self.bitrate = audio.info.bitrate
        self.sample_rate = audio.info.sample_rate
        
        # Load common tags
        if 'TIT2' in audio:
            self.title = str(audio['TIT2'])
        if 'TPE1' in audio:
            self.artist = str(audio['TPE1'])
        if 'TALB' in audio:
            self.album = str(audio['TALB'])
        if 'TCON' in audio:
            self.genre = str(audio['TCON'])
        if 'TYER' in audio:
            self.year = str(audio['TYER'])
        if 'TRCK' in audio:
            self.track_number = str(audio['TRCK'])
        if 'TCOM' in audio:
            self.composer = str(audio['TCOM'])
        if 'COMM' in audio:
            self.comment = str(audio['COMM'])
        if 'TPE2' in audio:
            self.album_artist = str(audio['TPE2'])
        
        # Try to find lyrics (USLT frames) and album covers (APIC frames)
        for key in audio:
            if key.startswith('USLT'):
                self.lyrics = str(audio[key].text) if hasattr(audio[key], 'text') else str(audio[key])
            elif key.startswith('APIC'):
                self.cover_data = audio[key].data
                self.cover_mime = audio[key].mime
        
        # Store all raw tags
        for key, value in audio.items():
            self.raw_tags[key] = str(value)
    
    def _load_flac_tags(self):
        """Load tags from FLAC files"""
        audio = FLAC(self.src)
        self.duration = audio.info.length
        self.bitrate = audio.info.bitrate
        self.sample_rate = audio.info.sample_rate
        
        # Load common tags
        self.title = self._get_first_value(audio.get('title'))
        self.artist = self._get_first_value(audio.get('artist'))
        self.album = self._get_first_value(audio.get('album'))
        self.genre = self._get_first_value(audio.get('genre'))
        self.year = self._get_first_value(audio.get('date'))
        self.track_number = self._get_first_value(audio.get('tracknumber'))
        self.composer = self._get_first_value(audio.get('composer'))
        self.comment = self._get_first_value(audio.get('comment'))
        self.album_artist = self._get_first_value(audio.get('albumartist'))
        self.disc_number = self._get_first_value(audio.get('discnumber'))
        self.lyrics = self._get_first_value(audio.get('lyrics')) or self._get_first_value(audio.get('unsyncedlyrics'))
        
        # Store all raw tags
        for key, value in audio.items():
            self.raw_tags[key] = str(value)
    
    def _load_mp4_tags(self):
        """Load tags from MP4/M4A files"""
        audio = MP4(self.src)
        self.duration = audio.info.length
        self.bitrate = audio.info.bitrate
        self.sample_rate = audio.info.sample_rate
        
        # MP4 tag mapping
        self.title = self._get_first_value(audio.get('\xa9nam'))
        self.artist = self._get_first_value(audio.get('\xa9ART'))
        self.album = self._get_first_value(audio.get('\xa9alb'))
        self.genre = self._get_first_value(audio.get('\xa9gen'))
        self.year = self._get_first_value(audio.get('\xa9day'))
        self.track_number = self._get_track_number(audio.get('trkn'))
        self.composer = self._get_first_value(audio.get('\xa9wrt'))
        self.comment = self._get_first_value(audio.get('\xa9cmt'))
        self.album_artist = self._get_first_value(audio.get('aART'))
        self.disc_number = self._get_disc_number(audio.get('disk'))
        self.lyrics = self._get_first_value(audio.get('\xa9lyr'))
        
        # Store all raw tags
        for key, value in audio.items():
            self.raw_tags[key] = str(value)
    
    def _load_ogg_tags(self):
        """Load tags from OGG Vorbis files"""
        audio = OggVorbis(self.src)
        self.duration = audio.info.length
        self.bitrate = audio.info.bitrate
        self.sample_rate = audio.info.sample_rate
        
        # Load common tags
        self.title = self._get_first_value(audio.get('title'))
        self.artist = self._get_first_value(audio.get('artist'))
        self.album = self._get_first_value(audio.get('album'))
        self.genre = self._get_first_value(audio.get('genre'))
        self.year = self._get_first_value(audio.get('date'))
        self.track_number = self._get_first_value(audio.get('tracknumber'))
        self.composer = self._get_first_value(audio.get('composer'))
        self.comment = self._get_first_value(audio.get('comment'))
        self.lyrics = self._get_first_value(audio.get('lyrics')) or self._get_first_value(audio.get('unsyncedlyrics'))
        
        # Store all raw tags
        for key, value in audio.items():
            self.raw_tags[key] = str(value)
    
    def _load_wav_tags(self):
        """Load basic info from WAV files"""
        audio = WAVE(self.src)
        self.duration = audio.info.length
        self.sample_rate = audio.info.sample_rate
        # WAV files typically don't have extensive metadata
        self.bitrate = audio.info.bitrate
    
    def _get_first_value(self, value):
        """Get first value from a list if it's a list, otherwise return the value"""
        if value is None:
            return None
        if isinstance(value, list) and len(value) > 0:
            return str(value[0])
        return str(value) if value else None
    
    def _get_track_number(self, track_data):
        """Extract track number from MP4 track data"""
        if track_data and len(track_data) > 0:
            track_info = track_data[0]
            if isinstance(track_info, tuple) and len(track_info) > 0:
                return str(track_info[0])
        return None
    
    def _get_disc_number(self, disc_data):
        """Extract disc number from MP4 disc data"""
        if disc_data and len(disc_data) > 0:
            disc_info = disc_data[0]
            if isinstance(disc_info, tuple) and len(disc_info) > 0:
                return str(disc_info[0])
        return None
    
    def to_dict(self) -> Dict:
        """Convert Sound object to dictionary"""
        return {
            'src': self.src,
            'file_name': self.file_name,
            'file_extension': self.file_extension,
            'file_size': self.file_size,
            'title': self.title,
            'artist': self.artist,
            'album': self.album,
            'genre': self.genre,
            'year': self.year,
            'track_number': self.track_number,
            'duration': self.duration,
            'bitrate': self.bitrate,
            'sample_rate': self.sample_rate,
            'composer': self.composer,
            'comment': self.comment,
            'album_artist': self.album_artist,
            'disc_number': self.disc_number,
            'lyrics': self.lyrics
        }
    
    def __str__(self) -> str:
        """String representation of Sound object"""
        return f"Sound(title='{self.title}', artist='{self.artist}', src='{self.src}')"


class SoundScanner:
    """Scanner for finding sound files and extracting their metadata"""
    
    # Supported audio formats
    SUPPORTED_EXTENSIONS = {
        '.mp3', '.flac', '.m4a', '.ogg', '.wav', '.aac', 
        '.opus', '.wma', '.aiff', '.ape'
    }
    
    def __init__(self, root_directory: str):
        self.root_directory = Path(root_directory)
        self.sound_files: List[Sound] = []
        self.scan_stats = {
            'total_files_scanned': 0,
            'supported_files_found': 0,
            'error_files': 0,
            'directories_scanned': 0
        }
    
    def scan(self, recursive: bool = True, extensions: Optional[set] = None) -> List[Sound]:
        """
        Scan directory for sound files
        
        Args:
            recursive: If True, scan subdirectories recursively
            extensions: Set of file extensions to look for (uses default if None)
        
        Returns:
            List of Sound objects
        """
        if extensions is None:
            extensions = self.SUPPORTED_EXTENSIONS
        
        pattern = '**/*' if recursive else '*'
        
        for file_path in self.root_directory.glob(pattern):
            if file_path.is_file():
                self.scan_stats['total_files_scanned'] += 1
                
                if file_path.suffix.lower() in extensions:
                    try:
                        sound = Sound(str(file_path))
                        self.sound_files.append(sound)
                        self.scan_stats['supported_files_found'] += 1
                        print(f"Found: {sound}")
                    except Exception as e:
                        self.scan_stats['error_files'] += 1
                        print(f"Error processing {file_path}: {e}")
            
            # Count directories (approximate for stats)
            if recursive and file_path.is_dir():
                self.scan_stats['directories_scanned'] += 1
        
        return self.sound_files
    
    def get_statistics(self) -> Dict:
        """Get scanning statistics"""
        return self.scan_stats
    
    def filter_by_artist(self, artist: str) -> List[Sound]:
        """Filter sound files by artist"""
        return [s for s in self.sound_files if s.artist and artist.lower() in s.artist.lower()]
    
    def filter_by_album(self, album: str) -> List[Sound]:
        """Filter sound files by album"""
        return [s for s in self.sound_files if s.album and album.lower() in s.album.lower()]
    
    def filter_by_genre(self, genre: str) -> List[Sound]:
        """Filter sound files by genre"""
        return [s for s in self.sound_files if s.genre and genre.lower() in s.genre.lower()]
    
    def get_unique_artists(self) -> List[str]:
        """Get list of unique artists"""
        artists = set()
        for sound in self.sound_files:
            if sound.artist:
                artists.add(sound.artist)
        return sorted(list(artists))
    
    def get_unique_albums(self) -> List[str]:
        """Get list of unique albums"""
        albums = set()
        for sound in self.sound_files:
            if sound.album:
                albums.add(sound.album)
        return sorted(list(albums))
    
    def get_unique_genres(self) -> List[str]:
        """Get list of unique genres"""
        genres = set()
        for sound in self.sound_files:
            if sound.genre:
                genres.add(sound.genre)
        return sorted(list(genres))
    
    def get_folders_with_music(self) -> List[str]:
        """Get a list of all folders that contain at least one sound file, including parent folders"""
        folders = set()
        
        # Normalize the root directory
        root_dir = os.path.normpath(str(self.root_directory))
        if root_dir == "" or root_dir == ".":
            root_dir = "."
            
        for sound in self.sound_files:
            folder = os.path.dirname(sound.src)
            if not folder:
                folder = "."
                
            folder = os.path.normpath(folder)
            
            # Keep adding parent directories until we reach the root directory
            current = folder
            while True:
                folders.add(current)
                if current == root_dir or current == os.path.dirname(current):
                    break
                current = os.path.dirname(current)
                if not current:
                    current = "."
                    
        return sorted(list(folders))
    
    def get_songs_by_folder(self, folder_path: str) -> List[Sound]:
        """Get all songs in the specified folder and its subfolders"""
        target_folder = os.path.abspath(folder_path)
        target_folder_norm = os.path.normpath(target_folder)
        songs_in_folder = []
        
        for sound in self.sound_files:
            sound_path = os.path.abspath(sound.src)
            try:
                if os.path.commonpath([target_folder_norm, sound_path]) == target_folder_norm:
                    songs_in_folder.append(sound)
            except ValueError:
                pass
                
        return songs_in_folder
    
    def save_to_json(self, output_file: str):
        """Save scan results to JSON file"""
        data = {
            'statistics': self.scan_stats,
            'sound_files': [sound.to_dict() for sound in self.sound_files]
        }
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        print(f"Saved results to {output_file}")


def main():
    """Example usage of the SoundScanner"""
    
    # Example 1: Scan current directory
    print("=" * 60)
    print("SOUND FILE SCANNER")
    print("=" * 60)
    
    # You can change this to any directory path
    directory_to_scan = input("Enter directory path to scan (or press Enter for current directory): ").strip()
    
    if not directory_to_scan:
        directory_to_scan = "."
    
    # Create scanner
    scanner = SoundScanner(directory_to_scan)
    
    print(f"\nScanning directory: {directory_to_scan}")
    print("Supported formats:", ', '.join(scanner.SUPPORTED_EXTENSIONS))
    print("\nScanning...")
    
    # Perform scan
    sound_files = scanner.scan(recursive=True)
    
    # Display statistics
    stats = scanner.get_statistics()
    print("\n" + "=" * 60)
    print("SCAN RESULTS")
    print("=" * 60)
    print(f"Total files scanned: {stats['total_files_scanned']}")
    print(f"Supported sound files found: {stats['supported_files_found']}")
    print(f"Files with errors: {stats['error_files']}")
    
    # Display found sound files
    if sound_files:
        print("\nFound Sound Files:")
        print("-" * 60)
        for i, sound in enumerate(sound_files, 1):
            print(f"{i}. {sound}")
            print(f"   Album: {sound.album or 'N/A'}")
            print(f"   Genre: {sound.genre or 'N/A'}")
            print(f"   Duration: {sound.duration:.2f} seconds" if sound.duration else "   Duration: N/A")
            print()
        
        # Show unique artists
        artists = scanner.get_unique_artists()
        if artists:
            print("\nUnique Artists Found:")
            for artist in artists[:10]:  # Show first 10
                print(f"  - {artist}")
            if len(artists) > 10:
                print(f"  ... and {len(artists) - 10} more")
        
        # Save to JSON
        save_choice = input("\nDo you want to save results to JSON file? (y/n): ").lower()
        if save_choice == 'y':
            output_file = "sound_files_metadata.json"
            scanner.save_to_json(output_file)
    
    else:
        print("\nNo supported sound files found in the specified directory.")


if __name__ == "__main__":
    # Install required library if not already installed
    try:
        import mutagen
    except ImportError:
        print("Installing required library 'mutagen'...")
        os.system("pip install mutagen")
        import mutagen
    
    main()