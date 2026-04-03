import yt_dlp

video_url = 'https://www.bilibili.com/video/BV1Kb41177UA' 

# 这次我们不仅提取，还要把它下载成一首 mp3/m4a 歌曲
ydl_opts = {
    'format': 'bestaudio/best',
    'outtmpl': '%(title)s.%(ext)s', # 下载的文件名设为“歌名.后缀”
    'postprocessors': [{            # 提取音频后，尽量转成常见的格式
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'm4a',
        'preferredquality': '192',
    }],
    'quiet': False # 开启控制台信息，看下载进度
}

print("正在施展魔法，伪装身份下载音频中...")

try:
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([video_url])
        print("\n✅ 下载完成！快去你的 VS Code 文件夹里看看是不是多了一首歌！")
except Exception as e:
    print(f"\n❌ 发生错误: {e}")