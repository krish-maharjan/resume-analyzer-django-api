from rest_framework import serializers
from api.models import Profile

class FileSerializer(serializers.Serializer):
    rdoc = serializers.FileField()

class ProfileSerializer(serializers.ModelSerializer):
    rdoc = serializers.ListField(child=serializers.FileField(), required=False)
    # rdoc = FileSerializer(many=True)

    class Meta:
        model = Profile
        fields = ['id', 'email', 'keywords_received', 'rdoc']

    def create(self, validated_data):
        files_data = validated_data.pop('rdoc')
        profile = Profile.objects.create(**validated_data)
        for file_data in files_data:
            profile.files.create(rdoc=file_data['rdoc'])
        return profile