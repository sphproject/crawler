# -*- coding: cp1252 -*-
from bs4 import BeautifulSoup
import sys
import os
import codecs
import re
import csv

###set working directory
os.chdir(os.getcwd()+'\\Data')


def ContentExtraction(num, input):

     soup=BeautifulSoup(input)
     index=num
 
     #standard straitstimes.com formet
     template='straitstimes_standard'

     try: title = soup.find("title").get_text().strip()
     except: title='NA'

     try: author=soup.find("div", {"class":"st2014-byline"}).get_text().strip()
     except: author='NA'

     try: time=soup.find("div",{"class":"st2014-published-text"}).get_text().strip()
     except: time='NA'

     category='others'
     try:           #parse all text lines in content into one line, separated by space
         content_soup=soup.find("div",{"class":"st2014-content"})
         content=''
         cons=content_soup.findAll("p")
         for c in cons:
            content=content+c.get_text().replace('\n','').replace('\r','').strip()+' '
         category='article'
     except: 
         try:           #event
           event_soup=soup.find("div",{"class":"st2014-event-description"})
           cons=event_soup.findAll("p")
           content=''
           for c in cons:
              content=content+c.get_text().replace('\n','').replace('\r','').strip()+' '
           category='event'
         except: content='NA'
    
     try:
         log_url=soup.find("div",{"class":"st2014-login-btn"}).find("a").get('href')
     
         if re.compile('.*/ldap/redirect\.html*').search(log_url) is not None:
             login=1
         else: login=0
     except: login=0

     try:
         sub_url=soup.find("div",{"class":"st2014-subscribe-btn"}).find("a").get('href')
         if re.compile('.*www\.sphsubscription\.com*').search(sub_url) is not None:
             subscription=1
         else: subscription=0
     except: subscription=0

     if login==1 or subscription==1:
         premium=1
     else: premium=0

     if author=='NA' and time=='NA' and content=='NA':
         author ='UNKNOWN'
         time='UNKNOWN'
         content='UNKNOWN'
         template='UNKNOWN'
         
     done='successful'

     if content=='': content='NO_TEXT'
     
     try:
         outwriter.writerow((index,template,title.encode('utf-8'),author.encode('utf-8'),time.encode('utf-8'),category,
                             content.encode('utf-8'),login,subscription,premium,done)) 

     except:
         done='unsuccessful'
         outwriter.writerow((index,done,done,done,done,done,done,login,subscription,premium,done))
         
     return 

    
def main(start_html, end_html):
     
    outwriter.writerow(('index','template','title','author','time','category',
                             'content','login','subscription','premium','done'))
    
    for i in xrange(int(start_html), int(end_html)+1):
        try:
            input = codecs.open('html_'+str(i)+'.html')         ###Read article i
            index=i;
            ContentExtraction(index, input)            
        except:pass
    return


#read keyboard input
start=raw_input('Enter the start line: ')
end=raw_input('Enter the end line: ')
out = codecs.open('out.csv','w')   #output to csv file, encoded with utf-8, or some 'string' cannot be written to file
outwriter=csv.writer(out,quoting=csv.QUOTE_NONNUMERIC, lineterminator='\n')
main(start,end)
out.close()
