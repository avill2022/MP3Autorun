import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from pathlib import Path
import pygame
import os
import sys
import time
import io
from PIL import Image, ImageTk

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from scanner import SoundScanner, Sound
from selecter import Selecter

class ModernMP3Player:
    def __init__(self, root):
        self.root = root
        self.root.title("MP3 Player")
        self.root.geometry("650x280")
        self.root.resizable(True, True)
        
        # Color palette matching mockup
        self.bg_color = '#121212'       # Very dark, almost black
        self.panel_bg = '#1e1e24'       # Charcoal grey for panels
        self.fg_color = '#ffffff'       # White text
        self.accent_color = '#00e5ff'   # Neon Cyan
        self.muted_color = '#a0a0a5'    # Muted grey
        self.hover_color = '#b829ea'    # Purple for accents/hover
        
        self.root.configure(bg=self.bg_color)
        
        pygame.mixer.init()
        
        self.scanner = None
        self.music_folders = []
        self.current_folder = ""
        self.current_song = None
        self.folder_songs = []
        
        self.playing = False
        self.paused = False
        self.repeat_mode = 'none'
        self.current_volume = 0.5
        pygame.mixer.music.set_volume(self.current_volume)
        
        self.setup_styles()
        self.setup_ui()
        self.initial_load()
        self.update_timer()

    def setup_styles(self):
        style = ttk.Style()
        style.theme_use('default')
        style.configure("Cyber.Horizontal.TProgressbar", 
                        background=self.accent_color,
                        troughcolor=self.bg_color, 
                        bordercolor=self.panel_bg, 
                        thickness=4)

    def create_small_art(self):
        from PIL import ImageDraw
        img = Image.new('RGB', (50, 50), color=self.bg_color)
        draw = ImageDraw.Draw(img)
        draw.rectangle([5, 5, 45, 45], outline=self.hover_color, width=2)
        draw.polygon([(25, 10), (40, 25), (25, 40), (10, 25)], outline=self.accent_color, width=2)
        return ImageTk.PhotoImage(img)

    def setup_ui(self):
        # --- Top Menu / Title ---
        top_bar = tk.Frame(self.root, bg=self.bg_color, height=40)
        top_bar.pack(fill='x', side='top')
        tk.Label(top_bar, text="▶ MUSIC BROWSER", bg=self.bg_color, fg=self.fg_color, font=('Helvetica', 12, 'bold')).pack(side='left', padx=15, pady=10)
        
        btn_opts = {'bg': self.panel_bg, 'fg': self.fg_color, 'activebackground': self.bg_color, 'activeforeground': self.accent_color, 'bd': 0, 'cursor': 'hand2'}
        tk.Button(top_bar, text="📂 SCAN NEW FOLDER", font=('Helvetica', 9, 'bold'), command=self.scan_new_folder, **btn_opts).pack(side='right', padx=15, pady=5)
        tk.Button(top_bar, text="💾 EXPORT JSON", font=('Helvetica', 9, 'bold'), command=self.export_json, **btn_opts).pack(side='right', padx=5, pady=5)

        # --- Bottom Player Bar ---
        self.bottom_bar = tk.Frame(self.root, bg=self.panel_bg, height=80)
        self.bottom_bar.pack(side='bottom', fill='x')
        self.bottom_bar.pack_propagate(False)
        
        # Bottom Bar: Left (Art & Info)
        info_frame = tk.Frame(self.bottom_bar, bg=self.panel_bg)
        info_frame.pack(side='left', padx=15, fill='y')
        
        self.default_art = self.create_small_art()
        self.art_label = tk.Label(info_frame, image=self.default_art, bg=self.panel_bg)
        self.art_label.pack(side='left', pady=10)
        
        text_frame = tk.Frame(info_frame, bg=self.panel_bg)
        text_frame.pack(side='left', padx=10, pady=10, fill='y')
        self.lbl_bottom_title = tk.Label(text_frame, text="No Song Selected", bg=self.panel_bg, fg=self.fg_color, font=('Helvetica', 10, 'bold'), anchor='w')
        self.lbl_bottom_title.pack(fill='x')
        self.lbl_bottom_artist = tk.Label(text_frame, text="-", bg=self.panel_bg, fg=self.muted_color, font=('Helvetica', 8), anchor='w')
        self.lbl_bottom_artist.pack(fill='x')
        
        self.btn_lyrics = tk.Button(text_frame, text="📝 Lyrics", font=('Helvetica', 8, 'bold'), command=self.show_lyrics, **btn_opts)
        
        # Bottom Bar: Center (Controls & Progress)
        center_frame = tk.Frame(self.bottom_bar, bg=self.panel_bg)
        center_frame.pack(side='left', expand=True, fill='both', padx=20)
        
        ctrl_frame = tk.Frame(center_frame, bg=self.panel_bg)
        ctrl_frame.pack(pady=(12, 0))
        
        # Playback controls as requested: next, play, pause (toggled), stop, repeat
        self.btn_repeat = tk.Button(ctrl_frame, text='🔁', font=('Helvetica', 14), command=self.toggle_repeat, **btn_opts)
        self.btn_repeat.pack(side='left', padx=10)
        
        self.btn_stop = tk.Button(ctrl_frame, text='⏹', font=('Helvetica', 14), command=self.stop_song, **btn_opts)
        self.btn_stop.pack(side='left', padx=10)
        
        self.btn_play = tk.Button(ctrl_frame, text='⏵', font=('Helvetica', 20), command=self.play_pause, **btn_opts)
        self.btn_play.pack(side='left', padx=10)
        
        self.btn_next = tk.Button(ctrl_frame, text='⏭', font=('Helvetica', 14), command=self.next_song, **btn_opts)
        self.btn_next.pack(side='left', padx=10)
        
        prog_frame = tk.Frame(center_frame, bg=self.panel_bg)
        prog_frame.pack(fill='x', pady=5)
        self.lbl_time_curr = tk.Label(prog_frame, text="0:00", bg=self.panel_bg, fg=self.muted_color, font=('Helvetica', 8))
        self.lbl_time_curr.pack(side='left')
        self.lbl_time_tot = tk.Label(prog_frame, text="0:00", bg=self.panel_bg, fg=self.muted_color, font=('Helvetica', 8))
        self.lbl_time_tot.pack(side='right')
        
        self.progress_bar = ttk.Progressbar(prog_frame, mode='determinate', style="Cyber.Horizontal.TProgressbar")
        self.progress_bar.pack(fill='x', padx=10, expand=True)
        self.progress_bar.bind('<Button-1>', self.seek_song)
        
        # Bottom Bar: Right (Volume)
        vol_frame = tk.Frame(self.bottom_bar, bg=self.panel_bg)
        vol_frame.pack(side='right', padx=15, pady=28)
        
        self.btn_vol_down = tk.Button(vol_frame, text='🔉', font=('Helvetica', 12), command=self.vol_down, **btn_opts)
        self.btn_vol_down.pack(side='left', padx=2)
        
        self.vol_bar = ttk.Progressbar(vol_frame, length=60, mode='determinate', style="Cyber.Horizontal.TProgressbar")
        self.vol_bar.pack(side='left', padx=5)
        self.vol_bar['value'] = self.current_volume * 100
        
        self.btn_vol_up = tk.Button(vol_frame, text='🔊', font=('Helvetica', 12), command=self.vol_up, **btn_opts)
        self.btn_vol_up.pack(side='left', padx=2)

        # --- Main Split Area ---
        self.split_pane = tk.PanedWindow(self.root, orient=tk.HORIZONTAL, bg=self.bg_color, bd=0, sashwidth=4)
        self.split_pane.pack(fill='both', expand=True, padx=15, pady=(0, 15))
        
        # Left Panel (Folders - Prominent)
        left_panel = tk.Frame(self.split_pane, bg=self.panel_bg, highlightbackground=self.bg_color, highlightthickness=1)
        self.split_pane.add(left_panel, minsize=250, width=300)
        
        folder_ctrl = tk.Frame(left_panel, bg=self.panel_bg)
        folder_ctrl.pack(fill='x', pady=10, padx=10)
        # Prev / Next Folder buttons as requested
        tk.Button(folder_ctrl, text='◁', font=('Helvetica', 9, 'bold'), command=self.prev_folder, **btn_opts).pack(side='left')
        tk.Button(folder_ctrl, text='▷', font=('Helvetica', 9, 'bold'), command=self.next_folder, **btn_opts).pack(side='right')
        
        tk.Label(left_panel, text="Music Folders", bg=self.panel_bg, fg=self.accent_color, font=('Helvetica', 14, 'bold'), anchor='w').pack(fill='x', padx=15, pady=(10, 5))
        
        # Folder Listbox
        self.list_folders = tk.Listbox(left_panel, bg=self.bg_color, fg=self.fg_color, selectbackground=self.hover_color, selectforeground='white', bd=0, highlightthickness=0, font=('Helvetica', 11))
        self.list_folders.pack(fill='both', expand=True, padx=15, pady=(0, 15))
        self.list_folders.bind('<<ListboxSelect>>', self.on_folder_select)
        
        # Right Panel (Songs - Secondary)
        right_panel = tk.Frame(self.split_pane, bg=self.panel_bg, highlightbackground=self.bg_color, highlightthickness=1)
        self.split_pane.add(right_panel, minsize=300)
        
        # Search Frame
        search_frame = tk.Frame(right_panel, bg=self.panel_bg)
        search_frame.pack(fill='x', padx=20, pady=(15, 0))
        
        self.entry_search = tk.Entry(search_frame, bg=self.bg_color, fg=self.fg_color, insertbackground=self.fg_color, bd=0, font=('Helvetica', 10))
        self.entry_search.pack(side='left', fill='x', expand=True, ipady=4)
        self.entry_search.bind('<Return>', self.search_songs)
        
        tk.Button(search_frame, text='🔍', bg=self.bg_color, fg=self.fg_color, bd=0, command=self.search_songs).pack(side='right', padx=(5, 0))
        
        self.lbl_folder_title = tk.Label(right_panel, text="Folder Tracks", bg=self.panel_bg, fg=self.fg_color, font=('Helvetica', 14, 'bold'), anchor='w')
        self.lbl_folder_title.pack(fill='x', padx=20, pady=15)
        
        # Song Listbox
        self.list_songs = tk.Listbox(right_panel, bg=self.bg_color, fg=self.fg_color, selectbackground=self.accent_color, selectforeground='black', bd=0, highlightthickness=0, font=('Helvetica', 10))
        self.list_songs.pack(fill='both', expand=True, padx=20, pady=(0, 20))
        self.list_songs.bind('<Double-Button-1>', self.on_song_double_click)
        self.list_songs.bind('<<ListboxSelect>>', self.on_song_single_click)

    def initial_load(self):
        initial_dir = os.getcwd()
        self.load_root_directory(initial_dir)
        
    def load_root_directory(self, directory_path):
        self.scanner = SoundScanner(directory_path)
        self.scanner.scan(recursive=True)
        self.music_folders = self.scanner.get_folders_with_music()
        
        self.list_folders.delete(0, tk.END)
        for f in self.music_folders:
            self.list_folders.insert(tk.END, os.path.basename(f) or f)
            
        if not self.music_folders:
            self.lbl_folder_title.config(text="No sound files found!")
            return
            
        self.current_folder = Selecter.get_current_folder(self.music_folders)
        self.update_folder_selection()
        # Fetch current song and auto-play on initial load
        self.load_folder_songs(auto_play=True)

    def update_folder_selection(self):
        try:
            idx = self.music_folders.index(self.current_folder)
            self.list_folders.selection_clear(0, tk.END)
            self.list_folders.selection_set(idx)
            self.list_folders.see(idx)
        except ValueError:
            pass

    def load_folder_songs(self, auto_play=True):
        if not self.current_folder:
            return
            
        self.folder_songs = self.scanner.get_songs_by_folder(self.current_folder)
        
        self.lbl_folder_title.config(text=f"{os.path.basename(self.current_folder)} - {len(self.folder_songs)} Tracks")
        self.list_songs.delete(0, tk.END)
        
        for i, s in enumerate(self.folder_songs):
            self.list_songs.insert(tk.END, f"{i+1}   {s.title or s.file_name}")
            
        if not self.folder_songs:
            self.current_song = None
            return
            
        self.current_song = Selecter.get_current_song(self.folder_songs, self.current_folder)
        self.update_song_selection()
        self.update_file_display()
        
        if auto_play:
            self.play_song()

    def update_song_selection(self):
        if not self.current_song or not self.folder_songs:
            return
        try:
            idx = self.folder_songs.index(self.current_song)
            self.list_songs.selection_clear(0, tk.END)
            self.list_songs.selection_set(idx)
            self.list_songs.see(idx)
        except ValueError:
            pass

    def on_folder_select(self, event):
        """Clicking a folder updates the list and auto-plays a song from it"""
        selection = self.list_folders.curselection()
        if selection:
            idx = selection[0]
            if self.current_folder != self.music_folders[idx]:
                self.current_folder = self.music_folders[idx]
                self.load_folder_songs(auto_play=True)

    def on_song_single_click(self, event):
        """Just select, don't play yet"""
        pass

    def on_song_double_click(self, event):
        """Double clicking a song explicitly plays it"""
        selection = self.list_songs.curselection()
        if selection:
            idx = selection[0]
            self.current_song = self.folder_songs[idx]
            self.update_file_display()
            self.play_song()

    def prev_folder(self):
        if not self.music_folders: return
        try:
            idx = self.music_folders.index(self.current_folder)
            idx = (idx - 1) % len(self.music_folders)
            self.current_folder = self.music_folders[idx]
        except ValueError:
            self.current_folder = self.music_folders[0]
            
        self.update_folder_selection()
        self.load_folder_songs(auto_play=True)

    def next_folder(self):
        if not self.music_folders: return
        try:
            idx = self.music_folders.index(self.current_folder)
            idx = (idx + 1) % len(self.music_folders)
            self.current_folder = self.music_folders[idx]
        except ValueError:
            self.current_folder = self.music_folders[0]
            
        self.update_folder_selection()
        self.load_folder_songs(auto_play=True)

    def scan_new_folder(self):
        folder_path = filedialog.askdirectory()
        if folder_path:
            self.load_root_directory(folder_path)

    def search_songs(self, event=None):
        query = self.entry_search.get().lower()
        if not query:
            if getattr(self, 'current_folder', '') == "Search_Results":
                self.current_folder = getattr(self, '_previous_folder', self.music_folders[0] if self.music_folders else "")
            self.load_folder_songs(auto_play=False)
            return
            
        if not self.scanner or not self.scanner.sound_files:
            return
            
        if getattr(self, 'current_folder', '') != "Search_Results":
            self._previous_folder = self.current_folder
            
        results = []
        for sound in self.scanner.sound_files:
            title = (sound.title or sound.file_name).lower()
            artist = (sound.artist or "").lower()
            if query in title or query in artist:
                results.append(sound)
                
        self.folder_songs = results
        self.current_folder = "Search_Results"
        
        self.lbl_folder_title.config(text=f"Search: '{query}' - {len(self.folder_songs)} Tracks")
        self.list_songs.delete(0, tk.END)
        
        for i, s in enumerate(self.folder_songs):
            self.list_songs.insert(tk.END, f"{i+1}   {s.title or s.file_name}")

    def export_json(self):
        if not self.scanner:
            messagebox.showinfo("Export", "No files scanned to export.")
            return
            
        file_path = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")],
            title="Save Data as JSON"
        )
        
        if file_path:
            try:
                self.scanner.save_to_json(file_path)
                messagebox.showinfo("Success", f"Data exported successfully.")
            except Exception as e:
                messagebox.showerror("Error", f"Could not save JSON: {e}")

    def update_file_display(self):
        if self.current_song:
            title = self.current_song.title or Path(self.current_song.file_name).stem
            if len(title) > 35: title = title[:32] + "..."
            self.lbl_bottom_title.config(text=title)
            
            artist = self.current_song.artist or "Unknown Artist"
            self.lbl_bottom_artist.config(text=artist[:35])
            
            if self.current_song.duration:
                self.lbl_time_tot.config(text=self.format_time(int(self.current_song.duration)))
            else:
                self.lbl_time_tot.config(text="0:00")

            if getattr(self.current_song, 'lyrics', None):
                self.btn_lyrics.pack(anchor='w', pady=(2, 0))
            else:
                self.btn_lyrics.pack_forget()

            # Update album art
            if getattr(self.current_song, 'cover_data', None):
                try:
                    image_data = io.BytesIO(self.current_song.cover_data)
                    img = Image.open(image_data)
                    # Resize to fit the label (default art is 50x50)
                    img = img.resize((50, 50), Image.Resampling.LANCZOS)
                    self.album_cover_img = ImageTk.PhotoImage(img)
                    self.art_label.config(image=self.album_cover_img)
                except Exception as e:
                    print(f"Error loading cover art: {e}")
                    self.art_label.config(image=self.default_art)
            else:
                self.art_label.config(image=self.default_art)

    def play_song(self):
        if not self.current_song: return
        try:
            pygame.mixer.music.load(self.current_song.src)
            print((self.current_song.erapse_time or 0) / 1000.0)
            pygame.mixer.music.play(start=(self.current_song.erapse_time or 0) / 1000.0)
            self.playing = True
            self.paused = False
            self.btn_play.config(text='⏸')
            self.update_song_selection()
            self.update_file_display()
        except Exception as e:
            messagebox.showerror("Error", f"Could not play file: {e}")

    def play_pause(self):
        if not self.current_song: return
        if not self.playing:
            if self.paused:
                pygame.mixer.music.unpause()
                self.paused = False
                self.playing = True
                self.btn_play.config(text='⏸')
            else:
                self.play_song()
        else:
            self.pause_song()

    def pause_song(self):
        if self.playing:
            pygame.mixer.music.pause()
            self.paused = True
            self.playing = False
            self.btn_play.config(text='⏵')

    def stop_song(self):
        pygame.mixer.music.stop()
        self.playing = False
        self.paused = False
        self.btn_play.config(text='⏵')
        self.progress_bar['value'] = 0
        self.lbl_time_curr.config(text="0:00")

    def next_song(self):
        if not self.folder_songs: return
        # Randomly select next song in current folder via Selecter
        self.current_song = Selecter.get_song_ramdomply(self.folder_songs, self.current_folder)
        self.stop_song()
        self.play_song()

    def seek_song(self, event):
        if self.playing or self.paused:
            x = event.x
            width = self.progress_bar.winfo_width()
            if width > 0:
                ratio = x / width
                if self.current_song and self.current_song.duration:
                    seek_pos = ratio * self.current_song.duration
                    pygame.mixer.music.play(start=seek_pos)
                    if self.paused: pygame.mixer.music.pause()

    def toggle_repeat(self):
        modes = ['none', 'one', 'all']
        self.repeat_mode = modes[(modes.index(self.repeat_mode) + 1) % len(modes)]
        if self.repeat_mode == 'none':
            self.btn_repeat.config(fg=self.fg_color)
        else:
            self.btn_repeat.config(fg=self.accent_color)

    def vol_up(self):
        self.current_volume = min(1.0, self.current_volume + 0.1)
        pygame.mixer.music.set_volume(self.current_volume)
        self.vol_bar['value'] = self.current_volume * 100

    def vol_down(self):
        self.current_volume = max(0.0, self.current_volume - 0.1)
        pygame.mixer.music.set_volume(self.current_volume)
        self.vol_bar['value'] = self.current_volume * 100

    def update_timer(self):
        if self.playing and not self.paused:
            try:
                current_pos = pygame.mixer.music.get_pos() / 1000
                if self.current_song and self.current_song.duration:
                    tot = self.current_song.duration
                    erapsed = (self.current_song.erapse_time/1000)
                    real = current_pos+erapsed
                    if tot > 0:
                        self.progress_bar['value'] = (real / tot) * 100
                        self.lbl_time_curr.config(text=self.format_time(int(real)))
                        
                        # Auto-play next song when finished
                        if real >= (tot - 0.3):
                            if self.repeat_mode == 'one':
                                self.play_song()
                            else:
                                self.current_song = Selecter.get_song_ramdomply(self.folder_songs, self.current_folder, use_random_offset=False)
                                self.play_song()
                                print(self.current_song.src)
            except: pass
        self.root.after(500, self.update_timer)

    def show_lyrics(self):
        if not self.current_song or not getattr(self.current_song, 'lyrics', None):
            return
            
        lyrics_window = tk.Toplevel(self.root)
        lyrics_window.title(f"Lyrics - {self.current_song.title or self.current_song.file_name}")
        lyrics_window.geometry("400x500")
        lyrics_window.configure(bg=self.bg_color)
        
        # Add a scrollbar
        scrollbar = tk.Scrollbar(lyrics_window)
        scrollbar.pack(side='right', fill='y')
        
        text_widget = tk.Text(lyrics_window, bg=self.bg_color, fg=self.fg_color, 
                             font=('Helvetica', 11), wrap='word', padx=20, pady=20,
                             yscrollcommand=scrollbar.set)
        text_widget.pack(fill='both', expand=True)
        scrollbar.config(command=text_widget.yview)
        
        # Insert lyrics
        text_widget.insert('1.0', self.current_song.lyrics)
        text_widget.config(state='disabled')

    def format_time(self, seconds):
        m, s = divmod(seconds, 60)
        h, m = divmod(m, 60)
        return f"{h}:{m:02d}:{s:02d}" if h > 0 else f"{m}:{s:02d}"

def main():
    root = tk.Tk()
    app = ModernMP3Player(root)
    root.mainloop()

if __name__ == "__main__":
    main()