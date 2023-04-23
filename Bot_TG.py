import telebot
import asyncio

from ParserAvito import AvitoParser  ### Данная библиотека лежит тут --> https://github.com/DimaChepuchtanov/Parsers/tree/ParserAvito
from apscheduler.schedulers.background import BackgroundScheduler


"""Наш ТГ токен"""
TOKEN = "Ваш ТЕЛЕГРАММ-ТОКЕН"

"""Создаем наш тг бот"""
bot = telebot.TeleBot(TOKEN)

"""Словарик городов"""
cityes = {
    'Абакан':'Abakan', 'Азов':'Azov', 'Александров':'Alexandrov', 'Алексин':'Aleksin', 'Альметьевск':'Almetyevsk', 'Анапа':'Anapa', 'Ангарск':'Angarsk', 'Анжеро-Судженск':'Anzhero-Sudzhensk', 'Апатиты':'Apatity',
    'Арзамас':'Arzamas', 'Армавир':'Armavir', 'Арсеньев':'Arseniev', 'Артем':'Artem', 'Архангельск':'Arkhangelsk', 'Асбест':'Asbestos', 'Астрахань':'Astrakhan', 'Ачинск':'Achinsk',
    
    'Балаково':'Balakovo', 'Балахна':'Balakhna', 'Балашиха':'Balashikha', 'Балашов':'Balashov', 'Барнаул':'Barnaul', 'Батайск':'Bataysk', 'Белгород':'Belgorod', 'Белебей':'Belebey', 'Белово':'Belovo', 'Белогорск':'Belogorsk', 'Белорецк':'Beloretsk', 'Белореченск':'Belorechensk', 'Бердск':'Berdsk',
    'Березник':'Berezniki', 'Березовский':'Berezovsky', 'Бийск':'Biysk', 'Биробиджан':'Birobidzhan', 'Благовещенск':'Blagoveshchensk', 'Бор':'Bor', 'Борисоглебск':'Borisoglebsk', 'Боровичи':'Borovichi', 'Братск':'Bratsk', 'Брянск':'Bryansk', 'Бугульма':'Bugulma', 'Буденновск':'Budennovs', 'Бузулук':'Buzuluk', 'Буйнакск':'Buynaksk',

    'Великие Луки':'Velikiye Luki','Великий Новгород':'Velikiy Novgorod','Верхняя Пышма':'Upper Pyshma','Видное':'Vidnoe','Владивосток':'Vladivostok','Владикавказ':'Vladikavkaz','Владимир':'Vladimir','Волгоград':'Volgograd','Волгодонск':'Volgodonsk','Волжск':'Volzhsk','Волжский':'Volzhsky','Вологда':'Vologda',
    'Вольск':'Volsk','Воркута':'Vorkuta','Воронеж':'Voronezh','Воскресенск':'Voskresensk','Воткинск':'Votkinsk','Всеволожск':'Vsevolozhsk','Выборг':'Vyborg','Выкса':'Vyksa','Вязьма':'Vyazma',

    'Гатчина':'Gatchina','Геленджик':'Gelendzhik','Георгиевск':'Georgievsk','Глазов':'Glazov','Горно-Алтайск':'Gorno-Altaisk','Грозный':'Grozny','Губкин':'Gubkin','Гудермес':'Gudermes','Гуково':'Gukovo','Гусь-Хрустальный':'Gus-Khrustalny',
    
    'Дербент':'Derbent','Дзержинск':'Dzerzhinsk','Димитровград':'Dimitrovgrad','Дмитров':'Dmitrov','Долгопрудный':'Dolgoprudny','Домодедово':'Domodedovo','Донской':'Donskoy','Дубна':'Dubna',

    'Евпатория':'Evpatoria','Егорьевск':'Yegorievsk','Ейск':'Yeysk','Екатеринбург':'Ekaterinburg','Елабуга':'Yelabuga','Елец':'Yelets','Ессентуки':'Essentuki',

    'Железногорск':'Zheleznogorsk','Жигулевск':'Zhigulevsk','Жуковский':'Zhukovsky',

    'Заречный':'Zarechnyy', 'Зеленогорск':'Zelenogorsk','Зеленодольск':'Zelenodolsk','Златоуст':'Zlatoust',

    'Иваново':'Ivanovo', 'Ивантеевка':'Ivanteevka', 'Ижевск':'Izhevsk', 'Избербаш':'Izberbash','Иркутск':'Irkutsk','Искитим':'Iskitim','Ишим':'Ishim','Ишимбай':'Ishimbay','Йошкар-Ола':'Yoshkar-Ola',

    'Казань':'Kazan','Калининград':'Kaliningrad','Калуга':'Kaluga','Каменск-Уральский':'Kamensk-Uralsky','Каменск-Шахтинский':'Kamensk-Shakhtinsky','Камышин':'Kamyshin','Канск':'Kansk','Каспийск':'Kaspiysk',
    'Кемерово':'Kemerovo','Керчь':'Kerch','Кинешма':'Kineshma','Кириши':'Kirishi','Киров':'Kirov','Кирово-Чепецк':'Kirovo-Chepetsk','Киселевск':'Kiselevsk','Кисловодск':'Kislovodsk',
    'Клин':'Klin','Клинцы':'Klintsy','Ковров':'Kovrov','Когалым':'Kogalym','Коломна':'Kolomna','Комсомольск-на-Амуре':'Komsomolsk-on-Amur','Копейск':'Kopeysk','Королев':'Korolev',
    'Кострома':'Kostroma','Котлас':'Kotlas','Красногорск':'Krasnogorsk','Краснодар':'Krasnodar','Краснокаменск':'Krasnokamensk','Краснокамск':'Krasnokamsk','Краснотурьинск':'Krasnoturinsk','Красноярск':'Krasnoyarsk',
    'Кропоткин':'Kropotkin','Крымск':'Krymsk','Кстово':'Kstovo','Кузнецк':'Kuznetsk','Кумертау':'Kumertau','Кунгур':'Kungur','Курган':'kurgan','Курск':'Kursk',
    'Кызыл':'Kyzyl',
    
    'Лабинск':'Labinsk','Лениногорск':'Leninogorsk','Ленинск-Кузнецкий':'Leninsk-Kuznetsky','Лесосибирск':'Lesosibirsk','Липецк':'Lipetsk','Лиски':'Liski','Лобня':'Lobnya','Лысьва':'Lysva','Лыткарино':'Lytkarino','Люберцы':'Lyubertsy',

    'Магадан':'Magadan','Магнитогорск':'Magnitogorsk','Майкоп':'Maykop','Махачкала':'Makhachkala','Междуреченск':'Mezhdurechensk','Мелеуз':'Meleuz','Миасс':'Miass','Минеральные Воды':'Mineral water','Минусинск':'Minusinsk',
    'Михайловка':'Mikhailovka','Михайловск':'Mikhailovsk','Мичуринск':'Michurinsk','Москва':'Moscow','Мурманск':'Murmansk','Муром':'Murom','Мытищи':'Mytishchi',

    'Набережные Челны':'Naberezhnye Chelny','Назарово':'Nazarovo','Назрань':'Nazran','Нальчик':'Nalchik','Наро-Фоминск':'Naro-Fominsk','Находка':'Nakhodka','Невинномысск':'Nevinnomyssk','Нерюнгри':'Neryungri',
    'Нефтекамск':'Neftekamsk','Нефтеюганск':'Nefteyugansk','Нижневартовск':'Nizhnevartovsk','Нижнекамск':'Nizhnekamsk','Нижний Новгород':'Nizhny Novgorod','Нижний Тагил':'Nizhny Tagil','Новоалтайск':'Novoaltaysk','Новокузнецк':'Novokuznetsk',
    'Новокуйбышевск':'Novokuibyshevsk','Новомосковск':'Novomoskovsk','Новороссийск':'Novorossiysk','Новосибирск':'Novosibirsk','Новотроицк':'Novotroitsk','Новоуральск':'Novouralsk','Новочебоксарск':'Novocheboksarsk','Новочеркасск':'Novocherkassk',
    'Новошахтинск':'Novoshakhtinsk','Новый Уренгой':'New Urengoy','Ногинск':'Noginsk','Норильск':'Norilsk','Ноябрьск':'Noyabrsk','Нягань':'Nyagan',

    'Обнинск':'Obninsk', 'Одинцово':'Odintsovo','Озерск':'Ozersk','Октябрьский':'Octobersk','Омск':'Omsk',
    'Орел':'orel','Оренбург':'Orenburg','Орехово-Зуево':'Orehovo-Zuevo','Орск':'Orsk',

    'Павлово':'Pavlovo','Павловский Посад':'Pavlovsky Posa','Пенза':'Penza','Первоуральск':'Pervouralsk','Пермь':'Perm','Петрозаводск':'Petrozavodsk',
    'Петропавловск-Камчатский':'Petropavlovsk-Kamchatsky','Подольск':'Podolsk','Полевской':'Polevskoy','Прокопьевск':'Prokopyevsk',
    'Прохладный':'prohladni','Псков':'Pskov','Пушкино':'Pushkino','Пятигорск':'Pyatigorsk',

    'Раменское':'Ramenskoye','Ревда':'Revda',
    'Реутов':'Reutov','Ржев':'Rzhev','Рославль':'Roslavl','Россошь':'Rossosh',
    'Ростов-на-Дону':'Rostov-on-Don','Рубцовск':'Rubtsovsk','Рыбинск':'Rybinsk','Рязань':'Ryazan',

    'Салават':'Salavat','Сальск':'Salsk','Самара':'Samara','Санкт-Петербург':'Saint Petersburg','Ступино':'Stupino','Сургут':'Surgut','Сызрань':'Sizran','Сыктывкар':'Syktyvkar',
    'Саранск':'Saransk','Сарапул':'Sarapul','Саратов':'Saratov','Саров':'Sarov','Свободный':'svobodni','Севастополь':'Sevastopol','Северодвинск':'Severodvinsk','Северск':'Seversk',
    'Сергиев Посад':'Sergiev Posad','Серов':'Serov','Серпухов':'Serpukhov','Сертолово':'Sertolovo','Сибай':'Sibay','Симферополь':'Simferopol','Славянск-на-Кубани':'Slavyansk-on-Kuban',
    'Смоленск':'Smolensk','Соликамск':'Solikamsk','Солнечногорск':'Solnechnogorsk','Сосновый Бор':'Pinery','Сочи':'Sochi','Ставрополь':'Stavropol','Старый Оскол':'Stary Oskol','Стерлитамак':'Sterlitamak',

    'Таганрог':'Taganrog','Тамбов':'Tambov','Тверь':'Tver','Тимашевск':'Timashevsk','Тихвин':'Tikhvin','Тихорецк':'Tikhoretsk',
    'Тобольск':'Tobolsk','Тольятти':'Tolyatti','Томск':'Tomsk','Троицк':'Troitsk',
    'Туапсе':'Tuapse','Туймазы':'Tuymazy','Тула':'Tula','Тюмень':'Tyumen',

    'Узловая':'Nodular',
    'Улан-Удэ':'Ulan-Ude','Ульяновск':'Ulyanovsk','Урус-Мартан':'Urus-Martan','Усолье-Сибирское':'Usolie-Sibirskoe',
    'Уссурийск':'Ussuriysk','Усть-Илимск':'Ust-Ilimsk','Уфа':'Ufa','Ухта':'Ukhta',

    'Феодосия':'Feodosia','Фрязино':'Fryazino',

    'Хабаровск':'Khabarovsk','Ханты-Мансийск':'Khanty-Mansiysk','Хасавюрт':'Khasavyurt','Химки':'Khimki',

    'Чайковский':'Chaikovsky','Чапаевск':'Chapaevsk',
    'Чебоксары':'Cheboksary','Челябинск':'Chelyabinsk','Черемхово':'Cheremkhovo','Череповец':'Cherepovets',
    'Черкесск':'Cherkessk','Черногорск':'Chernogorsk','Чехов':'Chekhov','Чистополь':'Chistopol','Чита':'Chita',

    'Шадринск':'Shadrinsk','Шали':'Shawls',
    'Шахты':'Shahti','Шуя':'Shuya',

    'Щекино':'Shchekino', 'Щелково':'Schelkovo',

    'Электросталь':'Elektrostal', 'Элиста':'Elista', 'Энгельс':'Engels',

    'Южно-Сахалинск':'Yuzhno-Sakhalinsk', 'Юрга':'Yurga',

    'Якутск':'Yakutsk', 'Ялта':'Yalta', 'Ярославль':'Yaroslavl',

    'Все':'All'
}

