from django import forms
from .models import Recipe, Category


class NewRecipeForm(forms.ModelForm):
    category = forms.ModelChoiceField(queryset=Category.objects.all(), required=True, label='Категория блюда', empty_label='Категория не выбрана')

    class Meta:
        model = Recipe
        fields = ['title', 'description', 'cooking_steps', 'cooking_time', 'photo', 'category']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-input'}),
            'description': forms.Textarea(attrs={'rows': 5, 'class': 'form-input'}),
            'cooking_steps': forms.Textarea(attrs={'rows': 10, 'class': 'form-input'})
        }
