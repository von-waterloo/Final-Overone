from config import key
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium_stealth import stealth
import wikipedia, os, re, sqlite3, random, asyncio
from Pillow import photo_to_gif_with_duck
from threading import Thread
wikipedia.set_lang('ru')

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

def markups(**kwargs):
    buttons_l = []
    for key, value in kwargs.items():
        buttons_l.append(InlineKeyboardButton(value, callback_data=key))
    buttons= []
    count = 0
    for i in buttons_l:
        if count == len(buttons_l):
            break
        if count+1 == len(buttons_l):
            buttons.append([buttons_l[count]])
            break
        buttons.append([buttons_l[count],buttons_l[count+1]])
        count +=2
    return InlineKeyboardMarkup(inline_keyboard=buttons)

quest_info = {}
userid_films = {}
@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    global quest_info, user_id, userid_films
    user_id = message.from_user.id
    quest_info[user_id] = 1
    userid_films[user_id] = []
    markup = types.InlineKeyboardMarkup()
    go = types.InlineKeyboardButton(text='Ну давай 😃', callback_data='go')
    markup.add(go)
    await message.answer("Привет! Я помогу шикарно провести время:)", reply_markup=markup)
    # await bot.send_message(chat_id=message.chat.id, text='╱▔▔▔▔▔▔▔╲╱▔▔▔▔▔╲')
    #
    # loading = ['╱▔▔▔▔▔▔▔╲╱▔▔▔▔▔╲', '▏╮╭┈┈╮╭┈╮▏╭╮┈╭╮▕', '▏┊╱▔▉┊╱▔▉▏▊┃▕▋┃▕', '▏╯╲▂╱┊╲▂╱▏▔▅┈▔▔▕', '╲╭┳┳╮▕▋╭╱╲┳┳┳┫▂╱',
    #            '┈▔▏┣┳┳┳┳▏▕┻┻┻╯▏┈', '┈┈▏╰┻┻┻┻▏▕▂▂▂╱┈┈', '┈┈╲▂▂▂▂▂▏┈┈┈┈┈┈┈', '']
    # count = 1
    # new_text = loading[0] + '\n' + loading[1]
    # for i in range(23):
    #     await asyncio.sleep(0.15)
    #     await bot.edit_message_text(chat_id=message.chat.id, text=new_text, message_id=message.message_id+1)
    #     count += 1
    #     new_text += '\n' + loading[count]
    #     if count == 8:
    #         count = 0
    #         new_text = loading[0]

