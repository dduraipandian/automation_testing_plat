from django.db.utils import IntegrityError
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render
from django.contrib import messages
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.views.decorators.http import require_http_methods

from automated_testing.models import Article, ArticleContent


def get_all_articles(id=None):
    if id:
        articles = Article.objects.get(id=id)
    else:
        articles = Article.objects.all().order_by('id')
    return articles


def get_all_published_articles(slug_title=None):
    if slug_title:
        articles = Article.objects.filter(status='PUBLISHED',
                                          slug_title=slug_title).first()
    else:
        articles = Article.objects.filter(status='PUBLISHED').order_by('id')
    return articles


@staff_member_required(login_url='/login/')
@login_required(login_url='/login/')
@require_http_methods(['GET', 'POST'])
def article_admin(request):
    template = 'article_admin.html'
    if request.method == 'POST':
        try:
            data = request.POST
        except Exception as e:
            messages.error(request, 'Not able to update the information.')
            response = render(request, template)
        else:
            messages.success(request, 'Password updated successfully. Please re-login.')
            response = redirect("/")
    elif request.method == 'GET' and request.user.is_authenticated:
        articles = get_all_articles()
        if not articles:
            messages.warning(request, 'No articles found.!')
        response = render(request, template, {'articles': articles})
    else:
        response = redirect("/")

    return response


@staff_member_required(login_url='/login/')
@login_required(login_url='/login/')
@require_http_methods(['GET', 'POST'])
def article_info(request, article_id=None):
    template = 'article_admin.html'
    if request.method == 'POST':
        try:
            data = request.POST
            id = data.get('id', None) or article_id
            dirty = data.get('dirty', True) in ['true', 1, '1', True]
            title = data['title']
            article_heading = data.get('article_heading', 'H3')
            author = request.user
            if not id:
                article, created = Article.objects.update_or_create(title=title,
                                                                    defaults={
                                                                        'author': author,
                                                                        'header_choice': article_heading
                                                                    })
            else:
                article = Article.objects.get(id=id)
                if dirty:
                    article.title = title
                    article.header_choice = article_heading
                    article.save()
        except Exception as e:
            if isinstance(e, IntegrityError):
                messages.error(request, 'Title already exists.!')
            else:
                messages.error(request, 'Not able to create article info.')
            response = render(request, template, {'article': article})
        else:
            response = HttpResponseRedirect(reverse('article_content', args=[article.id]))
    elif request.method == 'GET' and request.user.is_authenticated:
        article = get_all_articles(article_id)
        response = render(request, template, {'article': article})
    else:
        response = redirect("/")

    return response


@staff_member_required(login_url='/login/')
@login_required(login_url='/login/')
@require_http_methods(['GET', 'POST'])
def article_content(request, article_id=None):
    template = 'article_admin.html'
    if request.method == 'POST':
        try:
            data = request.POST
            article_id = data.get('id', None) or article_id
            dirty = data.get('dirty', True) in ['true', 1, '1', True]
            article_content, created = ArticleContent.objects.get_or_create(article_id=article_id)
            if dirty:
                content = data['content']
                article_content.content = content
                article_content.save()
        except Exception as e:
            messages.error(request, 'Not able to create article content.')
            response = render(request, template)
        else:
            response = HttpResponseRedirect(reverse('article_preview', args=[article_id]))
    elif request.method == 'GET' and request.user.is_authenticated:
        article = get_all_articles(article_id)
        response = render(request, template, {'article': article})
    else:
        response = redirect("/")

    return response


@staff_member_required(login_url='/login/')
@login_required(login_url='/login/')
@require_http_methods(['GET', 'POST'])
def article_preview(request, article_id=None):
    template = 'article_admin.html'
    if request.method == 'POST':
        try:
            data = request.POST
            article_id = data.get('id', None) or article_id
            article = ArticleContent.objects.get(article_id=article_id)
        except Exception as e:
            messages.error(request, 'Not able to create article content.')
            response = render(request, template)
        else:
            response = HttpResponseRedirect(reverse('article_final', args=[article.id]))
    elif request.method == 'GET' and request.user.is_authenticated:
        article = get_all_articles(article_id)
        response = render(request, template, {'article': article})
    else:
        response = redirect("/")

    return response


@staff_member_required(login_url='/login/')
@login_required(login_url='/login/')
@require_http_methods(['GET', 'POST'])
def article_final(request, article_id=None):
    template = 'article_admin.html'
    if request.method == 'POST':
        try:
            data = request.POST
            article_id = data.get('id', None) or article_id
            publish = data.get('publish', False) in ['true', 1, '1', True, 'on']
            article = Article.objects.get(id=article_id)
            article.status = 'PUBLISHED' if publish else 'DRAFT'
            article.save()
        except Exception as e:
            messages.error(request, 'Not able to update article status.')
            response = render(request, template)
        else:
            messages.success(request, f'Article "{article.title}" is saved.!')
            response = HttpResponseRedirect(reverse('article_admin'))
    elif request.method == 'GET' and request.user.is_authenticated:
        article = get_all_articles(article_id)
        response = render(request, template, {'article': article})
    else:
        response = redirect("/")

    return response


@login_required(login_url='/login/')
@require_http_methods(['GET'])
def get_article(request, title):
    article = get_all_published_articles(slug_title=title)
    template = 'article.html'

    if article:
        response = render(request, template, {'article': article})
    else:
        messages.warning(request, "Request article is not found.!")
        response = render(request, template)
    return response
