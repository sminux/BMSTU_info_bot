'''
Created on 17 янв. 2017 г.

@author: sminux
'''

import telebot
import constants
import random
import datetime
from urllib.request import urlopen
from bs4 import BeautifulSoup

bot = telebot.TeleBot(constants.token)

upd = bot.get_updates()
print("\n____________")
print(bot.get_me())

def log(message, answer):
    print("\n____________")
    from datetime import datetime
    print(datetime.now())
    print("Сообщение от {0} {1}. (id = {2}) \nТекст: {3}".format(message.from_user.first_name,
                                                                 message.from_user.last_name,
                                                                 str(message.from_user.id),
                                                                 message.text ))
    print(answer)
    
    
def get_week():
    url_bmstu = urlopen(constants.url_schedule).read()
    soup = BeautifulSoup(url_bmstu, "lxml")
    for paragraph in soup.findAll('h4'):
        schedule_week = paragraph.string    
    return schedule_week

def get_shedule_ch():
    url_bmstu = urlopen(constants.url_schedule).read()
    soup = BeautifulSoup(url_bmstu, "lxml")
    answer_ch = 'ЧС 📚\n'
    divs = soup.find_all('div', attrs = {"class":"col-md-6 hidden-xs"})
    for div in divs:
        answer_ch  += '📋'
        trs = div.find_all('tr')
        for tr in trs:
            td_time = tr.find_all('td', attrs={"class":"bg-grey text-nowrap"})
            lesson_success = tr.find_all('td', attrs={"class":"text-success"})
            lesson_ordinary = tr.find_all('td', attrs={"colspan":"2"})
            days = tr.find_all('strong')
            time = [i.text for i in td_time]
            lesson_cheslitel = [les.text for les in lesson_success]
            lesson_ordinary = [les.text for les in lesson_ordinary]
            day = [day.text for day in days]
            
            answer_ch += '<b>{}</b>\n<b>{}</b> {}{}'.format(day,
                                                                time,
                                                                lesson_cheslitel,
                                                                lesson_ordinary)

        answer_ch += '\n'
    answer_ch = answer_ch.replace('\\xa0', ' ')
    answer_ch = answer_ch.replace('[', '')
    answer_ch = answer_ch.replace(']', '')
    answer_ch = answer_ch.replace("'", '')
    answer_ch = answer_ch.replace("<b></b> <b></b>", '')
    answer_ch = answer_ch.replace("\n\n", '')        
    return  answer_ch
 
def get_shedule_zn():
    url_bmstu = urlopen(constants.url_schedule).read()
    soup = BeautifulSoup(url_bmstu, "lxml")

    answer_zn = 'ЗН 📚\n'
    divs = soup.find_all('div', attrs = {"class":"col-md-6 hidden-sm hidden-md hidden-lg"})
    for div in divs:
        answer_zn += '📋'
        trs = div.find_all('tr')
        for tr in trs:
            td_time = tr.find_all('td', attrs={"class":"bg-grey text-nowrap"})
            lesson_info = tr.find_all('td', attrs={"class":"text-info"})
            lesson_ordinary = tr.find_all('td', attrs={"colspan":"2"})
            days = tr.find_all('strong')
            time = [i.text for i in td_time]
            lesson_znamenatel = [les.text for les in lesson_info]
            lesson_ordinary = [les.text for les in lesson_ordinary]
            day = [day.text for day in days]
            
            answer_zn += '<b>{}</b>\n<b>{}</b> {}{}'.format(day,
                                                            time,
                                                            lesson_znamenatel,
                                                            lesson_ordinary)

        answer_zn += '\n'
    answer_zn = answer_zn.replace('\\xa0', ' ')
    answer_zn = answer_zn.replace('[', '')
    answer_zn = answer_zn.replace(']', '')
    answer_zn = answer_zn.replace("'", '')
    answer_zn = answer_zn.replace("<b></b> <b></b>", '')
    answer_zn = answer_zn.replace("\n\n", '')
    return  answer_zn

