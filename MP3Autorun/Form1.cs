using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.IO;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;
using YouSaw;

namespace MP3Autorun
{
    public partial class MP3Autorun_ : Form
    {
        int interval = 0;
        Image img1;
        Image img2;
        Timer timer_play;
        Timer timer_playing_now_time_elapsed;
        player_list player_List_;
        Help help_;
        Information information_;
        DirectoryInfo directory_nfo;
        FileInfo[] Files;
        public List<Station> stations = new List<Station>();
        public Random r;
        int iterator_station = 0;

        public MP3Autorun_()
        {
            InitializeComponent();
        }
        private void Form1_Load(object sender, EventArgs e)
        {
            player_List_ = new player_list(this);
            help_ = new Help();
            information_ = new Information();
            axWMPl.PlayStateChange += AxWMPl_PlayStateChange;
            timer_play = new Timer();
            timer_play.Interval = 1000;
            timer_play.Tick += Timer_play_Tick;
            timer_playing_now_time_elapsed = new Timer();
            timer_playing_now_time_elapsed.Interval = 1000;
            timer_playing_now_time_elapsed.Tick += Timer_playing_now_time_elapsed_Tick; ;
            img2 = ((PictureBox)panel_flolders.Controls[0]).Image;
            img1 = ((PictureBox)panel_flolders.Controls[1]).Image;

            stations = new List<Station>();
            r = new Random(int.Parse(TimeSpan.Parse(DateTime.Now.Hour + ":" + DateTime.Now.Minute + ":" + DateTime.Now.Second).TotalSeconds.ToString()));
            sann_folder();
            this.axWMPl.settings.volume = 0;
            easyPanel_ProgressBar1.Value = 0;
        }
        private void Timer_playing_now_time_elapsed_Tick(object sender, EventArgs e)
        {
            this.easyPanel_ProgressBar1.Maximum = (int)axWMPl.currentMedia.duration;
            if (wmps_current_position() < easyPanel_ProgressBar1.Maximum)
                easyPanel_ProgressBar1.Value = wmps_current_position();
            else
                easyPanel_ProgressBar1.Value = 0;
            this.label_transcurrent_time.Text = Convert.ToString(TimeSpan.FromSeconds(wmps_current_position()));
            easyPanel_ProgressBar1.Invalidate();
        }
        public Station get_station() {
            return stations[iterator_station];
        }
        public void openForm(object form, Panel _contentPanel)
        {
            if (_contentPanel.Controls.Count > 0)
                _contentPanel.Controls.RemoveAt(0);
            Form fh = form as Form;
            fh.TopLevel = false;
            fh.Dock = DockStyle.Fill;
            _contentPanel.Controls.Add(fh);
            _contentPanel.Tag = fh;
            fh.Show();
        }
        public int get_time()
        {
            return int.Parse(TimeSpan.Parse(DateTime.Now.Hour + ":" + DateTime.Now.Minute + ":" + DateTime.Now.Second).TotalSeconds.ToString());
        }
        private void Timer_play_Tick(object sender, EventArgs e)
        {
            if ((interval + 3) < get_time())
            {
                set_station();
                timer_play.Stop();
            }
        }

