from rest_framework import serializers
from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from .models import User


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        min_length=6,
        max_length=128,
        style={'input_type': 'password'}
    )
    password_confirm = serializers.CharField(
        write_only=True,
        min_length=6,
        max_length=128,
        style={'input_type': 'password'}
    )

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'phone', 'avatar', 'password', 'password_confirm')
        extra_kwargs = {
            'first_name': {'required': True, 'min_length': 2, 'max_length': 100},
            'last_name': {'required': True, 'min_length': 2, 'max_length': 100},
            'email': {'required': True},
            'phone': {'required': False},
            'avatar': {'required': False}
        }

    def validate(self, attrs):
        password = attrs.get('password')
        password_confirm = attrs.get('password_confirm')

        if password != password_confirm:
            raise serializers.ValidationError("Passwords do not match.")

        # Django password validation
        try:
            validate_password(password)
        except ValidationError as e:
            raise serializers.ValidationError({"password": e.messages})

        return attrs

    def create(self, validated_data):
        # Remove password_confirm from validated_data
        validated_data.pop('password_confirm', None)
        
        # Create user
        user = User.objects.create_user(**validated_data)
        return user


class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(
        required=True,
        write_only=True,
        style={'input_type': 'password'}
    )

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        if email and password:
            # Authenticate user
            user = authenticate(
                request=self.context.get('request'),
                email=email,
                password=password
            )

            if not user:
                raise serializers.ValidationError(
                    'Invalid email or password.',
                    code='authorization'
                )

            if not user.is_active:
                raise serializers.ValidationError(
                    'User account is disabled.',
                    code='authorization'
                )

            attrs['user'] = user
            return attrs
        else:
            raise serializers.ValidationError(
                'Must include email and password.',
                code='authorization'
            )


class UserSerializer(serializers.ModelSerializer):
    full_name = serializers.ReadOnlyField(source='get_full_name')
    
    class Meta:
        model = User
        fields = (
            'user_id', 'first_name', 'last_name', 'full_name', 
            'email', 'phone', 'avatar', 'is_active',
            'created_at', 'updated_at'
        )
        read_only_fields = ('user_id', 'created_at', 'updated_at')


class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'phone', 'avatar')
        extra_kwargs = {
            'first_name': {'required': False, 'min_length': 2, 'max_length': 100},
            'last_name': {'required': False, 'min_length': 2, 'max_length': 100},
        }

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance


class PasswordChangeSerializer(serializers.Serializer):
    old_password = serializers.CharField(
        required=True,
        write_only=True,
        style={'input_type': 'password'}
    )
    new_password = serializers.CharField(
        required=True,
        write_only=True,
        min_length=6,
        style={'input_type': 'password'}
    )
    new_password_confirm = serializers.CharField(
        required=True,
        write_only=True,
        min_length=6,
        style={'input_type': 'password'}
    )

    def validate(self, attrs):
        old_password = attrs.get('old_password')
        new_password = attrs.get('new_password')
        new_password_confirm = attrs.get('new_password_confirm')
        
        user = self.context['request'].user
        
        # Check old password
        if not user.check_password(old_password):
            raise serializers.ValidationError({"old_password": "Current password is incorrect."})
        
        # Check if new passwords match
        if new_password != new_password_confirm:
            raise serializers.ValidationError("New passwords do not match.")
        
        # Django password validation
        try:
            validate_password(new_password, user)
        except ValidationError as e:
            raise serializers.ValidationError({"new_password": e.messages})
        
        return attrs

    def save(self):
        user = self.context['request'].user
        user.set_password(self.validated_data['new_password'])
        user.save()
        return user