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
        fields = ['profile', 'linkedin_profile', 'github_profile', 'gitlab_profile', 'instagram_profile', 'youtube_profile', 'x_profile']

    # Define a method to update the social media profiles
    def update(self, instance, validated_data):
        # Update the social media profiles with the validated data
        instance.linkedin_profile = validated_data.get('linkedin_profile', instance.linkedin_profile)
        instance.github_profile = validated_data.get('github_profile', instance.github_profile)
        instance.gitlab_profile = validated_data.get('gitlab_profile', instance.gitlab_profile)
        instance.instagram_profile = validated_data.get('instagram_profile', instance.instagram_profile)
        instance.youtube_profile = validated_data.get('youtube_profile', instance.youtube_profile)
        instance.x_profile = validated_data.get('x_profile', instance.x_profile)
        # Save the updated social media profiles
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
        fields = ['profile', 'two_factor_auth', 'password_reset_token', 'last_login']

    # Define a method to update the security and authentication settings
    def update(self, instance, validated_data):
        # Update the security and authentication settings with the validated data
        instance.two_factor_auth = validated_data.get('two_factor_auth', instance.two_factor_auth)
        instance.password_reset_token = validated_data.get('password_reset_token', instance.password_reset_token)
        instance.last_login = validated_data.get('last_login', instance.last_login)
        # Save the updated security and authentication settings
        instance.save()
        return instance



# Define a serializer for the Profile model
class ProfileSerializer(serializers.ModelSerializer):
    """
    This serializer represents a user's profile.
    """
    # Include the social media profiles and security and authentication settings in the serializer
    social_media = ProfileSocialMediaSerializer(read_only=True)
    security_authentication = ProfileSecurityAuthenticationSerializer(read_only=True)

    class Meta:
        # Specify the model and fields for the serializer
        model = Profile
        fields = ['id', 'user', 'image', 'age', 'bio', 'location', 'language', 'social_media', 'security_authentication']

    # Define a method to create a new profile
    def create(self, validated_data):
        # Create a new profile with the validated data
        return Profile.objects.create(**validated_data)

    # Define a method to update an existing profile
    def update(self, instance, validated_data):
        # Update the profile with the validated data
        instance.image = validated_data.get('image', instance.image)
        instance.age = validated_data.get('age', instance.age)
        instance.bio = validated_data.get('bio', instance.bio)
        instance.location = validated_data.get('location', instance.location)
        instance.language = validated_data.get('language', instance.language)
        # Save the updated profile
        instance.save()
        return instance

    # Define a method to validate the profile data
    def validate(self, data):
        # Check if the age is 9 or older
        if data['age'] < 9:
            raise serializers.ValidationError('Age must be 9 or older')
        return data