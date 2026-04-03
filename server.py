from flask import Flask, request, jsonify, Response
from flask_cors import CORS
import yt_dlp
import requests

app = Flask(__name__)
# 允许跨域访问，让你的网页可以和服务器通信
CORS(app) 

@app.route('/api/parse')
def parse_video():
    video_url = request.args.get('url')
    if not video_url:
        return jsonify({'error': '没收到链接呀'})

    # 🌟 新增“聪明逻辑”：如果用户只输入了 BV 号，自动帮他补全完整网址
    if not video_url.startswith('http'):
        video_url = f'https://www.bilibili.com/video/{video_url}'

    print(f"收到解析请求: {video_url}")
    ydl_opts = {'format': 'bestaudio/best', 'quiet': True}
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(video_url, download=False)
            return jsonify({
                'title': info.get('title', '未知标题'),
                'cover': info.get('thumbnail', ''),
                'raw_audio_url': info.get('url', '')
            })
    except Exception as e:
        return jsonify({'error': str(e)})
# 核心魔法：帮前端“伪装身份”去 B 站拿音频流（破解防盗链）
# 核心魔法：帮前端“伪装身份”去 B 站拿音频流，并支持随意拖拽！
@app.route('/api/proxy')
def proxy_audio():
    audio_url = request.args.get('url')
    
    # 伪造工作牌
    headers = {
        'Referer': 'https://www.bilibili.com',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    
    # 🌟 核心修复：捕获前端的“跳转进度”请求（Range 请求头）
    # 把它原封不动地传给 B 站服务器
    if 'Range' in request.headers:
        headers['Range'] = request.headers['Range']

    # 边下边播
    req = requests.get(audio_url, headers=headers, stream=True)
    
    # 🌟 核心修复：把 B 站返回的“部分数据”头信息，原封不动地交还给前端
    resp_headers = {
        'Accept-Ranges': 'bytes',
        'Content-Type': req.headers.get('Content-Type', 'audio/mp4')
    }
    if 'Content-Range' in req.headers:
        resp_headers['Content-Range'] = req.headers['Content-Range']
    if 'Content-Length' in req.headers:
        resp_headers['Content-Length'] = req.headers['Content-Length']

    # chunk_size 改大一点 (1MB)，这样你拖拽之后缓冲会更快！
    return Response(
        req.iter_content(chunk_size=1024 * 1024), 
        status=req.status_code, 
        headers=resp_headers
    )
# 🌟 新增：一键获取整个收藏夹的列表
@app.route('/api/import_fav')
def import_fav():
    media_id = request.args.get('fid')
    if not media_id:
        return jsonify({'error': '缺少收藏夹 ID'})
    
    # B站官方获取收藏夹的隐藏接口 (为了演示，这里默认只拉取前 20 首)
    url = f'https://api.bilibili.com/x/v3/fav/resource/list?media_id={media_id}&pn=1&ps=20'
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
    
    try:
        res = requests.get(url, headers=headers).json()
        if res['code'] != 0:
            return jsonify({'error': res['message']})
        
        videos = res['data']['medias']
        result = []
        for v in videos:
            result.append({
                'title': v['title'],
                'bv': v['bvid'],
                'cover': v['cover']
            })
        return jsonify({'data': result})
    except Exception as e:
        return jsonify({'error': str(e)})
import os

if __name__ == '__main__':
    # 🌟 这里的 port 会优先读取云服务器分配的端口
    port = int(os.environ.get('PORT', 5000))
    print(f"🚀 云端服务启动，监听端口 {port}...")
    app.run(host='0.0.0.0', port=port)