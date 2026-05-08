from django import forms

from .models import Tip


class TipForm(forms.ModelForm):
    class Meta:
        model = Tip
        fields = ["content"]
        widgets = {
            "content": forms.TextInput(
                attrs={
                    "placeholder": "Content",
                    "required": True,
                }
            )
        }

class VoteForm(forms.ModelForm):
    class Meta:
        model = Tip
        fields = ["upvotes", "downvotes"]
        widgets = {
            "upvotes": forms.NumberInput(
                attrs={
                    "required": False,
                }
            ),
            "downvotes": forms.NumberInput(
                attrs={
                    "required": False,
                }
            )
        }