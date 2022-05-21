using System;
using System.Collections.Generic;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;
using WMPLib;

namespace YouSaw
{
    public class Station
    {
        public int _id_station = 0;
        public string _station_name = "";
        public string _date;
        public List<int> _categories = new List<int>();
        public List<int> _languages = new List<int>();
        public List<int> _genres = new List<int>();
        public string programation_ = null;
        public char _clasification;
        public int _number = 0;
        public List<int> series_reproducidas = new List<int>();

        public List<int> om_list = new List<int>();//series en otros canales

        private List<int> series = new List<int>();
        List<int> vs = new List<int>();

        public int tiempo_de_inicio = 0;
        public Random r = new Random(int.Parse(TimeSpan.Parse(DateTime.Now.Hour + ":" + DateTime.Now.Minute + ":" + DateTime.Now.Second).TotalSeconds.ToString()));

        public int duracion = 0;

        
        public ListBox.ObjectCollection listBox1;
        public List<string> mp3_list = new List<string>();
        List<int> mp3_list_r = new List<int>();
        private int _iterator = 0;
        public Station()
        {
            ListBox listbox = new ListBox();
            listBox1 = new ListBox.ObjectCollection(listbox);
            _iterator = 0;
            programation_ = "";
        }

        public List<List<string>> list = new List<List<string>>();

        public void set_time(int time_)
        {
            this.programation_ = programation_.Split('^')[0] + "^" + programation_.Split('^')[1] + "^" + programation_.Split('^')[2] + "^" + time_;
        }
        public void set_iterator(int iterator_)
        {
            _iterator = iterator_;
            this.programation_ = _iterator + "^" + programation_.Split('^')[1] + "^" + programation_.Split('^')[2] + "^" + programation_.Split('^')[3];
        }
        public string calcula_mp3()
        {
            if (mp3_list.Count != 0)
            {
                _iterator = get_iterator_file();
                if (aleatorio && mp3_list.Count !=1)
                {
                    if (list_mp3_r.Count == mp3_list.Count)
                    { 
                        int i = list_mp3_r[list_mp3_r.Count-1];
                        list_mp3_r.Clear();
                        list_mp3_r.Add(i);
                    }
                    do
                    {
                        _iterator = r.Next(mp3_list.Count);
                    } while (list_mp3_r.Contains(_iterator));

                    list_mp3_r.Add(_iterator);
                }
                else
                {
                    list_mp3_r.Clear();
                    list_mp3_r.Add(_iterator);
                }
                set_mp3(_iterator, listBox1[_iterator].ToString(), mp3_list[_iterator]);
            }
            return this.programation_;
        }
        public List<int> list_mp3_r = new List<int>();
        public string next_mp3()
        {
            if (mp3_list.Count != 0)
            {
                _iterator = get_iterator_file();
                if (aleatorio && mp3_list.Count != 1)
                {
                    if (list_mp3_r.Count == mp3_list.Count)
                    {
                        int i = list_mp3_r[list_mp3_r.Count - 1];
                        list_mp3_r.Clear();
                        list_mp3_r.Add(i);
                    }
                    do
                    {
                        _iterator = r.Next(mp3_list.Count);
                    } while (list_mp3_r.Contains(_iterator));

                    list_mp3_r.Add(_iterator);
                }
                else
                {
                    list_mp3_r.Clear();
                    list_mp3_r.Add(_iterator);
                    _iterator++;
                    if ((mp3_list.Count) == _iterator)
                        _iterator = 0;
                }
                set_mp3(_iterator, listBox1[_iterator].ToString(), mp3_list[_iterator]);
            }
            return this.programation_;
        }
        public string _previous_mp3()
        {
            if (mp3_list.Count != 0)
            {
                _iterator = get_iterator_file();
                if (aleatorio && mp3_list.Count != 1)
                {
                    if (list_mp3_r.Count == mp3_list.Count)
                    {
                        int i = list_mp3_r[list_mp3_r.Count - 1];
                        list_mp3_r.Clear();
                        list_mp3_r.Add(i);
                    }
                    do
                    {
                        _iterator = r.Next(mp3_list.Count);
                    } while (list_mp3_r.Contains(_iterator));

                    list_mp3_r.Add(_iterator);
                }
                else
                {
                    list_mp3_r.Clear();
                    list_mp3_r.Add(_iterator);
                    _iterator--;
                    if (_iterator < 0)
                        _iterator = mp3_list.Count - 1;
                }
                set_mp3(_iterator, listBox1[_iterator].ToString(), mp3_list[_iterator]);
            }
            return this.programation_;
        }
        public bool aleatorio = false;
        public string playing_now_name = "";
        public void set_mp3(int iterator,string name, string mp3)
        {
            this.programation_ = iterator + "^" + name + "^" + mp3 + "^" + time_now();

            this.duracion = (int)Duration();
            playing_now_name = name;
        }
        public Double Duration()
        {
            WindowsMediaPlayerClass wmp = new WindowsMediaPlayerClass();
            IWMPMedia mediainfo = wmp.newMedia(this.programation_.Split('^')[2]);
            return mediainfo.duration;
        }
        public int get_iterator_file()
        {
            if(!programation_.Equals(""))
                return int.Parse(this.programation_.Split('^')[0]);
            return _iterator;
        }

       
        public void updatestation()
        {
           /// this.programation = "S^0^" + url + "^0^" + time_now();
            /*SQLc.updateTable("station", "nombre = '" + this._station_name +
                "',fecha = '" + DateTime.Today.ToShortDateString() +
                "',categorias = '" + parse_to_string(this._categories) +
                "',idiomas = '" + parse_to_string(this._languages) +
                "',generos = '" + parse_to_string(this._genres) +
                "',programacion='" + programation + "'" +
                ",clasificacion = '" + _clasification +
                "',numero = '" + this._number +
                "',series = '" + parse_to_string(series_reproducidas) +
                "'", "id_station=\'" + _id_station + "\'");*/
        }

