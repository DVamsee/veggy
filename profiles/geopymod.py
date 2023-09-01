
from geopy import Nominatim
from geopy.distance import geodesic

class locate:
    def __init__(self,village,
                city,mandal, district,
                state, country='India', pin= None ):
        self.address = village+' '+city+' '+ mandal+' '+district+' '+state+' '+ country+' '+ pin
        
        obj = Nominatim(user_agent='projectA')
        self.loc = obj.geocode(self.address)
        if self.loc is None:
            self.address = self.address.replace(village+' ','')
            self.loc = obj.geocode(self.address)
        if self.loc is None:
            self.address = self.address.replace(mandal+' ','')
            self.loc = obj.geocode(self.address)
        if self.loc is None:
            self.address = state+' '+country+' '+pin
            self.loc = obj.geocode(self.address)
                
                
    
    def lat_lon(self):
        if self.loc is None:
            return 0,0
        lat = self.loc.latitude
        lon = self.loc.longitude
        return lat,lon
    

class Find_distance():
    def __init__(self,lat1,lon1,lat2,lon2):
        self.lat1 = lat1
        self.lon1 = lon1
        self.lat2 = lat2
        self.lon2 = lon2
    def distance(self):
        d = geodesic((self.lat1,self.lon1), (self.lat2,self.lon2)).km
        return d
    
    