from django.contrib.auth.decorators import login_required
from django.shortcuts import render, Http404, reverse, redirect
from django.contrib import messages
from .models import Article
from .forms import ArticleForm


def art(request):
    articles = Article.objects.filter(is_deleted__exact=False).order_by('-id')
    q = request.GET.get('q')
    if q:
        articles = articles.filter(title__icontains=q)
    return render(request, 'article/index.html', {'object_list': articles})


def detail(request, slug=None):
    context = {}
    if slug:
        article = Article.objects.get(slug=slug)
        context['object'] = article
        return render(request, 'article/detail.html', context)

    return Http404()


@login_required
def create(request):
    form = ArticleForm(request.POST or None, files=request.FILES)
    context = {
        'form':form
    }
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.success(request, 'Added an article')
            return redirect('articles:list')
    return render(request, 'article/create.html', context)


@login_required
def edit(request, slug=None):
    article = Article.objects.get(slug=slug)
    form = ArticleForm(instance=article)
    if request.method == 'POST':
        form = ArticleForm(data=request.POST, instance=article, files=request.FILES)
        form.save()
        messages.info(request, 'You edited the article')
        return redirect(reverse('articles:detail', kwargs={'slug': article.slug}))
    context = {
        'form': form
    }
    return render(request, 'article/edit.html', context)


@login_required
def delete(request, slug=None):
    article = Article.objects.get(slug=slug)
    if request.method == 'POST':
        article.is_deleted = True
        article.save()
        messages.error(request, 'The article was deleted')
        return redirect('articles:list')
    context = {
        'object': article
    }
    return render(request, 'article/delete.html', context)