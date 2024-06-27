from flask import Flask, render_template, request, session, redirect, url_for, send_from_directory, Response
from video import Video
import os
import traceback
import sys
import io
import urllib.parse
from pytube import Playlist, YouTube

app = Flask(__name__)
app.secret_key = '1111'

@app.route('/', methods = ['POST', 'GET'])
def index():
    if request.method == 'POST':
        try:
            video = Video(request.form['link'])
            session['url'] = request.form['link']
            return redirect(url_for('download'))
        except:
            try:
                playlist = Playlist(request.form['link'])
                print(playlist.video_urls) #проверяем существует ли этот плейлист
                session['url'] = request.form['link']
                return redirect(url_for('download_playlist'))
            except:
                return render_template('index.html')
    return render_template('index.html')

@app.route('/download', methods = ['POST', 'GET'])
def download():
    video = Video(session['url'], r'C:\Users\Admin\Desktop\yt downloader 2.0\static\videos')
    
    if request.method == 'POST':

        if request.form.get('download'):
            if 'resolution' not in session:
                session['resolution'] = video.get_resolutions()[0]
            video.download_video(session['resolution'])
            filename = video.get_filename()       
            with open(f'C:\\Users\\Admin\\Desktop\\yt downloader 2.0\\static\\videos\\{filename}', 'rb') as file:
                response = Response(file.read(), content_type = 'video/mp4')
                response.headers.set('Content-Disposition', 'attachment', filename = filename.encode(encoding = 'UTF-8', errors = 'strict'))
                return response

        elif request.form.get('download_mp3'):
            video.download_mp3()
            filename = video.get_mp3_filename()
            with open(f'C:\\Users\\Admin\\Desktop\\yt downloader 2.0\\static\\videos\\{filename}', 'rb') as file:
                response = Response(file.read(), content_type = 'video/mp3')
                response.headers.set('Content-Disposition', 'attachment', filename = filename.encode(encoding = 'UTF-8', errors = 'strict'))
                return response
    
        else:
            for r in video.get_resolutions(): # обработка нажатий кнопок выбора разрешения
                if request.form.get(r):
                    session['resolution'] = r
                    break  

    if 'resolution' in session:     
        return render_template('download.html', video_title = video.get_title(), thumbnail_url = video.video.thumbnail_url, video_id = video.get_id(), resolutions = video.get_resolutions(), selected_resolution = session['resolution'],)
    else:
        return render_template('download.html', video_title = video.get_title(), thumbnail_url = video.video.thumbnail_url, video_id = video.get_id(), resolutions = video.get_resolutions(), selected_resolution = video.get_resolutions()[0])


@app.route('/download_playlist', methods = ['POST', 'GET'])
def download_playlist():

    playlist = Playlist(session['url'])
    videos = []
    for url in playlist.video_urls:
        video = Video(video_url = url)
        videos.append({'thumbnail_url' : video.video.thumbnail_url, 'video_url' : url, 'title' : video.video_title})

    if request.method == 'POST':
        if request.form.get('download_all'):
            pass
        else:
            for url in playlist.video_urls:
                if request.form.get(url):
                    video = Video(url, r'C:\Users\Admin\Desktop\yt downloader 2.0\static\videos')
                    video.download_video(resolution = video.get_resolutions()[-1])
                    filename = video.get_filename()       
                    with open(f'C:\\Users\\Admin\\Desktop\\yt downloader 2.0\\static\\videos\\{filename}', 'rb') as file:
                        response = Response(file.read(), content_type = 'video/mp4')
                        response.headers.set('Content-Disposition', 'attachment', filename = filename.encode(encoding = 'UTF-8', errors = 'strict'))
                        return response

    return render_template('download_playlist.html', videos = videos)

if __name__ == '__main__':
    app.run(debug = True)
