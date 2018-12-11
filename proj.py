import requests
import json
import sqlite3 as sqlite
import plotly.plotly as py
import plotly.graph_objs as go
from prettytable import PrettyTable
from wordcloud import WordCloud
import matplotlib.pyplot as plt

from bs4 import BeautifulSoup
from selenium import webdriver

class Person:
    def __init__(self,rank='', href='',name='',networth='',age='',source='',country='',martial='',children='',education=''):
    # def __init__(self,name,age):
        self.rank=rank
        self.href=href
        self.name=name
        self.networth=networth
        self.age=age
        self.source=source
        self.country=country        
        self.martial=martial
        self.children=children
        self.education=education
        

    # def get_detailed(self):
    #     url='https://www.forbes.com'+self.href
    #     html = requests.get(url).text
    #     soup = BeautifulSoup(html, 'html.parser')
    #     stats=soup.find('div',class_="profile-stats")
    #     stats=stats.find_all('div',class_='profile-stats__item')        
    #     try:
    #         if stats[2].text[:15]=='Self-Made Score':
    #             flag=1
    #         else:
    #             flag=0
    #     except:
    #         flag=0
    #     if flag==1:
    #         try:
    #            self.martial=stats[5].text[14:]
    #         except:
    #             self.martial=''
    #         try:
    #             self.children=stats[6].text[8:]
    #         except:
    #             self.children=''
    #         try:
    #             self.education=stats[7].text[9:]
    #         except:
    #             self.education=''
    #     else:
    #         try:
    #             self.martial=stats[4].text[14:]
    #         except:
    #             self.martial=''
    #         try:
    #             self.children=stats[5].text[8:]
    #         except:
    #             self.children=''
    #         try:
    #             self.education=stats[6].text[9:]
    #         except:
    #             self.education=''

    def __str__(self):
            
        return ("#"+str(self.rank)+ ': '+ self.name +' (country:'+self.country+'    networth:'+self.networth+ '   age:' + str(self.age)+ '   source:' +self.source+ '   martial:' +self.martial+ '   children:' +self.children+ '   education:' +self.education+')')
    
    def printtable(self):
        x= PrettyTable(['rank','name','country','networth','age','source','martial','children','education'])
        x.align["rank"] = "l"
        x.padding_width = 1
        x.add_row([str(self.rank),self.name,self.country,self.networth,str(self.age),self.source,self.martial,self.children,self.education])
        print(x)    



def get_list():
    web='https://www.forbes.com/billionaires/list/6/#version:static'
    driver=webdriver.Chrome("./chromedriver.exe")
    driver.get(web)
    soup=BeautifulSoup(driver.page_source,'html5lib')
    people=soup.find('tbody',id="list-table-body")
    people=people.find_all('tr',class_='data')

    people_list=[]
    id=1
    for one in people:
        people_dict=dict()        
        if id>200:
            break
        
        people_dict['id']=id
        people_dict['rank']=one.find('td',class_='rank').text[1:]
        people_dict['href']=one.find('td',class_='name').find('a')['href']
        people_dict['name']=one.find('td',class_='name').find('a').text
        people_dict['networth']=one.find('td',class_='networth').text
        people_dict['age']=one.find_all('td')[4].text
        people_dict['source']=one.find_all('td')[5].text
        people_dict['country']=one.find_all('td')[6].text
        stat_dict=get_detailed_info(people_dict['href'])
        people_dict['martial']=stat_dict['martial']
        people_dict['children']=stat_dict['children']
        people_dict['education']=stat_dict['education']
        people_list.append(people_dict)
        # print(people_dict)
        id+=1
    return people_list

def get_country_list(li):
    country_list=[]
    for l in li:
        if l['country'] not in country_list:
            country_list.append(l['country'])
    return sorted(country_list)

def get_detailed_info(url):
    url='https://www.forbes.com'+url
    html = requests.get(url).text
    soup = BeautifulSoup(html, 'html.parser')
    stats=soup.find('div',class_="profile-stats")
    stats=stats.find_all('div',class_='profile-stats__item')
    stat_dict=dict()

    stat_dict['martial']=''
    stat_dict['children']=''
    stat_dict['education']=''
    
    for stat in stats:
        title=stat.find('span',class_='profile-stats__title').text
        if title=='Marital Status':
            stat_dict['martial']=stat.find('span',class_='profile-stats__text').text

    for stat in stats:
        title=stat.find('span',class_='profile-stats__title').text
        if title=='Children':
            stat_dict['children']=stat.find('span',class_='profile-stats__text').text

    for stat in stats:
        title=stat.find('span',class_='profile-stats__title').text
        if title=='Education':
            stat_dict['education']=stat.find('span',class_='profile-stats__text').text


    return stat_dict
    
