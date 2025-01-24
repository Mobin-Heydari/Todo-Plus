# Import necessary modules
from django.db import models
from Users.models import User

# Define the Profile model
class Profile(models.Model):
    """
    This model represents a user's profile.
    """
    # One-to-one relationship with the User model
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='profile',
    )

    # Image field to store the user's profile picture
    image = models.ImageField(
        upload_to="Profiles/",  # Upload images to the 'Profiles' directory
        blank=True,  # Allow the image field to be blank
        null=True,  # Allow the image field to be null
    )

    # Age field to store the user's age
    age = models.PositiveIntegerField(null=True, blank=True)

    # Bio field to store the user's bio
    bio = models.TextField(blank=True)

    # Location field to store the user's location
    location = models.CharField(max_length=255, blank=True)

    # Language field to store the user's language
    language = models.CharField(max_length=10, blank=True)


    # Return the user's username as a string representation of the profile
    def __str__(self):
        return f'{self.user.username}'

    # Define the meta options for the Profile model
    class Meta:
        verbose_name = "Profile"
        verbose_name_plural = "Profiles"


# Define the ProfileSocialMedia model
class ProfileSocialMedia(models.Model):
    """
    This model represents a user's social media profiles.
    """
    # One-to-one relationship with the Profile model
    profile = models.OneToOneField(
        Profile,
        on_delete=models.CASCADE,
        related_name='social_media',
    )

    # LinkedIn field to store the user's LinkedIn profile URL
    linkedin_profile = models.URLField(null=True, blank=True)

    # GitHub field to store the user's GitHub profile URL
    github_profile = models.URLField(null=True, blank=True)

    # GitLab field to store the user's GitLab profile URL
    gitlab_profile = models.URLField(null=True, blank=True)

    # Instagram field to store the user's Instagram profile URL
    instagram_profile = models.URLField(null=True, blank=True)

    # YouTube field to store the user's YouTube profile URL
    youtube_profile = models.URLField(null=True, blank=True)

    # X field to store the user's X profile URL
    x_profile = models.URLField(null=True, blank=True)

    # Return the user's username as a string representation of the social media profile
    def __str__(self):
        return f'{self.profile.user.username}\'s Social Media'

    # Define the meta options for the ProfileSocialMedia model
    class Meta:
        verbose_name = "Profile Social Media"
        verbose_name_plural = "Profiles Social Media"


# Define the ProfileSecurityAuthentication model
class ProfileSecurityAuthentication(models.Model):
    """
    This model represents the security and authentication settings for a user's profile.
    """
    # One-to-one relationship with the Profile model
    profile = models.OneToOneField(
        Profile,
        on_delete=models.CASCADE,
        related_name='security_authentication',
    )

    # Two-factor authentication status
    two_factor_auth = models.BooleanField(default=False)

    # Password reset token for account recovery
    password_reset_token = models.CharField(max_length=255, blank=True)

    # Timestamp of the last login
    last_login = models.DateTimeField(blank=True, null=True)

    # Return the user's username as a string representation of the security profile
    def __str__(self):
        return f'{self.profile.user.username}\'s Security'

    # Define the meta options for the ProfileSecurityAuthentication model
    class Meta:
        verbose_name = "Profile Security"
        verbose_name_plural = "Profiles Security"