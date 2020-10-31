import methods as mt

url = "https://en.wikipedia.org/wiki/List_of_Tom_Hanks_performances"

links = mt.get_movie_links(url)
movie_info=[]
for link in links:
    movie_info.append(mt.get_info(link))
    
mt.data2csv(movie_info)