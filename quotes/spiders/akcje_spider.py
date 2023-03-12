import scrapy
from ..items import AkcjeItem

class AkcjeSpider(scrapy.Spider):
    
    name = "akcje-full"
    
    default_filename= "symbole.txt"
    
    url_prefix= "https://www.biznesradar.pl"
    
    custom_settings = {
            'FEED_EXPORT_FIELDS': [
                'symbol_krotki', 'symbol', 'kurs', 'liczba_akcji', 'ostatnie_wiadomosci',
                'dyw_r_5','dyw_r_4','dyw_r_3','dyw_r_2','dyw_r_1','dyw_r_0','rok_dyw_0',
                'zysk_r_5','zysk_r_4','zysk_r_3','zysk_r_2','zysk_r_1','zysk_r_0','rok_zysk_r_0',
                'zysk_q_5','zysk_q_4','zysk_q_3','zysk_q_2','zysk_q_1','zysk_q_0','kwart_zysk_q_0',
                'cena_wk','cena_przychod','cena_zysk',
                'l_akcji_q_5','l_akcji_q_4','l_akcji_q_3','l_akcji_q_2','l_akcji_q_1','l_akcji_q_0','kwart_l_akcji_q_0',
                'l_akcji_r_5','l_akcji_r_4','l_akcji_r_3','l_akcji_r_2','l_akcji_r_1','l_akcji_r_0','rok_l_akcji_r_0',
                'reko_0','reko_1','reko_2','reko_3',
             ]
         }


    def parse_news(self, response, original_symbol):
    
        # https://www.biznesradar.pl/wiadomosci/PKN-ORLEN
    
        number_of_actions_as_string = response.xpath("//*[@class='profileSummary']//a[starts-with(@href,'/akcjonariat')]/text()").get().replace(' ','')
        
        data = AkcjeItem()

        data['symbol_krotki'] = original_symbol
        data['symbol']        = response.xpath("//a[starts-with(@href,'/notowania-historyczne')]/@href").get().split('/')[-1]
        data['kurs']          = float(response.xpath("//*[@class='q_ch_act']/text()").get())
        data['liczba_akcji']  = int(number_of_actions_as_string)
        data['ostatnie_wiadomosci'] = response.xpath("//*[@class='record record-type-NEWS']/*[@class='record-footer' and contains(.,'ESPI')]/*[@class='record-date']/text()").get()
        
        if hasattr(self,'full'):
            yield scrapy.Request(url=self.url_prefix + '/dywidenda/' + data.get('symbol'), callback=self.parse_dividends, cb_kwargs=dict(data=data))
        else:
            yield data
        
        
        
    def parse_dividends(self, response, data):
    
        # https://www.biznesradar.pl/dywidenda/PKN-ORLEN
        
        divs_table = response.xpath("//*[@id='dividends']//*[@class='table-c']/table//tr[./td]")

        dividends = [( row.xpath("./td[1]/text()").get(), row.xpath("./td[3]/*/text()").get()) for row in divs_table]
        div_values = [float(x) if x.replace('.','').isdigit() else None for x in [d[1] for d in dividends]][:6]
        for i,d in [x for x in enumerate(div_values)][::-1]:
            data[f"dyw_r_{i}"] = d
        
        data['rok_dyw_0'] = dividends[0][0]
        
        yield scrapy.Request(url=self.url_prefix + '/raporty-finansowe-rachunek-zyskow-i-strat/' + data.get('symbol'), callback=self.parse_financial_profit_year, cb_kwargs=dict(data=data))
        
        
    
    def parse_financial_profit_year(self, response, data):
    
        # https://www.biznesradar.pl/raporty-finansowe-rachunek-zyskow-i-strat/PKN-ORLEN
    
        # //*[@class='report-table']//th[starts-with(@class,'thq')]
        # //*[@class='report-table']//tr[@data-field='IncomeShareholderNetProfit']//td[starts-with(@class,'h')]/*[@class='value']/span/span/text()
        header_selectors = response.xpath("//*[@class='report-table']//th[starts-with(@class,'thq')]")
        headers=[q.get().replace('\t','').replace('\n','') for q in [x.xpath('./text()')[0] for x in header_selectors]][-6:]
        value_selectors = response.xpath("//*[@class='report-table']//tr[@data-field='IncomeShareholderNetProfit']//td[starts-with(@class,'h')]/*[@class='value']/span/span/text()")
        values =[d.replace(' ','') for d in value_selectors[-6:].getall()]
        
        for i,v in [v for v in enumerate(values[::-1])][::-1]:
            data[f"zysk_r_{i}"] = int(v)
            
        data['rok_zysk_r_0'] = headers[-1]
        
        yield scrapy.Request(url=self.url_prefix + '/raporty-finansowe-rachunek-zyskow-i-strat/' + data.get('symbol') + ',Q', callback=self.parse_financial_profit_quarter, cb_kwargs=dict(data=data))
        
        
    def parse_financial_profit_quarter(self, response, data):
    
        # https://www.biznesradar.pl/raporty-finansowe-rachunek-zyskow-i-strat/TORPOL,Q
    
        # //*[@class='report-table']//th[starts-with(@class,'thq')]
        # //*[@class='report-table']//tr[@data-field='IncomeShareholderNetProfit']//td[starts-with(@class,'h')]/*[@class='value']/span/span/text()
        header_selectors = response.xpath("//*[@class='report-table']//th[starts-with(@class,'thq')]")
        headers=[q.get().replace('\t','').replace('\n','') for q in [x.xpath('./text()')[0] for x in header_selectors]][-6:]
        value_selectors = response.xpath("//*[@class='report-table']//tr[@data-field='IncomeShareholderNetProfit']//td[starts-with(@class,'h')]/*[@class='value']/span/span/text()")
        values =[d.replace(' ','') for d in value_selectors[-6:].getall()]
        
        for i,v in [v for v in enumerate(values[::-1])][::-1]:
            data[f"zysk_q_{i}"] = int(v)
            
        data['kwart_zysk_q_0'] = headers[-1]
        
        yield scrapy.Request(url=self.url_prefix + '/wskazniki-wartosci-rynkowej/' + data.get('symbol') + ',1', callback=self.parse_indicators, cb_kwargs=dict(data=data))
        
        
    def parse_indicators(self, response, data):
    
        # https://www.biznesradar.pl/wskazniki-wartosci-rynkowej/PKN-ORLEN,1
        
        # Cena / Wartość księgowa
        c_wk_str = response.xpath("//*[@data-field='CWKCurrent']//*[@class='h newest']//*[@class='pv']/span/text()").get()
        data['cena_wk'] = float(c_wk_str) if c_wk_str is not None and c_wk_str.replace('.','').isnumeric() else None
        
        # Cena / Przychody ze sprzedaży 
        c_przychod_str = response.xpath("//*[@data-field='CPCurrent']//*[@class='h newest']//*[@class='pv']/span/text()").get()
        data['cena_przychod'] = float(c_przychod_str) if c_przychod_str is not None and c_przychod_str.replace('.','').isnumeric() else None
        
        # Cena / Zysk
        c_zysk_str = response.xpath("//*[@data-field='CZCurrent']//*[@class='h newest']//*[@class='pv']/span/text()").get()
        data['cena_zysk'] = float(c_zysk_str) if c_zysk_str is not None and c_zysk_str.replace('.','').isnumeric() else None
        
        # liczba akcji na koniec kwartału
        headers = [x for x in response.xpath("//*[@class='report-table']//th[starts-with(@class,'thq')]/text()").getall()][::2]
        headers = [h.replace('\n','').replace('\t','') for h in headers]
        
        shares = response.xpath("//*[@class='report-table']//tr[@data-field='ShareAmountCurrent']//*[@class='pv']/span/text()").getall()
        
        for i,v in [x for x in enumerate(shares[-6:][::-1])]:
            data[f"l_akcji_q_{i}"] = int(v.replace(' ',''))
            
        data['kwart_l_akcji_q_0'] = headers[-1]
        
        # liczba akcji na koniec roku (Q4)
        headers_shares = [x for x in zip(headers,shares)]
        for i,v in [x for x in enumerate([y for x,y in headers_shares if 'Q4' in x][-6:][::-1])]:
           data[f"l_akcji_r_{i}"] = int(v.replace(' ',''))
        
        data['rok_l_akcji_r_0'] = [x for x in headers if 'Q4' in x][-1]
        
        yield scrapy.Request(url=self.url_prefix + '/rekomendacje-spolki/' + data.get('symbol'), callback=self.parse_recommendations, cb_kwargs=dict(data=data))
    
        
        
    def parse_recommendations(self, response, data):
    
        # https://www.biznesradar.pl/rekomendacje-spolki/PKN-ORLEN
    
        recommendations = response.xpath("//table[contains(@class,'recommendations')]//tr/td[2]/text()").getall()
        
        for i,v in enumerate(recommendations[:4]):
            data[f"reko_{i}"] = float(v) if v.replace('.','').isnumeric() else None
        
        yield data

    qq = [
            ("/wiadomosci/{}", parse_news),
            ("/dywidenda/{}", parse_dividends),
            ("/raporty-finansowe-rachunek-zyskow-i-strat/{}", parse_financial_profit_year),
            ("/raporty-finansowe-rachunek-zyskow-i-strat/{},Q", parse_financial_profit_quarter),
            ("/wskazniki-wartosci-rynkowej/{},1", parse_indicators),
            ("/rekomendacje-spolki/{}", parse_recommendations)

        ]

    def start_requests(self):
        symbols_filename = getattr(self, 'symbole') if hasattr(self, 'symbole') else self.default_filename

        with open(symbols_filename) as f:
            symbols = [line.rstrip() for line in f]

        for symbol in symbols:
            yield scrapy.Request(url=self.url_prefix + '/wiadomosci/' + symbol, callback=self.parse_news,
                                 cb_kwargs=dict(original_symbol=symbol))