class MainWork():

    # Функция иницилизации класса ( конструктор )
    def __init__(self, pasers):
        """ Создание расписания """
        self.scheduler = BackgroundScheduler()
        self.scheduler.start()
        self.start_schedule()

        """ Создание парсера """
        self.parseres = pasers

    # Функция создания нового расписаиня, со входными параметрами : url, id                 
    def NewSchedule(self, url, id):
        """
        Функция, где создается новое расписание.
        Каждое расписание имеет свои параметры:
            1) Критерий расписания : Интервал
            2) Время интервала (в секундах) : 60
            3) Персональный номер (id) : Персональная ссылка на страницу
            4) Аргументы : Персональная ссылка и индивидуальынй номер.

        Входные данные:
        :: url -> Ссылка (url-addres), которую мы будем парсить
        :: id  -> Индивидуальный номер пользователя в ТГ.

        Выходные данные:
        :: None

        """

        self.parser(url, id)

        # планирование задания
        self.scheduler.add_job(self.parser, 'interval', seconds=60,
                               id=url, args=[url, id])

    # Функция ассинхронного бесконечного цикла для расписания
    async def start_schedule(self):
        while True:
                 await asyncio.sleep(10)

    # Функция парсера со входными параметрами: *args
    def parser(self, *args):
        """
        Функция парса.
        ВХОДНЫЕ ПАРАМЕТРЫ:
        :: *args --> Список аргументов, который передается в разные переменные
            args[0] ---> url -> ссылка, которую мы передаем в парсер
            args[1] ---> id  -> индивидуальный номер пользователя, который написал в тг

        ВЫХОДНЫЕ ПАРАМЕТРЫ:
        :: None 
        """
        text, count = self.parseres.pars(args[0])
        if text != "":
            text_split = text.split("\n")
            new_text = []                       
            while len(text_split) != 1: # дробим наше сообщение на 10 равных сообщений (легче воспринимается пользоватаелем)
                text = ""
                for i in range(10):
                    if len(text_split) == 1:
                        break
                    text += text_split[0]+"\n"
                    text_split.remove(text_split[0])
                new_text.append(text)                           
            bot.send_message(chat_id=args[1], 
                             text="На странице \n" + args[0] + " \nпоявилось " + str(count) + " объявлений!", 
                             disable_web_page_preview=True)
            for i in new_text:
                bot.send_message(chat_id=args[1],
                                 text=i, 
                                 disable_web_page_preview=True)

        else:
            bot.send_message(args[1], "Нет ничего")