def create_db(DB_name,LIST):
    
    try:
        conn = sqlite.connect(DB_name)
    except:
        print("Create DataBase fail!")
    
    cur = conn.cursor()
    statement = '''
        DROP TABLE IF EXISTS 'People';
    '''
    cur.execute(statement)

    statement = '''
        DROP TABLE IF EXISTS 'Country';
    '''

    cur.execute(statement)

    # Create tables
    # create Country table
    statement = '''
        CREATE TABLE 'Country' (
                'id' INTEGER PRIMARY KEY AUTOINCREMENT,
                'country' TEXT NOT NULL
        );
    '''
    cur.execute(statement)
    country_list=get_country_list(LIST)
    for l in country_list:
        statement= '''
            INSERT INTO 'Country' (country) VALUES (?)
        '''        
        cur.execute(statement, (l,))



    # create People table
    statement = '''
        CREATE TABLE 'People' (
                'id' INTEGER PRIMARY KEY AUTOINCREMENT,
                'rank' INTEGER NOT NULL,
                'href' TEXT NOT NULL,
                'name' TEXT NOT NULL,
                'networth' TEXT NOT NULL,
                'age' INTEGER NOT NULL,
                'source' TEXT NOT NULL,
                'countryid' INTEGER,
                'martial' TEXT,
                'children' TEXT,
                'education' TEXT,
                FOREIGN KEY ('countryid') REFERENCES Country('id')
        );
    '''
    cur.execute(statement)

    for l in LIST:
        statement= '''
            INSERT INTO 'People' (rank, href,name,networth,age,source,countryid,martial,children,education) VALUES (?,?,?,?,?,?,?,?,?,?)
        '''        
        countryid=country_list.index(l['country'])+1
        cur.execute(statement, (l['rank'],l['href'],l['name'],l['networth'],l['age'],l['source'],countryid,l['martial'],l['children'],l['education']))

    

    # Close connection
    conn.commit()
    conn.close()


def fetch_data_by_country(DB_name,country_name):
    conn = sqlite.connect(DB_name)    
    cur = conn.cursor()
    statement = '''
        SELECT p.name,p.age,p.networth FROM People AS p
        JOIN Country AS c
        on c.id=p.countryid
        WHERE c.country LIKE 
    '''
    statement+='"'+country_name+'"'

    results=cur.execute(statement)
    result_list = results.fetchall()
    people_list=[]
    for one_person in result_list:
        p=Person(name=one_person[0],age=one_person[1],networth=one_person[2])
        people_list.append(p)
        # print(p)
    return people_list


def select_by_rank(rank):
    conn = sqlite.connect(DB_name)    
    cur = conn.cursor()
    statement = '''
        SELECT * FROM People AS p
        JOIN Country AS c
        on c.id=p.countryid
        WHERE p.id =
    '''
    statement+= str(rank)

    results=cur.execute(statement)
    result_list = results.fetchall()
    people_list=[]
    for one_person in result_list:
        p=Person(one_person[1],one_person[2],one_person[3],one_person[4],one_person[5],one_person[6],one_person[12],one_person[8],one_person[9],one_person[10])
        people_list.append(p)
        p.printtable()
    return people_list

def select_all():
    conn = sqlite.connect(DB_name)    
    cur = conn.cursor()
    statement = '''
        SELECT * FROM People AS p
        JOIN Country AS c
        on c.id=p.countryid
    '''
    
    results=cur.execute(statement)
    result_list = results.fetchall()
    people_list=[]
    x= PrettyTable(['rank','name','country','networth','age','source','martial','children','education'])
    x.align["rank"] = "l"
    x.align["education"] = "l"
    x.padding_width = 1
    for one_person in result_list:
        p=Person(one_person[1],one_person[2],one_person[3],one_person[4],one_person[5],one_person[6],one_person[12],one_person[8],one_person[9],one_person[10])
        people_list.append(p)
        
        x.add_row([str(p.rank),p.name,p.country,p.networth,str(p.age),p.source,p.martial,p.children,p.education])
        
        # print(p)
    print(x)
    return people_list



def plot_networth(LI):
    worth_dict=dict()
    x_list=[]
    y_list=[]
    for l in LI:
        if l['country'] in worth_dict:
            worth_dict[l['country']]+=float(l['networth'][1:-2])
        else:
            worth_dict[l['country']]=float(l['networth'][1:-2])
            x_list.append(l['country'])
    for one in x_list:
        y_list.append(worth_dict[one])
    data = [go.Bar(
                x=x_list,
                y=y_list
        )]    
    py.iplot(data, filename='networth-bar', auto_open=True)

