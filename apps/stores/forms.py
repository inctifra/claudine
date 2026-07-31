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

from .models import Store


class StoreModelForm(forms.ModelForm):
    name = forms.CharField(
        max_length=200,
        label="Store Name",
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "This is your store name",
        }),
    )
    class Meta:
        model = Store
        fields = ["name"]

    def __init__(self, *args, **kwargs):
        self.owner = kwargs.pop("owner")
        super().__init__(*args, **kwargs)

    def save(self, commit=...):
        instance = super().save(commit=False)
        instance.owner = self.owner

        if commit:
            instance.save()
            self.save_m2m()

        return instance

