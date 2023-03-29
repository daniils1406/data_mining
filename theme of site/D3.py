import re
import nltk
import numpy as np
import torch
import math
import operator
from scipy import spatial
from collections import Counter
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from scipy.spatial import distance
import torch.nn.functional as F
from sklearn.metrics.pairwise import cosine_similarity,cosine_distances
nltk.download('stopwords')
from nltk.corpus import stopwords
stop_words = set(stopwords.words('russian'))
import requests
from bs4 import BeautifulSoup

WORD = re.compile(r"\w+")

def get_cosine(vec1, vec2):
    intersection = set(vec1.keys()) & set(vec2.keys())
    numerator = sum([vec1[x] * vec2[x] for x in intersection])

    sum1 = sum([vec1[x] ** 2 for x in list(vec1.keys())])
    sum2 = sum([vec2[x] ** 2 for x in list(vec2.keys())])
    denominator = math.sqrt(sum1) * math.sqrt(sum2)

    if not denominator:
        return 0.0
    else:
        return float(numerator) / denominator


def text_to_vector(text):
    words = WORD.findall(text)
    return Counter(words)


raw_science_words_original="физика химия математика биология знания школа учёный профессор научный учение учитель учёба учить университет опыт история исследование книга открытие лаборатория институт философия астрономия космос география эксперимент техника ум прогресс жизнь изучать формула изучение медицина учебник предмет микроскоп диссертация мозг Ньютон теория психология Эйнштейн халат геометрия изобретение гранит работа человек урок технология люди умный доктор алгебра информатика очки разум студент академик анатомия Ломоносов филология труд ученик ботаника зоология литература язык колба мозги диплом премия академия гипотеза кандидат искусство степень учиться философ практика пробирка развитие преподаватель точная мир врач идея закон физик деньги доклад истина логика кафедра природа теорема генетика лаборант обучение учёные магистр научная фантастика монография статистика доцент филолог нанотехнологии методология обсерватория геолог феномен физиология фразеология геральдика тригонометрия метрика доктрина экспедиция метод изобретатель освоение хронология теоретик идеология термодинамика частицы термин терминология альберт эйнштейн лаборантка семантика этика опыты механика реактивы учения клонирование нейтрон фотон мифология лингвист материализм протон формулы ген литературовед языкознание фермент эколог агроном светило отрасль астроном гибрид тяготение патология симпозиум лауреат аналогия аспирантура просвещение флористика ион трактат номенклатура дипломатия сионизм вектор орбитальная станция пробирки инфузория трансцендентность концепция конференция методика факт атеист специфика углеводород ликбез публицистика одноклеточный навигация социум понятие премудрость парадокс изотоп учебники арифметика зоотехника наблюдение атомы роботы наклонность прорыв фразеологизм самоучитель структура"
raw_sport_words_original="футбол   бег   баскетбол   спортсмен   здоровье   волейбол   мяч   хоккей   соревнование   игра   Олимпиада   теннис   сила   тренер   плавание   лыжи   бокс   победа   тренировка   прыжки   жизнь   спортивный   чемпион   медаль   шахматы   мышцы   кроссовки   атлетика   матч   штанга   чемпионат   травма   физкультура   судья   команда   гимнастика   стадион   спортзал   гольф   танцы   коньки   фитнес   биатлон   ракетка   заниматься   зал   регби   борьба   гантели   велосипед   пот   гандбол   занятие   тренажёр   гол   вода   рекорд   награда   пресс   финиш   форма   турнир   человек   труд   атлет   старт   ворота   клюшка   мускулы   болельщики   кубок   шайба   допинг   движение   скакалка   скорость   велоспорт   выносливость   дух   время   бейсбол   достижения   поле   тело   гонки   успех   бассейн   упражнения   гиря   игроки   мир   Сочи   боль   счёт   мастер   снаряд   ходьба   зарядка   тайм   бутсы олимпийские игры   лёгкая атлетика   фигурное катание   тяжёлая атлетика   вид спорта   здоровый образ жизни   конный спорт   большой спорт   водное поло   спортивная одежда   спортивный костюм   спортивный комплекс   спортивная гимнастика   мастер спорта   спортивная ходьба   спортивный человек   американский футбол   спортивный зал   спортивные игры   спортивная форма   спортивное питание   синхронное плавание   спортивные соревнования"
raw_shopping_words_original="покупки   магазин   деньги   одежда   вещи   товар   обувь   шоп   трата   девушка   платье   сумка   шмотки   пакеты   покупать   болезнь   туфли   распродажа   бутик   подруги   продавец   скидки   женщина   цена   супермаркет   подарки   Милан   карта   центр   покупатель   Сейл   мода   макет   доллар   сапоги   радость   Нью-Йорк   фетишизм   примерочная   дура   жена   акция   дамочка   кошелёк   сумочка   тёлочки   растрата   ресторан   торговый   хождение   маркетинг   потребление   развлечение   удовольствие   муж   чек   очки   шуба   Бренд   город   касса   мания   марки   поход   шляпа   времени   молодёжь   общество"
raw_news_words_original="телевизор   газета   вести   радио   канал   Интернет   политика   погода   плохие   хорошие   телевидение   война   СМИ   Украина   журнал   новость   новое   ведущий   события   сплетни   смотреть   время   интервью   информация   журналист   люди   программа   пресса   телефон   президент   свежие   спорт   убийство   интересные   ведущая   передача   пожар   Россия   читать   слушать   мир   новый   письмо   статья   страна   известие   репортаж   репортёр   дня   Путин   получать   разговор   интересно   происшествия   дом   жизнь   книга   камера   радость   реклама   премьера   объявление   вечер   новые   почта   слухи   страх   диктор   знания   правда   смерть   рассказ   сенсация   сообщение   Крым   ложь   утро   лента   повод   факты   авария   выпуск   друзья   интерес   слышать   компьютер   рассказать   телеграмма   расследования   важные   ведущие газеты   сводка   газетка   НТВ   газетчик   эфир   корреспондент   телеканал   хроника   вконтакте   радиоприёмник   осведомитель   радиостанция   публицистика   стенгазета   журналистика   радиоузел   сообщения   рубрика   журналистка   журналы   редакция   транзистор   приёмник   Яндекс   телекомпания   твиттер   говорить   Фейсбук   прогноз   обозрение   факт   редактор   глянец   синоптик   киножурнал   циклон   просмотр   комментатор   сплетница   телезритель   гугл   внимание   прогноз погоды   распространение   онлайн   радиограмма   дирижабль   антисемитизм   совещание   важное   заголовок   оон (организация объединённых наций)   магнитофон   антициклон   итоги   экран   обсуждение   панорама   тема   пропаганда   очевидец   реальность   катастрофа   сайт   бюллетень   плазма   антенна   болтовня   комсомолка   контакт   мнения   юстиция   альманах   подписка   развитие   показание   тираж   диалог   печать   источник   ленточка   поиск   завтрак   издательство   итог   переписка   кризис   диван   читатель   собеседник   полдень   государство   сеть   писать   влияние   преступник   общество   чупакабра   инаугурация "

