import time
import requests
from lxml import etree
import re
import json
import urllib
import xlwt
import os
from selenium import webdriver
from selenium.webdriver.common.by import By


url ="https://music.163.com/discover/toplist?id=3779629"
headers = {'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36'}#反爬虫
workbook=xlwt.Workbook(encoding='utf-8')
globals()
#写入表头
wooksheet=workbook.add_sheet('歌曲')
wooksheet.write(0,0,'歌曲名')
wooksheet.write(0,1,'歌手名')
wooksheet.write(0,2,'专辑名')
wooksheet.write(0,3,'专辑封面')
wooksheet.write(0,4,'歌词')
wooksheet.write(0,5,'评论')
wooksheet.write(0,6,'歌曲外部链接')
#wooksheet.write(0,7,'歌手个人介绍')
#wooksheet.write(0,8,'歌手头像')

response = requests.get(url,headers=headers)
html = etree.HTML(response.text)
ids = html.xpath('//ul[@class="f-hide"]//a/@href')


#定义循环输出id的函数
def parseArtist(url):
    response = requests.get(url, headers=headers)
    html = etree.HTML(response.text)
    artist_id = html.xpath('//p[@class="des s-fc4"]//a[@class="s-fc7"]/@href')
    for i in range(len(artist_id)):
        artist_id[i] = re.sub('\D', '', artist_id[i])
    artist_id.remove(artist_id[1])
    del artist_id[1:]
    print(artist_id)
    for i in range(len(artist_id)):
        url1=f"https://music.163.com/artist?id={artist_id[i]}"
        response = requests.get(url1, headers=headers)
        html = etree.HTML(response.text)
        user_id = html.xpath('//a[@id="artist-home"]/@href')

    for i in range(len(user_id)):
        user_id[i] = re.sub('\D', '', user_id[i])
    print(user_id)

    return user_id



#去除url前面部分，只留下id
for i in range(len(ids)):
    ids[i] = re.sub('\D', '', ids[i])

#组合形成新的url
for i in range(len(ids)):
    song_tree = f"https://music.163.com/song?id={ids[i]}"
    song_tree_out=f"https://music.163.com/outchain/player?type=2&id={ids[i]}&auto=0&height=430"


    response = requests.get(song_tree,headers=headers)
    html = etree.HTML(response.text)
    music_info = html.xpath('//title/text()')
    ly=f'http://music.163.com/api/song/lyric?' + 'id=' + str(ids[i]) + '&lv=1&kv=1&tv=-1'





    res=requests.get(ly,headers=headers)
    json_obj=res.text

    j=json.loads(json_obj)
    lrc=j['lrc']['lyric']
    pat=re.compile(r'\[.*\]')
    lrc=re.sub(pat,"",lrc)
    lrc=lrc.strip()
    rl = 'http://music.163.com/weapi/v1/resource/comments/R_SO_4_' + ids[i] + '?csrf_token='
    data = {
        'params': 'zC7fzWBKxxsm6TZ3PiRjd056g9iGHtbtc8vjTpBXshKIboaPnUyAXKze+KNi9QiEz/IieyRnZfNztp7yvTFyBXOlVQP/JdYNZw2+GRQDg7grOR2ZjroqoOU2z0TNhy+qDHKSV8ZXOnxUF93w3DA51ADDQHB0IngL+v6N8KthdVZeZBe0d3EsUFS8ZJltNRUJ',
        'encSecKey': '4801507e42c326dfc6b50539395a4fe417594f7cf122cf3d061d1447372ba3aa804541a8ae3b3811c081eb0f2b71827850af59af411a10a1795f7a16a5189d163bc9f67b3d1907f5e6fac652f7ef66e5a1f12d6949be851fcf4f39a0c2379580a040dc53b306d5c807bf313cc0e8f39bf7d35de691c497cda1d436b808549acc'}
    postdata = urllib.parse.urlencode(data).encode('utf8')  # 进行编码
    request = urllib.request.Request(rl, headers=headers, data=postdata)
    reponse = urllib.request.urlopen(request).read().decode('utf8')
    json_dict = json.loads(reponse)  # 获取json
    hot_commit = json_dict['hotComments']
    music_name = music_info[0].split('-')[0]
    singer=music_info[0].split('-')[1]
    dis = html.xpath("//div[@class='cnt']//p[@class='des s-fc4']//a/@href")
    for a in range(len(dis)):
        dis[a] = re.sub('\D', '', dis[a])
    isd=dis[1]
    result= isd.split('\n')
    uli=[]
    for c in range(len(result)):
        music_albums = f"https://music.163.com/album?id={result[c]}"
        rse=requests.get(music_albums,headers=headers)
        html = etree.HTML(rse.text)
        album=html.xpath("//h2/text()")
        album_image_url=html.xpath("//img[@class='j-img']/@src")
        wooksheet.write(i+1,2,album)
        wooksheet.write(i+1,3,album_image_url)



    # user_id_sum=''.join(parseArtist(song_tree))
    # user_url = f'https://music.163.com/user/home?id={user_id_sum}'
    # driver = webdriver.Edge()
    # driver.get(user_url)
    # time.sleep(4)
    # frame = driver.find_element(By.ID, 'g_iframe')
    # print(frame)
    # driver.switch_to.frame(frame)
    #
    # intro = driver.find_element(By.XPATH, '//*[@id="head-box"]/dd/div[2]')
    #
    # print(intro.text)
    # picture_url = driver.find_element(By.XPATH, '//*[@id="ava"]/img')
    # print(picture_url.get_attribute('src'))
    # list=[]
    # list.append(intro.text)
    # list.append( picture_url.get_attribute('src'))
    # driver.close()
    #
    # wooksheet.write(i + 1, 7, list[0])
    # wooksheet.write(i + 1, 8, list[1])





    for item in hot_commit:
        mi=item['content']
    #存储信息
    wooksheet.write(i+1,0,music_name)
    wooksheet.write(i+1,1,singer)
    wooksheet.write(i+1,4,lrc)
    wooksheet.write(i+1,5,mi)
    wooksheet.write(i+1,6,song_tree_out)
    workbook.save(os.path.join(os.getcwd(), "song.xls"))
    try:
        print('正在爬取', music_name)
        print('爬取成功')
    except:
        print('爬取失败')