def plot_networth_by_country(people_list):
    x_list=[]
    y_list=[]
    for p in people_list:
        x_list.append(p.name)
        y_list.append(p.networth)
    data = [go.Bar(
                x=x_list,
                y=y_list
        )]    
    py.iplot(data, filename='country-networth-bar', auto_open=True)


def plot_age(people_list):
    x_list=[]
    y_list=[]
    for p in people_list:
        x_list.append(p.name)
        y_list.append(p.age)
    data = [go.Bar(
                x=x_list,
                y=y_list
        )]    
    py.iplot(data, filename='age-bar', auto_open=True)


def plot_number(LI):
    worth_dict=dict()
    x_list=[]
    y_list=[]
    for l in LI:
        if l['country'] in worth_dict:
            worth_dict[l['country']]+=1
        else:
            worth_dict[l['country']]=1
            x_list.append(l['country'])
    for one in x_list:
        y_list.append(worth_dict[one])
    data = [go.Bar(
                x=x_list,
                y=y_list
        )]    
    py.iplot(data, filename='number-bar', auto_open=True)


def plot_wordcloud(LI):
    # Create a list of word
    text=""
    for l in LI:
        text+=l['source']+' '
    # Create the wordcloud object
    wordcloud = WordCloud(width=480, height=480, margin=0).generate(text)
    
    # Display the generated image:
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis("off")
    plt.margins(x=0, y=0)
    plt.show()



if __name__ == "__main__":

    
    CACHE_FNAME = 'cache.json'
    DB_name='proj.sqlite'
    try:
        cache_file = open(CACHE_FNAME, 'r')
        cache_contents = cache_file.read()
        CACHE= json.loads(cache_contents)
        cache_file.close()
    
    except:
        CACHE= get_list()
        dumped_json_cache = json.dumps(CACHE,indent=4)
        file_cache=open(CACHE_FNAME,'w')
        file_cache.write(dumped_json_cache)
        file_cache.close()
    
    LI=CACHE
    create_db(DB_name,LI)    
    # plot_number(LI)
    # plot_wordcloud(LI)
    # plot_age(fetch_data_by_country(DB_name,'China'))
    # fetch_data_by_country(DB_name,'China')

    while True:
        content=input("Enter command(or 'help' for options): ")
        
        if content=='help':
            help_prompt= """
        rank <rank>
            available anytime
            return the millionaire with the rank closest rank
            <rank> should be from 1 to 200
        list
            available anytime
            lists all 2018 top 200 millionaires 
        wordcloud
            available anytime
            display the wordcloud made by the source of all the billionaires
        networth
            available anytime
            display the barchart of sum of all billionaires's networth in each country 
        networth <country>
            available anytime
            display the barchart of all billionaires's networth in the user selected country
        number
            available anytime
            display the barchart of the number billionaires in each country 
        age <country>
            available anytime
            display the barchart of all billionaires' age in the country input by user
        rebuild database
            available anytime
            rebuild the database with cache
        exit
            exits the program
        help
            lists available commands (these instructions) """

            print(help_prompt)

        elif content=='list':
            select_all()
        elif content=='exit':
            print('Bye!')
            break
        elif content[0:4]=='rank':
            r=content[5:]
            
            if r.isdigit() and int(r)>=1 and int(r)<=200:
                select_by_rank(int(r))
            else:
                print('Invalid input! Please enter a number from 1 to 200!')
            continue
        elif content=='wordcloud':
            plot_wordcloud(LI)
        elif content=='networth':
            plot_networth(LI)
        elif content[:8]=='networth':
            c=content[9:]
            if c in get_country_list(LI):
                plot_networth_by_country(fetch_data_by_country(DB_name,c))
            else:
                print('No such country or no millionaires in that country,please input a country in the list shown below:')
                c_list=''
                for c in get_country_list(LI):
                    c_list+=c+' '
                print(c_list)
        elif content=='number':
            plot_number(LI)
        elif content[:3]=='age':
            c=content[4:]
            if c in get_country_list(LI):
                plot_age(fetch_data_by_country(DB_name,c))
            else:
                print('No such country or no millionaires in that country,please input a country in the list shown below:')
                c_list=''
                for c in get_country_list(LI):
                    c_list+=c+' '
                print(c_list)
        elif content=='rebuild database':
            try:
                create_db(DB_name,LI)  
                print('Rebuild databse successfully!')
            except:
                print("Fail to rebuild databse!")
        else:
            print('Invalid input! Please input \'help\' for options')
        