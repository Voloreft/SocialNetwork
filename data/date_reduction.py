import datetime
import pymorphy2


def reduct_date(date_elapsed):
    morph = pymorphy2.MorphAnalyzer()
    s = date_elapsed.seconds
    seconds = morph.parse('секунда')[0]
    min = s // 60
    mins = morph.parse('минута')[0]
    h = min // 60
    hours = morph.parse('час')[0]
    d = date_elapsed.days
    days = morph.parse('день')[0]
    m = d // 30
    months = morph.parse('месяц')[0]
    y = m // 365
    years = morph.parse('год')[0]
    if y > 0:
        return f'{y} {years.make_agree_with_number(y).word} назад'
    elif m > 0:
        return f'{m} {months.make_agree_with_number(y).word} назад'
    elif d > 0:
        return f'{d} {days.make_agree_with_number(y).word} назад'
    elif h > 0:
        return f'{h} {hours.make_agree_with_number(y).word} назад'
    elif min > 0:
        return f'{min} {mins.make_agree_with_number(y).word} назад'
    else:
        return f'{s} {seconds.make_agree_with_number(y).word} назад'
