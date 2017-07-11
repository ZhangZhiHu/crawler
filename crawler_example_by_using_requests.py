#-*-coding: utf-8 -*-
#@author:tyhj
import requests
from bs4 import BeautifulSoup

username,password=open(r'C:\Python27\zht\whu\account').read().split('\n')

session=requests.session()
#--------------------------------------------------------------------------------
#using the login page to get cookies
url1=r'http://cas.whu.edu.cn/authserver/login?service=http://my.whu.edu.cn/'
header1={
    'Host':'cas.whu.edu.cn',
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:54.0) Gecko/20100101 Firefox/54.0',
    'Referer':'http://my.whu.edu.cn/'
}

r1=session.get(url1,headers=header1)

#-----------------------------------------------------------------------------------------
#login
soup1=BeautifulSoup(r1.content,'lxml')
form=soup1.find_all("form",{'id':'casLoginForm'})[0]

lt=form.find('input',{'name':'lt'})['value']
dllt=form.find('input',{'name':'dllt'})['value']
execution=form.find('input',{'name':'execution'})['value']
_eventId=form.find('input',{'name':'_eventId'})['value']
rmShown=form.find('input',{'name':'rmShown'})['value']

url2=r'http://cas.whu.edu.cn/authserver/login?service=http://my.whu.edu.cn/'
header2={
    'Host': 'cas.whu.edu.cn',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:54.0) Gecko/20100101 Firefox/54.0',
    'Referer':'http://cas.whu.edu.cn/authserver/login?service=http%3A%2F%2Fmy.whu.edu.cn%2F'
}

postdata={'username':username,
          'password':password,
          'lt':lt,  #these items can be get from html
          'dllt':dllt,
          'execution':execution,
          '_eventId':_eventId,
          'rmShown':rmShown
          }

r2=session.post(url2,data=postdata,headers=header2,allow_redirects=False)

if 'location' in r2.headers.keys():
    print 'login successfully!'


#------------------------------------------------------------------------------------------------
#get the infomations
location=r2.headers['location']
url3=location
header3={
    'Host': 'my.whu.edu.cn',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:54.0) Gecko/20100101 Firefox/54.0',
    'Referer':'http://cas.whu.edu.cn/authserver/login?service=http%3A%2F%2Fmy.whu.edu.cn%2F'
}

# r3=session.get(url3,headers=header3,allow_redirects=False)
r3=session.get(url3,headers=header3)
with open('content3.html','w') as f:
    f.write(r3.content)

soup3=BeautifulSoup(r3.content,'lxml')
li=soup3.find('li',text='个人信息')

urlInfo=r'http://my.whu.edu.cn/'+li.a['href']
header4={
    'Host': 'my.whu.edu.cn',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:54.0) Gecko/20100101 Firefox/54.0',
    'Referer':'http://my.whu.edu.cn/'
}


r4=session.get(urlInfo,headers=header4)


#parse the data
soup4=BeautifulSoup(r4.content)
table=soup4.find('table',{'class':'pa-main-table'})
text=table.text
text1=text.strip()
text2=text1.split('\n\n\n')

studentId=text2[0].split('\n')[1].strip()
name=text2[0].split('\n')[3].strip()
gender=text2[1].split('\n')[1].strip()
birthday=text2[1].split('\n')[3].strip()
nationality=text2[1].split('\n')[5].strip()
ploticalStatus=text2[2].split('\n')[1].strip()
idNumber=text2[2].split('\n')[3].strip()
grade=text2[3].split('\n')[1].strip()
category=text2[3].split('\n')[3].strip()
faculty=text2[3].split('\n')[5].strip()
major=text2[4].split('\n')[1].strip()
dormitory=text2[4].split('\n')[3].strip()
address=text2[4].split('\n')[5].strip()

#get picture
img=soup4.find('img',{'alt':'图片'})
urlPic=r'http://my.whu.edu.cn/'+img['src']
r5=session.get(urlPic)
with open(username+'.jpg','wb') as f:
    f.write(r5.content)