        #region axWMPl control
        private void AxWMPl_PlayStateChange(object sender, AxWMPLib._WMPOCXEvents_PlayStateChangeEvent e)
        {
            if (axWMPl.playState == WMPLib.WMPPlayState.wmppsPlaying)
            {
                timer_play.Stop();
                label_artist.Text = axWMPl.currentMedia.getItemInfo("Artist");
                label_album.Text = axWMPl.currentMedia.getItemInfo("Album");
                file_name.Text = stations[iterator_station].playing_now_name;
                label_duration_time.Text = Convert.ToString(TimeSpan.FromSeconds(stations[iterator_station].duracion));
                stations[iterator_station].duracion = (int)axWMPl.currentMedia.duration;
                easyPanel_ProgressBar1.Maximum = stations[iterator_station].duracion;
                easyPanel_ProgressBar1.Value = wmps_current_position();
                timer_playing_now_time_elapsed.Start();

                string ur_ = stations[iterator_station]._playing_now_url();
                string s = ur_.Split('\\')[ur_.Split('\\').Length - 1];

                directory_nfo = new DirectoryInfo(ur_.Substring(0, ur_.Length - s.Length));
                Files = directory_nfo.GetFiles("*.jpg");
                foreach (FileInfo file in Files)
                {
                    panel_content.BackgroundImage = Image.FromFile(file.FullName);
                    panel_content.Invalidate();
                    break;
                }
            }
            if (axWMPl.playState == WMPLib.WMPPlayState.wmppsPaused)
            {
            }
            if (axWMPl.playState == WMPLib.WMPPlayState.wmppsMediaEnded)
            {
            }
            if (axWMPl.playState == WMPLib.WMPPlayState.wmppsStopped)
            {
                timer_play.Stop();
                if (!panel_stoped.Visible)
                {
                    timer_playing_now_time_elapsed.Stop();
                    if (panel_repeticion_mode.Visible)
                    {
                        if (stations[iterator_station].aleatorio)
                        {
                            if (stations[iterator_station].list_mp3_r.Count == (stations[iterator_station].mp3_list.Count))
                            {
                                stations[iterator_station].list_mp3_r.Clear();
                                next_station_();
                                stations[iterator_station].calcula_mp3();
                                player_List_.set_listBox_(stations[iterator_station].listBox1, stations[iterator_station].mp3_list);
                                player_List_.set_item(stations[iterator_station].get_iterator_file());
                            }
                            else
                            {
                                stations[iterator_station].next_mp3();
                                player_List_.set_item(stations[iterator_station].get_iterator_file());
                            }
                        }
                        else
                        if (stations[iterator_station].get_iterator_file() == (stations[iterator_station].mp3_list.Count - 1))
                        {
                            stations[iterator_station].next_mp3();
                            next_station_();
                            stations[iterator_station].get_playing_now_time_elapsed();
                            player_List_.set_listBox_(stations[iterator_station].listBox1, stations[iterator_station].mp3_list);
                            player_List_.set_item(stations[iterator_station].get_iterator_file());
                        }
                        else
                        {
                            stations[iterator_station].next_mp3();
                            player_List_.set_item(stations[iterator_station].get_iterator_file());
                        }

                    }
                    else
                    {
                        stations[iterator_station].next_mp3();
                        player_List_.set_item(stations[iterator_station].get_iterator_file());
                    }
                    timer_play.Start();
                }
            }
        }
        public int wmps_current_position()
        {
            try
            {
                return (int)axWMPl.Ctlcontrols.currentPosition;
            }
            catch (System.Runtime.InteropServices.InvalidComObjectException)
            {

                return 0;
            }
        }
        #endregion
        #region control options menu
        private void panel_information_file_Click(object sender, EventArgs e)
        {
            if (panel_information_file.Visible)
            {
                panel_information_a.Visible = false;
                panel_information.Visible = true;
                panel_information_file.Visible = false;
                if (panel_content.Controls.Count == 0)
                    openForm(information_, this.panel_content);
                else
                {
                    if (panel_content.Controls.Count > 0)
                        panel_content.Controls.RemoveAt(0);
                    openForm(information_, this.panel_content);
                }
            }
            else {
                panel_information_file.Visible = true;
                if (panel_content.Controls.Count > 0)
                    panel_content.Controls.RemoveAt(0);
            }
        }
        private void panel_information_MouseLeave(object sender, EventArgs e)
        {
            if (panel_information_file.Visible)
            {
                panel_information.Visible = false;
            }
        }
        private void panel_information_file_MouseHover(object sender, EventArgs e)
        {
            panel_information.Visible = true;
        }
        private void panel_repeticion_mode_Click(object sender, EventArgs e)
        {
            if (panel_repeticion_mode.Visible)
            {
                panel_repeticion.Visible = true;
                panel_repeticion_mode.Visible = false;
            }
            else {
                panel_repeticion_mode.Visible = true;
            }
        }
        private void panel_repeticion_MouseLeave(object sender, EventArgs e)
        {
            if (panel_repeticion_mode.Visible)
            {
                panel_repeticion.Visible = false;
            }
        }
        private void panel_repeticion_mode_MouseHover(object sender, EventArgs e)
        {
            panel_repeticion.Visible = true;
        }
        private void panel_aleatorio__Click(object sender, EventArgs e)
        {
            if (panel_aleatorio_file.Visible)
            {
                foreach (Station s in stations) {
                    s.aleatorio = true;
                }
                panel_aleatorio_.Visible = true;
                panel_aleatorio_file.Visible = false;
            }
            else
            {
                foreach (Station s in stations)
                {
                    s.aleatorio = false;
                }
                panel_aleatorio_file.Visible = true;
            }
        }
        private void panel_aleatorio__MouseLeave(object sender, EventArgs e)
        {
            if (panel_aleatorio_file.Visible)
            {
                panel_aleatorio_.Visible = false;
            }
        }
        private void panel_aleatorio_file_MouseHover(object sender, EventArgs e)
        {
            panel_aleatorio_.Visible = true;
        }

