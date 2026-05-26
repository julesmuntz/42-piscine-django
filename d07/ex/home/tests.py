from django.test import TestCase
from django.urls import reverse

from .models import Article, User, UserFavoriteArticle


class AccessControlAndFavoritesTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.author = User.objects.create_user(
            username="author",
            password="author-password",
        )
        cls.reader = User.objects.create_user(
            username="reader",
            password="reader-password",
        )
        cls.article = Article.objects.create(
            title="First article",
            author=cls.author,
            synopsis="A short synopsis",
            content="An article body",
        )

    def _assert_redirects_to_login(self, response, target_url):
        self.assertRedirects(response, f"{reverse('login')}?next={target_url}")

    def test_favorites_view_redirects_anonymous_user_to_login(self):
        favorites_url = reverse("favorites")

        response = self.client.get(favorites_url)

        self._assert_redirects_to_login(response, favorites_url)

    def test_favorites_view_uses_favorites_template_for_authenticated_user(self):
        self.client.force_login(self.reader)

        response = self.client.get(reverse("favorites"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "d07/templates/favorites.html")

    def test_publications_view_redirects_anonymous_user_to_login(self):
        publications_url = reverse("publications")

        response = self.client.get(publications_url)

        self._assert_redirects_to_login(response, publications_url)

    def test_publications_view_uses_publications_template_for_authenticated_user(self):
        self.client.force_login(self.author)

        response = self.client.get(reverse("publications"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "d07/templates/publications.html")

    def test_publication_detail_view_redirects_anonymous_user_to_login(self):
        publication_url = reverse("publication", args=[self.article.pk])

        response = self.client.get(publication_url)

        self._assert_redirects_to_login(response, publication_url)

    def test_publication_detail_view_uses_publication_template_for_author(self):
        self.client.force_login(self.author)

        response = self.client.get(reverse("publication", args=[self.article.pk]))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "d07/templates/publication.html")

    def test_publish_post_redirects_anonymous_user_to_login_without_creating_article(self):
        publications_url = reverse("publications")
        initial_count = Article.objects.count()

        response = self.client.post(
            publications_url,
            {
                "title": "Blocked article",
                "synopsis": "Blocked synopsis",
                "content": "Blocked content",
            },
        )

        self._assert_redirects_to_login(response, publications_url)
        self.assertEqual(Article.objects.count(), initial_count)

    def test_register_view_redirects_authenticated_user_away_from_creation_form(self):
        self.client.force_login(self.reader)

        response = self.client.get(reverse("register"))

        self.assertRedirects(
            response,
            reverse("home"),
            fetch_redirect_response=False,
        )

    def test_add_favorite_view_redirects_anonymous_user_to_login(self):
        favorite_url = reverse("favorite", args=[self.article.pk])

        response = self.client.post(favorite_url)

        self._assert_redirects_to_login(response, favorite_url)
        self.assertEqual(UserFavoriteArticle.objects.count(), 0)

    def test_adding_same_article_to_favorites_twice_creates_single_favorite(self):
        self.client.force_login(self.reader)
        favorite_url = reverse("favorite", args=[self.article.pk])

        first_response = self.client.post(favorite_url)
        second_response = self.client.post(favorite_url)

        self.assertRedirects(first_response, reverse("favorites"))
        self.assertRedirects(second_response, reverse("favorites"))
        self.assertEqual(
            UserFavoriteArticle.objects.filter(
                user=self.reader,
                article=self.article,
            ).count(),
            1,
        )
