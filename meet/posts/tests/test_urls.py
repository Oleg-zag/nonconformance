from http import HTTPStatus

from django.core.cache import cache
from django.test import Client, TestCase

from ..models import Group, Post, User

INDEX_PAGE = '/'
GROUP_SLAG_PAGE = '/group/{group_slug}/'
PROFILE_ID_PAGE = '/profile/{author}/'
CREATE_PAGE = '/create/'
POSTS = '/posts/'
EDIT = '/edit/'
UNEXISTING_PAGE = '/unexisting_page/'
COMMENT = '/comment/'


class PostGroupURLTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create(username='auth')
        cls.user_1 = User.objects.create(username='auth_1')
        cls.group = Group.objects.create(
            title='тестовый заголовок',
            description='Тестовое описание',
            slug='test-slug',
        )

        cls.post = Post.objects.create(
            author=cls.user,
            text='Тестовый пост',
            pub_date='Тестовая дата',
            group=cls.group,
        )

    def setUp(self):
        '''Не/авторизированный клиент/пользователь'''
        self.guest_client = Client()
        self.authorized_client = Client()
        self.authorized_client_1 = Client()
        self.authorized_client.force_login(self.user)
        self.authorized_client_1.force_login(self.user_1)
        cache.clear()

    def test_URL_authorized_author_template_match(self):
        '''URL соответсвует шаблону для создателя поста (auth)'''
        templates_url_names = {
            INDEX_PAGE: 'posts/index.html',
            GROUP_SLAG_PAGE.format(
                group_slug=self.group.slug): 'posts/group_list.html',
            PROFILE_ID_PAGE.format(author=self.user): 'posts/profile.html',
            f'{POSTS}{self.post.id}/': 'posts/post_detail.html',
            f'{POSTS}{self.post.id}{EDIT}': 'posts/create_post.html',
            CREATE_PAGE: 'posts/create_post.html',
        }
        for address, template in templates_url_names.items():
            with self.subTest(address=address):
                response = self.authorized_client.get(address)
                self.assertTemplateUsed(response, template)

    def test_URL_authorized_nonauthor_template_match(self):
        '''URL соответствует шаблону для  авторизованного не автора'''
        templates_url_names = {
            INDEX_PAGE: 'posts/index.html',
            GROUP_SLAG_PAGE.format(
                group_slug=self.group.slug): 'posts/group_list.html',
            PROFILE_ID_PAGE.format(author=self.user): 'posts/profile.html',
            f'{POSTS}{self.post.id}/': 'posts/post_detail.html',
            CREATE_PAGE: 'posts/create_post.html',
        }
        for address, template in templates_url_names.items():
            with self.subTest(address=address):
                response = self.authorized_client_1.get(address)
                self.assertTemplateUsed(response, template)

    def test_URL_nonauthorized_template_match(self):
        '''URL соответсвует шаблону для гостя'''
        templates_url_names = {
            INDEX_PAGE: 'posts/index.html',
            GROUP_SLAG_PAGE.format(
                group_slug=self.group.slug): 'posts/group_list.html',
            PROFILE_ID_PAGE.format(author=self.user): 'posts/profile.html',
            f'{POSTS}{self.post.id}/': 'posts/post_detail.html',
        }
        for address, template in templates_url_names.items():
            with self.subTest(address=address):
                response = self.guest_client.get(address)
                self.assertTemplateUsed(response, template)

    def test_URL_get_urls_for_athorized_nonauth(self):
        '''Доступ к страницам для авторизованного пользователя'''
        urls_HTTP_names = {
            INDEX_PAGE: HTTPStatus.OK,
            PROFILE_ID_PAGE.format(author=self.user): HTTPStatus.OK,
            GROUP_SLAG_PAGE.format(group_slug=self.group.slug): HTTPStatus.OK,
            f'{POSTS}{self.post.id}/': HTTPStatus.OK,
            f'{POSTS}{self.post.id}{EDIT}': HTTPStatus.FOUND,
            CREATE_PAGE: HTTPStatus.OK,
            UNEXISTING_PAGE: HTTPStatus.NOT_FOUND,
        }
        for page, htp in urls_HTTP_names.items():
            with self.subTest(address=page):
                response = self.authorized_client_1.get(page)
                self.assertEqual(response.status_code, htp)

    def test_URL_get_urls_for_non_athorized(self):
        '''Доступ к страницам для гостя'''
        urls_HTTP_names = {
            INDEX_PAGE: HTTPStatus.OK,
            PROFILE_ID_PAGE.format(author=self.user): HTTPStatus.OK,
            GROUP_SLAG_PAGE.format(group_slug=self.group.slug): HTTPStatus.OK,
            f'{POSTS}{self.post.id}/': HTTPStatus.OK,
            f'{POSTS}{self.post.id}{EDIT}': HTTPStatus.FOUND,
            CREATE_PAGE: HTTPStatus.FOUND,
            UNEXISTING_PAGE: HTTPStatus.NOT_FOUND,
        }
        for page, htp in urls_HTTP_names.items():
            with self.subTest(address=page):
                response = self.guest_client.get(page)
                self.assertEqual(response.status_code, htp)

    def test_URL_get_urls_for_athorized_auth(self):
        '''Доступ к страницам для создателя поста (auth)'''
        urls_HTTP_names = {
            INDEX_PAGE: HTTPStatus.OK,
            PROFILE_ID_PAGE.format(author=self.user): HTTPStatus.OK,
            GROUP_SLAG_PAGE.format(group_slug=self.group.slug): HTTPStatus.OK,
            f'{POSTS}{self.post.id}/': HTTPStatus.OK,
            f'{POSTS}{self.post.id}{EDIT}': HTTPStatus.OK,
            CREATE_PAGE: HTTPStatus.OK,
            UNEXISTING_PAGE: HTTPStatus.NOT_FOUND,
        }
        for page, htp in urls_HTTP_names.items():
            with self.subTest(address=page):
                response = self.authorized_client.get(page)
                self.assertEqual(response.status_code, htp)

    def test_URL_nonathorized_nonauth_correct_riderect(self):
        '''/create перенаправит неавторизованного
        пользователя на страницу /auth/login/?next=/.
        '''
        urls_HTTP_names = {
            f'{POSTS}{self.post.id}{COMMENT}':
            f'/auth/login/?next={POSTS}{self.post.id}{COMMENT}',
            CREATE_PAGE: '/auth/login/?next=/create/',
        }
        for page, pages in urls_HTTP_names.items():
            with self.subTest(address=page):
                response = self.guest_client.get(
                    page, follow=True)
                self.assertRedirects(
                    response, pages)

    def test_urls_get_for_athorized_nonauth_correct_riderect(self):
        ''' Страница post/detail/EDIT перенаправит авторизованного
        пользователя на автора на страницу /post/detail/
        '''
        urls_HTTP_names = [
            f'{POSTS}{self.post.id}{COMMENT}',
            f'{POSTS}{self.post.id}{EDIT}',
        ]
        for page in urls_HTTP_names:
            with self.subTest(address=page):
                response = self.authorized_client_1.get(
                    page, follow=True)
                self.assertRedirects(
                    response, f'{POSTS}{self.post.id}/')
