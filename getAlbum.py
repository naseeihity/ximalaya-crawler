import requests, os
from contextlib import closing
from progressBar import ProgressBar
musicArr = []
base_url = 'https://www.ximalaya.com/revision/play/album'
## 用户输入url
url = input("Please input the album input:")
## 示例：观影风向标url
# url = 'https://www.ximalaya.com/yingshi/232161/'

## 获取当前专辑的id
if url.endswith('/'):
  albumId = url.split('/')[-2]
else:
  albumId = url.split('/')[-1]

pageNum = 1
pageSize = 30
sort = 0 ## 顺序
## 请求头
header = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:57.0) Gecko/20100101 Firefox/57.0'}
## 参数
payload = {
    'albumId': albumId,
    'pageNum': pageNum,
    'sort': sort,
    'pageSize': pageSize
}

## 发送请求
## 获取返回值
temp = True
data = []
while temp:
  r = requests.get(base_url, params=payload, headers=header)
  res = r.json()
  if (res and res['ret'] == 200):
    data.extend(res['data']['tracksAudioPlay'])
    if res['data']['hasMore']:
      payload['pageNum'] += 1
    else:
      temp = False
    
  else:
    print('request failed!')
    temp = False

albumName = data[0]['albumName']

for item in data:
  musicArr.append({'src':item['src'], 'name': item['trackName']})

if not os.path.exists(albumName):
  os.makedirs(albumName)

for m in musicArr:
  if os.path.exists(albumName + '/%s.m4a' % m['name']):
    continue
  with closing(requests.get(m['src'], headers=header, stream=True)) as res:
    chunk_size = 1024  # 单次请求最大值
    content_size = int(res.headers['content-length'])  # 内容体总大小
    progress = ProgressBar(m['name'], total=content_size,
                           unit="KB", chunk_size=chunk_size, run_status="downloading", fin_status="finished")
    
    with open(albumName + '/%s.m4a' % m['name'], 'wb') as f:
      for data in res.iter_content(chunk_size=chunk_size):
        f.write(data)
        progress.refresh(count=len(data))
