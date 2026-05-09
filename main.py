import os
import sys
from scanner import SoundScanner
from selecter import Selecter

def print_songs(songs):
    if not songs:
        print("No songs found.")
        return
    print(f"\nFound {len(songs)} songs:")
    print("-" * 60)
    for i, song in enumerate(songs, 1):
        duration_str = f"{song.duration:.2f}s" if song.duration else "N/A"
        title = song.title if song.title else song.file_name
        artist = song.artist if song.artist else 'Unknown Artist'
        print(f"{i}. {title} - {artist} ({duration_str})")
        print(f"   Path: {song.src}")
    print("-" * 60)

def main():
    print("=" * 60)
    print("Welcome to the Music Player / Scanner")
    print("=" * 60)
    
    directory_to_scan = input("Enter directory path to scan (or press Enter for current directory): ").strip()
    if not directory_to_scan:
        directory_to_scan = "."
    
    if not os.path.isdir(directory_to_scan):
        print(f"Error: Directory '{directory_to_scan}' does not exist.")
        sys.exit(1)
        
    print(f"\nInitializing scanner and loading files from '{directory_to_scan}'...")
    scanner = SoundScanner(directory_to_scan)
    
    # Load the files ONE time and keep them in memory
    print("Scanning for music files (this may take a moment)...")
    scanner.scan(recursive=True)
    
    stats = scanner.get_statistics()
    print(f"Scan complete! Found {stats['supported_files_found']} supported music files.")
    
    while True:
        print("\n" + "=" * 60)
        print("MUSIC PLAYER MENU")
        print("=" * 60)
        print("1. View all unique artists")
        print("2. View all unique albums")
        print("3. View all unique genres")
        print("4. View all folders containing music")
        print("5. Filter songs by artist")
        print("6. Filter songs by album")
        print("7. Filter songs by genre")
        print("8. Get all songs in a specific folder")
        print("9. Show scan statistics")
        print("10. Select a song randomly from a folder")
        print("11. Get a folder randomly")
        print("12. Get current folder")
        print("13. Get current song from a folder")
        print("0. Exit")
        
        choice = input("\nEnter your choice (0-13): ").strip()
        
        if choice == '1':
            artists = scanner.get_unique_artists()
            print("\nUnique Artists:")
            for artist in artists:
                print(f" - {artist}")
                
        elif choice == '2':
            albums = scanner.get_unique_albums()
            print("\nUnique Albums:")
            for album in albums:
                print(f" - {album}")
                
        elif choice == '3':
            genres = scanner.get_unique_genres()
            print("\nUnique Genres:")
            for genre in genres:
                print(f" - {genre}")
                
        elif choice == '4':
            folders = scanner.get_folders_with_music()
            print("\nFolders with Music:")
            for i, folder in enumerate(folders, 1):
                print(f"{i}. {folder}")
                
        elif choice == '5':
            artist = input("\nEnter artist name to search: ").strip()
            songs = scanner.filter_by_artist(artist)
            print_songs(songs)
            
        elif choice == '6':
            album = input("\nEnter album name to search: ").strip()
            songs = scanner.filter_by_album(album)
            print_songs(songs)
            
        elif choice == '7':
            genre = input("\nEnter genre to search: ").strip()
            songs = scanner.filter_by_genre(genre)
            print_songs(songs)
            
        elif choice == '8':
            folders = scanner.get_folders_with_music()
            if not folders:
                print("\nNo folders found.")
                continue
                
            print("\nAvailable folders:")
            for i, folder in enumerate(folders, 1):
                print(f"{i}. {folder}")
                
            folder_choice = input("\nEnter folder number or type the full path: ").strip()
            folder_path = ""
            
            if folder_choice.isdigit():
                idx = int(folder_choice) - 1
                if 0 <= idx < len(folders):
                    folder_path = folders[idx]
                else:
                    print("Invalid folder number.")
                    continue
            else:
                folder_path = folder_choice
                
            if folder_path:
                songs = scanner.get_songs_by_folder(folder_path)
                print_songs(songs)
                
        elif choice == '9':
            stats = scanner.get_statistics()
            print("\nScan Statistics:")
            for key, value in stats.items():
                print(f" - {key.replace('_', ' ').title()}: {value}")
                
        elif choice == '10':
            folders = scanner.get_folders_with_music()
            if not folders:
                print("\nNo folders found.")
                continue
                
            print("\nAvailable folders:")
            for i, folder in enumerate(folders, 1):
                print(f"{i}. {folder}")
                
            folder_choice = input("\nEnter folder number or type the full path: ").strip()
            folder_path = ""
            
            if folder_choice.isdigit():
                idx = int(folder_choice) - 1
                if 0 <= idx < len(folders):
                    folder_path = folders[idx]
                else:
                    print("Invalid folder number.")
                    continue
            else:
                folder_path = folder_choice
                
            if folder_path:
                songs = scanner.get_songs_by_folder(folder_path)
                selected_song = Selecter.get_song_ramdomply(songs, folder_path)
                if selected_song:
                    print("\nRandomly Selected Song:")
                    print_songs([selected_song])
                    print(f"   Elapsed Time: {selected_song.erapse_time} ms")
                else:
                    print("\nNo songs available in this folder to select.")
                    
        elif choice == '11':
            folders = scanner.get_folders_with_music()
            if not folders:
                print("\nNo folders found.")
                continue
            folder = Selecter.get_folder_ramdomly(folders)
            print(f"\nRandomly Selected Folder: {folder}")
            
        elif choice == '12':
            folders = scanner.get_folders_with_music()
            if not folders:
                print("\nNo folders found.")
                continue
            folder = Selecter.get_current_folder(folders)
            print(f"\nCurrent Folder: {folder}")
            
        elif choice == '13':
            folders = scanner.get_folders_with_music()
            if not folders:
                print("\nNo folders found.")
                continue
                
            print("\nAvailable folders:")
            for i, folder in enumerate(folders, 1):
                print(f"{i}. {folder}")
                
            folder_choice = input("\nEnter folder number or type the full path: ").strip()
            folder_path = ""
            
            if folder_choice.isdigit():
                idx = int(folder_choice) - 1
                if 0 <= idx < len(folders):
                    folder_path = folders[idx]
                else:
                    print("Invalid folder number.")
                    continue
            else:
                folder_path = folder_choice
                
            if folder_path:
                songs = scanner.get_songs_by_folder(folder_path)
                selected_song = Selecter.get_current_song(songs, folder_path)
                if selected_song:
                    print("\nCurrent Song:")
                    print_songs([selected_song])
                    print(f"   Elapsed Time: {selected_song.erapse_time} ms")
                else:
                    print("\nNo songs available in this folder to select.")
            
        elif choice == '0':
            print("\nExiting player. Goodbye!")
            break
            
        else:
            print("\nInvalid choice. Please enter a number between 0 and 13.")

if __name__ == "__main__":
    main()
