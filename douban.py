#encoding: utf-8
import  string,os,sys,re, json,datetime,time,requests
from bs4 import BeautifulSoup






cookiesfile = '/Users/chenxiaojun/Desktop/python/douban/cookies.txt'#通过抓包把自己cookies数据放入到文件中 此处为文件绝对路径
settingfile = '/Users/chenxiaojun/Desktop/python/douban/setting.json'#通过抓包把自己cookies数据放入到文件中 此处为文件绝对路径
resultfile = '/Users/chenxiaojun/Desktop/python/douban/result.json'#通过抓包把自己cookies数据放入到文件中 此处为文件绝对路径


cookies = {};
setting = {};
result = {}

headers = {'user-agent': 'my-app/0.0.1'}
def compare_time(time1,time2):#如果time1晚于time2 则返回 True
    s_time = time.mktime(time.strptime(time1,"%Y-%m-%d %H:%M:%S"))
    e_time = time.mktime(time.strptime(time2,"%Y-%m-%d %H:%M:%S"))
    return (int(s_time) - int(e_time)) > 0

def fetchData(lasttime):
	if not lasttime:
		return True;
	ThreeAgo = datetime.date.today() - datetime.timedelta(days=3)
	#3天时间之前的数据返回False
	if compare_time(ThreeAgo.strftime("%Y-%m-%d %H:%M:%S"),lasttime):
		print '三天前数据 over'
		return False
	#最后一条时间和 上一次执行时间比较
	if setting.get('lasttime') and compare_time(setting.get('lasttime'),lasttime):
		print '更新到最新了'
		return False
	return True

def dealWithXML(text):#处理数据 并且返回最后一条数据的时间
 	soup = BeautifulSoup(text,'html.parser')
 	hrefs = [];
 	lasttime = '';
 	for td in soup.find_all('td'):
 		if td.attrs.get('class') and td.attrs.get('nowrap') and td.attrs.get('title'):
 			lasttime = td.attrs.get('title')
 			# print lasttime
	for a in soup.find_all('a'):
	 	if a.attrs.get('class') and a.attrs.get('title') and a.attrs.get('href'):
	 		url = a.attrs.get('href');
	 		# print url + '    ' + a.attrs.get('title')
	 		content = a.attrs.get('title');
	 		for keyword in setting['keywords']:
	 			if keyword in content:
	 				print "get:" + content;
	 				if not result.get(url):#不存在先用列表中
	 					result[url] = content;
	return lasttime;


def main():
	#通过文件获取cookies信息
	with open(cookiesfile, 'r') as f:
		text = f.read();
		arr = text.split(";");
		for c in arr:
			item = c.split('=');
			cookies[item[0]] = item[1];
	with open(resultfile,'r') as f:
		obj = json.loads(f.read());
		for k, v in obj.items():
			result[k] = v;

	while True:
		with open(settingfile, 'r') as f:
			# setting = json.loads(f.read());
			obj = json.loads(f.read());
			for k, v in obj.items():
				setting[k] = v;
		start = 0;
		lasttime = ""#最后一条数据的时间
		while fetchData(lasttime):#通过时间戳来判断是否继续获取数据
			url = "https://www.douban.com/group/?start=" + str(start);
			req = requests.get(url,cookies=cookies,headers=headers);
			lasttime = dealWithXML(req.text);
			time.sleep(7);#休息5s防止被抓
			start += 50;

		print '本次执行结束'
		#写入上次执行的时间
		with open(settingfile, 'w') as f:
			dt = datetime.datetime.now();
			setting['lasttime'] = dt.strftime("%Y-%m-%d %H:%M:%S");
			f.write(json.dumps(setting));

		#写入最新数据	
		with open(resultfile, 'w') as f:
			f.write(json.dumps(result));
		time.sleep(3600);

if __name__ == '__main__':
		main();

