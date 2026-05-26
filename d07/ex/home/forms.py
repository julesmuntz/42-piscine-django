from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import gettext_lazy as _
from .models import Article, User, UserFavoriteArticle


class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ["title", "synopsis", "content"]
        widgets = {
            "title": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": _("Title"),
                    "required": True,
                }
            ),
            "synopsis": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "placeholder": _("Synopsis"),
                    "required": True,
                    "rows": 3,
                }
            ),
            "content": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "placeholder": _("Content"),
                    "required": True,
                    "rows": 8,
                }
            )
        }


class LoginForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": _("Username"),
                "autocomplete": "username",
                "required": True,
            }
        )
    )
    password = forms.CharField(
        strip=False,
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "placeholder": _("Password"),
                "autocomplete": "current-password",
                "required": True,
            }
        ),
    )


class RegisterForm(forms.ModelForm):
    username = forms.CharField(
        error_messages={"required": _("Username is required")},
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": _("Username"),
                "autocomplete": "username",
                "required": True,
            }
        ),
    )
    password = forms.CharField(
        strip=False,
        error_messages={"required": _("Password is required")},
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "placeholder": _("Password"),
                "autocomplete": "new-password",
                "required": True,
            }
        ),
    )
    password_confirm = forms.CharField(
        strip=False,
        label=_("Confirm password"),
        error_messages={"required": _("Password confirmation is required")},
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "placeholder": _("Confirm password"),
                "autocomplete": "new-password",
                "required": True,
            }
        ),
    )

    class Meta:
        model = User
        fields = ["username"]

    def clean_username(self):
        username = self.cleaned_data["username"]
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError(_("User already exists"))
        return username

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_confirm = cleaned_data.get("password_confirm")
        if password and password_confirm and password != password_confirm:
            self.add_error("password_confirm", _("Passwords do not match"))
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user

class UserFavoriteArticleForm(forms.ModelForm):
    class Meta:
        model = UserFavoriteArticle
        fields = "__all__"