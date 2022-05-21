using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;

namespace MP3Autorun
{
    public partial class player_list : Form
    {
        MP3Autorun_ form_;
        public player_list(MP3Autorun_ form)
        {
            InitializeComponent();
            listBox1.BackColor = Color.FromArgb(0,1,62);
            listBox1.ForeColor = Color.WhiteSmoke;
            listBox1.Items.Clear();
            form_ = form;
        }
        public void clear()
        {
            listBox1.Items.Clear();
        }
        List<string> listBox2 = new List<string>();
        public void set_listBox_(ListBox.ObjectCollection collection, List<string> listBox2_) {
            int i = 1;
            listBox1.Items.Clear();
            foreach (object c in collection) {
                listBox1.Items.Add(i + ":" + c);
                i++;
            }
            
            listBox2 = listBox2_;
        }
        public void set_item(int iterator) {
            listBox1.SelectedIndex = iterator;
        }
        private void listBox1_SelectedIndexChanged(object sender, EventArgs e)
        {
            //form_.get_station().set_mp3(listBox1.SelectedIndex, listBox1.Items[listBox1.SelectedIndex].ToString(), listBox2[listBox1.SelectedIndex]);
            //MessageBox.Show("" + listBox1.SelectedIndex);
            
        }

        private void listBox1_MouseDown(object sender, MouseEventArgs e)
        {
            //Si selecciono por medio del mouse
            if (((ListBox)sender).IndexFromPoint(new Point(e.X, e.Y)) >= 0)
            {
                form_.get_station().set_mp3(listBox1.SelectedIndex, listBox1.Items[listBox1.SelectedIndex].ToString(), listBox2[listBox1.SelectedIndex]);
                form_.set_station();
            }
        }
    }
}
