from rest_framework import generics, filters
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q

from articles.models import Article, Tag
from articles.serializers import ArticleSerializer, TagSerializer

class ArticleCustomFilter(DjangoFilterBackend):
    def filter_queryset(self, request, queryset, view):
        if 'tags' in request.GET:
            list_ = request.GET.getlist('tags')
            return queryset.filter(Q(tags__id__in = list_) | Q(tags__parent__id__in = list_))
        return queryset

class ArticleListCreateAPIView(generics.ListCreateAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    search_fields = ['title', 'content']
    ordering_fields = ('title', 'created_at')
    filter_fields = ('tags',)
    filter_backends = (filters.SearchFilter, filters.OrderingFilter, ArticleCustomFilter)


class ArticleDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer


class TagListCreateAPIView(generics.ListCreateAPIView):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class TagDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
