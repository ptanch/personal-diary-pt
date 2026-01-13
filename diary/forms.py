from django import forms

from diary.models import Diary


class DiaryForm(forms.ModelForm):
    """Форма для создания и редактирования дневниковой записи"""

    class Meta:
        model = Diary
        fields = ("title", "note", "is_private")

        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control", "placeholder": "Заголовок (необязательно)"}),
            "note": forms.Textarea(
                attrs={"class": "form-control", "rows": 8, "placeholder": "Напиши свои мысли здесь…"}),
            "is_private": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }

    def clean_note(self):
        note = (self.cleaned_data.get("note") or "").strip()
        if not note:
            raise forms.ValidationError("Запись не может быть пустой.")
        return note
