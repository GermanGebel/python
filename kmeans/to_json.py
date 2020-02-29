import json
from bs4 import BeautifulSoup
import requests as req
import string
import logging

JSONFILE = 'planes_data.json'
def getSoup(url):
    try:
        page = req.get(url)
        soup = BeautifulSoup(page.text, 'html.parser')
        return soup
    except req.exceptions.Timeout:
        return None
    except req.exceptions.MissingSchema:
        return None
def delProbel(text:str):
    return int(''.join([i for i in text if i.isnumeric()]))

def toValue(text:str):
    if text == '':
        return None
    else:
        if '-' not in text:
            return delProbel(text)
        else:
            s = text.split('-')
            return (delProbel(s[0])+delProbel(s[1]))//2

def log(text, INFO=False, ERROR=False):
    logging.basicConfig(filename='main-info.log',level=logging.INFO)
    if INFO:
        logging.info(text)
    elif ERROR:
        logging.error(text)

def writeDataToJsonFile(data,filename):
    with open(filename,'r') as write_file:
        olddata = json.load(write_file)
        print(olddata)
        # if  olddata != '' or olddata!=None:
        #     olddata = json.loads(olddata)
        #     data = olddata.update(data)
        write_file.close()
    with open(filename,'w') as write_file:
        json.dump(data,write_file)
        write_file.close()
    
def writeDataToFile(data,filename):
    with open(filename,'w') as write_file:
        write_file.write(data)
        write_file.close()

def getDataFromFile(filename):
    with open(filename,'r') as read_file:
        data = read_file.read()
        read_file.close()
    return data

def main():
    url = "https://www.airlines-inform.ru/commercial-aircraft/"

    soup = getSoup(url)
    article = soup.find('article',class_="text blok-central white")
    a = article.find_all('a')

    planes = dict()
    count = 0

    

    for i in a: 

        count += 1
        # if count == 10:
        #     break

        newUrl = i['href']
        newSoup = getSoup(newUrl)
        if newSoup!=None:
            td_km = newSoup.find('td',text='Дальность полета с макс. загрузкой (км)')
            td_seats = newSoup.find('td', text='Кол-во кресел (эконом)')
            if td_km != None and td_seats != None:
                name = i.text
                km = toValue(td_km.find_next('td').text)
                seats = toValue(td_seats.find_next('td').text)
                if km != None and seats != None:
                    plane = {
                        name : {
                            'km':km,
                            'seats':seats
                        }
                    }
                    planes.update(plane)
                    log('--> Plane #{} is wrote'.format(count),INFO=True)
                else:
                    log('--> Plane #{} isnot wrote'.format(count),ERROR=True)      
            else:
                continue
        else:
            log('--> Plane #{} isnot wrote'.format(count),ERROR=True)     
        
    
    print('DICT PLANES ARE READY')
    with open(JSONFILE, 'w') as file:
        json.dump(planes,file)
        file.close()
    print('FINISH!!!!!!!!!!')
    
if __name__ == "__main__":
    main()