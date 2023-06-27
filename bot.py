from config import key
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os, re, sqlite3, random, asyncio
from Pillow import photo_to_gif_with_duck

# SELENIUM
options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")
# options.add_argument("--headless")
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)

bot = Bot(key)
dp = Dispatcher(bot)


def markups(**kwargs):
    buttons_l = []
    for key, value in kwargs.items():
        buttons_l.append(InlineKeyboardButton(value, callback_data=key))
    buttons = []
    count = 0
    for i in buttons_l:
        if count == len(buttons_l):
            break
        if count + 1 == len(buttons_l):
            buttons.append([buttons_l[count]])
            break
        buttons.append([buttons_l[count], buttons_l[count + 1]])
        count += 2
    return InlineKeyboardMarkup(inline_keyboard=buttons)


alk = ['🍹', '🍸', '🥃', '🍷']
bar_dict = { 'home': 'Домашний слинг', 'bianko': 'Бьянко бриз', 'rhino': 'Розовый носорог', 'smash': 'Текила смэш', 'negr': 'Негрони', 'daiq': 'Дайкири', 'long': 'Лонг айленд айс ти', 'cosmo': 'Космополитен',
            'sky': 'Небеса',
            'snake': 'Гремучая змея', 'marg': 'Маргарита', 'sex': 'Секс на пляже', 'lagoon': 'Голубая лагуна',
            'b52': 'Б-52', 'maj': 'Май тай',
            'green': 'Зеленая фея', 'manh': 'Манхэттен', 'ws': 'Виски сауэр', 'hiro': 'Хиросима',
            'espresso': 'Эспрессо мартини', 'paloma': 'Палома', 'obl': 'Облака', 'ledi': 'Белая леди',
            'bum': 'Текила бум', 'spritz': 'Апероль Шприц', 'mimoza': 'Мимоза', 'sosok': 'Скользкий сосок',
            'blur': 'Облако дыма', 'kiss': 'Поцелуй дьявола', 'blackrus': 'Черный русский', 'martin': 'Водка мартини',
            'vodkared': 'Водка энергетик', 'moh': 'Мохито', 'rose': 'Розовый сад', 'basil': 'Базиликовый удар',
            'french': 'Френч 75', 'breeze': 'Летний бриз', 'cocumber': 'Джин тоник с огурцом', 'juce': 'Отвертка',
            'orgasm': 'Модный оргазм', 'sunrise': 'Текила санрайз', 'bell': 'Беллини', 'shmel': 'Шмель',
            'gott': 'Карел Готт', 'tonic': 'Джин тоник', 'whiskey': 'Виски кола', 'sling': 'Сингапурский слинг',
            'pina': 'Пина колада', 'tom': 'Том и Джерри', 'brendi': 'Бренди и кола', 'amigo': 'Амиго', 'fors': 'Форсаж',
            'lolita': 'Лолита', 'vegan': 'Демон-веган',
            'cherry': 'Зимняя вишня', 'flam': 'Роял фламбе', 'barbi': 'Барби', 'baunty': 'Баунти мартини',
            'porn': 'Порнозвезда', 'dno': 'Золотое дно', 'shashki': 'Алко-шашки', 'bojar': 'Боярский',
            'bojar2': 'Дочь Боярского', 'blood': 'Кровавая Мэри', 'reddog': 'Красный пес', 'dog': 'Собака.ру',
            'reanimator': 'Реаниматор', 'controlshot': 'Контрольный выстрел', 'oyster': 'Устричный шутер',
            'devil': 'Тессманский дьявол', 'aurora': 'Северное сияние', 'belrus': 'Белый русский'}