        public List<int> get_muestra_pelicula()
        {
            /*if (SQLc.getListDatostoInt(creaConsulta("pelicula WHERE pelicula.id_pelicula != '0'"), 0).Count != 0)
            {
                peliculas = desordenarLista(SQLc.getListDatostoInt(creaConsulta("pelicula WHERE pelicula.estado = '0'"), 0));
                if (peliculas.Count == 0)
                {
                    SQLc.updateTable("pelicula", "estado = '0'", creaConsulta("estado = '1'"));
                    peliculas = desordenarLista(SQLc.getListDatostoInt(creaConsulta("pelicula WHERE pelicula.estado = '0'"), 0));
                }
                return peliculas;
            }
            else
            {
                peliculas.Clear();
                return peliculas;
            }*/
            return null;

        }
        public List<int> get_muestra_series()
        {
            vs = new List<int>();
            /*series = desordenarLista(SQLc.getListDatostoInt(creaConsulta("serie WHERE serie.id_serie != '0' "), 0));
            if (series.Count != 0)
            {
                //List<int> svs = muestra_1(series);
                //vs = muestra_2(svs);
                vs = muestra_2(series);

                return vs;
            }*/
            return series;
        }
        public List<int> muestra_1(List<int> ls)
        {
            List<int> vss = new List<int>();
            foreach (int s in ls)
                vss.Add(s);
            //quito las que ya han sido vistas en este station, si no hay se vuelven a cargar en lista auxiliar
            foreach (int f in om_list)
            {
                if (ls.Contains(f))
                    vss.Remove(f);
            }
            if (vss.Count == 0)
                foreach (int s in series)
                    vss.Add(s);
            return vss;
        }
        public List<int> muestra_2(List<int> ls)
        {
            //quito las que se estan reproduciendo en otro canal, si no hay se vuelven a cargar en lista auxiliar
            if (series_reproducidas.Count > 0)
            {
                List<int> vss = new List<int>();
                foreach (int a in ls)
                    vss.Add(a);
                foreach (int a in series_reproducidas)
                {
                    if (vss.Contains(a))
                        vss.Remove(a);
                }
                if (vss.Count == 0)
                {
                    foreach (int s in ls)
                        vss.Add(s);
                    this.series_reproducidas.Clear();
                    updatestation();
                }
                return vss;
            }
            return ls;
        }

