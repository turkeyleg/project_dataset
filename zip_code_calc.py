import urllib2
import pickle
from bs4 import BeautifulSoup



zip1 = '01966'
zip2 = '02139'



class ZipCodesUtil:
    def __init__(self):
        try:
            pkl_file = open('zip_dict.pkl', 'rb')
            self.zip_dict = pickle.load(pkl_file)
        except:
            self.zip_dict = {}
    def get_distance(self, zip1, zip2):
        if zip1 in self.zip_dict:
            if zip2 in self.zip_dict[zip1]:
                return self.zip_dict[zip1][zip2]
            else:
                distance = self.get_distance_from_web(zip1, zip2)
                self.zip_dict[zip1][zip2] = distance
                return distance
        else:
            self.zip_dict[zip1] = {}
            distance = self.get_distance_from_web(zip1, zip2)
            self.zip_dict[zip1][zip2] = distance
            return distance

    def get_distance_from_web(self, zip1, zip2):
        zipURLtemplate = 'http://www.melissadata.com/lookups/zipdistance.asp?zip1=%s&zip2=%s'
        html = urllib2.urlopen(zipURLtemplate %(zip1, zip2)).read()
        soup = BeautifulSoup(html, 'html.parser')
        # hacky, but hey
        try:
            distance =  float(soup.find_all('b')[4].string)
            return distance
        except Exception as e:
            print 'Exception parsing results for %s and %s' %(zip1, zip2)
            print e
            print soup.find_all('b')
            self.pickle()

    def pickle(self):
        pkl_file = open('zip_dict.pkl', 'wb')
        pickle.dump(self.zip_dict, pkl_file)
        pkl_file.close()










