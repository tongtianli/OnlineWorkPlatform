import markdown as markdown
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.views import View

from kbase.forms import ArticlePostForm
from kbase.models import Article
from mail.models import Message

User = get_user_model()


class KBaseView(LoginRequiredMixin, View):
    def get(self, request):
        user = request.user
        articles = Article.objects.filter(author=user)
        return render(request, 'kbase/kbase.html', {'articles': articles})


class ArticleView(LoginRequiredMixin, View):
    def get(self, request, article_id):
        article = get_object_or_404(Article, pk=article_id)
        # 将markdown语法渲染成html样式
        article.body = markdown.markdown(article.body, extensions=[
            # 包含 缩写、表格等常用扩展
            'markdown.extensions.extra',
            # 语法高亮扩展
            'markdown.extensions.codehilite',
        ])
        return render(request, 'kbase/article-detail.html', {'article': article})


class ArticleCreateView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'kbase/article-create.html')

    def post(self, request):
        form = ArticlePostForm(request.POST)
        if form.is_valid():
            new_article = form.save(commit=False)
            new_article.author = request.user
            new_article.save()
            # 向其他组员发送通知
            for user in User.objects.filter(groupID=request.user.groupID):
                if user != request.user:
                    Message(owner=user, type=2, item_id=new_article.id, content=new_article.title,
                            involved=request.user).save()
            return redirect('kbase:main')
        else:
            return HttpResponse('表单内容有误，请重新填写')


class ArticleDeleteView(LoginRequiredMixin, View):
    def post(self, request, article_id):
        article = get_object_or_404(Article, pk=article_id)
        article.delete()
        return redirect('kbase:main')


class ArticleUpdateView(LoginRequiredMixin, View):
    def get(self, request, article_id):
        article = get_object_or_404(Article, pk=article_id)
        form = ArticlePostForm(article)
        return render(request, 'kbase/article-update.html', locals())

    def post(self, request, article_id):
        article = get_object_or_404(Article, pk=article_id)
        form = ArticlePostForm(request.POST)
        if form.is_valid():
            article.title = form.cleaned_data['title']
            article.body = form.cleaned_data['body']
            article.save()
            return redirect('kbase:article-detail', article_id=article_id)
        else:
            return HttpResponse('表单内容有误，请重新填写')
