
import requests
from requests_html import HTML
import pandas as pd
import pprint
import re

class market_price:
    
    def __init__(self) :
        self.districts = [
            'ANANTAPUR',
            'CHITTOOR',
            'ELURU',
            'GUNTUR',
            'KADAPA',
            'KAKINADA',
            'KURNOOL',
            'MACHILIPATNAM',
            'NELLORE',
            'ONGOLE',
            'SRIKAKULAM',
            'VISAKHAPATNAM',
            'VIZIANAGARAM',
        ]
#converts the given url to th html text 
    def price(self,product,district):
        district = district.capitalize()
        if district not in self.districts:
            veg=requests.get(f'https://market.todaypricerates.com/Andhra-Pradesh-vegetables-price')
            fru= requests.get(f'https://market.todaypricerates.com/Andhra-Pradesh-fruits-price')
        else:
            veg=requests.get(f'https://market.todaypricerates.com/{district}-vegetables-price-in-Andhra-Pradesh')
            fru= requests.get(f'https://market.todaypricerates.com/{district}-fruits-price-in-Andhra-Pradesh')

        if veg.status_code == 200 and fru.status_code == 200:
            veg_text = veg.text
            fru_text = fru.text
        product = product.capitalize()
        
        if not (veg_text and fru_text):
            return False
        result = {}
        for html_text in [veg_text,fru_text]:
            r_html = HTML(html=html_text)
            t_class = '.Table'
            r_table = r_html.find(t_class)
            table_data=[]
            header_names =[]
            
            if len(r_table) == 0:
                return False
            parsed_table = r_table[0]
            rows = parsed_table.find('.Row')
            header_row = parsed_table.find('.Heading')[0]
            header_cols = header_row.find('.Cellth')
            header_names = [ x.text for x in header_cols]
            for row in rows:
                cols = row.find('.Cell')
                row_data =[]
                for col in cols:
                    row_data.append(col.text)
                table_data.append(row_data)
        

            for table in table_data:
                for i in range(len(table)):
                    if i == 0:
                        result[table[i]]={}
                    else:
                        result[table[0]][header_names[i]] = table[i]
        for pdt in result:
            x = re.search(product,pdt)
            if x:
                return result[x.string]
            
            
if __name__ == '__main__':
                
    x = market_price()
    xe = x.price('tomato','chittoor')            
            
    print(xe)   
 