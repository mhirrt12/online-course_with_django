from rest_framework import serializers
from course.models import Course ,Category,User,Review
from django.contrib.auth.password_validation import validate_password


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['id', 'rating', 'comment', 'created_at']
        read_only_fields = fields
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model=Category
        fields='__all__'
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']
class CourseSerializer(serializers.ModelSerializer):
     category_details = CategorySerializer(
        source='category',
        read_only=True
     )
     instructor_details = UserSerializer(
        source='instructor',
        many=True,
        read_only=True
     )
     reviews = ReviewSerializer(
    source='review_set',
    many=True,
    read_only=True
)
     students=UserSerializer(
         source='enrolled_courses',
         read_only=True
     )
     class Meta:
        model=Course
        fields='__all__'
        read_only_fields=['students','instructor','created_at','updated_at']

class CourseSerializer2(serializers.ModelSerializer):
    class Meta:
        model=Course
        fields='__all__'

class RegisterSerializer(serializers.ModelSerializer):
      password2 = serializers.CharField(write_only=True)

      class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password2']
        extra_kwargs = {
            'password': {'write_only': True}
        }

      def validate_password(self, value):
        validate_password(value)
        return value
      def validate(self, attrs):
       if attrs['password'] != attrs['password2']:
        raise serializers.ValidationError({
            'password2': 'Passwords do not match.'
        })

       return attrs
      def validate_email(self, value):
           if User.objects.filter(email=value).exists():
                raise serializers.ValidationError(
            "This email is already registered."
        )
           return value

      def create(self, validated_data):
        validated_data.pop('password2')
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )

        return user