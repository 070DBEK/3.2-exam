from rest_framework import serializers
from .models import Review
from users.serializers import UserLightSerializer


class ReviewSerializer(serializers.ModelSerializer):
    user = UserLightSerializer(read_only=True)

    class Meta:
        model = Review
        fields = '__all__'
        read_only_fields = ['user', 'created_at', 'updated_at']

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)