@bot.message_handler(commands = ['help'])
def handle_help(message):
    bot.send_message(message.chat.id, 'Тебе никто не поможет 😈 \nP.S.\n🔘Чтобы обратиться к порталу ru.bmstu.wiki, пишите "Кто такой ФИО?"\n🔘Чтобы узнать свой порядковый номер, запросите "список группы"\n🔘Также вы можете узнать "расписание" на неделю\n🔘Команда "новости" предоставит последнюю новостную заметку\nℹ️Вопросы и предложения пишите автору: @sminux')
        
@bot.message_handler(commands = ['start'])
def handle_start(message):
    user_markup = telebot.types.ReplyKeyboardMarkup(True, False)
    user_markup.row('/start', '/stop', '/news')
    user_markup.row('список группы', 'диск', 'неделя (ч/з)')
    user_markup.row('расписание', 'сегодня' )
    bot.send_message(message.chat.id, "Чем могу помочь...", reply_markup=user_markup)
    
@bot.message_handler(commands = ['stop'])
def handle_stop(message):   
     hide_markup = telebot.types.ReplyKeyboardRemove()
     bot.send_message(message.chat.id, "...", reply_markup = hide_markup)
     
@bot.message_handler(commands = ['news'])
def handle_news(message):   
        answer = 'Въ салонѣ тихо, пыльно и пусто.\nТолько въ одномъ изъ угловъ вышиваетъ гладью пожилая княжна.'
        url_news = urlopen('https://vk.com/pr.bmstu').read()
        soup = BeautifulSoup(url_news, "lxml")
        news = soup.find('div', attrs={"class": "pi_text"})
        answer = '📰' + news.text
        log(message, answer)
        bot.send_message(message.chat.id, answer) 

