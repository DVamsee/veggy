
import requests
from requests_html import HTML
import pandas as pd
import pprint
import re

class market_price:
    url=''
    def __init__(self):
        veg=requests.get('https://market.todaypricerates.com/Andhra-Pradesh-vegetables-price')
        fru= requests.get('https://market.todaypricerates.com/Andhra-Pradesh-fruits-price')

        if veg.status_code == 200 and fru.status_code == 200:
            self.veg_text = veg.text
            self.fru_text = fru.text
        else:
            self.veg_text = None
            self.fru_text = None
#converts the given url to th html text 
    def price(self,product):
        product = product.capitalize()
        veg_text = self.veg_text
        fru_text = self.fru_text
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
            
        
                    
        
        
 