# Функция бота. Обработка события "сообщение /new"
@bot.message_handler(commands=['new'])
def start_message(message):
    """
    Функция, которыая обробатывает сообщение /new
    ВХОДНЫЕ ПАРАМЕТРЫ:
    :: message --> событие, tg-event
    """
    def create_url(message):
        """
            Функция - обработчик. 
            Функция обробатывает входное сообщение и создает рабочую ссылку. 
            ВХОДНЫЕ ПАРАМЕТРЫ::
            :: message --> событие, tg-event

            ОШИБКИ:
            :: Неверно введенный город --> функция отправляет сообщение об ошибке и сбрасывает результат
        """
        text = message.text
        if "https://www.avito.ru/" in text:
            work.NewSchedule(url=text+"&s=104", id=message.chat.id)

        else:
            text = text.split(",")
            city = ""
            for key, values in cityes.items():
                if key.lower() == text[0].lower():
                    city = values.lower() 
            if city != "":
                items = text[1].split(" ")
                url = f"https://www.avito.ru/{city}/?q="
                for i in items:
                    url += "+"+i
                url = url + "&s=104"
                work.NewSchedule(url=url,
                                 id=message.chat.id)
            else:
                bot.send_message(chat_id=message.chat.id,
                                 text="""
Вы указали не верный город, пожалуйста, повторите процедуру
""")

    
    bot.send_message(chat_id=message.chat.id,
                     text="""
Уважаемый пользователь, отправьте пожалуйста сообщение в формате:

https://www.avito.ru

или

Тольятти, Машина под ключ
""",
                     disable_web_page_preview=True)
    bot.register_next_step_handler(message, create_url) # передаем событие в след. функцию

# Функция бота. Обработка события "сообщение /del"
@bot.message_handler(commands=['del'])
def del_schedule(message):
    """
    Функция, которая обрабатывает событие /del
    ВХОДНЫЕ ПАРАМЕТРЫ:
    :: message --> tg-event
    """
    def deleted(message):
        """
        Функция, удаляет из расписание предмет
        ВХОДНЫЕ ПАРАМЕТРЫ:
        :: message --> tg-event
        """
        work.scheduler.remove_job(message.text)
        del work.parseres.site[message.text]
        if message.text in work.parseres.site:
            bot.send_message(message.chat.id,"Что-то пошло не так, повторите попытку", disable_web_page_preview=True)
        else:
            bot.send_message(message.chat.id,"Готово!", disable_web_page_preview=True)

    list_site = "Вот список всех активных ссылок: \n"
    for key, values in parseres.site.items():
        list_site+=key+"\n"+"\n"

    list_site+="Укажите ссылку, которую хотите удалить: "

    bot.send_message(message.chat.id,list_site, disable_web_page_preview=True)
    bot.register_next_step_handler(message,deleted)



if __name__ == "__main__":
    parseres = AvitoParser()
    work = MainWork(parseres)
    bot.infinity_polling()