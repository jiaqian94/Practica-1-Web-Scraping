from bs4 import BeautifulSoup as bs
import requests
import csv

def clean_info(linea): # limpiar los datos de td
    if linea.find("li"): # si existe elemento list
        return [li.get_text(" ",strip=True).replace("\xa0","") for li in linea.find_all("li")]
    elif linea.find("br"):
        return [text for text in linea.stripped_strings]
    else:
        return linea.get_text(" ",strip=True).replace("\xa0","")

def get_info(url):
    req = requests.get(url)
    soup = bs(req.content, features="html.parser")
    info_box = soup.find(class_="infobox vevent")
    info_lineas = info_box.find_all("tr")

    info_peli = {}
    for index, linea in enumerate(info_lineas):
        if index == 0: # tabla indice 0 es el titulo
            info_peli['title'] = linea.find("th").get_text()
            print("Getting information of movie " + info_peli['title'] + "...")    
        elif index == 1:
            continue # table indice 1 es el imagen
        else:
            clave = linea.find("th").get_text(" ",strip=True) # obtener la clave en la cabecera
            valor = clean_info(linea.find("td"))
            info_peli[clave] = valor
    print("Movie " + info_peli['title'] + " completed")
    return info_peli

def get_movie_links(url):
    movie_links=[]
    wikipedia = "https://en.wikipedia.org"

    req = requests.get(url)
    soup = bs(req.content, features="html.parser")
    table = soup.select(".wikitable.sortable")[1] # de las tres tablas, solo escoger la segunda que es de peliculas
    lineas = table.find_all("i") # todos los links estan cursivas
    
    for linea in lineas:
        movie_links.append(wikipedia + linea.a['href'])
        print("Getting url of movie " + linea.a['title']+"...")
    
    print("Getting urls completed")
    return movie_links

def data2csv(datas):
    csv_columns=['title','Directed by','Produced by',
                'Written by','Starring','Music by',
                'Based on', 'Cinematography','Screenplay by',
                'Edited by','Production company','Production companies',
                'Distributed by','Story by','Narrated by',
                'Release date','Running time','Country',
                'Language','Budget','Box office']
    csv_file = "Tom_Hanks_movies.csv"
    with open(csv_file,'w', encoding='utf-8') as file:
        writer = csv.DictWriter(file,fieldnames=csv_columns)
        writer.writeheader()
        for data in datas:
            writer.writerow(data)