        private void panel_information_application_Click(object sender, EventArgs e)
        {
            if (panel_information_application.Visible)
            {
                panel_information.Visible = false;
                panel_information_file.Visible = true;

                panel_information_a.Visible = true;
                panel_information_application.Visible = false;
                if (panel_content.Controls.Count == 0)
                    openForm(help_, this.panel_content);
                else
                {
                    if (panel_content.Controls.Count > 0)
                        panel_content.Controls.RemoveAt(0);
                    openForm(help_, this.panel_content);
                }

            }
            else
            {
                panel_information_application.Visible = true;
                if (panel_content.Controls.Count > 0)
                    panel_content.Controls.RemoveAt(0);
            }
        }
        private void panel_information_a_MouseLeave(object sender, EventArgs e)
        {
            if (panel_information_application.Visible) {
                panel_information_a.Visible = false;
            }
        }
        private void panel_information_application_MouseHover(object sender, EventArgs e)
        {
            panel_information_a.Visible = true;
        }
        private void panel_mute_Click(object sender, EventArgs e)
        {
            mute();
        }
        public void mute() {
            if (axWMPl.settings.mute)
            {
                axWMPl.settings.mute = false;
                panel_mute.Visible = true;
                panel_mute_.Visible = false;
            }
            else
            {
                axWMPl.settings.mute = true;
                panel_mute.Visible = false;
                panel_mute_.Visible = true;
            }
        }
        private void panel_mute__MouseHover(object sender, EventArgs e)
        {
            panel_mute_.Visible = true;
        }
        private void panel_mute__MouseLeave(object sender, EventArgs e)
        { if (panel_mute.Visible) {
                panel_mute_.Visible = false;
            }
        }
        #endregion
        #region window form
        private void panel_reduce_Click(object sender, EventArgs e)
        {
            if (panel_reduce.Visible)
            {
                panel_reduce.Visible = false;
                panel_stop_m.Visible = true;
                panel_change__menu.Visible = false;
                this.Size = new System.Drawing.Size(150, 13);

            }
            else {
                panel_reduce.Visible = true;
                panel_stop_m.Visible = false;
                panel_change__menu.Visible = true;
                this.Size = new System.Drawing.Size(345, 172);
            }
        }
        private void panel_reduce_MouseHover(object sender, EventArgs e)
        {
            panel_reduce_.Visible = true;
        }
        private void panel4_MouseLeave_1(object sender, EventArgs e)
        {
            if(panel_reduce.Visible)
                panel_reduce_.Visible = false;
        }
        private void panel4_MouseLeave(object sender, EventArgs e)
        {
            panel__minimized_.Visible = false;
        }
        private void panel_close_window_Click(object sender, EventArgs e)
        {
            close();
        }
        public void close() {
            stop();
            Application.Exit();
        }
        private void panel_minimized_Click(object sender, EventArgs e)
        {
            this.WindowState = FormWindowState.Minimized;
        }
        private void panel_close_window_MouseHover(object sender, EventArgs e)
        {
            panel_close_.Visible = true;
        }
        private void panel_close_window_MouseLeave(object sender, EventArgs e)
        {
            panel_close_.Visible = false;
        }
        private void panel_minimized_MouseHover(object sender, EventArgs e)
        {
            panel__minimized_.Visible = true;
        }