@bot.message_handler(content_types = ['text'])
def handle_text(message):
        answer = "Не понятно🤔  Попробуйте ещё раз."
        msg = message.text
        if msg == 'диск':
            answer = 'https://drive.google.com/open?id=0Bwpp4JuViU2KNWpic3loeGlPeHM'
            log(message, answer)
            bot.send_message(message.chat.id, answer)   
        elif msg == 'неделя (ч/з)':
            '''from datetime import date
            today = date.today()
            month = today.strftime("%b")
            day = today.strftime("%d")'''
            answer = get_week()
            log(message, answer)
            bot.send_message(message.chat.id, answer) 
            img = open('Plan.png', 'rb')               
            bot.send_photo(message.chat.id, img)
            img.close()
        elif msg == 'список группы':
            answer = "список группы ИУ8-" + (constants.sem).__str__() + "2:"
            i = 0
            for student in constants.group_list:
                answer += '\n' + (i+1).__str__() + '.  ' + constants.group_list[i]
                i = i + 1            
            log(message, answer)
            bot.send_message(message.chat.id, answer)   
        elif msg == 'расписание':
            answer = '📥 Загружаю...'
            log(message, answer)
            bot.send_message(message.chat.id, answer)  
            if (get_week().find('числитель', 0)>=0):
               answer = get_shedule_ch()
            elif (get_week().find('знаменатель', 0)>=0): 
                answer = get_shedule_zn()
            log(message, answer)
            bot.send_message(message.chat.id, answer, parse_mode='HTML')  
        elif msg == 'сегодня':
            if (datetime.datetime.today().isoweekday()==1):
                img = open('/Schedule/1.png', 'rb')               
                bot.send_photo(message.chat.id, img)
                img.close()
            elif (datetime.datetime.today().isoweekday()==2): 
                img = open('/Schedule/2.png', 'rb')               
                bot.send_photo(message.chat.id, img)
                img.close()
            elif (datetime.datetime.today().isoweekday()==3): 
                img = open('/Schedule/3.png', 'rb')               
                bot.send_photo(message.chat.id, img)
                img.close()
            elif (datetime.datetime.today().isoweekday()==4): 
                img = open('/Schedule/4.png', 'rb')               
                bot.send_photo(message.chat.id, img)
                img.close()
            elif (datetime.datetime.today().isoweekday()==5): 
                img = open('/Schedule/5.png', 'rb')               
                bot.send_photo(message.chat.id, img)
                img.close()
            elif (datetime.datetime.today().isoweekday()==6): 
                img = open('/Schedule/6.png', 'rb')               
                bot.send_photo(message.chat.id, img)
                img.close()  
            else:
                answer = 'Въ салонѣ тихо, пыльно и пусто.\nТолько въ одномъ изъ угловъ вышиваетъ гладью пожилая княжна.'
                log(message, answer)
                bot.send_message(message.chat.id, answer)  
            
        elif ((msg.find('кто такой', 0)>=0) | (msg.find('кто такая', 0)>=0) | (msg.find('Кто такой', 0)>=0) | (msg.find('Кто такая', 0)>=0)):
            str = msg.replace("?", '')
            str = str.replace(',', '')
            str = str.replace('.', '')
            str = str.replace('/', '')
            str = str.replace('&', '')
            str = str.replace('Кто', '')
            str = str.replace('кто', '')
            str = str.replace('такой', '') 
            str = str.replace('такая', '')
            text = ''
            fio = str.split(' ')
            if len(fio) != 5:
                text = 'Мне нужны полные данные [ФИО]. Повторите запрос.'
            elif len(fio) == 5:
                text = constants.wiki + fio[2].capitalize() + ',_' + fio[3].capitalize() + '_' + fio[4].capitalize()

            answer = text
            log(message, answer)
            bot.send_message(message.chat.id, answer)  
        elif ((msg.find('студент', 0)>=0) | (msg.find('МГТУ', 0)>=0) | (msg.find('мгту', 0)>=0) | (msg.find('бауманк', 0)>=0) | (msg.find('сдаст', 0)>=0) | (msg.find('сдадим', 0)>=0)):
            answer = "Ага\n"
            answer += constants.loud_tips[random.randint(0,10)]
            log(message, answer)
            bot.send_message(message.chat.id, answer)
        elif ((msg.find('академ', 0)>=0) | (msg.find('Академ', 0)>=0)):
            answer = constants.academ_tips[random.randint(0,4)]
            log(message, answer)
            bot.send_message(message.chat.id, answer)
        elif ((msg.find('аха', 0)>=0) | (msg.find('🤗', 0)>=0) | (msg.find('😀', 0)>=0) | (msg.find('😬', 0)>=0) | (msg.find('😁', 0)>=0) | (msg.find('😂', 1)>=0) | (msg.find('😃', 0)>=0) | (msg.find('😉', 0)>=0) | (msg.find('😄', 0)>=0) | (msg.find('😅', 0)>=0) | (msg.find('😆', 0)>=0) | (msg.find('😊', 0)>=0) | (msg.find('☺️', 0)>=0) | (msg.find('😜', 0)>=0) | (msg.find('😎', 0)>=0)):
            answer = "☺️ 😉"
            log(message, answer)
            bot.send_message(message.chat.id, answer)
        elif ((msg.find('😞', 0)>=0) | (msg.find('😟', 0)>=0) | (msg.find('☹️', 0)>=0) | (msg.find('🙁', 0)>=0) | (msg.find('😣', 1)>=0) | (msg.find('😖', 0)>=0) | (msg.find('😩', 0)>=0) | (msg.find('😤', 0)>=0) | (msg.find('😧', 0)>=0) | (msg.find('😯', 0)>=0) | (msg.find('😨', 0)>=0) | (msg.find('😭', 0)>=0) | (msg.find('😪', 0)>=0) | (msg.find('😢', 0)>=0) | (msg.find('🤕', 0)>=0) | (msg.find('🤒', 0)>=0)):
            answer = "😯 😞 "
            log(message, answer)
            bot.send_message(message.chat.id, answer)
        elif ((msg.find('рк', 0)>=0) | (msg.find('РК', 0)>=0) | (msg.find('жуков', 0)>=0) | (msg.find('Жуков', 0)>=0)):
            answer = '!@#$%&'
            log(message, answer)
            bot.send_message(message.chat.id, answer)
        else:
            log(message, answer) 
            bot.send_message(message.chat.id, answer)
            

    
bot.polling(none_stop = True)

