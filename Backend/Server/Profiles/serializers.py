# Import necessary modules
from rest_framework import serializers
from .models import Profile, ProfileSocialMedia, ProfileSecurityAuthentication



# Define a serializer for the ProfileSocialMedia model
class ProfileSocialMediaSerializer(serializers.ModelSerializer):
    """
    This serializer represents a user's social media profiles.
    """
    class Meta:
        # Specify the model and fields for the serializer
        model = ProfileSocialMedia
        exclude = ['profile', 'id']

    
    def update(self, instance, validated_data):
        # Update the instance with the validated data
        instance.linkedin_profile = validated_data.get('linkedin_profile', instance.linkedin_profile)
        instance.github_profile = validated_data.get('github_profile', instance.github_profile)
        instance.gitlab_profile = validated_data.get('gitlab_profile', instance.gitlab_profile)
        instance.instagram_profile = validated_data.get('instagram_profile', instance.instagram_profile)
        instance.youtube_profile = validated_data.get('youtube_profile', instance.youtube_profile)
        instance.x_profile = validated_data.get('x_profile', instance.x_profile)

        instance.save()

        return instance



# Define a serializer for the ProfileSecurityAuthentication model
class ProfileSecurityAuthenticationSerializer(serializers.ModelSerializer):
    """
    This serializer represents the security and authentication settings for a user's profile.
    """
    class Meta:
        # Specify the model and fields for the serializer
        model = ProfileSecurityAuthentication
        exclude = ['profile', 'id']
        read_only_fields = ['two_factor_auth']

    
    def update(self, instance, validated_data):
        instance.last_login = validated_data.get('last_login', instance.last_login)
        instance.password_reset_token = validated_data.get('password_reset_token', instance.password_reset_token)

        instance.save()

        return instance


class ProfileSerializer(serializers.ModelSerializer):
    """
    This serializer represents a user's profile.
    """
    social_media = ProfileSocialMediaSerializer()
    security_authentication = ProfileSecurityAuthenticationSerializer()

    class Meta:
        # Specify the model and fields for the serializer
        model = Profile
        fields = '__all__'
    
    
    def update(self, instance, validated_data):

        # Update the profile instance
        instance.image = validated_data.get('image', instance.image)
        instance.age = validated_data.get('age', instance.age)
        instance.bio = validated_data.get('bio', instance.bio)
        instance.location = validated_data.get('location', instance.location)
        instance.language = validated_data.get('language', instance.language)
        instance.save()

        return instance