        public bool mouse_down = false;
        private void Form1_MouseDown(object sender, MouseEventArgs e)
        {
            mouse_down = true;
            mosex = e.X;
            mousey = e.Y;
        }
        int mosex;
        int mousey;
        private void Form1_MouseMove(object sender, MouseEventArgs e)
        {
            if (mouse_down)
            {

                this.SetDesktopLocation(MousePosition.X - mosex, MousePosition.Y - mousey);
            }
        }
        private void Form1_MouseUp(object sender, MouseEventArgs e)
        {
            mouse_down = false;
        }
        #endregion
        #region folder control
        private void directory_MouseClick(object sender, MouseEventArgs e)
        {
            if (!panel_pause.Visible && !panel_stoped.Visible)
            {
                panel_information.Visible = false;
                panel_information_file.Visible = true;
                player_List_.clear();
                iterator_station = int.Parse(((System.Windows.Forms.Control)sender).Tag.ToString());
                if (panel_content.Controls.Count != 0)
                    if (panel_content.Controls.Count > 0)
                        if (panel_content.Controls[0].Equals(information_))
                            openForm(player_List_, this.panel_content);
                set_station();
                player_List_.set_listBox_(stations[iterator_station].listBox1, stations[iterator_station].mp3_list);
                player_List_.set_item(stations[iterator_station].get_iterator_file());
            }
        }
        private void panel_next_folder_Click(object sender, EventArgs e)
        {
            next_folder();
        }
        public void next_folder()
        {
            if (!panel_pause.Visible && !panel_stoped.Visible)
            {
                next_station_();
                panel_information.Visible = false;
                panel_information_file.Visible = true;
                if (stations.Count > 0)
                {
                    player_List_.set_listBox_(stations[iterator_station].listBox1, stations[iterator_station].mp3_list);
                    player_List_.set_item(stations[iterator_station].get_iterator_file());
                    if (panel_content.Controls.Count != 0)
                        if (panel_content.Controls.Count > 0)
                            panel_content.Controls.RemoveAt(0);
                    set_station();
                }
            }
        }
        private void panel_previous_folder_Click(object sender, EventArgs e)
        {
            previous_folder();
        }
        public void previous_folder()
        {
            if (!panel_pause.Visible && !panel_stoped.Visible)
            {
                previous_station_();
                panel_information.Visible = false;
                panel_information_file.Visible = true;
                if (stations.Count > 0)
                {
                    player_List_.set_listBox_(stations[iterator_station].listBox1, stations[iterator_station].mp3_list);
                    player_List_.set_item(stations[iterator_station].get_iterator_file());
                    if (panel_content.Controls.Count != 0)
                        if (panel_content.Controls.Count > 0)
                            panel_content.Controls.RemoveAt(0);
                    set_station();
                }

            }
        }
        private void panel_change__menu_Click(object sender, EventArgs e)
        {
            if (panel_content.Controls.Count == 0)
                openForm(player_List_, this.panel_content);
            else
            {
                if (panel_content.Controls.Count > 0)
                    panel_content.Controls.RemoveAt(0);
            }
        }
        #endregion
        #region file control
        protected override bool ProcessCmdKey(ref Message msg, Keys keyData)
        {
            switch (keyData)
            {
                case Keys.Delete:
                case Keys.Enter:
                    stop();
                    return true;
                case Keys.Left:
                    panel_previous_file_MouseUp();
                    return true;
                case Keys.Right:
                    panel_next_file_MouseUp();
                    return true;
                case Keys.Up:
                    next_folder();
                    return true;
                case Keys.Down:
                    previous_folder();
                    return true;
                case Keys.Escape:
                    this.close();
                    return true;
                case Keys.VolumeMute:
                    //mute();
                    break;
                case Keys.VolumeDown:
                    if (axWMPl.settings.volume > 0)
                        axWMPl.settings.volume = (axWMPl.settings.volume - 5);
                    break;
                case Keys.VolumeUp:
                    if (axWMPl.settings.volume < 100)
                        axWMPl.settings.volume = (axWMPl.settings.volume + 5);
                    break;
                case Keys.MediaStop:
                    stop_file();
                    break;
                case Keys.MediaPlayPause:
                    if (axWMPl.playState == WMPLib.WMPPlayState.wmppsPlaying)
                        pause();
                    else
                        play();
                        break;
                case Keys.MediaNextTrack:
                    panel_next_file_MouseUp();
                    break;
                case Keys.MediaPreviousTrack:
                    panel_previous_file_MouseUp();
                    break;
            }
            return base.ProcessCmdKey(ref msg, keyData);
        }
        private void panel_previous_file_Click(object sender, EventArgs e)
        {
            panel_stoped.Visible = false;
            panel_pause.Visible = false;
            panel_next.Visible = false;
            panel_play_file.Visible = false;
            panel_pre.Visible = true;
        }
        private void panel_previous_file_MouseDown(object sender, MouseEventArgs e)
        {
            panel_pre.Visible = true;
        }
        private void panel_previous_file_MouseUp(object sender, MouseEventArgs e)
        {
            panel_previous_file_MouseUp();
        }
        public void panel_previous_file_MouseUp() {
            panel_pre.Visible = false;
            if (stations.Count > 0)
                if (!panel_pause.Visible && !panel_stoped.Visible)
                {
                    if (panel_repeticion_mode.Visible)
                    {
                        if (stations[iterator_station].aleatorio)
                        {
                            if (stations[iterator_station].list_mp3_r.Count == (stations[iterator_station].mp3_list.Count))
                            {
                                stations[iterator_station].list_mp3_r.Clear();
                                previous_station_();
                                stations[iterator_station].calcula_mp3();
                                player_List_.set_listBox_(stations[iterator_station].listBox1, stations[iterator_station].mp3_list);
                                player_List_.set_item(stations[iterator_station].get_iterator_file());
                            }
                            else
                            {
                                stations[iterator_station].next_mp3();
                                player_List_.set_item(stations[iterator_station].get_iterator_file());
                            }
                        }
                        else
                            //si esta al final pone el siguiente station
                            if (stations[iterator_station].get_iterator_file() == 0)
                        {
                            previous_station_();
                            stations[iterator_station].set_iterator(stations[iterator_station].mp3_list.Count - 1);
                            stations[iterator_station].calcula_mp3();
                            player_List_.set_listBox_(stations[iterator_station].listBox1, stations[iterator_station].mp3_list);
                            player_List_.set_item(stations[iterator_station].get_iterator_file());

                        }
                        else
                        {
                            stations[iterator_station]._previous_mp3();
                            player_List_.set_item(stations[iterator_station].get_iterator_file());
                        }
                    }
                    else
                    {
                        stations[iterator_station]._previous_mp3();
                        player_List_.set_item(stations[iterator_station].get_iterator_file());
                    }
                    set_station();
                }
        }
        private void panel_next_file_Click(object sender, EventArgs e)
        {
            panel_stoped.Visible = false;
            panel_pause.Visible = false;
            panel_play_file.Visible = false;
            panel_pre.Visible = false;
            panel_next.Visible = true;
        }
        private void panel_next_file_MouseDown(object sender, MouseEventArgs e)
        {
            panel_next.Visible = true;
        }
        private void panel_next_file_MouseUp(object sender, MouseEventArgs e)
        {
            panel_next_file_MouseUp();
        }
        public void panel_next_file_MouseUp() {
            panel_next.Visible = false;
            if (stations.Count > 0)
                if (!panel_pause.Visible && !panel_stoped.Visible)
                {
                    if (panel_repeticion_mode.Visible)
                    {
                        if (stations[iterator_station].aleatorio)
                        {
                            if (stations[iterator_station].list_mp3_r.Count == (stations[iterator_station].mp3_list.Count))
                            {
                                stations[iterator_station].list_mp3_r.Clear();
                                next_station_();//cambio de estacion
                                stations[iterator_station].calcula_mp3();
                                player_List_.set_listBox_(stations[iterator_station].listBox1, stations[iterator_station].mp3_list);
                                player_List_.set_item(stations[iterator_station].get_iterator_file());
                            }
                            else
                            {
                                stations[iterator_station].next_mp3();
                                player_List_.set_item(stations[iterator_station].get_iterator_file());
                            }
                        }
                        else
                        if (stations[iterator_station].get_iterator_file() == (stations[iterator_station].mp3_list.Count - 1))
                        {
                            stations[iterator_station].set_iterator(0);
                            next_station_();
                            stations[iterator_station].calcula_mp3();
                            stations[iterator_station].set_iterator(0);
                            player_List_.set_listBox_(stations[iterator_station].listBox1, stations[iterator_station].mp3_list);
                            player_List_.set_item(stations[iterator_station].get_iterator_file());
                        }
                        else
                        {
                            stations[iterator_station].next_mp3();
                            player_List_.set_item(stations[iterator_station].get_iterator_file());
                        }
                    }
                    else
                    {

                        {
                            stations[iterator_station].next_mp3();
                            player_List_.set_item(stations[iterator_station].get_iterator_file());
                        }

                    }
                    set_station();
                }
        }
        private void panel_play_file_Click(object sender, EventArgs e)
        {
            panel_play_file.Visible = true;
        }
        private void panel_play_MouseDown(object sender, MouseEventArgs e)
        {
            panel_play_file.Visible = true;
        }
        private void panel_play_MouseUp(object sender, MouseEventArgs e)
        {
            play();
        }
        public void play() {
            if (panel_pause.Visible)
            {
                int r = (get_time() - time_s);
                if (stations.Count > 0)
                    stations[iterator_station].set_time(int.Parse(stations[iterator_station].programation_.Split('^')[3]) + r);
            }
            else
            {
                if (stations.Count > 0)
                    stations[iterator_station].set_time(this.get_time());
            }
            panel_information.Visible = false;
            panel_information_file.Visible = true;
            player_List_.clear();

            if (stations.Count > 0)
            {

                if (panel_content.Controls.Count != 0)
                    if (panel_content.Controls.Count > 0)
                        if (panel_content.Controls[0].Equals(information_))
                            openForm(player_List_, this.panel_content);
                set_station();
                player_List_.set_listBox_(stations[iterator_station].listBox1, stations[iterator_station].mp3_list);
                player_List_.set_item(stations[iterator_station].get_iterator_file());
            }
            panel_stoped.Visible = false;
            panel_pause.Visible = false;
            panel_play_file.Visible = false;
        }
        private void panel_pause_file_Click(object sender, EventArgs e)
        {
            pause();
        }
        public void pause() {
            panel_stoped.Visible = false;
            panel_play_file.Visible = false;
            panel_next.Visible = false;
            panel_pre.Visible = false;
            panel_pause.Visible = true;
            axWMPl.Ctlcontrols.pause();
            time_s = get_time();
        }
        int time_s = 0;
        private void panel_stop_file_Click(object sender, EventArgs e)
        {
            stop();
        }
        public void stop()
        {
            panel_play_file.Visible = false;
            panel_pause.Visible = false;
            panel_next.Visible = false;
            panel_pre.Visible = false;
            panel_stoped.Visible = true;
            axWMPl.Ctlcontrols.stop();
            timer_play.Stop();
            set_current_position(0);
            label_transcurrent_time.Text = "00:00:00";
            label_duration_time.Text = "00:00:00";
            label_artist.Text = "!!";
            label_album.Text = "";
            file_name.Text = "";
        }

