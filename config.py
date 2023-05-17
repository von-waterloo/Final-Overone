key = '5900058312:AAF6-fLpSwJLHrnIJqyt2lrz6ZPmEHtaRzc'

import re
st = ['Розовые фламинго (мини-сериал, 2020)', 'Рука бога (сериал, 2023)', 'Сядь за руль моей машины (сериал)', 'Конь', 'Сериал']
new_st = []
for i in st:
    new_st.append(re.sub(r' \((мини-)*сериал(,)*( )*(\d\d\d\d)*\)','',i))
# print(new_st)

# Список просмотренных мной фильмов, спарсенный с Кинопоиска
# read = open('films.txt', 'r', encoding='UTF-8')
# readlist = read.read().strip('\'').split('\', \'')
# print(readlist)


