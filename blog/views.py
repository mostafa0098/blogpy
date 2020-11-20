from django.shortcuts import render

# Create your views here.
from django.views.generic import TemplateView
from .models import Article


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
        context = {
            'article_data': article_data
        }

        return render(request, 'index.html', context)
