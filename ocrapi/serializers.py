from rest_framework import serializers

class UploadSimilarNamedFileSerializer(serializers.Serializer):
    similar_file = serializers.IntegerField()