from django import forms
from django.core.cache import cache
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import Client, TestCase
from django.urls import reverse

from posts.models import Comment, Follow, Group, Post, User
from posts.utils import POSTS_PAR_PAGE

POSTS_ON_SECOND_PAGE = 4
TOTAL_POSTS = POSTS_PAR_PAGE + POSTS_ON_SECOND_PAGE


class PostViewsTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create(username='auth')
        cls.group = Group.objects.create(
            title='тестовый заголовок',
            description='Тестовое описание',
            slug='test-slug',
        )

        cls.group_1 = Group.objects.create(
            title='тестовый заголовок_1',
            description='Тестовое описание_1',
            slug='test-slug_1',
        )
        small_gif = (
            b'\x47\x49\x46\x38\x39\x61\x01\x00'
            b'\x01\x00\x00\x00\x00\x21\xf9\x04'
            b'\x01\x0a\x00\x01\x00\x2c\x00\x00'
            b'\x00\x00\x01\x00\x01\x00\x00\x02'
            b'\x02\x4c\x01\x00\x3b'
        )
        uploaded = SimpleUploadedFile(
            name='small.gif',
            content=small_gif,
            content_type='image/gif')

        cls.post = Post.objects.create(
            author=cls.user,
            text='Тестовый пост',
            group=cls.group,
            image=uploaded)

        cls.comment = Comment.objects.create(
            text='Тестовый комментарий',
            author=cls.user,
            post=cls.post,
        )

    def setUp(self):
        '''Не/авторизированный клиент/пользователь'''
        self.guest_client = Client()
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)
        cache.clear()

    def test_views_template_authorized_nonauth(self):
        '''veiw работает с правильным шаблоном для
        авторизированного пользователя
        '''
        template_pages_names = {
            reverse('posts:index'): 'posts/index.html',
            reverse('posts:group_list', args=(self.group.slug,)):
                'posts/group_list.html',
            reverse('posts:profile', args=(self.user,)):
                'posts/profile.html',
            reverse('posts:post_detail', args=(self.post.id,)):
                'posts/post_detail.html',
            reverse('posts:post_edit', args=(self.post.id,)):
                'posts/create_post.html',
            reverse('posts:add_comment', args=(self.post.id,)):
                'posts/post_detail.html',
        }
        for reverse_name, template in template_pages_names.items():
            with self.subTest(reverse_name=reverse_name):
                responce = self.authorized_client.get(
                    reverse_name, follow=True)
                self.assertTemplateUsed(responce, template)

    def test_views_check_context_combined(self):
        '''в index, group_list, profile передан правильный контекст'''
        context_name = [
            reverse('posts:index'),
            reverse('posts:group_list', args=(self.group.slug,)),
            reverse('posts:profile', args=(self.post.author,)),
        ]
        for reverse_name in context_name:
            with self.subTest(reverse_name=reverse_name):
                response = self.authorized_client.get(reverse_name)
                res_post = response.context['page_obj'][0]
                self.assertEqual(res_post.group, self.group)
                self.assertEqual(res_post.author, self.user)
                self.assertEqual(res_post.text, self.post.text)
                self.assertEqual(res_post.image, self.post.image)

    def test_views_check_context_post_detail(self):
        '''в post_detail передан правильный контекст'''
        response = self.authorized_client.get(
            reverse('posts:post_detail', args=(self.post.id,)))
        self.assertEqual(
            response.context.get('post_detail').group, self.group)
        self.assertEqual(
            response.context.get('post_detail').author, self.user)
        self.assertEqual(
            response.context.get('post_detail').text, self.post.text)

    def test_views_check_create_edit_post(self):
        '''в create_post  передан правильный контекст'''
        response = self.authorized_client.get(
            reverse('posts:post_edit', args=(self.post.id,)))
        self.assertTrue(response.context['is_edit'])
        self.assertTrue(response.context['form'])

    def test_views_check_forms_create_edit_post(self):
        '''тест формы создания/редактирования поста'''
        context_name = [
            reverse('posts:post_create'),
            reverse('posts:post_edit', args=(self.post.id,)),
        ]
        form_fields = {

            'text': forms.fields.CharField,
            'group': forms.fields.ChoiceField,
            'image': forms.fields.ImageField,
        }
        for reverse_name in context_name:
            with self.subTest(reverse_name=reverse_name):
                response = self.authorized_client.get(reverse_name)
                for value, expected in form_fields.items():
                    form_field = response.context.get(
                        'form').fields.get(value)
                    self.assertIsInstance(form_field, expected)

    def test_views_post_with_group_in_correct_page(self):
        '''Пост с группой не попал на страницу с неправильной группой'''
        response = self.authorized_client.get(
            reverse('posts:group_list', args=(self.group_1.slug,)))
        self.assertEqual(len(response.context['page_obj']), 0)

    def test_views_comments_add(self):
        '''комментарий передан на страницу поста'''
        response = self.authorized_client.get(
            reverse('posts:post_detail', args=(self.post.id,)))
        self.assertEqual(len(response.context['comments']), 1)


class PostViewsPaginatorTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create(username='auth')
        cls.group = Group.objects.create(
            title='тестовый заголовок',
            description='Тестовое описание',
            slug='test-slug',
        )

        cls.group_1 = Group.objects.create(
            title='тестовый заголовок_1',
            description='Тестовое описание_1',
            slug='test-slug_1',
        )

        Post.objects.bulk_create(
            [
                Post(
                    text='Тестовый пост',
                    author=cls.user,
                    group=cls.group,
                ) for i in range(TOTAL_POSTS)
            ]
        )

    def setUp(self):
        '''Не/авторизированный клиент/пользователь'''
        self.guest_client = Client()
        cache.clear()

    def test_views_paginator_ten_records(self):
        '''Проверка количетсва записей = 10'''
        urls_contents_name = [
            reverse('posts:index'),
            reverse('posts:group_list', args=(self.group.slug,)),
            reverse('posts:profile', args=(self.user,)),
        ]
        for address in urls_contents_name:
            with self.subTest(address=address):
                response = self.client.get(address)
                self.assertEqual(
                    len(response.context['page_obj']),
                    POSTS_PAR_PAGE)

    def test_views_paginator_four_records(self):
        '''Проверка количетсва записей = 4'''
        urls_contents_name = [
            reverse('posts:index'),
            reverse('posts:group_list', args=(self.group.slug,)),
            reverse('posts:profile', args=(self.user,)),
        ]
        for address in urls_contents_name:
            with self.subTest(address=address):
                response = self.client.get((address), {'page': 2})
                self.assertEqual(
                    len(response.context['page_obj']),
                    POSTS_ON_SECOND_PAGE)


class CacheViewsTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create(username='auth')
        cls.group = Group.objects.create(
            title='тестовый заголовок',
            description='Тестовое описание',
            slug='test-slug',
        )
        cls.post = Post.objects.create(
            author=cls.user,
            text='Тестовый пост КЭШ',
            group=cls.group,
        )

    def setUp(self):
        '''Не/авторизированный клиент/пользователь'''
        self.guest_client = Client()

    def test_views_cach_index_page(self):
        '''тест КЭШа'''
        response = self.guest_client.get(reverse('posts:index'))
        self.post.delete()
        response_1 = self.guest_client.get(reverse('posts:index'))
        self.assertEqual(
            response.content.decode(), response_1.content.decode())
        cache.clear()
        response_1 = self.guest_client.get(reverse('posts:index'))
        self.assertNotEqual(
            response.content.decode(), response_1.content.decode())


class FollowViewsTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create(username='author')
        cls.user_1 = User.objects.create(username='follower')
        cls.post = Post.objects.create(
            author=cls.user,
            text='Тестовый пост',
        )

    def setUp(self):
        '''Не/авторизированный клиент/пользователь'''
        self.authorized_client = Client()
        self.authorized_client_1 = Client()
        self.authorized_client.force_login(self.user)
        self.authorized_client_1.force_login(self.user_1)
        cache.clear()

    def test_views_follower_signon_action(self):
        '''проверка подписки на автора
            авторизированнным пользователем
        '''
        count_0 = len(Follow.objects.all())
        self.authorized_client_1.get(
            reverse('posts:profile_follow', args=(self.user,)))
        count_1 = len(Follow.objects.all())
        self.assertEqual(count_1 - count_0, 1)

    def test_views_follower_signoff_action(self):
        '''проверка отписки на автора
            авторизированнным пользователем
        '''
        Follow.objects.create(user=self.user_1, author=self.user)
        count_0 = len(Follow.objects.all())
        self.authorized_client_1.get(
            reverse('posts:profile_unfollow', args=(self.user,)))
        count_1 = len(Follow.objects.all())
        self.assertEqual(count_0 - count_1, 1)


class FollowPagesViewsTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create(username='author')
        cls.user_1 = User.objects.create(username='follower')
        cls.user_2 = User.objects.create(username='unfollower')
        cls.post = Post.objects.create(
            author=cls.user,
            text='пост для подписчика',
        )

        cls.follow = Follow.objects.create(
            author=cls.user,
            user=cls.user_1,
        )

    def setUp(self):
        '''Не/авторизированный клиент/пользователь'''
        self.authorized_client = Client()
        self.authorized_client_1 = Client()
        self.authorized_client_2 = Client()
        self.authorized_client.force_login(self.user)
        self.authorized_client_1.force_login(self.user_1)
        self.authorized_client_2.force_login(self.user_2)
        cache.clear()

    def test_views_page_available_for_follower_only(self):
        '''Новая запись пользователя появляется в ленте тех,
           кто на него подписан
        '''
        response = self.authorized_client_1.get(
            reverse('posts:follow_index'))
        self.assertContains(response, 'пост для подписчика')

    def test_views_page_unavailable_for_nonfollower(self):
        '''Новая запись пользователя  не появляется в ленте тех,
           кто не подписан
        '''
        response = self.authorized_client_2.get(
            reverse('posts:follow_index'))
        self.assertNotContains(response, 'пост для подписчика')

    def test_views_following_available_once(self):
        '''Подписка на автора возможна только один раз'''
        self.authorized_client_1.get(
            reverse('posts:profile_follow', args=(self.user,)))
        count_0 = len(Follow.objects.all())
        self.authorized_client_1.get(
            reverse('posts:profile_follow', args=(self.user,)))
        count_1 = len(Follow.objects.all())
        self.assertEqual(count_0 - count_1, 0)
