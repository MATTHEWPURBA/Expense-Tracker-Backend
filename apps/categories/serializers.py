from rest_framework import serializers
from .models import Category

class CategorySerializer(serializers.ModelSerializer):
    """
    Serializer for Category model
    """
    class Meta:
        model = Category
        fields = ['id', 'name', 'type', 'icon', 'color', 'description', 'is_active', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def validate(self, attrs):
        """
        Validate category data
        """
        user = self.context['request'].user
        name = attrs.get('name')
        type_value = attrs.get('type')
        
        # Check for duplicate category name for the same user and type
        if self.instance:
            # Updating existing category
            existing = Category.objects.filter(
                user=user, 
                name=name, 
                type=type_value
            ).exclude(id=self.instance.id)
        else:
            # Creating new category
            existing = Category.objects.filter(
                user=user, 
                name=name, 
                type=type_value
            )
        
        if existing.exists():
            raise serializers.ValidationError(
                f"A {type_value} category with this name already exists."
            )
        
        return attrs
    
    def create(self, validated_data):
        """
        Create a new category for the current user
        """
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)

class CategoryCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating categories
    """
    class Meta:
        model = Category
        fields = ['name', 'type', 'icon', 'color', 'description']
    
    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data) 