lower_raw_sciense_word=raw_science_words_original.lower()
lower_raw_sport_word=raw_sport_words_original.lower()
lower_raw_shopping_word=raw_shopping_words_original.lower()
lower_raw_news_word=raw_news_words_original.lower()

no_wspace_raw_sciense_word = lower_raw_sciense_word.strip()
no_wspace_raw_sport_word = lower_raw_sport_word.strip()
no_wspace_raw_shopping_word = lower_raw_shopping_word.strip()
no_wspace_raw_news_word = lower_raw_news_word.strip()

lst_sciense_string = [no_wspace_raw_sciense_word][0].split()
lst_sport_string = [no_wspace_raw_sport_word][0].split()
lst_shopping_string = [no_wspace_raw_shopping_word][0].split()
lst_news_string = [no_wspace_raw_news_word][0].split()


for i in lst_sciense_string:
    if i in stop_words:
        lst_sciense_string.remove(i)

for i in lst_sport_string:
    if i in stop_words:
        lst_sport_string.remove(i)

for i in lst_shopping_string:
    if i in stop_words:
        lst_shopping_string.remove(i)

for i in lst_news_string:
    if i in stop_words:
        lst_news_string.remove(i)


def get_text(url):
    rs = requests.get(url)
    root = BeautifulSoup(rs.content, 'html.parser')
    article = root.select_one('article')

    return article.text


url = 'https://habr.com/ru/company/spbifmo/blog/343320/'
text = get_text(url)
text=text.lower()
text=text.strip()
vectortext = text_to_vector(text)
text = [text][0].split()
for i in text:
    if i in stop_words:
        text.remove(i)



vectorscience = text_to_vector(raw_science_words_original)
vectorsport = text_to_vector(raw_sport_words_original)
vectorshopping = text_to_vector(raw_shopping_words_original)
vectornews = text_to_vector(raw_news_words_original)

print("ТЕМАТИКИ ПО МЕТРИКЕ КОСИНУСА")
print("НАУКА:",get_cosine(vectortext,vectorscience))
print("СПОРТ:",get_cosine(vectortext,vectorsport))
print("ШОППИНГ:",get_cosine(vectortext,vectorshopping))
print("НОВОСТИ:",get_cosine(vectortext,vectornews))


def jaccard(list1, list2):
 intersection = len(list(set(list1).intersection(list2)))
 union = (len(list1) + len(list2)) - intersection
 return float(intersection) / union


jaccardresult=[]
jaccardresult.append(jaccard(text, lst_sciense_string))
jaccardresult.append(jaccard(text, lst_sport_string))
jaccardresult.append(jaccard(text, lst_shopping_string))
jaccardresult.append(jaccard(text, lst_news_string))

max=0
for result in jaccardresult:
    if(result>max):
        max=result

print("ТЕМАТИКИ ПО ЖАККАРДУ")
print("НАУКА: ",jaccardresult[0])
print("СПОРТ: ",jaccardresult[1])
print("ШОППИНГ: ",jaccardresult[2])
print("НОВОСТИ: ",jaccardresult[3])