# SI507_FinalProject

## Data source
[![The World's Billionaires]](https://www.forbes.com/billionaires/list/)
[![https://www.forbes.com/billionaires/list/]](https://www.forbes.com/billionaires/list/)

Since the website uses js scripts to generate the result shown on the website, we cannot use crawling directly. Here I use selenium and 
chromedriver to simulate the process of using chrome and get data from that. Hence when running the program, chromedriver.exe must be put in the same folder with proj.py.


## Code structure
* class: Person
  * Variable: 
    * rank: billionaire's rank
    * name: billionaire's name
    * href: billionaire's href in the website
    * networth: billionaire's networth
    * age: billionaire's age
    * country: billionaire's country
    * source: source of billionaire's networth

* function:
  * get_list():
    * get a list of people from Forbes website.
  * get_detailed_info(url):
    * get detailed information of a person by his/her url.
  * create_db(DB_name,LIST):
    * create databse with the crawling data or cache data
  * fetch_data_by_country(DB_name,country_name):
    * get data of specified country from the database
    * return a list of class Person in the country
    
## User Guide
User can input the following command:
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
    lists available commands (these instructions) 
  
