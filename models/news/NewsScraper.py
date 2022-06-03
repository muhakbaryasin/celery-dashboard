from slugify import slugify
from datetime import datetime
from models.Scraper import Scraper
from db.news.repo.ArticleRepository import ArticleRepository
from db.news.repo.LanguageRepository import LanguageRepository
from db.news.repo.MediaRepository import MediaRepository
from db.news.repo.JournalistRepository import JournalistRepository
from models.xmlsettings import XMLSettings


class NewsScraper(object):
    url = None
    media_url = None
    category_path = None
    name = None
    page = 0
    last_page = None
    time_format = '%H:%M:%S'

    def __init__(self):
        self.scraper = Scraper()
        self.article_repo = ArticleRepository()
        self.media_repo = MediaRepository()
        self.lang_repo = LanguageRepository()
        self.jour_repo = JournalistRepository()
        self.config = XMLSettings(('conf_xml/' + self.__class__.__name__ + ".conf.xml").lower())

    def set_page_num(self, page_num):
        if not self.is_recently_accessed() and self.get_page_num() != 0:
            return

        self.config.put('page', page_num)
        self.config.save()

    def get_page_num(self) -> int:
        return int(self.config.get('page', 0))

    def update_last_accessed_time(self):
        self.config.put('time', datetime.now().strftime(self.time_format))
        self.config.save()

    def is_recently_accessed(self):
        saved_time = self.config.get('time', None)

        if saved_time is None:
            return False

        time_delta = datetime.now() - datetime.strptime(saved_time, self.time_format)

        if time_delta.seconds / 60 / 60 > 6:
            return False

        return True

    def get_list(self) -> list:
        pass

    def get_content(self, news) -> dict:
        pass

    def get_url(self):
        if self.is_recently_accessed():
            return self.get_next_url()

        return self.url

    def get_next_url(self) -> str:
        pass

    def next(self, recursive=True):
        media = self.media_repo.get_by_name(self.name)

        if media is None:
            media = self.media_repo.add({'name': self.name, 'url': self.media_url})

        lang = self.lang_repo.get_by_name('Bahasa Indonesia')

        if lang is None:
            lang = self.lang_repo.add({'name': 'Bahasa Indonesia'})

        news_list = self.get_list()
        exist = False

        for news in news_list:
            existing = self.article_repo.get_by_title(news['title'])

            if existing is not None:
                print(existing.id, existing.url)
                exist = True
            else:
                try:
                    article_entity = {}
                    news_content = self.get_content(news)

                    if news_content['author'] is None:
                        continue

                    article_entity['slug'] = slugify(news['title'])
                    article_entity['url'] = news['link']
                    article_entity['title_original'] = news['title']
                    article_entity['content'] = news_content['content']
                    article_entity['image'] = news_content['image']
                    article_entity['date'] = news_content['date']
                    article_entity['media_id'] = media.id
                    article_entity['language_id'] = lang.id

                    journalist = self.jour_repo.get_by_name(news_content['author'])

                    if journalist is None:
                        journalist = self.jour_repo.add({'name': news_content['author']})

                    article_entity['journalist_id'] = journalist.id
                    self.article_repo.add(article_entity)
                except:
                    print(article_entity)
                    raise Exception

        if self.get_url() == self.url:
            self.update_last_accessed_time()

        if recursive and exist:
            self.next()

    @staticmethod
    def convert_date_1(date_str):
        months = [(" Januari ", "-01-"),
                  (" Februari ", "-02-"),
                  (" Maret ", "-03-"),
                  (" April ", "-04-"),
                  (" Mei ", "-05-"),
                  (" Juni ", "-06-"),
                  (" Juli ", "-07-"),
                  (" Agustus ", "-08-"),
                  (" September ", "-09-"),
                  (" Oktober ", "-10-"),
                  (" November ", "-11-"),
                  (" Desember ", "-12-")]

        for month in months:
            if date_str.find(month[0]) > -1:
                return date_str.replace(month[0], month[1])

        raise Exception("Unrecognized date format {}".format(date_str))

    @staticmethod
    def convert_date_2(date_str):
        months = [(" January ", "-01-"),
                  (" February ", "-02-"),
                  (" March ", "-03-"),
                  (" April ", "-04-"),
                  (" May ", "-05-"),
                  (" June ", "-06-"),
                  (" July ", "-07-"),
                  (" August ", "-08-"),
                  (" September ", "-09-"),
                  (" October ", "-10-"),
                  (" November ", "-11-"),
                  (" December ", "-12-")]

        for month in months:
            if date_str.find(month[0]) > -1:
                return date_str.replace(month[0], month[1])

        raise Exception("Unrecognized date format {}".format(date_str))
