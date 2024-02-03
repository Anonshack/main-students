from django.shortcuts import render, redirect, reverse, get_object_or_404
from .models import Recipe, RecipeIngredient, Tag
from django.contrib.auth.decorators import login_required
from .forms import RecipeCreateForm, RecipeUpdateForm, TagForm, RecipeIngredientForm
from django.contrib import messages
from django.http import HttpResponse


def recipe_list(request):
    recipes = Recipe.objects.filter(is_active=True).order_by('-id')
    tags_list = Tag.objects.all()
    q = request.GET.get('q')
    tag = request.GET.get('tag')
    if q:
        recipes = recipes.filter(title__icontains=q)
    if tag:
        recipes = recipes.filter(tags__title=tag)
    ctx = {
        'recipes': recipes,
        'tags_list': tags_list
    }
    return render(request, 'recipes/list.html', ctx)


@login_required
def my_recipes(request):
    user = request.user
    recipes = Recipe.objects.filter(author=user)
    tags_list = Tag.objects.all()
    tag = request.GET.get('tag')
    if tag:
        recipes = recipes.filter(tags__title=tag)
    ctx = {
        "recipes": recipes,
        'tags_list': tags_list
    }
    return render(request, 'recipes/list.html', ctx)


def recipe_detail(request, slug):
    recipe = get_object_or_404(Recipe, slug=slug)
    ctx = {
        "recipe": recipe
    }
    return render(request, 'recipes/detail.html', ctx)


@login_required
def recipe_create(request, *args, **kwargs):
    form = RecipeCreateForm()
    if request.method == 'POST':
        form = RecipeCreateForm(request.POST or None)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.author = request.user
            obj.is_active = True
            obj.save()
            form.save_m2m()
            return redirect(reverse("recipes:detail", kwargs={'slug': obj.slug}))
    ctx = {
        'form': form
    }
    return render(request, 'recipes/create.html', ctx)


@login_required
def recipe_update(request, slug):
    obj = get_object_or_404(Recipe, slug=slug)
    form = RecipeUpdateForm(request.POST or None, instance=obj)
    if request.user != obj.author:
        if not request.user.is_superuser:
            return HttpResponse('<h1>What are you doing?</h1>')
    if request.method == 'POST':
        form = RecipeUpdateForm(data=request.POST, instance=obj)
        if form.is_valid():
            form.save()
            return redirect(reverse("recipes:detail", kwargs={'slug': obj.slug}))
    ctx = {
        "form": form
    }
    return render(request, 'recipes/update.html', ctx)


@login_required
def recipe_delete(request, slug):
    obj = get_object_or_404(Recipe, slug=slug)
    if request.user != obj.author:
        if not request.user.is_superuser:
            return HttpResponse('<h1>What are you doing?</h1>')
    if request.method == 'POST':
        obj.delete()
        messages.error(request, f"<b>{obj.title}</b> ochirildi")
        return redirect("recipes:list")
    ctx = {
        'object': obj
    }
    return render(request, 'recipes/delete.html', ctx)


def tag_list(request):
    tag = Tag.objects.all
    ctx = {
        "object_list": tag
    }
    return render(request, 'recipes/tag/list.html', ctx)


def tag_detail(requst, pk):
    obj = get_object_or_404(Tag, id=pk)
    ctx = {
        'object': obj
    }
    return render(requst, 'recipes/tag/detail.html', ctx)


@login_required
def tag_update(request, pk):
    obj = get_object_or_404(Tag, id=pk)
    form = TagForm(instance=obj)
    if request.method == 'POST':
        form = TagForm(data=request.POST, instance=obj)
        if form.is_valid():
            form.save()
            return redirect(reverse('recipes:tag_detail', kwargs={"pk": obj.id}))
    ctx = {
        'form': form
    }
    return render(request, 'recipes/tag/update.html', ctx)


@login_required
def tag_delete(request, pk):
    obj = get_object_or_404(Tag, id=pk)
    if request.method == 'POST':
        obj.delete()
        messages.error(request, f'<b>{obj.title}</b> ochirildi')
        return redirect('recipes:tag_list')
    ctx = {
        'object': obj
    }
    return render(request, 'recipes/tag/delete.html', ctx)


@login_required
def tag_create(request):
    form = TagForm()
    if request.method == 'POST':
        form = TagForm(request.POST)
        if form.is_valid():
            obj = form.save()
            return redirect(reverse('recipes:tag_detail', kwargs={"pk": obj.id}))
    ctx = {
        'form': form
    }
    return render(request, 'recipes/tag/create.html', ctx)


@login_required
def ing_create(request, recipe_slug, *args, **kwargs):
    form = RecipeIngredientForm()
    recipe = get_object_or_404(Recipe, slug=recipe_slug)
    if request.user != recipe.author:
        if not request.user.is_superuser:
            return HttpResponse('<h1>What are you doing?</h1>')
    if request.method == 'POST':
        form = RecipeIngredientForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.recipe = recipe
            obj.save()
            return redirect(reverse("recipes:detail", kwargs={"slug": recipe.slug}))
    ctx = {
        'form': form
    }
    return render(request, 'recipes/ing/create.html', ctx)


@login_required
def ing_update(request, recipe_slug, pk):
    obj = get_object_or_404(RecipeIngredient, id=pk)
    recipe = get_object_or_404(Recipe, slug=recipe_slug)
    form = RecipeIngredientForm(instance=obj)
    if request.user != recipe.author:
        if not request.user.is_superuser:
            return HttpResponse('<h1>What are you doing?</h1>')
    if request.method == 'POST':
        form = RecipeIngredientForm(request.POST, instance=obj)
        if form.is_valid():
            form.save()
            return redirect(reverse("recipes:detail", kwargs={"slug": recipe.slug}))
    ctx = {
        'form': form
    }
    return render(request, 'recipes/ing/update.html', ctx)


@login_required
def ing_delete(request, recipe_slug, pk):
    obj = get_object_or_404(RecipeIngredient, id=pk)
    recipe = get_object_or_404(Recipe, slug=recipe_slug)
    if request.user != recipe.author:
        if not request.user.is_superuser:
            return HttpResponse('<h1>What are you doing?</h1>')
    if request.method == 'POST':
        obj.delete()
        messages.error(request, f"<b>{obj.title}</b> ochirildi")
        return redirect(reverse("recipes:detail", kwargs={"slug": recipe.slug}))
    ctx = {
        'object': obj
    }
    return render(request, 'recipes/ing/delete.html', ctx)