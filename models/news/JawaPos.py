from urllib.parse import urlencode
import json
from lxml.etree import ParserError
from pyquery import PyQuery as Pq
from models.news.NewsScraper import NewsScraper


class JawaPos(NewsScraper):
    url = 'https://www.jawapos.com/berita-hari-ini/?date=&category=117888'
    more = 'https://www.jawapos.com/desktop-get-posts'
    params = {'section': 'search', 'post_type[0]': 'post', 'per_page': 15,
              'taxonomy': 'category', 'terms': '117888', 'date': '', 'security': '23bc90a48c', 'page_no': 2}
    last_page = None
    name = 'JawaPos'
    page = 1
    media_url = 'https://www.jawapos.com'
    category_path = '/ekonomi/'

    @staticmethod
    def convert_date(date_str):
        return NewsScraper.convert_date_1(date_str)

    def get_list(self):
        page = self.get_page_num()

        if page <= 1:
            page = 1

        url = self.get_url()

        if url.find('desktop') > -1:
            self.last_page = json.loads(
                self.scraper.request_data(url=url, method="POST", data=urlencode(self.params).encode()))['posts']
        else:
            self.last_page = self.scraper.request_data(url=url, method="GET")

        try:
            links = Pq(self.last_page)('.post-list__item')('.post-list__title')('h3')('a')
        except ParserError:
            print('Requested document is empty {}'.format(url))
            return []

        items = []

        for link in links:
            link_el = Pq(link)
            a_href = link_el.attr('href')

            if a_href.find(self.category_path) > -1:
                a_title = link_el.text().strip()

                items.append({'link': a_href + '?page=all', 'title': a_title})

        self.set_page_num(page + 1)

        return items

    def get_content(self, news):
        content = Pq(self.scraper.request_data(url=news['link'], method="GET"))

        if content is None:
            return None

        date = content('.single-meta')('.time').text().split(',')[0].split(' ')
        date = self.convert_date("{} {} {:02d}".format(date[2], date[1], int(date[0])))
        return {'content': content('.content')('p').text(),
                'author': content('.content-reporter')('p').eq(0).text().replace('Editor : ', '').strip(),
                'image': content('.single-featured')('img').attr('data-src'), 'date': date}

    def get_next_url(self) -> str:
        page = self.get_page_num()

        if page <= 1:
            page = 1

        url = self.more
        self.params['page_no'] = page

        return url


class JawaPosBisnis(JawaPos):
    url = 'https://www.jawapos.com/berita-hari-ini/?date=&category=117887'
    params = {'section': 'search', 'post_type[0]': 'post', 'per_page': 15, 'taxonomy': 'category', 'terms': '117887',
              'date': '', 'security': '23bc90a48c', 'page_no': 2}


class JawaPosFinance(JawaPos):
    url = 'https://www.jawapos.com/berita-hari-ini/?date=&category=117893'
    params = {'section': 'search', 'post_type[0]': 'post', 'per_page': 15, 'taxonomy': 'category', 'terms': '117893',
              'date': '', 'security': '23bc90a48c', 'page_no': 2}


class JawaPosNasional(JawaPos):
    url = 'https://www.jawapos.com/berita-hari-ini/?date=&category=117875'
    params = {'section': 'search', 'post_type[0]': 'post', 'per_page': 15, 'taxonomy': 'category', 'terms': '117875',
              'date': '', 'security': '23bc90a48c', 'page_no': 2}
    category_path = '/nasional/'
