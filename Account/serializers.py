from .models import UserAccount
from Post.models import Post
from Post.serializers import PostSerializer
from rest_framework import serializers

class AccountSerializer(serializers.ModelSerializer):
    posts = serializers.SerializerMethodField('get_user_posts')
    date_joined= serializers.SerializerMethodField('date_format')


    class Meta:
        model = UserAccount
        fields = ['id', 'profileImage', 'username', 'email', 'date_joined', 'friends', 'bio', 'posts', 'isWriter']

    
    def get_user_posts(self, user):
        post = Post.objects.filter(user = user.id)
        serializer = PostSerializer(post, many=True)
        return serializer.data

    def date_format(self, user):
        date = user.date_joined.strftime("%m/%d/%Y %I:%M:%S %p UTC")
        return date
    
    def update(self, instance, validated_data):
        """
            Update user information
        """
        instance.username = validated_data.get('username')
        instance.email = validated_data.get('email')
        instance.bio = validated_data.get('bio')
        instance.profileImage = validated_data.get('profileImage')
        instance.save()
        return instance



class AccountRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAccount
        fields = ['username', 'email', 'bio', 'password']

    def create(self, validated_data):
        """ Creates and returns a new user """
        user = UserAccount(
            username=validated_data.get('username'),
            email= validated_data.get('email')
        )

        user.set_password(validated_data.get('password'))
        user.save()
        return user
    
    def update(self, instance, validated_data):
        """
            Update user information
        """
        instance.username = validated_data.get('username')
        instance.email = validated_data.get('email')
        instance.bio = validated_data.get('bio')
        instance.save()
        return instance

   


