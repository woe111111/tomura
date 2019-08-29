import requests
#http://wiki.jikexueyuan.com/project/elasticsearch-definitive-guide-cn/030_Data/05_Document.html
res = requests.get('http://www.baidu.com',
                  proxies={'http': '127.0.0.1:8887',"https":"127.0.0.1:8888"})
print(res.text)
print(res.headers)

# import urllib3
# import urllib3.response
# http = urllib3.PoolManager()
#
# r = http.request('get','http://wiki.jikexueyuan.com/project/elasticsearch-definitive-guide-cn/030_Data/05_Document.html',headers={'User-Agent': 'python-requests/2.19.1', 'Accept-Encoding': 'gzip, deflate', 'Accept': '*/*', 'Connection': 'keep-alive'})
# print(r.headers)
# # print('111',r.data)
# CONNECT www.baidu.com:443 HTTP/1.0\r\n\r\n
# CONNECT www.baidu.com:443 HTTP/1.0\r\n\r\n
