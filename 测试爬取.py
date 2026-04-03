import requests

def test_bili_fav(media_id):
    print(f"🕵️ 正在测试爬取收藏夹 ID: {media_id} ...\n")
    
    # B站公开收藏夹的隐藏 API (pn=1代表第1页，ps=20代表取20个)
    url = f'https://api.bilibili.com/x/v3/fav/resource/list?media_id={media_id}&pn=1&ps=20'
    
    # 必须伪装成浏览器，不然 B站 的保安不给进
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    
    try:
        # 发送请求并解析返回的 JSON 数据
        response = requests.get(url, headers=headers)
        data = response.json()
        
        # 检查 B站 是不是放行了
        if data['code'] != 0:
            print(f"❌ 爬取失败！B站返回错误: {data['message']}")
            return
            
        videos = data['data']['medias']
        print(f"✅ 成功！一共爬到了 {len(videos)} 首歌，列表如下：\n" + "="*40)
        
        # 遍历打印出歌名和 BV 号
        for index, video in enumerate(videos, 1):
            title = video['title']
            bvid = video['bvid']
            print(f"{index}. {title}  -->  {bvid}")
            
    except Exception as e:
        print(f"❌ 发生异常: {e}")

# 填入你截图里的 fid
test_bili_fav('3864160460')