        public string _playing_now_url()
        {
            if (_iterator == -1)
                return programation_.Split('^')[2];
            if (!programation_.Equals(""))
                return programation_.Split('^')[2];
            else
                return calcula_mp3().Split('^')[2];
        }
        public int get_playing_now_time_elapsed()
        {
            if (!programation_.Equals(""))
            {
                if (this.time_now() >= int.Parse(programation_.Split('^')[3]))
                {
                    if ((this.time_now() - int.Parse(programation_.Split('^')[3])) < this.duracion)
                        return this.time_now() - int.Parse(programation_.Split('^')[3]);
                    else
                    {
                        int afd = ((this.time_now() - int.Parse(programation_.Split('^')[3])) - duracion);

                        if (afd > (duracion / 3))
                        {
                            next_mp3();
                            int rd = r.Next((duracion / 3));
                            time_change(rd, 0);
                            return rd;
                        }
                        else
                        {
                            next_mp3();
                            time_change(afd, 0);
                            return afd;
                        }
                    }
                }
                else
                {
                    next_mp3();
                    int rd = r.Next((duracion / 3));
                    time_change(rd, 0);
                    return rd;
                }
            }
            else {
                calcula_mp3();
                return 0;
            }
        }

        public void time_change(int t_ajuste, int t_current)
        {
            if (t_ajuste < t_current)
            {
                int ajuste = int.Parse(programation_.Split('^')[3]) + (t_current - t_ajuste);
                this.programation_ = programation_.Split('^')[0] + "^" + programation_.Split('^')[1] + "^" + programation_.Split('^')[2] + "^" + ajuste;
            }
            else if (t_ajuste > t_current)//mayor
            {
                int ajuste = int.Parse(programation_.Split('^')[3]) - (t_ajuste - t_current);
                this.programation_ = programation_.Split('^')[0] + "^" + programation_.Split('^')[1] + "^" + programation_.Split('^')[2] + "^" + ajuste;
            }
            if (this._id_station != 0)
                updatestation();
        }
        public int time_now()
        {
            return int.Parse(TimeSpan.Parse(DateTime.Now.Hour + ":" + DateTime.Now.Minute + ":" + DateTime.Now.Second).TotalSeconds.ToString());
        }




        public void add_file_(string file_name, string file_url)
        {
            add_list(file_url);
        }
        public void add_list(string ur_)
        {
            string s = ur_.Split('\\')[ur_.Split('\\').Length - 1];
            string _ur_ = ur_.Substring(0, ur_.Length - s.Length - 1);

            foreach (List<string> lss in list)
            {
                if(lss.Count<r.Next(4,7))
                foreach (string ds in lss)
                {
                    if (ds.Contains(_ur_.Split('\\')[_ur_.Split('\\').Length - 1]))
                    {
                        lss.Add(ur_);
                        return;
                    }
                }
            }
            list.Add(new List<string>() { ur_ });
        }
        public void reload()
        {
            int n = list.Count - 1;
            for (int i = n; i > 0; i--)
            {
                int rand = r.Next(0, i);
                List<string> temp = _list_reorder(list[i]);
                list[i] = list[rand];
                list[rand] = temp;

            }
            foreach(List<string> s in list)
            {
                foreach (string ss in s)
                {
                    listBox1.Add(ss.Split('\\')[ss.Split('\\').Length - 1].Split('.')[0]);
                    mp3_list.Add(ss);
                }
            }
        }
        private List<string> _list_reorder(List<string> p)
        {
            int n = p.Count - 1;
            for (int i = n; i > 0; i--)
            {
                int rand = r.Next(0, i);
                string temp = p[i];
                p[i] = p[rand];
                p[rand] = temp;

            }
            return p;
        }
    }
}
