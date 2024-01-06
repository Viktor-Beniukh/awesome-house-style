from django import forms

from goods.models import Category, Product


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ("name",)


class ProductForm(forms.ModelForm):
    name = forms.CharField(
        widget=forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Enter product name...",
                "required": True
            })
    )
    description = forms.CharField(
        widget=forms.Textarea(attrs={
                "class": "form-control",
                "placeholder": "Enter product description...",
                "rows": 5,
                "required": True
            })
    )
    price = forms.DecimalField(
        max_digits=10,
        decimal_places=2,
        widget=forms.NumberInput(attrs={
            "class": "form-control",
            "placeholder": "Enter product price...",
            "min": 0,
            "step": 0.01,
            "required": True,
        })
    )
    discount = forms.DecimalField(
        max_digits=5,
        decimal_places=2,
        widget=forms.NumberInput(attrs={
            "class": "form-control",
            "placeholder": "Enter product discount...",
            "min": 0,
            "step": 0.01,
        })
    )
    quantity = forms.IntegerField(
        initial=1,
        widget=forms.NumberInput(attrs={
            "class": "form-control",
            "placeholder": "Enter product quantity...",
            "min": 0
        })
    )
    category = forms.ModelChoiceField(
        queryset=Category.objects.exclude(name="All goods"),
        widget=forms.Select(attrs={"class": "form-control"})
    )
    image_product = forms.ImageField(required=False)

    class Meta:
        model = Product
        fields = (
            "name",
            "description",
            "price",
            "discount",
            "quantity",
            "category",
            "image_product"
        )
