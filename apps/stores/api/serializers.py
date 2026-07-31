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
from rest_framework import serializers
from apps.stores.models import Store
from claudine.users.api.serializers import UserSerializer


class StoreSerializer(serializers.ModelSerializer):
    owner = UserSerializer(read_only=True)

    class Meta:
        model = Store
        fields = ["id", "owner", "name", "slug", "created_at", "updated_at"]
        read_only_fields = ["id", "owner", "slug", "created_at", "updated_at"]

    def create(self, validated_data):
        # Auto-assign the logged-in user as owner
        validated_data["owner"] = self.context["request"].user
        return super().create(validated_data)
