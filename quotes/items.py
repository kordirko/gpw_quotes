# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class AkcjeItem(scrapy.Item):

    # define the fields for your item here like:
    # name = scrapy.Field()
    
    # https://www.biznesradar.pl/wiadomosci/PKN-ORLEN
    symbol_krotki = scrapy.Field()
    symbol = scrapy.Field()
    kurs = scrapy.Field()
    liczba_akcji = scrapy.Field()
    ostatnie_wiadomosci = scrapy.Field()

    # https://www.biznesradar.pl/dywidenda/PKN-ORLEN
    dyw_r_5 = scrapy.Field()
    dyw_r_4 = scrapy.Field()
    dyw_r_3 = scrapy.Field()
    dyw_r_2 = scrapy.Field()
    dyw_r_1 = scrapy.Field()
    dyw_r_0 = scrapy.Field()
    rok_dyw_0 = scrapy.Field()
    
    # https://www.biznesradar.pl/raporty-finansowe-rachunek-zyskow-i-strat/PKN-ORLEN
    zysk_r_5 = scrapy.Field()
    zysk_r_4 = scrapy.Field()
    zysk_r_3 = scrapy.Field()
    zysk_r_2 = scrapy.Field()
    zysk_r_1 = scrapy.Field()
    zysk_r_0 = scrapy.Field()
    rok_zysk_r_0 =  scrapy.Field()
    
    # https://www.biznesradar.pl/raporty-finansowe-rachunek-zyskow-i-strat/PKN-ORLEN,Q
    zysk_q_5 = scrapy.Field()
    zysk_q_4 = scrapy.Field()
    zysk_q_3 = scrapy.Field()
    zysk_q_2 = scrapy.Field()
    zysk_q_1 = scrapy.Field()
    zysk_q_0 = scrapy.Field()
    kwart_zysk_q_0 = scrapy.Field()
    
    # https://www.biznesradar.pl/wskazniki-wartosci-rynkowej/PKN-ORLEN,1
    # Cena / Wartość księgowa
    cena_wk = scrapy.Field()
    # Cena / Przychody ze sprzedaży
    cena_przychod = scrapy.Field()
    # Cena / Zysk
    cena_zysk = scrapy.Field()


    l_akcji_q_5 = scrapy.Field()
    l_akcji_q_4 = scrapy.Field()
    l_akcji_q_3 = scrapy.Field()
    l_akcji_q_2 = scrapy.Field()
    l_akcji_q_1 = scrapy.Field()
    l_akcji_q_0 = scrapy.Field()
    kwart_l_akcji_q_0 = scrapy.Field()


    l_akcji_r_5 = scrapy.Field()
    l_akcji_r_4 = scrapy.Field()
    l_akcji_r_3 = scrapy.Field()
    l_akcji_r_2 = scrapy.Field()
    l_akcji_r_1 = scrapy.Field()
    l_akcji_r_0 = scrapy.Field()
    rok_l_akcji_r_0 = scrapy.Field()
    
    # https://www.biznesradar.pl/rekomendacje-spolki/PKN-ORLEN
    reko_0 = scrapy.Field()
    reko_1 = scrapy.Field()
    reko_2 = scrapy.Field()
    reko_3 = scrapy.Field()
    
    pass