            #endregion
            #region directorios
            public int sann_folder()
        {
            int iterator = 0;
            panel_flolders.Controls.Clear();
            try
            {
                string[] directories = Directory.GetDirectories(".\\");
                foreach (string d in directories)
                {
                    PictureBox directory = new PictureBox();
                    directory.Image = img2;
                    directory.Location = new System.Drawing.Point(33, 3);
                    directory.Name = "pictureBox3";
                    directory.Size = new System.Drawing.Size(9, 9);
                    directory.SizeMode = System.Windows.Forms.PictureBoxSizeMode.AutoSize;
                    directory.TabIndex = 2;
                    directory.TabStop = false;
                    directory.Tag = iterator+"";
                    directory.MouseClick += directory_MouseClick;
                    panel_flolders.Controls.Add(directory);
                    stations.Add(new Station());
                    get_directory(d);
                    iterator++;
                }
                get_files(".\\");
            }
            catch (System.IO.DirectoryNotFoundException e)
            {
                Console.WriteLine(" Error en de ubicacion " + "" + e);
            }
            foreach (Station s in stations)
                s.reload();
            if (stations.Count > 0) {
                iterator_station = r.Next(stations.Count);
                player_List_.set_listBox_(stations[iterator_station].listBox1, stations[iterator_station].mp3_list);
                player_List_.set_item(stations[iterator_station].get_iterator_file());
                set_station();
            }
            return 0;
         }
        public void _deselect_panel_folders_(int iter)
        {
            foreach (object o in panel_flolders.Controls)
            {
                ((PictureBox)o).Image = img2;
            }
            ((PictureBox)(panel_flolders.Controls[iter])).Image = img1;
        }
        public void get_directory(string directory)
        {
            try
            {
                string[] directories = Directory.GetDirectories(directory);
                foreach (string d in directories)
                {
                        get_directory(d);
                }
                get_files(directory);
            }
            catch (System.IO.DirectoryNotFoundException e)
            {
                Console.WriteLine(" Error en de ubicacion " + "" + e);
            }
        }
        public void get_files(string directory)
        {
            directory_nfo = new DirectoryInfo(@directory);
            Files = directory_nfo.GetFiles("*.mp3");
            /**/
            foreach (FileInfo file in Files)
            {
                stations[stations.Count-1].add_file_(file.Name , file.FullName);
            }
            return;
        }
        #endregion
        public void set_station()
        {
            if (stations.Count > 0)
            {
                if (iterator_station > stations.Count)
                    iterator_station = 0;

                if (stations.Count > iterator_station)
                {
                    _deselect_panel_folders_(iterator_station);

                    int curr = stations[iterator_station].get_playing_now_time_elapsed();
                    axWMPl.URL = stations[iterator_station]._playing_now_url();
                    set_current_position(curr);
                }
                else {
                    _deselect_panel_folders_(iterator_station);
                    next_station_();
                }
            }
        }
        public void previous_station_()
        {
            if (stations.Count > 0)
            {
                if (iterator_station >= 1)
                    iterator_station -= 1;
                else
                    iterator_station = stations.Count - 1;
            }
        }
        public void next_station_()
        {
            if (stations.Count > 0)
            {
                if (iterator_station < stations.Count - 1)
                    iterator_station += 1;
                else
                    iterator_station = 0;
            }
        }
        private void easyPanel_ProgressBar1_Click(object sender, EventArgs e)
        {
            if (stations.Count > 0) {
                easyPanel_ProgressBar1.Value = 0;
                float absoluteMouse = (PointToClient(MousePosition).X - easyPanel_ProgressBar1.Bounds.X);
                float calcFactor = easyPanel_ProgressBar1.Width / (float)easyPanel_ProgressBar1.Maximum;
                float relativeMouse = absoluteMouse / calcFactor;
                easyPanel_ProgressBar1.Value = Convert.ToInt32(relativeMouse);
                stations[iterator_station].time_change(Convert.ToInt32(relativeMouse), this.wmps_current_position());
                set_station();
            }
        }
        public void set_current_position(int current)
        {
            if (current <= 0)
                axWMPl.Ctlcontrols.currentPosition = 0;
            else
                axWMPl.Ctlcontrols.currentPosition = current;
        }
        


