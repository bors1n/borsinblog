import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from django.test import LiveServerTestCase
from blog.models import Article
from datetime import datetime
import pytz
import os
import time

import undetected_chromedriver as uc
driver = uc.Chrome(version_main=117)

class BasicInstallTest(LiveServerTestCase):

    def setUp(self):
        self.browser = webdriver.Chrome('/Users/bors1n/Downloads/chromedriver_mac_arm64/chromedriver')
        staging_server = os.environ.get('STAGING_SERVER') #пытаемся загрузить из окружение ссылку в переменной staging_server
        if staging_server:
            self.live_server_url = 'http://' + staging_server

        Article.objects.create(title='title 1',
                               summary='summary 1',
                               full_text='full_test 1',
                               pubdate=datetime.utcnow().replace(tzinfo=pytz.utc),
                               slug='test_slug-1'
                               )
        Article.objects.create(title='title 2',
                               summary='summary 2',
                               full_text='full_test 2',
                               pubdate=datetime.utcnow().replace(tzinfo=pytz.utc),
                               slug='test_slug-2'
                               )
        Article.objects.create(title='title 3',
                               summary='summary 3',
                               full_text='full_test 3',
                               pubdate=datetime.utcnow().replace(tzinfo=pytz.utc),
                               slug='test_slug-3'
                               )
#так как LiveServerTestCase для тестов осздает новую базу, в ней нет статей
#добавили в setUp функционал с болванкой статьи для проведения тестов.
    def tearDown(self):
        #time.sleep(10)
        self.browser.quit()

    def test_home_page_title(self):
        # тест открытия сайта и загаловка сайта
        self.browser.get(self.live_server_url)
        self.assertIn('Borsin blog', self.browser.title)
        # self.fail('Finish the test!')

    def test_home_page_header(self):
        # тест шапки сайта
        self.browser.get(self.live_server_url)
        header = self.browser.find_element(By.CLASS_NAME, 'avatar-top')
        self.assertIn('Alexander Borsin', header.text)
        # self.fail('Finish the test!')

    def test_layout_and_styling(self):
        #тест внешнего вида страницы
        self.browser.get(self.live_server_url)
        self.browser.set_window_size(1024, 768)
        #проверяем загрузились ли стили
        footer = self.browser.find_element(By.CLASS_NAME, 'footer')
        self.assertTrue(footer.location['y'] > 200)

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

    def test_article_page_header_has_link_that_leads_to_home(self):
        self.browser.get(self.live_server_url)
        initial_url = self.browser.current_url

        article = self.browser.find_element(By.CLASS_NAME, 'article')
        article_title = article.find_element(By.CLASS_NAME, 'article-title')
        article_link = article_title.find_element(By.TAG_NAME, 'a')

        self.browser.get(article_link.get_attribute('href'))

        page_header = self.browser.find_element(By.CLASS_NAME, 'avatar-top')
        href_back = page_header.find_element(By.TAG_NAME, 'a').get_attribute('href')
        self.browser.get(href_back)

        final_url = self.browser.current_url

        self.assertEqual(initial_url, final_url)

    def test_favicon_icon(self):
        self.browser.get(self.live_server_url)
        head = self.browser.find_element(By.TAG_NAME, 'head')
        link = head.find_element(By.TAG_NAME, 'link')
        favicon = link.get_attribute('rel')
        self.assertEqual(favicon, 'shortcut icon')

    def test_about_page_has_link_that_leads_to_aboutpage(self):
        # посетитель зашел на сайт и уидиел надпись "обо мне"
        self.browser.get(self.live_server_url)
        about_page = self.browser.find_element(By.CLASS_NAME, 'about_page')
        #посетитель кликнул на надпись "обо мне"
        about_page_text = about_page.text
        about_page_link = about_page.find_element(By.TAG_NAME, 'a')
        #посетитель перешел по ссылке
        self.browser.get(about_page_link.get_attribute('href'))
        #посетитель видет заголовок страницы "Обо мне".
        about_page_title = self.browser.find_element(By.TAG_NAME, 'h1')
        self.assertIn(about_page_text, about_page_title.text)




if __name__ == '__main__':
    unittest.main()