@dp.callback_query_handler()
async def callback_inline(call: types.CallbackQuery):

    if call.data == 'go':
        markup = types.InlineKeyboardMarkup()
        film_recom = types.InlineKeyboardButton(text='Посоветуй фильм 📺', callback_data='film_recom')
        coctail_recom = types.InlineKeyboardButton(text='Бар-бот 🍸', callback_data='coctail_recom')
        quest_recom = types.InlineKeyboardButton(text='Разомнём мозги 💡', callback_data='quest_recom')
        art_quest = types.InlineKeyboardButton(text='Арт-викторина 🎨', callback_data='art_quest')
        duck = types.InlineKeyboardButton(text='Хочу гифку с уточкой! 🦆', callback_data='duck')
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
        if quest_info[user_id] == 1:
            await bot.send_message(call.message.chat.id, '<em>У тебя 10 секунд на чтение вопроса и минута на размышления.\nЧерез 10 секунд после появления вопроса запустится таймер</em>', parse_mode='HTML')
            quest_info[user_id] = 0
        driver.get(f'http://db.chgk.net/random/answers/types1/{random.choice(range(1, 842662771))}')
        rand_quest = driver.find_element(By.CLASS_NAME, 'random_question').text.split("Ответ:")[0].split("Вопрос 1:")[1].strip(' \n')

        right_answer = driver.find_element(By.CLASS_NAME, 'random_question').text.split("Вопрос 2")[0].split("Ответ:")[1].split(
            'Источник(и):')[0].strip(' ')
        right_answer2 = right_answer.split('Источник:')[0].strip(' ')
        right_answer3 = right_answer2.split('Автор(ы):')[0].strip(' ')
        right_answer4 = right_answer3.split('Автор:')[0].strip(' ')
        await bot.send_message(call.message.chat.id, f'{rand_quest}')
        await asyncio.sleep(10)
        await bot.send_message(call.message.chat.id, f'<b>Правильный ответ</b>:\n<tg-spoiler>{right_answer4}</tg-spoiler>', parse_mode='HTML')
        await asyncio.sleep(1)
        global marka
        marka = types.InlineKeyboardMarkup()
        go = types.InlineKeyboardButton(text='🔙', callback_data='go')
        more = types.InlineKeyboardButton(text='Ещё!', callback_data='quest_recom')
        marka.add(go, more)
        timer = await bot.send_message(call.message.chat.id, '‼️ У тебя 60 секунд ‼️', reply_markup=marka)
        time_list = ['🔟', '9️⃣', '🎱', '7️⃣', '6️⃣', '🤚', '4️⃣', '3️⃣', '✌️', '1️⃣']
        seconds = 60
        count = 0
        while True:
            await asyncio.sleep(1)
            seconds -= 1
            if seconds <=10:
                if seconds == 0:
                    await bot.edit_message_text(f'<b>Правильный ответ</b>:\n{right_answer4}', call.message.chat.id, message_id=timer.message_id -1, parse_mode='HTML')
                    await bot.edit_message_text('☠️☠️☠️ ВРЕМЯ ВЫШЛО ☠️☠️☠️', call.message.chat.id,
                                                message_id=timer.message_id, reply_markup=marka)
                    break
                else:
                    await bot.edit_message_text(f'‼️ У тебя {time_list[count]} секунд ‼️', call.message.chat.id,
                                                message_id=timer.message_id, reply_markup=marka)
                count +=1
            else:
                await bot.edit_message_text(f'‼️ У тебя {seconds} секунд ‼️', call.message.chat.id, message_id=timer.message_id, reply_markup=marka)


    #АРТ-ВИКТОРИНА
    elif call.data == 'art_quest':
        while True:
            artist_list = [i for i in os.listdir('E:/Art')]
            global artist1
            artist1 = artist_list.pop(random.choice(range(0, len(artist_list))))
            artist2 = artist_list.pop(random.choice(range(0, len(artist_list))))
            artist3 = artist_list.pop(random.choice(range(0, len(artist_list))))
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
        await asyncio.sleep(1)
        await bot.send_message(call.message.chat.id, 'Бинго!')
        await asyncio.sleep(1)
        await bot.send_message(call.message.chat.id, '🥰', reply_markup=markup)
    elif call.data == 'artist2' or call.data == 'artist3' or call.data == 'artist4':
        markup = types.InlineKeyboardMarkup()
        go = types.InlineKeyboardButton(text='🔙', callback_data='go')
        more = types.InlineKeyboardButton(text='Ещё!', callback_data='art_quest')
        markup.add(go, more)
        try:
            global scream_id
            scream = await bot.copy_message(call.message.chat.id, from_chat_id=call.message.chat.id, message_id=scream_id)
            scream_id = scream.message_id
        except:
            scream = await bot.send_sticker(call.message.chat.id, open('Scream.tgs', 'rb'))
            scream_id = scream.message_id
        await asyncio.sleep(1)
        await bot.send_message(call.message.chat.id,f'Нет, на самом деле это {artist1}')
        await asyncio.sleep(1)
        await bot.send_message(call.message.chat.id, 'Что дальше?', reply_markup=markup)

    #РЕКОММЕНДЦИЯ ХОРОШЕГО ФИЛЬМА, КОТОРЫЙ НЕ СМОТРЕЛ
    elif call.data == 'film_recom':
        async def loading():
            coffe = ['♥', '♪)', '(♫', '❤️ )']
            coffe_mes = await bot.send_message(call.message.chat.id, '██Ɔ')
            coffe_id = coffe_mes.message_id
            anime = '██Ɔ'
            for i in range(16):
                await asyncio.sleep(0.4)
                anime = coffe.pop() + '\n' + anime
                await bot.edit_message_text(anime, call.message.chat.id, coffe_id)
                if i == 15:
                    break
                elif len(coffe) == 0:
                    await asyncio.sleep(0.4)
                    anime = '██Ɔ'
                    await bot.edit_message_text(anime, call.message.chat.id, coffe_id)
                    coffe = ['♥', '♪)', '(♫', '❤️ )']

        if len(userid_films[user_id]) == 0:
            #     #парсим просмотренные за последний год фильмы с моей странички Кинопоиска
            #     driver.get('https://www.kinopoisk.ru/user/4759790/votes/list/year_from/2022/year_to/2023/vs/novote/#list')
            #     elements = driver.find_elements(By.CLASS_NAME, 'nameRus')
            #     kinopoisk_list = []
            #     for i in elements:
            #         if 'сериал' not in i.text:
            #             kinopoisk_list.append(i.text[0:-7].replace('\xa0',' '))

            #парсим 50 лучших за последний год фильмов с сайта Критиканство
            best_films = []
            for i in range(0, 50, 10):
                driver.get(f'https://kritikanstvo.ru/top/movies/best/2022/start/{i}/')
                elements = driver.find_elements(By.TAG_NAME, 'h2')
                for j in elements:
                    best_films.append(j.text)
            # убираем из этого списка просмотренные фильмы
            base_list = []
            try:
                with sqlite3.connect('films_base.db') as con:
                    cur = con.cursor()
                    table_name = f'films{user_id}'
                    cur.execute(f"""SELECT films_list FROM {table_name}""")
                    con.commit()
                    result = cur.fetchall()
                    for i in result:
                        base_list.append(i[0])
            except:
                pass

            for i in best_films:
                if i not in base_list:
                    userid_films[user_id].append(i)
            try:
                while True:
                    userid_films[user_id].remove('')
            except ValueError:
                pass
        global random_film
        print(userid_films[user_id])
        random_film = userid_films[user_id].pop(random.choice(range(0,len(userid_films[user_id]))))
        driver.get('https://kritikanstvo.ru/top/movies/best/2023/')
        driver.find_element(By.NAME, 's').send_keys(random_film)
        driver.find_element(By.NAME, 's').submit()
        driver.find_element(By.CLASS_NAME, 'cover').click()
        photo_url = driver.find_elements(By.CLASS_NAME, 'gallery_common')[-1].get_attribute('href')
        cast = driver.find_element(By.CLASS_NAME, 'page_item_info').find_element(By.TAG_NAME, 'dl').text
        year_search_list = driver.find_element(By.CLASS_NAME, 'page_item_info').find_elements(By.TAG_NAME, 'p')
        year = min([re.search(r'\d{4}', i.text)[0] for i in year_search_list])
        try:
            global story
            story = driver.find_element(By.CLASS_NAME, 'page_item_story').text
        except:
            story = 0
        reply_markup = markups(trailer='Смотреть трейлер 🎞',)
        driver.get('http://hdrezka.co/')
        driver.find_element(By.CLASS_NAME, 'b-search__field').send_keys(f'{random_film} {year}')
        driver.find_element(By.CLASS_NAME, 'b-search__field').submit()
        driver.find_element(By.CLASS_NAME, 'b-content__inline_item-cover').click()
        film_page = driver.current_url
        reply_markup.add(InlineKeyboardButton('Смотреть фильм 📽', film_page))
        reply_markup.add(InlineKeyboardButton('Уже смотрел', callback_data='already'), InlineKeyboardButton('Давай ещё', callback_data='film_recom'))
        story2 = driver.find_element(By.CLASS_NAME, 'b-post__description_text').text
        if story == 0:
            await bot.send_photo(call.message.chat.id, photo_url, f'{random_film.upper()} ({year})\n\n{story2}', reply_markup=reply_markup)
        else:
            await bot.send_photo(call.message.chat.id, photo_url, f'{random_film.upper()} ({year})\n\n{story}',
                                 reply_markup=reply_markup)
    if call.data == 'trailer':
        driver.find_element(By.CLASS_NAME, "b-sidelinks__text").click()
        driver.implicitly_wait(2)
        trailer = driver.find_element(By.XPATH, '//*[@id="ps-trailer-player"]/iframe').get_attribute('src').split('?iv_load_policy')[0].replace('youtube', 'ssyoutube')
        driver.get(trailer)
        driver.implicitly_wait(6.5)
        trailer2 = driver.find_element(By.XPATH, '//*[@id="sf_result"]/div/div[1]/div[2]/div[2]/div[1]/a').get_attribute('href')
        # driver.find_element(By.ID, 'ps-close').click()
        # await bot.send_message(call.message.chat.id, trailer)
        await bot.send_video(call.message.chat.id, trailer2)
    elif call.data == 'already':
        with sqlite3.connect('films_base.db') as con:
            cur = con.cursor()
            table_name = f'films{user_id}'
            cur.execute(f"""CREATE TABLE IF NOT EXISTS {table_name} (
            films_list TEXT)""")
            cur.execute(f"""INSERT INTO {table_name}(films_list) VALUES ('{random_film}')""")
        await call.answer('Фильм добавлен в базу данных и больше не будет рекомендоваться')



    #БАР-БОТ (НА СТАДИИ РАЗРАБОТКИ)
    elif call.data == 'coctail_recom':
        try:
            global orange_id
            orange = await bot.copy_message(call.message.chat.id, from_chat_id = call.message.chat.id, message_id = orange_id)
            await bot.delete_message(call.message.chat.id, message_id = orange_id)
            orange_id = orange.message_id
        except:
            orange = await bot.send_animation(call.message.chat.id, open('bar/Clockwork_intro.mp4', 'rb'))
            orange_id = orange.message_id
        await asyncio.sleep(4)
        await bot.send_message(call.message.chat.id, '🌀Добро пожаловать в бар-консультант🌀')
        await asyncio.sleep(2)
        await bot.send_message(call.message.chat.id, '🌀Сейчас мы что-нибудь тебе подберём🌀')
        await asyncio.sleep(2)
        await bot.send_photo(call.message.chat.id, open('bar/octopus.jpg', 'rb'), '         Укажи ориентир, мудачина поганая:', reply_markup= markups(
                                                                        classic = 'По классике',
                                                                        sweat='Для девочек',
                                                                        dead = 'Убей меня',
                                                                        boss='Босс — пидорас',
                                                                        girl='Бросила девушка',
                                                                        hot='Пощекочем сосочки',
                                                                        rand = 'Рандом',
                                                                        zoz = 'ЗОЖ'
                                                                        ))
    elif call.data == 'zoz':
        await bot.send_message(call.message.chat.id, 'Пошёл нахуй')

executor.start_polling(dispatcher= dp, skip_updates=True)
