import re, json, csv, time
from selenium import webdriver
from bs4 import BeautifulSoup

root_id =['5edb0d1492a58c2d9436363a']
loop = 5

profile = webdriver.FirefoxProfile("((((PATH TO YOUR PROFILE))))")
driver = webdriver.Firefox(profile)

f = open("xfan_data.csv", "a")
f.close()

def getinfo(xfanid):
	link = "https://xfantazy.com/video/"+xfanid
  
	global driver
	driver.get(link)
	# time.sleep(2)
	soup =BeautifulSoup(driver.page_source,'lxml')

	xfan_id = link.split('/')[-1]
	k2s_id= re.findall(r'\/[^\/]*\/main\/',driver.page_source)[0][1:-6]

	xfan_name=soup.find('h1')
	xfan_name = xfan_name.text

	try:
		categories = soup.find('h2', text = 'Categories').parent.text
		categories = categories.replace('Categories','')
	except:
		categories = ""

	try:
		tags = soup.find('h2', text = 'Tags').parent.text
		tags = tags.replace('Tags','')
	except:
		tags = ""

	temp = soup.find_all('a')
	recommendation=[]
	for t in temp:
		if t.has_attr('data-stats'):
			if 'video:recommended' in t['data-stats']:
        ####################################################################################
        ####### ADD your condition here.
				if any( te in t.text.lower() for te in ["dlrrs", "dlrok","dlrsl","dlotr","dlrss", "dlzts", "dlvbs", "dlhpd"]):
					recommendation += [ t['href'].split('/')[-1] ]

	recommendation = list(set(recommendation))
	return [xfan_id,k2s_id,xfan_name,categories,tags,recommendation]

data = csv.reader(open('xfan_data.csv'))
data =list(data)

try:
	dataid = [ t[0] for t in data]
except:
	dataid = []

for t in range(1,loop+1):
	next_id = []
	for xfanid in range(len(root_id)):
		if root_id[xfanid] not in dataid:
			info = getinfo(root_id[xfanid])
			print(info)
			next_id+=info[-1]
			dataid+=[info[0]]
			data+=[info[:-1]]
			with open("xfan_data.csv", "w", newline="") as f:
				writer = csv.writer(f)
				writer.writerows(data)
			print('progress: {}/{} ..... {}%'.format(str(xfanid+1),str(len(root_id)), str((xfanid+1)/len(root_id)*10000//1/100) ))
	root_id = next_id
	print(dataid)
	print('!!____ loop count: '+str(t))

driver.close()