async def coc(name, call):
    user_id = call.from_user.id
    ranalk = random.choice(alk)
    if name == 'Манхэттен':
        await bot.send_photo(call.message.chat.id, open('bar/godzilla.jpg', 'rb'))
        await asyncio.sleep(1)
    elif name == 'Белый русский':
        await bot.send_photo(call.message.chat.id, open('bar/lebo.jpg', 'rb'))
        await asyncio.sleep(1.5)
        await bot.send_message(call.message.chat.id, random.choice(
            ['"Только вдруг появляется какая-то мразь и ссыт на твой ковер."', '"Где деньги, Лебовски?"',
             '"Я тебя люблю, Уолтер, но рано или поздно ты должен признать, что ты — дебил."',
             '"Слышь, Чувак! А где твоя тачка?"', '"Ковёр задавал стиль всей комнате."',
             '"Смоки, тут не Вьетнам. Это — боулинг. Здесь есть правила."',
             '"Бывает, ты ешь медведя, а бывает, медведь тебя."',
             '"Великолепный план, Уолтер. Просто охуенный, если я правильно понял. Надёжный, блядь, как швейцарские часы."']))
        await asyncio.sleep(1.5)
    rec_name = await bot.send_message(call.message.chat.id, f'<b>{name.upper()}</b> (<em>Загрузка</em>)',
                                      parse_mode='HTML')
    try:
        driver = drivers_dict[user_id]
        driver.refresh()
    except:
        drivers_dict[user_id] = webdriver.Chrome(options=options)
        driver = drivers_dict[user_id]
    await bot.edit_message_text(f'<b>{name.upper()}</b> (<em>Загрузка: </em>{ranalk})', call.message.chat.id,
                                rec_name.message_id, parse_mode='HTML')
    driver.get(f'https://ru.inshaker.com/cocktails')
    await bot.edit_message_text(f'<b>{name.upper()}</b> (<em>Загрузка: </em>{ranalk * 2})', call.message.chat.id,
                                rec_name.message_id, parse_mode='HTML')
    driver.find_element(By.CLASS_NAME, 'search-input').send_keys(name)
    await asyncio.sleep(1.2)
    driver.find_element(By.CLASS_NAME, 'search-input').submit()
    await asyncio.sleep(1)
    elem = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.LINK_TEXT, name)))
    icons_list = []

    icons = driver.find_element(By.CLASS_NAME, 'cocktail-item-goods').find_elements(By.TAG_NAME, 'img')
    for i in icons:
        icons_list.append(i.get_attribute('src'))
        if len(icons_list) == 10:
            break
    driver.get(elem.get_attribute('href'))
    await bot.edit_message_text(f'<b>{name.upper()}</b> (<em>Загрузка: </em>{ranalk * 3})', call.message.chat.id,
                                rec_name.message_id, parse_mode='HTML')
    rec_list = driver.find_element(By.CLASS_NAME, 'steps').find_elements(By.TAG_NAME, 'li')
    img = driver.find_element(By.CLASS_NAME, 'image').get_attribute('src')
    await asyncio.sleep(1)
    await bot.edit_message_text(f'<b>{name.upper()}</b>', call.message.chat.id, rec_name.message_id, parse_mode='HTML')
    ing_list = [i.text.replace('\n', ' ') for i in
                driver.find_element(By.TAG_NAME, 'table').find_elements(By.TAG_NAME, 'tr')][1:]
    ing_list = str(ing_list).strip('[]').replace("'", "")
    await bot.send_message(call.message.chat.id, f'Необходимые ингредиенты: {ing_list}')
    media = types.MediaGroup()
    for i in icons_list:
        media.attach_photo(types.InputMediaPhoto(i))
    await asyncio.sleep(1)
    await bot.send_media_group(call.message.chat.id, media)
    await asyncio.sleep(1)
    for i in rec_list:
        await bot.send_message(call.message.chat.id, f'⚜️ {i.text}')
        await asyncio.sleep(1)
    await bot.send_photo(call.message.chat.id, img, f'"Опля"! —  <b>"{name}</b>"', reply_markup=markups(bar='🔙'),
                         parse_mode='HTML')
    try:
        warning[user_id] += 1
    except:
        warning[user_id] = 1

    async def danger(n):
        await asyncio.sleep(2)
        await bot.send_message(call.message.chat.id, '☠️')
        await asyncio.sleep(2)
        await bot.send_message(call.message.chat.id, f'Это твой {n}-й коктейль!')
        await asyncio.sleep(1)
        await bot.send_message(call.message.chat.id, 'Чрезмерное употребление ведёт к...')
        await asyncio.sleep(1)
        await bot.send_photo(call.message.chat.id, open('bar/warning.jpg', 'rb'))
        await asyncio.sleep(1)
        await bot.send_message(call.message.chat.id, '...такому состоянию')
        await asyncio.sleep(2)
        await bot.send_message(call.message.chat.id, 'Уверен, что хочешь продолжить?',
                               reply_markup=markups(bar='Продолжим 😈', go2='Хватит 😇'))

    if warning[user_id] % 5 == 0:
        await danger(warning[user_id])

quest_info = {}
userid_films = {}
drivers_dict = {}
random_film_byid = {}
warning = {}
result = {}
rand_coc = {}
@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    user_id = message.from_user.id
    markup = types.InlineKeyboardMarkup()
    go = types.InlineKeyboardButton(text='Ну давай 😃', callback_data='go')
    markup.add(go)
    skull = await bot.send_message(chat_id=message.chat.id, text='╱▔▔▔▔▔▔▔╲╱▔▔▔▔▔╲')

    loading = ['╱▔▔▔▔▔▔▔╲╱▔▔▔▔▔╲', '▏╮╭┈┈╮╭┈╮▏╭╮┈╭╮▕', '▏┊╱▔▉┊╱▔▉▏▊┃▕▋┃▕', '▏╯╲▂╱┊╲▂╱▏▔▅┈▔▔▕', '╲╭┳┳╮▕▋╭╱╲┳┳┳┫▂╱',
               '┈▔▏┣┳┳┳┳▏▕┻┻┻╯▏┈', '┈┈▏╰┻┻┻┻▏▕▂▂▂╱┈┈', '┈┈╲▂▂▂▂▂▏┈┈┈┈┈┈┈', '']
    count = 1
    new_text = loading[0] + '\n' + loading[1]
    for i in range(23):
        await asyncio.sleep(0.15)
        await bot.edit_message_text(chat_id=message.chat.id, text=new_text, message_id=skull.message_id)
        if i == 22:
            await asyncio.sleep(0.2)
            await bot.edit_message_text(reply_markup=markup, chat_id=message.chat.id,
                                        text=new_text + '\n' + 'Салют! Повеселимся?', message_id=skull.message_id)
        count += 1
        new_text += '\n' + loading[count]
        if count == 8:
            count = 0
            new_text = loading[0]


