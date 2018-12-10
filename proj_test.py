from proj import *
import unittest

class TestData(unittest.TestCase):

    def testlist(self):

        people_list=get_list()
        country_list=get_country_list(people_list)
        last={'id': 200, 'rank': '198 ', 'href': '/profile/patrick-soon-shiong/?list=billionaires', 'name': 'Patrick Soon-Shiong', 'networth': '$7.8 B', 'age': '66', 'source': 'pharmaceuticals', 'country': 'United States'}
        
        self.assertEqual(len(people_list), 200)
        self.assertEqual(len(country_list), 33)
        self.assertEqual(people_list[-1], last)


        p_list=fetch_data_by_country('proj.sqlite','China')
        self.assertEqual(p_list[0].name, 'Ma Huateng')
        self.assertEqual(p_list[1].name, 'Jack Ma')
        for p in p_list:
            self.assertIsInstance(p,Person)




class TestDB(unittest.TestCase):
    def test_join(self):
        conn = sqlite.connect('proj.sqlite')
        cur = conn.cursor()

        sql = '''
            SELECT * FROM People AS p
            JOIN Country AS c
            on c.id=p.countryid
        '''
        results = cur.execute(sql)
        result_list = results.fetchall()
        self.assertEqual(len(result_list), 200)
        self.assertEqual(result_list[0][0], 1)
        conn.close()

    def test_country(self):
        conn = sqlite.connect('proj.sqlite')
        cur = conn.cursor()

        sql = '''
            SELECT * FROM Country 
        '''
        results = cur.execute(sql)
        result_list = results.fetchall()
        self.assertEqual(len(result_list), 33)        
        conn.close()

    def test_select(self):
        conn = sqlite.connect('proj.sqlite')
        cur = conn.cursor()

        sql = '''
            SELECT p.name,p.age,p.networth FROM People AS p
            JOIN Country AS c
            on c.id=p.countryid
            WHERE c.country LIKE 'China'
        '''
        results = cur.execute(sql)
        result_list = results.fetchall()
        self.assertEqual(len(result_list), 21)   

        sql = '''
            SELECT p.name,p.age,p.networth FROM People AS p
            JOIN Country AS c
            on c.id=p.countryid
            WHERE p.id =1
        '''
        results = cur.execute(sql)
        result_list = results.fetchone()
        self.assertEqual(result_list[0], 'Jeff Bezos')     
         
        conn.close()


    def test_db(self):
        conn = sqlite.connect('proj.sqlite')
        cur = conn.cursor()

        sql = '''
            SELECT * FROM People AS p
            JOIN Country AS c
            on c.id=p.countryid
        '''
        results = cur.execute(sql)
        result_list = results.fetchall()
        self.assertEqual(len(result_list), 200)
        conn.close()



class TestPlot(unittest.TestCase):    
    def test_plot(self):
        people_list=get_list()
        try:
            plot_number(people_list)            
        except:
            self.fail()
        try:
            plot_networth(people_list)            
        except:
            self.fail()
        try:
            plot_wordcloud(people_list)            
        except:
            self.fail()
        p_list=fetch_data_by_country('proj.sqlite','China') 
        try:
            plot_networth_by_country(p_list)      
        except:
            self.fail()
        try:
            plot_age(p_list)      
        except:
            self.fail()


if __name__ == "__main__":
    unittest.main()
