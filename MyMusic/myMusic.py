from mutagen.mp3 import MP3
import pygame
import requests
from PySide2.QtCore import QFile, QStringListModel, QTimer
from PySide2.QtUiTools import QUiLoader
from PySide2.QtWidgets import QApplication

# http://www.gequdaquan.net/gqss/


class Music_Download:
    def __init__(self):
        super(Music_Download, self).__init__()

        qfile = QFile('UI.ui')
        qfile.open(QFile.ReadOnly)
        qfile.close()

        self.ui = QUiLoader().load(qfile)

        self.ui.Bsearch.clicked.connect(self.get_song_list)
        self.ui.Bpause.clicked.connect(self.pause_song)
        self.ui.Bup.clicked.connect(self.vol_up)
        self.ui.Bdown.clicked.connect(self.vol_down)
        self.ui.Bnetease.clicked.connect(self.source_netease)
        self.ui.Bkugou.clicked.connect(self.source_kugou)
        self.ui.Bbaidu.clicked.connect(self.source_baidu)
        self.ui.Bxiami.clicked.connect(self.source_xiami)

        self.ui.song_list.doubleClicked.connect(self.doublechecked_song)

        self.timer1 = QTimer()
        self.timer1.start(1000)
        self.timer1.timeout.connect(self.show_info)

        self.url = 'http://www.gequdaquan.net/gqss/api.php?callback=jQuery111309785577532049254_1610118818132'
        self.headers = {
            'Referer': 'http://www.gequdaquan.net/gqss/',
            'User-Agent': 'Mozilla/5.0(Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
                          '(KHTML, like Gecko) Chrome/87.0.4280.88 Safari / 537.36',
            'X-Requested-With': 'XMLHttpRequest'
        }

        self.song_list = []
        self.ui.Bnetease.setChecked(True)
        self.ui.Bnetease.setEnabled(False)
        self.source = 'netease'
        self.search_name = ''
        self.song_name = ''
        self.song_id = ''
        self.song_artist = ''
        self.show_list = []
        self.song_url = ''
        self.index = ''
        pygame.init()
        self.pause_state = 0
        self.time_length = float(0)

        pygame.mixer.music.set_volume(0.7)
        self.get_vol = pygame.mixer.music.get_volume()

    def get_song_list(self):
        self.show_list = []
        self.get_edit_text()
        data = {
            'types': 'search',
            'count': 20,
            'source': self.source,
            'pages': 1,
            'name': self.search_name
        }
        response = requests.post(url=self.url, headers=self.headers, data=data)
        # result = response.text.replace(r'\\', '/')
        result = response.text.encode().decode('unicode_escape')
        result = result.strip('jQuery111309785577532049254_1610118818132()')
        self.song_list = eval(result)
        for song in self.song_list:
            self.song_name = song.get('name')
            self.song_id = song.get('id')
            self.song_artist = ' '.join(song.get('artist'))
            self.show_list.append(self.song_name + ' *-* ' + self.song_artist)
        self.add_show_list()

    def get_edit_text(self):
        self.search_name = self.ui.Edit_input.text()

    def add_show_list(self):
        list_model = QStringListModel()
        list_model.setStringList(self.show_list)
        self.ui.song_list.setModel(list_model)

    def get_song_url(self):
        data = {
            'types': 'url',
            'id': self.song_id,
            'source': self.source,
        }

        response = requests.post(url=self.url, headers=self.headers, data=data)
        result = response.text.replace('\\', '')
        result = result.encode().decode('unicode_escape')
        result = result.strip('jQuery111309785577532049254_1610118818132()')
        result = eval(result)
        self.song_url = result.get('url')

    def download_song(self):

        self.get_song_url()
        response = requests.get(url=self.song_url, headers=self.headers)
        self.ui.label_state.setText('正在下载' + self.song_name + '-' + self.song_artist + '.mp3')
        with open(self.song_name + '-' + self.song_artist + '.mp3', 'wb') as w:
            w.write(response.content)
        self.ui.label_state.setText('下载完成')
        self.play_song()
        self.pause_state = 1
        self.ui.label_state.setText('正在播放： ' + self.song_name + '-' + self.song_artist + '.mp3')

    def checked_song(self, index):
        self.index = index
        song = self.song_list[index.row()]
        self.song_id = song.get('id')
        self.source = song.get('source')
        self.song_name = self.show_list[index.row()].split(' *-* ')[0]
        self.song_artist = self.show_list[index.row()].split(' *-* ')[1]

    def doublechecked_song(self, index):
        self.checked_song(index)
        self.download_song()

    def play_song(self):
        pygame.init()
        pygame.mixer.music.load(self.song_name + '-' + self.song_artist + '.mp3')
        self.time_length = MP3(self.song_name + '-' + self.song_artist + '.mp3').info.pprint().\
            split(',')[-1].replace('seconds', '').strip()
        pygame.mixer.music.play()

    def pause_song(self):
        if self.pause_state == 1:
            pygame.mixer.music.pause()
            self.ui.Bpause.setText('继续')
            self.ui.label_state.setText('已暂停： ' + self.song_name + '-' + self.song_artist + '.mp3')
            self.pause_state = 0
        else:
            pygame.mixer.music.unpause()
            self.ui.Bpause.setText('暂停')
            self.ui.label_state.setText('正在播放： ' + self.song_name + '-' + self.song_artist + '.mp3')
            self.pause_state = 1

    def show_info(self):
        if self.time_length != float(0):
            all_m, all_s = divmod(float(self.time_length), 60)
            all_time = str(int(all_m)) + ':' + str(int(all_s))
            get_time = pygame.mixer.music.get_pos() / 1000
            get_m, get_s = divmod(float(get_time), 60)
            now_time = str(int(get_m)) + ':' + str(int(get_s))

            vol = str(int(self.get_vol * 100)) + '%'
            self.ui.label_info.setText(now_time + '/' + all_time + ' ' * 25 + '音量：' + vol)

    def vol_up(self):
        self.get_vol += 0.1
        if self.get_vol >= 1:
            self.get_vol = 1
        pygame.mixer.music.set_volume(self.get_vol)

    def vol_down(self):
        self.get_vol -= 0.1
        if self.get_vol <= 0:
            self.get_vol = 0
        pygame.mixer.music.set_volume(self.get_vol)

    def button_init(self):
        self.ui.Bnetease.setChecked(False)
        self.ui.Bkugou.setChecked(False)
        self.ui.Bbaidu.setChecked(False)
        self.ui.Bxiami.setChecked(False)
        self.ui.Bnetease.setEnabled(True)
        self.ui.Bkugou.setEnabled(True)
        self.ui.Bbaidu.setEnabled(True)
        self.ui.Bxiami.setEnabled(True)

    def source_netease(self):
        self.source = 'netease'
        self.button_init()
        self.ui.Bnetease.setChecked(True)
        self.ui.Bnetease.setEnabled(False)
        self.get_song_list()

    def source_kugou(self):
        self.source = 'kugou'
        self.button_init()
        self.ui.Bkugou.setChecked(True)
        self.ui.Bkugou.setEnabled(False)
        self.get_song_list()

    def source_baidu(self):
        self.source = 'baidu'
        self.button_init()
        self.ui.Bbaidu.setChecked(True)
        self.ui.Bbaidu.setEnabled(False)
        self.get_song_list()

    def source_xiami(self):
        self.source = 'xiami'
        self.button_init()
        self.ui.Bxiami.setChecked(True)
        self.ui.Bxiami.setEnabled(False)
        self.get_song_list()


if __name__ == '__main__':
    app = QApplication([])
    app.setStyle('Fusion')
    windows = Music_Download()
    windows.ui.show()
    app.exec_()

