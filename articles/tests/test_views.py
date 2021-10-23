from rest_framework import status
from rest_framework.test import APITestCase

from django.urls import reverse

from articles.models import Article, Tag
from articles.tests.factories import ArticleFactory, TagFactory


class ArticleListCreateAPIViewTest(APITestCase):
    def test_list(self):
        article1, article2 = ArticleFactory.create_batch(2)
        response = self.client.get(reverse("article_list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            [article["id"] for article in response.data], [article1.id, article2.id]
        )

    def test_create(self):
        self.assertEqual(Article.objects.count(), 0)
        data = {
            "title": "Test Article",
            "slug": "test-article",
            "content": "Lorem ipsum",
        }
        response = self.client.post(reverse("article_list"), data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        article = Article.objects.get(id=response.data["id"])  # newly-created
        self.assertEqual(article.slug, "test-article")

    def test_sort(self):
        article1, article2 = ArticleFactory.create_batch(2)
        response = self.client.get(reverse("article_list")+"?ordering=-title")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            [article["id"] for article in response.data], [article2.id, article1.id]
        )

    def test_filter(self):
        ArticleFactory.create_batch(2)
        data = {
            "title": "Test Article",
            "slug": "test-article",
            "content": "Lorem ipsum",
        }
        response = self.client.post(reverse("article_list"), data=data)
        response = self.client.get(reverse("article_list")+"?search=Test Article")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)


class ArticleDetailAPIViewTest(APITestCase):
    def test_update(self):
        article = ArticleFactory(slug="my-slug")
        data = {"slug": "updated-slug"}
        url = reverse("article_detail", args=(article.id,))
        response = self.client.patch(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        updated_article = Article.objects.get(id=article.id)
        self.assertEqual(updated_article.slug, "updated-slug")

    def test_delete(self):
        article = ArticleFactory()
        url = reverse("article_detail", args=(article.id,))
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Article.objects.count(), 0)

class TagListCreateAPIViewTest(APITestCase):
    def test_list(self):
        tag1, tag2 = TagFactory.create_batch(2)
        response = self.client.get(reverse("tag_list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            [tag["id"] for tag in response.data], [tag1.id, tag2.id]
        )

    def test_create(self):
        self.assertEqual(Tag.objects.count(), 0)
        data = {
            "name": "Test tag",
            "slug": "test-tag",
        }
        response = self.client.post(reverse("tag_list"), data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        tag = Tag.objects.get(id=response.data["id"])  # newly-created
        self.assertEqual(tag.slug, "test-tag")


class TagDetailAPIViewTest(APITestCase):
    def test_update(self):
        tag = TagFactory(slug="my-slug")
        data = {"slug": "updated-slug"}
        url = reverse("tag_detail", args=(tag.id,))
        response = self.client.patch(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        updated_tag = Tag.objects.get(id=tag.id)
        self.assertEqual(updated_tag.slug, "updated-slug")

    def test_delete(self):
        tag = TagFactory()
        url = reverse("tag_detail", args=(tag.id,))
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Tag.objects.count(), 0)
