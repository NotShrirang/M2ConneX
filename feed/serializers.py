from feed.models import Feed, FeedAction
from rest_framework.serializers import ModelSerializer

class FeedSerializer(ModelSerializer):
    class Meta:
        model = Feed
        fields = '__all__'

class FeedActionSerializer(ModelSerializer):
    class Meta:
        model = FeedAction
        fields = '__all__'