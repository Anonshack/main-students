from django import forms
from .models import Recipe, Tag, RecipeIngredient
from django.core.exceptions import ValidationError


class RecipeCreateForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = ['id', 'author', 'title', 'is_active', 'tags']
        exclude = ['slug', 'author']

    def __init__(self, *args, **kwargs):
        super(RecipeCreateForm, self).__init__(*args, **kwargs)
        self.fields['title'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Recipe..',
        })
        self.fields['tags'].widget.attrs.update({
            'class': 'form-control tags'
        })

    def clean_title(self):
        title = self.cleaned_data['title']
        if len(title) < 5:
            raise ValidationError('More than 5 letters')
        if title.capitalize() != title:
            raise ValidationError('First letter should be capitalized')
        return title


class RecipeUpdateForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = ['id', 'author', 'title', 'is_active', 'tags']
        exclude = ['author']

    def __init__(self, *args, **kwargs):
        super(RecipeUpdateForm, self).__init__(*args, **kwargs)
        self.fields['title'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Recipe..',
        })
        self.fields['is_active'].widget.attrs.update({
            'class': 'form-check-input',
        })
        self.fields['tags'].widget.attrs.update({
            'class': 'form-control tags',
        })


class TagForm(forms.ModelForm):
    class Meta:
        model = Tag
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(TagForm, self).__init__(*args, **kwargs)
        self.fields['title'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Tag..',
        })


class RecipeIngredientForm(forms.ModelForm):
    class Meta:
        model = RecipeIngredient
        fields = '__all__'
        exclude = ['recipe']

    def __init__(self, *args, **kwargs):
        super(RecipeIngredientForm, self).__init__(*args, **kwargs)
        self.fields['title'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Ingredient..',
        })
        self.fields['quantity'].widget.attrs.update({
            'class': 'form-control',
        })
        self.fields['unit'].widget.attrs.update({
            'class': 'form-control',
        })