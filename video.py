from pytube import YouTube
from moviepy.editor import *
import os
from urllib.parse import urlparse


class Video:
    def __init__(self, video_url, video_folder = ''):
        self.folder = video_folder
        self.video = YouTube(video_url)
        self.video_url = video_url
        self.video_title = self.video.title

    def get_id(self):
        url = urlparse(self.video_url)
        if url.hostname == 'youtu.be': # для таких ссылок : https://youtu.be/
            return url.path.split('/')[1]
        elif self.video_url.split('/')[3].split('=')[0] == 'watch?v' and '&' not in self.video_url: # для таких ссылок : https://www.youtube.com/watch?v=
            return self.video_url.split('/')[3].split('=')[1]
        elif self.video_url.split('&')[1].split('=')[0] == 'list': # для таких ссылок https://www.youtube.com/watch?v=&list=
            return self.video_url.split('=')[1].split('&')[0]
        
    def get_filename(self):
        return self.video.streams.get_highest_resolution().default_filename
    
    def get_mp3_filename(self):
        return f'{self.video.streams.get_highest_resolution().default_filename[:-1]}3'    
        
    def get_resolutions(self, only_progressive = True) -> list:
        '''Returns list of available resolutions for this video.'''
        all_resolutions = ['144p', '240p', '360p', '480p', '720p', '1080p', '1440p', '2160p']
        available_resolutions = []
        if only_progressive:
            for i in all_resolutions:
                if self.video.streams.get_by_resolution(i):
                    available_resolutions.append(i)
        else:
            for i in all_resolutions:
                if any(self.video.streams.filter(resolution = i)):
                    available_resolutions.append(i)
        return available_resolutions

    def download_video(self, resolution : str):
        '''Скачивает видео с указаным разрешением'''   
        if resolution == '360p' or resolution == '720p':
            stream = self.video.streams.get_by_resolution(resolution)
            print(self.video.streams)
            stream.download(self.folder)
        else:
            video_stream = self.video.streams.filter(resolution = resolution)[0]
            video_stream.download(f'{self.folder}\\temp\\video')
            audio_stream = self.video.streams.filter(only_audio = True)[0]
            audio_stream.download(f'{self.folder}\\temp\\audio')
            video_clip = VideoFileClip(f'{self.folder}\\temp\\video\\{self.get_filename()}')
            audio_clip = AudioFileClip(f'{self.folder}\\temp\\audio\\{self.get_filename()}')
            final_clip = video_clip.set_audio(audio_clip)
            final_clip.write_videofile(f'{self.folder}\\{self.get_filename()}')


    def download_mp3(self):
        '''Скачивает видео в формате mp4 и конвертирует в mp3'''
        stream = self.video.streams.get_by_resolution('360p')
        stream.download(self.folder)
        mp4_video = VideoFileClip(f'{self.folder}\\{self.get_filename()}') 
        mp3_filename = f'{self.get_filename()[:-1]}3'
        mp4_video.audio.write_audiofile(f'{self.folder}\\{mp3_filename}', codec='libmp3lame')
        mp4_video.close()
        os.remove(f'{self.folder}\\{self.get_filename()}')
        


# v = Video('https://youtu.be/K9FwzGv-gqk?si=ZRb7Fh6Th4BZ5Eci', r'C:\Users\Admin\Desktop\yt downloader 2.0\static\videos')
# print(v.get_resolutions())
# print(v.get_resolutions(only_progressive=False))
# print(v.video.streams.get_by_resolution('720p'))
