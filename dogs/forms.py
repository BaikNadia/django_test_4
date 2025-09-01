from django.forms import ModelForm, BooleanField

from django.utils import timezone
from django.core.exceptions import ValidationError

from dogs.models import Dog, Parent


class StyleFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for fild_name, fild in self.fields.items():
            if isinstance(fild, BooleanField):
                fild.widget.attrs['class'] = "form-check-input"
            else:
                fild.widget.attrs['class'] = "form-control"

class DogForm(StyleFormMixin, ModelForm):
    class Meta:
        model = Dog
        exclude = ("views_counter",) # для вывода всех полей, кроме "views_counter"

class ParentForm(StyleFormMixin, ModelForm):
    class Meta:
        model = Parent
        fields = "__all__" # для вывода всех полей модели

    def clean_year_born(self):
        year_born = self.cleaned_data['year_born']
        current_year = timezone.now().year
        timedelta = current_year - year_born
        if timedelta >= 100:
            raise ValidationError("Собаки столько не живут, проверьте год рождения")
        return year_born
