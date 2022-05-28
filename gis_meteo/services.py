from datetime import date


class GMGetter:
    def __init__(self):
        self.parsed = None
        self.main_div = None
        self.current_year = date.today().year

    @property
    def months_map(self):
        return {
            'января': 1,
            'февраля': 2,
            'марта': 3,
            'апреля': 4,
            'мая': 5,
            'июня': 6,
            'июля': 7,
            'августа': 8,
            'сентября': 9,
            'октября': 10,
            'ноября': 11,
            'декабря': 12,
        }

    @property
    def times_list(self):
        return [
            '00:00',
            '03:00',
            '06:00',
            '09:00',
            '12:00',
            '15:00',
            '18:00',
            '21:00',
        ]

    def get_month(self, month_name):
        return self.months_map.get(month_name)

    def load_data(self):
        import requests
        from bs4 import BeautifulSoup

        url = 'https://www.gismeteo.ru/weather-moscow-4368/gm/'
        r = requests.get(url, headers={
            'User-Agent': 'PostmanRuntime/7.28.3',
        })
        self.parsed = BeautifulSoup(r.text, 'html.parser')
        self.main_div = self.parsed.find_all("div", {"class": "gm-wrap"})[0]

    def prepare_page_data(self):
        res = []
        for idx_row, row in enumerate(self.main_div.find_all(recursive=False)):
            if idx_row == 0:  # Заголовочная часть
                continue
            items = row.find_all('div', recursive=False)
            res += self.prepare_row_data(items)
        return res

    def prepare_row_data(self, items):
        res = []
        prepared_date = None
        for idx, item in enumerate(items):
            if idx == 0:
                date_str = item.text.split(", ")[1]  # 'Ср, 18 мая' -> '18 мая'
                day_str, month_name = date_str.split(' ')  # -> ['18', 'мая']
                day, month = int(day_str), self.get_month(month_name)  # -> [18, 5]
                prepared_date = date(self.current_year, month, day)  # -> date(2022-05-18), using current year
            else:
                res.append([prepared_date, self.times_list[idx - 1], int(item.text)])
        return res

    def get_data(self):
        self.load_data()
        return self.prepare_page_data()