@dp.callback_query_handler()
async def callback_inline(call: types.CallbackQuery):
    if call.data == 'go':
        markup = types.InlineKeyboardMarkup()
        film_recom = types.InlineKeyboardButton(text='Посоветуй фильм 📺', callback_data='film_recom')
        coctail_recom = types.InlineKeyboardButton(text='Бар-бот 🍸', callback_data='bar')
        quest_recom = types.InlineKeyboardButton(text='Разомнём мозги 💡', callback_data='quest_recom')
        art_quest = types.InlineKeyboardButton(text='Арт-викторина 🎨', callback_data='art_quest')
        duck = types.InlineKeyboardButton(text='Хочу гифку с уточкой! 🦆', callback_data='duck')
        but_list = [duck, art_quest, quest_recom, coctail_recom, film_recom]
        await asyncio.sleep(0.5)
        mes = await call.message.answer('Чего изволишь?', reply_markup=markup)
        for i in range(5):
            await asyncio.sleep(0.5)
            markup.add(but_list.pop())
            await bot.edit_message_reply_markup(call.message.chat.id, mes.message_id, reply_markup=markup)

    elif call.data == 'go2':
        markup = types.InlineKeyboardMarkup()
        film_recom = types.InlineKeyboardButton(text='Посоветуй фильм 📺', callback_data='film_recom')
        quest_recom = types.InlineKeyboardButton(text='Разомнём мозги 💡', callback_data='quest_recom')
        art_quest = types.InlineKeyboardButton(text='Арт-викторина 🎨', callback_data='art_quest')
        duck = types.InlineKeyboardButton(text='Хочу гифку с уточкой! 🦆', callback_data='duck')
        but_list = [duck, art_quest, quest_recom, film_recom]
        await asyncio.sleep(0.5)
        mes = await call.message.answer('Чего изволишь?', reply_markup=markup)
        for i in range(4):
            await asyncio.sleep(0.5)
            markup.add(but_list.pop())
            await bot.edit_message_reply_markup(call.message.chat.id, mes.message_id, reply_markup=markup)

    # УТОЧКА:)
    elif call.data == 'duck':
        await bot.send_message(call.message.chat.id, 'Скинь мне картинку, я сделаю из неё гифку')

        @dp.message_handler(content_types=['photo'])
        async def get_photo(message: types.Message):
            await message.photo[-1].download(destination_file=('E:\OVERONE\Final project\photos\gettedimg.jpg'))
            async def load():
                coffe = ['♥', '♪)', '(♫', '❤️ )']
                coffe_mes = await bot.send_message(call.message.chat.id, '██Ɔ')
                coffe_id = coffe_mes.message_id
                anime = '██Ɔ'
                for i in range(12):
                    await asyncio.sleep(0.18)
                    anime = coffe.pop() + '\n' + anime
                    await bot.edit_message_text(anime, call.message.chat.id, coffe_id)
                    if i == 11:
                        break
                    elif len(coffe) == 0:
                        await asyncio.sleep(0.18)
                        anime = '██Ɔ'
                        await bot.edit_message_text(anime, call.message.chat.id, coffe_id)
                        coffe = ['♥', '♪)', '(♫', '❤️ )']
            await asyncio.gather(load(),photo_to_gif_with_duck('E:\OVERONE\Final project\photos\gettedimg.jpg'))
            gifka = await bot.send_document(message.chat.id, open('gif/duck.gif', 'rb'), disable_content_type_detection=True)
            await bot.delete_message(message.chat.id, gifka.message_id-1)
            await bot.delete_message(message.chat.id, gifka.message_id-2)
            await bot.delete_message(message.chat.id, gifka.message_id-3)

    # ВОПРОС ИЗ БАЗЫ "ЧТО? ГДЕ? КОГДА?"
    elif call.data == 'quest_recom':
        user_id = call.from_user.id
        try:
            driver = drivers_dict[user_id]
            driver.refresh()
            try:
                if quest_info[user_id] == 0:
                    pass
            except:
                quest_info[user_id] = 1
        except:
            drivers_dict[user_id] = webdriver.Chrome(options=options)
            driver = drivers_dict[user_id]
            quest_info[user_id] = 1
        if quest_info[user_id] == 1:
            await bot.send_message(call.message.chat.id,
                                   '<em>У тебя 10 секунд на чтение вопроса и минута на размышления.\nЧерез 10 секунд после появления вопроса запустится таймер</em>',
                                   parse_mode='HTML')
            quest_info[user_id] = 0
        driver.get(f'http://db.chgk.net/random/answers/types1/{random.choice(range(1, 842662771))}')
        rand_quest = driver.find_element(By.CLASS_NAME, 'random_question').text.split("Ответ:")[0].split("Вопрос 1:")[
            1].strip(' \n')

        right_answer = \
        driver.find_element(By.CLASS_NAME, 'random_question').text.split("Вопрос 2")[0].split("Ответ:")[1].split(
            'Источник(и):')[0].strip(' ')
        right_answer2 = right_answer.split('Источник:')[0].strip(' ')
        right_answer3 = right_answer2.split('Автор(ы):')[0].strip(' ')
        right_answer4 = right_answer3.split('Автор:')[0].strip(' ')
        await bot.send_message(call.message.chat.id, f'{rand_quest}')
        await asyncio.sleep(10)
        answer = await bot.send_message(call.message.chat.id,
                                        f'<b>Правильный ответ</b>:\n<tg-spoiler>{right_answer4}</tg-spoiler>',
                                        parse_mode='HTML')
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
            if seconds <= 10:
                if seconds == 0:
                    await bot.edit_message_text(f'<b>Правильный ответ</b>:\n{right_answer4}', call.message.chat.id,
                                                message_id=answer.message_id, parse_mode='HTML')
                    await bot.edit_message_text('☠️☠️☠️ ВРЕМЯ ВЫШЛО ☠️☠️☠️', call.message.chat.id,
                                                message_id=timer.message_id, reply_markup=marka)
                    break
                else:
                    await bot.edit_message_text(f'‼️ У тебя {time_list[count]} секунд ‼️', call.message.chat.id,
                                                message_id=timer.message_id, reply_markup=marka)
                count += 1
            else:
                await bot.edit_message_text(f'‼️ У тебя {seconds} секунд ‼️', call.message.chat.id,
                                            message_id=timer.message_id, reply_markup=marka)

    # АРТ-ВИКТОРИНА
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
        butt1 = types.InlineKeyboardButton(text=f'{artist1}', callback_data='artist1')
        butt2 = types.InlineKeyboardButton(text=f'{artist2}', callback_data='artist2')
        butt3 = types.InlineKeyboardButton(text=f'{artist3}', callback_data='artist3')
        butt4 = types.InlineKeyboardButton(text=f'{artist4}', callback_data='artist4')
        butt_set = set()
        butt_set.add(butt1), butt_set.add(butt2), butt_set.add(butt3), butt_set.add(butt4)
        butt_list = list(butt_set)
        mkp.add(butt_list[0], butt_list[1], butt_list[2], butt_list[3])
        await bot.send_photo(call.message.chat.id, image, 'Кто автор этой картины?', reply_markup=mkp)
        image.close()
    if call.data == 'artist1':
        markup = types.InlineKeyboardMarkup()
        go = types.InlineKeyboardButton(text='🔙', callback_data='go')
        more = types.InlineKeyboardButton(text='Ещё!', callback_data='art_quest')
        markup.add(go, more)
        try:
            global win_id
            win = await bot.copy_message(call.message.chat.id, from_chat_id=call.message.chat.id, message_id=win_id)
            win_id = win.message_id
        except:
            win = await bot.send_sticker(call.message.chat.id, open('Win.tgs', 'rb'))
            win_id = win.message_id
        await asyncio.sleep(1)
        await bot.send_message(call.message.chat.id, 'Бинго!')
        await asyncio.sleep(1)
        await bot.send_message(call.message.chat.id, 'Что дальше', reply_markup=markup)
    elif call.data == 'artist2' or call.data == 'artist3' or call.data == 'artist4':
        markup = types.InlineKeyboardMarkup()
        go = types.InlineKeyboardButton(text='🔙', callback_data='go')
        more = types.InlineKeyboardButton(text='Ещё!', callback_data='art_quest')
        markup.add(go, more)
        try:
            global scream_id
            scream = await bot.copy_message(call.message.chat.id, from_chat_id=call.message.chat.id,
                                            message_id=scream_id)
            scream_id = scream.message_id
        except:
            scream = await bot.send_sticker(call.message.chat.id, open('Scream.tgs', 'rb'))
            scream_id = scream.message_id
        await asyncio.sleep(1)
        await bot.send_message(call.message.chat.id, f'Нет, на самом деле это {artist1}')
        await asyncio.sleep(1)
        await bot.send_message(call.message.chat.id, 'Что дальше?', reply_markup=markup)

    # РЕКОММЕНДЦИЯ ХОРОШЕГО ФИЛЬМА, КОТОРЫЙ НЕ СМОТРЕЛ
    elif call.data == 'film_recom':
        user_id = call.from_user.id

        load_mes = await bot.send_message(call.message.chat.id, 'Загрузка: ▒▒▒▒▒▒▒▒▒▒ 0%')
        load_id = load_mes.message_id
        if userid_films == {}:
            userid_films[user_id] = []
        if len(userid_films[user_id]) == 0:
            best_films = []
            try:
                drivers_dict[user_id].get(f'https://kritikanstvo.ru/top/movies/best/2021-2023/start/0/')
            except:
                drivers_dict[user_id] = webdriver.Chrome(options=options)
                drivers_dict[user_id].get(f'https://kritikanstvo.ru/top/movies/best/2021-2023/start/0/')
            await bot.edit_message_text('Загрузка: █▒▒▒▒▒▒▒▒▒ 10%', call.message.chat.id, load_id)
            drivers_dict[user_id].find_element(By.CLASS_NAME, 'pseudolink').click()
            await asyncio.sleep(0.5)
            drivers_dict[user_id].find_element(By.CLASS_NAME, 'pseudolink').click()
            await asyncio.sleep(0.5)
            drivers_dict[user_id].find_element(By.CLASS_NAME, 'pseudolink').click()
            await asyncio.sleep(0.5)
            drivers_dict[user_id].find_element(By.CLASS_NAME, 'pseudolink').click()
            await asyncio.sleep(0.5)
            drivers_dict[user_id].find_element(By.CLASS_NAME, 'pseudolink').click()
            await asyncio.sleep(0.5)
            await bot.edit_message_text('Загрузка: ██▒▒▒▒▒▒▒▒ 20%', call.message.chat.id, load_id)
            drivers_dict[user_id].find_element(By.CLASS_NAME, 'pseudolink').click()
            await asyncio.sleep(0.5)
            drivers_dict[user_id].find_element(By.CLASS_NAME, 'pseudolink').click()
            await asyncio.sleep(0.5)
            drivers_dict[user_id].find_element(By.CLASS_NAME, 'pseudolink').click()
            await asyncio.sleep(0.5)
            # for i in range(0, 60, 10):
            #     drivers_dict[user_id].get(f'https://kritikanstvo.ru/top/movies/best/2021-2023/start/{i}/')
            #     if i == 30:
            elements = drivers_dict[user_id].find_elements(By.TAG_NAME, 'h2')
            for j in elements:
                best_films.append(j.text)
            await bot.edit_message_text('Загрузка: ███▒▒▒▒▒▒▒ 30%', call.message.chat.id, load_id)
            # убираем из этого списка просмотренные фильмы
            base_list = []
            try:
                with sqlite3.connect('films_base.db') as con:
                    cur = con.cursor()
                    table_name = f'films{user_id}'
                    cur.execute(f"""SELECT films_list FROM {table_name}""")
                    con.commit()
                    result_list = cur.fetchall()
                    for i in result_list:
                        base_list.append(i[0])
            except:
                pass
            await asyncio.sleep(0.5)
            await bot.edit_message_text('Загрузка: ████▒▒▒▒▒▒ 40%', call.message.chat.id, load_id)
            for i in best_films:
                if i not in base_list:
                    userid_films[user_id].append(i)
            try:
                while True:
                    userid_films[user_id].remove('')
            except ValueError:
                pass
        random_film = userid_films[user_id].pop(random.choice(range(0, len(userid_films[user_id]))))
        random_film_byid[user_id] = random_film
        try:
            drivers_dict[user_id].get('https://kritikanstvo.ru/top/movies/best/2021-2023/start/0/')
        except:
            drivers_dict[user_id] = webdriver.Chrome(options=options)
            drivers_dict[user_id].get('https://kritikanstvo.ru/top/movies/best/2021-2023/start/0/')
        await bot.edit_message_text('Загрузка: █████▒▒▒▒▒ 50%', call.message.chat.id, load_id)
        drivers_dict[user_id].find_element(By.NAME, 's').send_keys(random_film)
        drivers_dict[user_id].find_element(By.NAME, 's').submit()
        drivers_dict[user_id].find_element(By.CLASS_NAME, 'cover').click()
        await asyncio.sleep(0.5)
        await bot.edit_message_text('Загрузка: ██████▒▒▒▒ 60%', call.message.chat.id, load_id)
        photo_url = drivers_dict[user_id].find_elements(By.CLASS_NAME, 'gallery_common')[0].get_attribute('href')
        try:
            photo_url2 = drivers_dict[user_id].find_elements(By.CLASS_NAME, 'gallery_common')[1].get_attribute('href')
        except:
            photo_url2 = drivers_dict[user_id].find_elements(By.CLASS_NAME, 'gallery_common')[0].get_attribute('href')
        year_search_list = drivers_dict[user_id].find_element(By.CLASS_NAME, 'page_item_info').find_elements(
            By.TAG_NAME, 'p')
        year = min([re.search(r'\d{4}', i.text)[0] for i in year_search_list])
        try:
            story = drivers_dict[user_id].find_element(By.CLASS_NAME, 'page_item_story').text
        except:
            story = 0
        await bot.edit_message_text('Загрузка: ███████▒▒▒ 70%', call.message.chat.id, load_id)
        drivers_dict[user_id].get('http://hdrezka.co/')
        await bot.edit_message_text('Загрузка: ████████▒▒ 80%', call.message.chat.id, load_id)
        drivers_dict[user_id].find_element(By.CLASS_NAME, 'b-search__field').send_keys(f'{random_film} {year}')
        drivers_dict[user_id].find_element(By.CLASS_NAME, 'b-search__field').submit()
        for i in drivers_dict[user_id].find_elements(By.CLASS_NAME, 'b-content__inline_item'):
            if i.find_element(By.CLASS_NAME, 'entity').text == 'Фильм' or i.find_element(By.CLASS_NAME,
                                                                                         'entity').text == 'Мультфильм':
                i.click()
                break
        film_page = drivers_dict[user_id].current_url
        await bot.edit_message_text('Загрузка: █████████▒ 90%', call.message.chat.id, load_id)
        await asyncio.sleep(0.5)
        reply_markup = markups(trailer='Смотреть трейлер 🎞')
        reply_markup.add(InlineKeyboardButton('Смотреть фильм 📽', film_page))
        reply_markup.add(InlineKeyboardButton('Уже смотрел', callback_data='already'),
                         InlineKeyboardButton('Ещё', callback_data='film_recom'))
        reply_markup.add(InlineKeyboardButton('🔙', callback_data='go'))
        if story == 0:
            story2 = drivers_dict[user_id].find_element(By.CLASS_NAME, 'b-post__description_text').text
            await bot.edit_message_text('Загрузка: ██████████ 100%', call.message.chat.id, load_id)
            try:
                await asyncio.sleep(0.5)
                result[user_id] = await bot.send_photo(call.message.chat.id, photo_url,
                                                       f'{random_film.upper()} ({year})\n\n{story2}',
                                                       reply_markup=reply_markup)
            except:
                result[user_id] = await bot.send_photo(call.message.chat.id, photo_url2,
                                                       f'{random_film.upper()} ({year})\n\n{story2}',
                                                       reply_markup=reply_markup)

        else:
            await asyncio.sleep(0.5)
            await bot.edit_message_text('Загрузка: ██████████ 100%', call.message.chat.id, load_id)
            try:
                result[user_id] = await bot.send_photo(call.message.chat.id, photo_url,
                                                   f'{random_film.upper()} ({year})\n\n{story}',
                                                   reply_markup=reply_markup)
            except:
                result[user_id] = await bot.send_photo(call.message.chat.id, photo_url2,
                                                       f'{random_film.upper()} ({year})\n\n{story}',
                                                       reply_markup=reply_markup)
        await asyncio.sleep(0.5)
        await bot.delete_message(call.message.chat.id, load_id)

    if call.data == 'trailer':
        user_id = call.from_user.id
        try:
            rezka_link = WebDriverWait(drivers_dict[user_id], 7).until(
                EC.presence_of_element_located((By.CLASS_NAME, "b-sidelinks__text")))
            rezka_link.click()
            trailer = WebDriverWait(drivers_dict[user_id], 7).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="ps-trailer-player"]/iframe'))).get_attribute(
                'src').split('?iv_load_policy')[0].replace('youtube', 'ssyoutube')

            drivers_dict[user_id].get(trailer)
            element = WebDriverWait(drivers_dict[user_id], 6).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="sf_result"]/div/div[1]/div[2]/div[2]/div[1]/a')))
            trailer2 = element.get_attribute('href')
            await bot.send_video(call.message.chat.id, trailer2)
        except:
            drivers_dict[user_id].get('https://www.youtube.com/')
            WebDriverWait(drivers_dict[user_id], 7).until(EC.presence_of_element_located((By.NAME, 'search_query')))
            drivers_dict[user_id].find_element(By.NAME, 'search_query').send_keys(
                random_film_byid[user_id] + f' официальный русский трейлер')
            await asyncio.sleep(1)
            drivers_dict[user_id].find_element(By.NAME, 'search_query').submit()
            WebDriverWait(drivers_dict[user_id], 7).until(EC.presence_of_element_located((By.ID, 'title-wrapper')))
            trailer_link_youtube = drivers_dict[user_id].find_element(By.XPATH,
                                                                         '/html/body/ytd-app/div[1]/ytd-page-manager/ytd-search/div[1]/ytd-two-column-search-results-renderer/div/ytd-section-list-renderer/div[2]/ytd-item-section-renderer/div[3]/ytd-video-renderer[1]/div[1]/div/div[1]/div/h3/a').get_attribute(
                'href')
            drivers_dict[user_id].get(drivers_dict[user_id].find_element(By.XPATH,
                                                                         '/html/body/ytd-app/div[1]/ytd-page-manager/ytd-search/div[1]/ytd-two-column-search-results-renderer/div/ytd-section-list-renderer/div[2]/ytd-item-section-renderer/div[3]/ytd-video-renderer[1]/div[1]/div/div[1]/div/h3/a').get_attribute(
                'href').replace('youtube', 'ssyoutube'))
            try:
                element = WebDriverWait(drivers_dict[user_id], 7).until(
                    EC.presence_of_element_located((By.XPATH, '//*[@id="sf_result"]/div/div[1]/div[2]/div[2]/div[1]/a')))
                trailer2 = element.get_attribute('href')
                await bot.send_video(call.message.chat.id, trailer2)
            except:
                await bot.send_message(call.message.chat.id, trailer_link_youtube)



    elif call.data == 'already':
        user_id = call.from_user.id
        with sqlite3.connect('films_base.db') as con:
            cur = con.cursor()
            table_name = f'films{user_id}'
            cur.execute(f"""CREATE TABLE IF NOT EXISTS {table_name} (
            films_list TEXT)""")
            cur.execute(f"""INSERT INTO {table_name}(films_list) VALUES ('{random_film_byid[user_id]}')""")
        new_markup = markups(trailer='Смотреть трейлер 🎞')
        new_markup.add(InlineKeyboardButton('Смотреть фильм 📽', drivers_dict[user_id].current_url))
        new_markup.add(InlineKeyboardButton('Уже смотрел ✔️', callback_data='already'),
                       InlineKeyboardButton('Ещё', callback_data='film_recom'))
        new_markup.add(InlineKeyboardButton('🔙', callback_data='go'))

        await bot.edit_message_reply_markup(call.message.chat.id, result[user_id].message_id, reply_markup=new_markup)
        bd = await bot.send_message(call.message.chat.id,
                                    f'Фильм "{random_film_byid[user_id]}" добавлен в базу данных и больше не будет рекомендоваться')
        await asyncio.sleep(2.5)
        await bot.delete_message(call.message.chat.id, bd.message_id)

    # БАР-БОТ
    elif call.data == 'bar':
        await bot.send_message(call.message.chat.id, '🌀Добро пожаловать в бар-бот!🌀')
        await asyncio.sleep(1)
        await bot.send_photo(call.message.chat.id, open('bar/octopus.jpg', 'rb'), reply_markup=markups(
            classic='Классика',
            sweat='Для девочек',
            dead='Убей меня',
            milk='MOLOKO+',
            hot='Пощекочем сосочки',
            rand='Рандом',
            zoz='ЗОЖ',
            go='🔙'
        ))
    elif call.data == 'zoz':
        haha = await bot.send_message(call.message.chat.id, 'Пошёл нахуй')
        await asyncio.sleep(0.5)
        await bot.delete_message(call.message.chat.id, haha.message_id)
        await bot.send_photo(call.message.chat.id, open('bar/shwarz2.jpg', 'rb'), 'Вкусняшки для зожников',
                             reply_markup=markups(dno='Золотое дно', basil='Базиликовый удар', blood='Кровавая Мэри',
                                                  gott='Карелл Готт', vegan = 'Демон-веган', shmel='Шмель', bar='🔙'))
    elif call.data == 'hot':
        try:
            global rango_id
            rango = await bot.copy_message(call.message.chat.id, from_chat_id=call.message.chat.id, message_id=rango_id,
                                           caption='Коктейли и шоты с TABASCO® 🌶',
                                           reply_markup=markups(bojar='Боярский', bojar2='Дочь Боярского',
                                                                reddog='Красный пёс', fors='Форсаж', dog='Собака.ру',
                                                                reanimator='Реаниматор',blood='Кровавая Мэри', oyster='Устричный шутер',
                                                                devil='Тессманский дьявол', controlshot='Контрольный выстрел', bar='🔙'))
            rango_id = rango.message_id
        except:
            rango = await bot.send_animation(call.message.chat.id, open('bar/Rango-min.gif', 'rb'),
                                             caption='Коктейли и шоты с TABASCO® 🌶',
                                             reply_markup=markups(bojar='Боярский', bojar2='Дочь Боярского',
                                                                  reddog='Красный пёс', fors='Форсаж', dog='Собака.ру',
                                                                  reanimator='Реаниматор', blood='Кровавая Мэри', oyster='Устричный шутер',
                                                                  devil='Тессманский дьявол', controlshot='Контрольный выстрел', bar='🔙'))
            rango_id = rango.message_id
    elif call.data == 'sweat':
        await bot.send_photo(call.message.chat.id, open(f'bar/girls{random.choice(range(1, 4))}.jpg', 'rb'),
                             caption='Девочкам понравится',
                             reply_markup=markups(barbi='Барби', baunty='Баунти мартини', rose='Розовый сад',
                                                  porn='Порнозвезда', sex='Секс на пляже', orgasm='Модный оргазм',
                                                  sosok='Скользкий сосок', cocumber='Джин тоник с огурцом',
                                                  ledi='Белая леди', blur='Облако дыма', bell='Беллини',
                                                  mimoza='Мимоза', bar='🔙'))
    elif call.data == 'dead':
        await bot.send_message(call.message.chat.id,
                               '<em>Что тебя не убивает, делает тебя пьянее</em> \n\n© Тибетская мудрость',
                               parse_mode='HTML')
        await asyncio.sleep(2.5)
        await bot.send_photo(call.message.chat.id, open('bar/Горькое пойло, Адриан Брауэр, 1631.jpg', 'rb'),
                             reply_markup=markups(hiro='Хиросима', aurora='Северное сияние', sky='Небеса',
                                                  bum='Текила бум', negr='Негрони', green='Зелёная фея',
                                                  blackrus='Чёрный русский', french='Френч 75', martin='Водка мартини',
                                                  controlshot='Контрольный выстрел', bar='🔙'))
    elif call.data == 'milk':
        try:
            global orange_id
            orange = await bot.copy_message(call.message.chat.id, from_chat_id=call.message.chat.id,
                                            message_id=orange_id,
                                            reply_markup=markups(pina='Пина колада', orgasm='Модный оргазм', tom='Том и Джерри',
                                                                 brendi='Бренди и кола', amigo='Амиго',
                                                                 belrus='Белый русский', cherry='Зимняя вишня',
                                                                 shashki='Алко-шашки', bar='🔙'))
            orange_id = orange.message_id
        except:
            orange = await bot.send_animation(call.message.chat.id, open('bar/Clockwork_intro.mp4', 'rb'),
                                              caption='Коктейли с молоком/сливками 🥛',
                                              reply_markup=markups(pina='Пина колада', orgasm='Модный оргазм', belrus='Белый русский',
                                                                   tom='Том и Джерри', brendi='Бренди и кола',
                                                                   amigo='Амиго', cherry='Зимняя вишня',
                                                                   shashki='Алко-шашки', bar='🔙'))
            orange_id = orange.message_id

    elif call.data == 'rand':
        try:
            global roulette
            global rand_mes
            await bot.delete_message(call.message.chat.id, rand_mes.message_id)
            await bot.delete_message(call.message.chat.id, roulette.message_id)
            roulette = await bot.copy_message(call.message.chat.id,call.message.chat.id, roulette.message_id)

            user_id = call.from_user.id
            coc_list = [values for values in bar_dict.values()]
            await asyncio.sleep(1)
            rand_mes = await bot.send_message(call.message.chat.id,
                                              coc_list.pop(random.choice(range(len(coc_list) - 1))))
            for i in range(10):
                if i < 9:
                    await asyncio.sleep(0.25)
                    await bot.edit_message_text(coc_list.pop(random.choice(range(len(coc_list) - 1))),
                                                call.message.chat.id, rand_mes.message_id)

                elif i == 9:
                    await asyncio.sleep(0.25)
                    rand_coc[user_id] = coc_list.pop(random.choice(range(len(coc_list) - 1)))
                    await bot.edit_message_text(rand_coc[user_id], call.message.chat.id, rand_mes.message_id)
                    await asyncio.sleep(0.5)
                    await bot.edit_message_reply_markup(call.message.chat.id, rand_mes.message_id,
                                                        reply_markup=markups(confirm='☑️', rand='🌀', bar='🔙'))
                    await asyncio.sleep(0.5)
        except:
            user_id = call.from_user.id
            coc_list = [values for values in bar_dict.values()]
            roulette = await bot.send_document(call.message.chat.id, open('bar/roulette.gif', 'rb'), disable_content_type_detection=True)
            await asyncio.sleep(0.5)
            rand_mes = await bot.send_message(call.message.chat.id, coc_list.pop(random.choice(range(len(coc_list)-1))))
            for i in range(10):
                if i < 9:
                    await asyncio.sleep(0.25)
                    await bot.edit_message_text(coc_list.pop(random.choice(range(len(coc_list)-1))), call.message.chat.id, rand_mes.message_id)

                elif i == 9:
                    await asyncio.sleep(0.25)
                    rand_coc[user_id] = coc_list.pop(random.choice(range(len(coc_list)-1)))
                    await bot.edit_message_text(rand_coc[user_id], call.message.chat.id, rand_mes.message_id)
                    await asyncio.sleep(0.5)
                    await bot.edit_message_reply_markup(call.message.chat.id, rand_mes.message_id, reply_markup=markups(confirm = '☑️', rand = '🌀', bar ='🔙'))
                    await asyncio.sleep(0.5)

    elif call.data == 'confirm':
        user_id = call.from_user.id
        await coc(rand_coc[user_id], call)

    elif call.data == 'classic':
        rm = types.InlineKeyboardMarkup()
        editmes = await bot.send_photo(call.message.chat.id, open('bar/coc.jpg', 'rb'), reply_markup=rm)
        buttons = [types.InlineKeyboardButton(text='Космополитен', callback_data='cosmo'),
                   types.InlineKeyboardButton(text='Дайкири', callback_data='daiq'),
                   types.InlineKeyboardButton(text='Апероль Шприц', callback_data='spritz'),
                   types.InlineKeyboardButton(text='Манхэттен', callback_data='manh'),
                   types.InlineKeyboardButton(text='Май тай', callback_data='maj'),
                   types.InlineKeyboardButton(text='Негрони', callback_data='negr'),
                   types.InlineKeyboardButton(text='Мохито', callback_data='moh'),
                   types.InlineKeyboardButton(text='Сингапурский слинг', callback_data='sling'),
                   types.InlineKeyboardButton(text='Текила санрайз', callback_data='sunrise'),
                   types.InlineKeyboardButton(text='Маргарита', callback_data='marg'),
                   types.InlineKeyboardButton(text='Куба либре', callback_data='libre'),
                   types.InlineKeyboardButton(text='Б-52', callback_data='b52'),
                   types.InlineKeyboardButton(text='Лонг айленд айс ти', callback_data='long'),
                   types.InlineKeyboardButton(text='Виски сауэр', callback_data='ws')]
        for i in range(int(len(buttons) / 2 + 1)):
            await asyncio.sleep(0.5)
            if len(buttons) == 0:
                rm.add(types.InlineKeyboardButton(text='🔙', callback_data='bar'))
            else:
                rm.add(buttons.pop(), buttons.pop())
            await bot.edit_message_reply_markup(call.message.chat.id, editmes.message_id, reply_markup=rm)

    elif call.data in bar_dict:
        await coc(bar_dict[call.data], call)


executor.start_polling(dispatcher=dp, skip_updates=True)
