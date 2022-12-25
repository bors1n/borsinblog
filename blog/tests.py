from django.urls import resolve
from django.test import TestCase
from blog.views import home_page, article_page, about_page
from django.http import HttpRequest
from blog.models import Article
from datetime import datetime
import pytz
from django.urls import reverse


class ArticlePageTest(TestCase):
    def test_article_page_displays_correct_article(self):
        Article.objects.create(title='title 1',
                               summary='summary 1',
                               full_text='full_test 1',
                               pubdate=datetime.utcnow().replace(tzinfo=pytz.utc),
                               slug='test_slug'
                               )

        request = HttpRequest()
        response = article_page(request, 'test_slug')
        html = response.content.decode('utf8')

        self.assertIn('title 1', html)
        self.assertIn('full_test 1', html)
        self.assertNotIn('summary 1', html)


class HomePageTest(TestCase):

    def test_home_page_displays_articles(self):
        Article.objects.create(title='title 1',
                               summary='summary 1',
                               full_text='full_test 1',
                               pubdate=datetime.utcnow().replace(tzinfo=pytz.utc),
                               slug='slug-1'
                               )
        Article.objects.create(title='title 2',
                               summary='summary 2',
                               full_text='full_test 2',
                               pubdate=datetime.utcnow().replace(tzinfo=pytz.utc),
                               slug='slug-2'
                               )

        request = HttpRequest()
        response = home_page(request)
        html = response.content.decode('utf8')

        self.assertIn('title 1', html)
        self.assertIn('/blog/slug-1', html)
        self.assertIn('summary 1', html)
        self.assertNotIn('full_test 1', html)

        self.assertIn('title 2', html)
        self.assertIn('/blog/slug-2', html)
        self.assertIn('summary 2', html)
        self.assertNotIn('full_test 2', html)

    def test_home_page_returns_correct_html(self):
        url = reverse('home_page') #преабразует название из файла url в ссылку
        response = self.client.get(url) #получаем ответ из адреса ссылки
        self.assertTemplateUsed(response, 'home_page.html') #проверяем что в ответе загружен темлейт home_page


class AboutPageTest(TestCase):

    def test_about_page_returns_correct_html(self):
        url = reverse('about_page')
        response = self.client.get(url)
        self.assertTemplateUsed(response, 'about_page.html')


class ArticleModelTest(TestCase):

    def test_article_model_save_and_retrieve(self):
        #создать статью 1
        #сохране статью 1 в базе
        article1 = Article(
            title='artivle 1',
            full_text='full_text 1',
            summary='summary 1',
            category='category 1',
            pubdate =datetime.utcnow().replace(tzinfo=pytz.utc),
            slug='slug-1'
        )
        article1.save()
        #создай статью 2
        #сохрани статью 2 в базе
        article2 = Article(
            title='artivle 2',
            full_text='full_text 2',
            summary='summary 2',
            category='category 2',
            pubdate=datetime.utcnow().replace(tzinfo=pytz.utc),
            slug='slug-2'
        )
        article2.save()
        #загрузи из базы все статьи
        all_articles = Article.objects.all()
        #проверь: статей должно быть 2
        self.assertEqual(len(all_articles), 2)

        #проверь: 1 загруженная из базы статья == 1
        self.assertEqual(
            all_articles[0].title,
            article1.title
        )
        self.assertEqual(
            all_articles[0].slug,
            article1.slug
        )

        #проверь: 2 загруженная из базы статья == 2
        self.assertEqual(
            all_articles[1].title,
            article2.title
        )
        self.assertEqual(
            all_articles[1].slug,
            article2.slug
        )
