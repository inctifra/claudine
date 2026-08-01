# Copyright 2026 liont
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from django import forms
from django.core.validators import MinValueValidator

from .models import Category, Product, ProductImage


class CategoryModelForm(forms.ModelForm):
    name = forms.CharField(
        max_length=255,
        required=True,
        widget=forms.TextInput(
            attrs={"placeholder": "Category Name", "class": "form-control mx-2"},
        ),
    )
    is_active = forms.BooleanField(
        required=False,
        initial=True,
        label="Initial the status of the category as active",
        widget=forms.CheckboxInput(attrs={"class": "form-check-input"}),
    )

    class Meta:
        model = Category
        fields = ["name", "is_active"]

    def __init__(self, *args, **kwargs):
        self.store = kwargs.pop("store")
        super().__init__(*args, **kwargs)

    def save(self, commit=...):
        instance = super().save(commit=False)
        instance.store = self.store
        if commit:
            instance.save()
        return instance



class ProductForm(forms.ModelForm):
    name = forms.CharField(
        max_length=200,
        label="Product Name",
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "e.g. Gold Necklace",
        }),
    )
    category = forms.ModelChoiceField(
        queryset=Category.objects.none(),
        label="Category",
        widget=forms.Select(attrs={"class": "custom-select form-control"}),
    )
    price = forms.IntegerField(
        label="Price",
        validators=[MinValueValidator(0)],
        widget=forms.NumberInput(attrs={
            "class": "form-control",
            "placeholder": "0",
            "min": "0",
        }),
    )
    stock_quantity = forms.IntegerField(
        label="Stock Quantity",
        initial=1,
        validators=[MinValueValidator(0)],
        widget=forms.NumberInput(attrs={
            "class": "form-control",
            "min": "0",
        }),
    )
    colors = forms.CharField(
        max_length=200,
        required=False,
        label="Colors",
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "Red, Blue, Green",
        }),
        help_text="Comma-separated list of available colors.",
    )
    description = forms.CharField(
        required=False,
        label="Description",
        widget=forms.Textarea(attrs={
            "class": "form-control",
            "rows": 8,
            "placeholder": "Describe your product...",
        }),
    )
    is_active = forms.BooleanField(
        required=False,
        initial=True,
        label="Active",
        widget=forms.CheckboxInput(attrs={"class": "form-check-input"}),
    )

    class Meta:
        model = Product
        fields = ["name", "category", "price", "stock_quantity", "colors", "description", "is_active"]

    def __init__(self, *args, store=None, **kwargs):
        super().__init__(*args, **kwargs)
        if store:
            self.fields["category"].queryset = Category.objects.for_store(store)


class ProductImageForm(forms.ModelForm):
    image = forms.ImageField(
        required=False,
        widget=forms.ClearableFileInput(attrs={
            "class": "form-control",
            "accept": "image/*",
        }),
    )
    is_primary = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={"class": "form-check-input"}),
    )

    class Meta:
        model = ProductImage
        fields = ["image", "is_primary"]


ProductImageFormSet = forms.inlineformset_factory(
    Product,
    ProductImage,
    form=ProductImageForm,
    extra=3,  # Show 3 empty upload slots
    can_delete=True,
    max_num=5,  # Max 5 images per product
)
