import unittest

from selenium import webdriver
from selenium.webdriver.common.by import By
from django.test import LiveServerTestCase
from blog.models import Article
from datetime import datetime
import pytz


class BasicInstallTest(LiveServerTestCase):

    def setUp(self):
        self.browser = webdriver.Chrome()
        Article.objects.create(title='title 1',
                               summary='summary 1',
                               full_text='full_test 1',
                               pubdate=datetime.utcnow().replace(tzinfo=pytz.utc),
                               slug='test_slug'
                               )
#так как LiveServerTestCase для тестов осздает новую базу, в ней нет статей
#добавили в setUp функционал с болванкой статьи для проведения тестов.
    def tearDown(self):
        self.browser.quit()

    def test_home_page_title(self):
        # тест открытия сайта и загаловка сайта
        self.browser.get(self.live_server_url)
        self.assertIn('Borsin Blog', self.browser.title)
        # self.fail('Finish the test!')

    def test_home_page_header(self):
        # тест шапки сайта
        self.browser.get(self.live_server_url)
        header = self.browser.find_element(By.TAG_NAME, 'h1')
        self.assertIn('Alexander Borsin', header.text)
        # self.fail('Finish the test!')

    def test_layout_and_styling(self):
        #тест внешнего вида страницы
        self.browser.get(self.live_server_url)
        self.browser.set_window_size(1024, 768)
        #проверяем горизонтальный отступ заголовка
        header = self.browser.find_element(By.TAG_NAME, 'h1')
        self.assertTrue(header.location['x'] > 10)

    def test_home_page_blog(self):
        # проверка что под шапкой сайта расположен болк статей.
        self.browser.get(self.live_server_url)
        article_list = self.browser.find_element(By.CLASS_NAME, 'article-list')
        # находим блок статей.
        self.assertTrue(article_list)

    def test_home_page_articles_look_correct(self):
        # проверка что у каждой статьи есть заголовок и абзац с текстом
        self.browser.get(self.live_server_url)
        article_title = self.browser.find_element(By.CLASS_NAME, 'article-title')
        # находим статью, если есть заголовок статьи то есть и статья
        article_summary = self.browser.find_element(By.CLASS_NAME, 'article-summary')
        self.assertTrue(article_title)
        self.assertTrue(article_summary)

    def test_home_page_article_title_links_leads_to_article_page(self):
        # проверка того что в заголовке статьи есть ссылка
        self.browser.get(self.live_server_url)
        article_title = self.browser.find_element(By.CLASS_NAME, 'article-title')
        #находим ссылку в заголовке статьи
        article_title_text = article_title.text
        article_link = article_title.find_element(By.TAG_NAME, 'a')
        # переход по ссылки которую мы нашли
        self.browser.get(article_link.get_attribute('href'))

        article_page_title = self.browser.find_element(By.CLASS_NAME, 'article-title')
        self.assertIn(article_title_text, article_page_title.text)


if __name__ == '__main__':
    unittest.main()
