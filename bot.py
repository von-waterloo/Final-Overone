from config import key
from aiogram import Bot, Dispatcher, executor, types
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium_stealth import stealth
import wikipedia, os, random, asyncio
from Pillow import photo_to_gif_with_duck
wikipedia.set_lang('ru')

result_list = []

# SELENIUM
options = webdriver.ChromeOptions()
# options.add_argument("--headless")
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)
driver = webdriver.Chrome(options=options)

stealth(driver,
        languages=["en-US", "en"],
        vendor="Google Inc.",
        platform="Win32",
        webgl_vendor="Intel Inc.",
        renderer="Intel Iris OpenGL Engine",
        fix_hairline=True,
        )

bot = Bot(key)
dp = Dispatcher(bot)

@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    markup = types.InlineKeyboardMarkup()
    go = types.InlineKeyboardButton(text='Ну давай', callback_data='go')
    markup.add(go)
    await message.answer("Привет! Я помогу шикарно провести время:)", reply_markup=markup)

@dp.callback_query_handler()
async def callback_inline(call: types.CallbackQuery):
    if call.data == 'go':
        markup = types.InlineKeyboardMarkup()
        film_recom = types.InlineKeyboardButton(text='Посоветуй фильм', callback_data='film_recom')
        coctail_recom = types.InlineKeyboardButton(text='Посоветуй коктейль', callback_data='coctail_recom')
        quest_recom = types.InlineKeyboardButton(text='Разомнём мозги', callback_data='quest_recom')
        art_quest = types.InlineKeyboardButton(text='Арт-викторина', callback_data='art_quest')
        duck = types.InlineKeyboardButton(text='Хочу гифку с уточкой!', callback_data='duck')
        markup.add(film_recom)
        markup.add(coctail_recom)
        markup.add(art_quest)
        markup.add(quest_recom, duck)
        await call.message.answer('Чего изволишь?', reply_markup=markup)

    #УТОЧКА:)
    elif call.data == 'duck':
        await bot.send_message(call.message.chat.id, '<b>Скинь картинку</b>', parse_mode='HTML')
        @dp.message_handler(content_types=['photo'])
        async def get_photo(message: types.Message):
            await message.photo[-1].download(destination_file=('E:\OVERONE\Final project\photos\gettedimg.jpg'))
            photo_to_gif_with_duck('E:\OVERONE\Final project\photos\gettedimg.jpg')
            await bot.send_video(message.chat.id, open('gif/duck.gif', 'rb'),5)

    # ВОПРОС ИЗ БАЗЫ "ЧТО? ГДЕ? КОГДА?"
    elif call.data == 'quest_recom':
        driver.get(f'http://db.chgk.net/random/answers/types1/{random.choice(range(1, 842662771))}')
        rand_quest = driver.find_element(By.CLASS_NAME, 'random_question').text.split("Ответ:")[0].split("Вопрос 1:")[1].strip(' \n')
        try:
            try:
                right_answer = driver.find_element(By.CLASS_NAME, 'random_question').text.split("Вопрос 2")[0].split("Ответ:")[1].split(
                'Источник(и):')[0].strip(' ')
            except:
                right_answer = driver.find_element(By.CLASS_NAME, 'random_question').text.split("Вопрос 2")[0].split("Ответ:")[
                    1].split(
                    'Источник:')[0].strip(' ')
        except:
            try: right_answer = driver.find_element(By.CLASS_NAME, 'random_question').text.split("Вопрос 2")[0].split("Ответ:")[1].split(
                'Автор(ы):')[0].strip(' ')
            except: right_answer = driver.find_element(By.CLASS_NAME, 'random_question').text.split("Вопрос 2")[0].split("Ответ:")[1].split(
                'Автор:')[0].strip(' ')
        await bot.send_message(call.message.chat.id, f'{rand_quest}')
        await bot.send_message(call.message.chat.id, f'<b>Правильный ответ</b>:\n<tg-spoiler><em>{right_answer}</em></tg-spoiler>', parse_mode='HTML')

    #АРТ-ВИКТОРИНА
    elif call.data == 'art_quest':
        while True:
            artist_list = [i for i in os.listdir('E:/Art')]
            global artist1
            artist1 = artist_list.pop(random.choice(range(0, len(artist_list))))
            global artist2
            artist2 = artist_list.pop(random.choice(range(0, len(artist_list))))
            global artist3
            artist3 = artist_list.pop(random.choice(range(0, len(artist_list))))
            global artist4
            artist4 = artist_list.pop(random.choice(range(0, len(artist_list))))
            artwork_list = [i for i in os.listdir(f'E:/Art/{artist1}')]
            artwork = artwork_list.pop(random.choice(range(0, len(artwork_list))))
            if os.path.getsize(f'E:/Art/{artist1}/{artwork}') > 10485760:
                continue
            else:
                global image
                image = open(f'E:/Art/{artist1}/{artwork}', 'rb')
                break
        mkp = types.InlineKeyboardMarkup(row_width=2)
        butt1 = types.InlineKeyboardButton(text= f'{artist1}', callback_data='artist1')
        butt2 = types.InlineKeyboardButton(text= f'{artist2}', callback_data='artist2')
        butt3 = types.InlineKeyboardButton(text= f'{artist3}', callback_data='artist3')
        butt4 = types.InlineKeyboardButton(text= f'{artist4}', callback_data='artist4')
        butt_set = set()
        butt_set.add(butt1), butt_set.add(butt2), butt_set.add(butt3), butt_set.add(butt4)
        butt_list = list(butt_set)
        mkp.add(butt_list[0],butt_list[1], butt_list[2], butt_list[3])
        await bot.send_photo(call.message.chat.id, image, 'Кто автор этой картины?', reply_markup=mkp)
        image.close()
    if call.data == 'artist1':
        markup = types.InlineKeyboardMarkup()
        go = types.InlineKeyboardButton(text='🔙', callback_data='go')
        more = types.InlineKeyboardButton(text='Ещё!', callback_data='art_quest')
        markup.add(go, more)
        await bot.send_message(call.message.chat.id, 'Бинго!')
        await bot.send_message(call.message.chat.id, '🥰', reply_markup=markup)
    elif call.data == 'artist2' or call.data == 'artist3' or call.data == 'artist4':
        markup = types.InlineKeyboardMarkup()
        go = types.InlineKeyboardButton(text='🔙', callback_data='go')
        more = types.InlineKeyboardButton(text='Ещё!', callback_data='art_quest')
        markup.add(go, more)
        await bot.send_message(call.message.chat.id,f'Нет, на самом деле это {artist1}')
        await bot.send_sticker(call.message.chat.id, open('AnimatedSticker.tgs', 'rb'))
        await asyncio.sleep(1)
        await bot.send_message(call.message.chat.id, 'Что дальше?', reply_markup=markup)

    #РЕКОММЕНДЦИЯ ХОРОШЕГО ФИЛЬМА, КОТОРЫЙ НЕ СМОТРЕЛ
    elif call.data == 'film_recom':
        # point = ''
        # for i in range(24):
        #     await asyncio.sleep(0)
        #     await call.message.edit_text(text=f"Загрузка: {point}")
        #     point += '🥰'
        #     await asyncio.sleep(0.3)
        #     if point == '🥰🥰🥰🥰':
        #         point = ''

        if len(result_list) == 0:

            #парсим просмотренные за последний год фильмы с моей странички кинопоиска
            driver.get('https://www.kinopoisk.ru/user/4759790/votes/list/year_from/2021/year_to/2023/vs/novote/#list')
            elements = driver.find_elements(By.CLASS_NAME, 'nameRus')
            kinopoisk_list = []
            for i in elements:
                if 'сериал' not in i.text:
                    kinopoisk_list.append(i.text[0:-7].replace('\xa0',' '))
            print(kinopoisk_list)

            #парсим 50 лучших за последний год фильмов с сайта Критиканство
            best_films = []
            for i in range(0, 50, 10):
                driver.get(f'https://kritikanstvo.ru/top/movies/best/2022/start/{i}/')
                elements = driver.find_elements(By.TAG_NAME, 'h2')
                for j in elements:
                    best_films.append(j.text)
            print(best_films)
            #убираем из этого списка просмотренные фильмы
            for i in best_films:
                if i not in kinopoisk_list:
                    result_list.append(i)
            try:
                while True:
                    result_list.remove('')
            except ValueError:
                pass
        # print(result_list)
        random_film = result_list.pop(random.choice(range(0,len(result_list))))
        search_film = f'{random_film}, фильм'
        film_text = wikipedia.summary(wikipedia.search(search_film)[0], sentences=5)
        try:
            driver.get(wikipedia.page(wikipedia.search(search_film)[0]).url)
            driver.find_element(By.CLASS_NAME, 'infobox-image').click()
            driver.implicitly_wait(2)
            driver.find_element(By.CLASS_NAME, 'mw-mmv-stripe-button-container').find_element(By.TAG_NAME, 'a').click()
            img_link = driver.find_element(By.CLASS_NAME, 'fullMedia').find_element(By.TAG_NAME, 'a').get_attribute('href')
            await bot.send_photo(call.message.chat.id, img_link, f'{film_text}')
        except:
            await bot.send_message(call.message.chat.id,f'{film_text}')

    #БАР-БОТ (НА СТАДИИ РАЗРАБОТКИ)
    elif call.data == 'coctail_recom':
        await bot.send_animation(call.message.chat.id, open('Clockwork_intro.mp4', 'rb'), 10)
        await bot.send_message(call.message.chat.id, 'Сейчас мы что-нибудь тебе подберём')
        boss = types.InlineKeyboardButton('Босс - скотина', callback_data= 'boss')
        girl = types.InlineKeyboardButton('Бросила девушка', callback_data= 'girl')
        buttons = [boss, girl]
        mkp = types.InlineKeyboardMarkup(2, [buttons])
        await bot.send_message(call.message.chat.id, 'Укажи ориентир', reply_markup= mkp)



executor.start_polling(dispatcher= dp, skip_updates=True)
