from django.shortcuts import render
from pprint import pprint
# Create your views here.
from django.views.generic import TemplateView
from .models import *
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from . import serializers
from django.contrib.auth.models import User


class IndexPage(TemplateView):
    def get(self, request, *args, **kwargs):
        """
        docstring
        """
        article_data = []

        all_artcles = Article.objects.all().order_by('-created_at')[:9]
        for article in all_artcles:
            article_data.append({
                'title': article.title,
                'cover': article.cover.url,
                'category': article.category.title,
                'created_at': article.created_at.date()
            })
        promotes_data = []
        all_promotes = Article.objects.filter(promote=True)

        for promote in all_promotes:
            pprint(dir(promote.author.user))
            promotes_data.append({'cover': promote.cover.url, 'avatar': promote.author.avatar.url,
                                  'category': promote.category.title, 'title': promote.title, 'date': promote.created_at.date(
                                  ), 'author': promote.author.user.first_name+' '+promote.author.user.last_name})

        context = {
            'article_data': article_data,
            'promotes_data': promotes_data
        }

        return render(request, 'index.html', context)


class AllArticlesAPIView(APIView):
    def get(self, req):
        try:
            all_articles = Article.objects.all().order_by('-created_at')[:10]
            data = []
            for article in all_articles:
                data.append({
                    "title": article.title,
                    "cover": article.cover.url if article.cover else None,
                    "content": article.content,
                    "created_at": article.created_at,
                    "category": article.category.title,
                    "author": article.author.user.first_name + ' ' + article.author.user.last_name,
                    "promote": article.promote
                })
            return Response({'data': data}, status=status.HTTP_200_OK)
        except:
            return Response({'status': 'internal server error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class SingleArticleAPIView(APIView):
    def get(self, req):
        try:
            article_title = req.GET['article_title']
            article = Article.objects.filter(title__contains=article_title)
            serialized_data = serializers.SingleArticleSerializer(
                article, many=True)
            data = serialized_data.data
            return Response({'data': data}, status=status.HTTP_200_OK)
        except:
            return Response({'status': 'internal error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class SearchArticleAPIView(APIView):
    def get(self, request):
        try:
            from django.db.models import Q
            query = request.GET['query']
            articles = Article.objects.filter(Q(content__icontains=query))
            data = []
            for article in articles:
                data.append({
                    'title': article.title,
                    'cover': article.cover.url if article.cover else None,
                    'content': article.content,
                    'created_at': article.created_at,
                    "category": article.category.title,
                    "author": article.author.user.first_name + ' ' + article.author.user.last_name,
                    "promote": article.promote
                })
            return Response({'data': data}, status=status.HTTP_200_OK)
        except:
            return Response({'status': 'error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class SubmitArticleAPIView(APIView):
    def post(self, req):
        try:
            serializer = serializers.SubmitArticleSerializer(data=req.data)
            if serializer.is_valid():
                title = serializer.data.get('title')
                cover = req.FILES['cover']
                content = serializer.data.get('content')
                category_id = serializer.data.get('category_id')
                author_id = serializer.data.get('author_id')
                promote = serializer.data.get('promote')
            else:
                return Response({'status': 'bad request'}, status=status.HTTP_400_BAD_REQUEST)
            user = User.objects.get(id=author_id)
            author = UserProfile.objects.get(user=user)
            category = Category.objects.get(id=category_id)
            article = Article()
            article.title = title
            article.cover = cover
            article.content = content
            article.category = category
            article.author = author
            article.promote = promote
            article.save()
            return Response({'status': 'success'}, status=status.HTTP_200_OK)
        except:
            return Response({'status': 'err'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class UpdateArticleAPIView(APIView):
    def patch(self, req):
        try:
            serializer = serializers.UpdateArticleCoverSerializer(
                data=req.data)
            if serializer.is_valid():
                article_id = serializer.data['article_id']
                cover = req.FILES['cover']
                Article.objects.filter(id=article_id).update(cover=cover)
                return Response({'status': 'success'}, status=status.HTTP_200_OK)
            else:
                return Response({'status': 'bad req'}, status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response({'status': 'err'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class DeleteArticleAPIView(APIView):
    def delete(self, req):
        try:
            serializer = serializers.DeleteArticleCoverSerializer(
                data=req.data)
            if serializer.is_valid():
                article_id = serializer.data['article_id']

                Article.objects.filter(id=article_id).delete()
                return Response({'status': 'success'}, status=status.HTTP_200_OK)
            else:
                return Response({'status': 'bad req'}, status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response({'status': 'err'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
