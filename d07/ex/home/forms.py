from django import forms

from .models import Article, User, UserFavoriteArticle


class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ["title", "synopsis", "content"]
        widgets = {
            "title": forms.TextInput(
                attrs={
                    "placeholder": "Title",
                    "required": True,
                }
            ),
            "synopsis": forms.Textarea(
                attrs={
                    "placeholder": "Synopsis",
                    "required": True,
                }
            ),
            "content": forms.Textarea(
                attrs={
                    "placeholder": "Content",
                    "required": True,
                }
            )
        }


class RegisterForm(forms.ModelForm):
    username = forms.CharField(error_messages={"required": "Username is required"})
    password = forms.CharField(
        strip=False,
        error_messages={"required": "Password is required"},
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}),
    )
    password_confirm = forms.CharField(
        strip=False,
        label="Confirm password",
        error_messages={"required": "Password confirmation is required"},
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}),
    )

    class Meta:
        model = User
        fields = ["username"]

    def clean_username(self):
        username = self.cleaned_data["username"]
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("User already exists")
        return username

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_confirm = cleaned_data.get("password_confirm")
        if password and password_confirm and password != password_confirm:
            self.add_error("password_confirm", "Passwords do not match")
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