        private void panel_next_file_MouseUp(object sender, EventArgs e)
        {

        }

        private void panel_stop_m_Click(object sender, EventArgs e)
        {
            stop_file();

        }
        public void stop_file()
        {
            if (axWMPl.playState == WMPLib.WMPPlayState.wmppsPaused)
            {
                int r = (get_time() - time_s);
                stations[iterator_station].set_time(int.Parse(stations[iterator_station].programation_.Split('^')[3]) + r);
                panel_information.Visible = false;
                panel_information_file.Visible = true;
                player_List_.clear();
                if (panel_content.Controls.Count != 0)
                    if (panel_content.Controls.Count > 0)
                        if (panel_content.Controls[0].Equals(information_))
                            openForm(player_List_, this.panel_content);
                set_station();
                player_List_.set_listBox_(stations[iterator_station].listBox1, stations[iterator_station].mp3_list);
                player_List_.set_item(stations[iterator_station].get_iterator_file());
                panel_stoped.Visible = false;
                panel_pause.Visible = false;
                panel_play_file.Visible = false;
            }
            else
            {
                panel_stoped.Visible = false;
                panel_play_file.Visible = false;
                panel_next.Visible = false;
                panel_pre.Visible = false;
                panel_pause.Visible = true;
                axWMPl.Ctlcontrols.pause();
                time_s = get_time();
            }
        }

     
    }
}
