from rest_framework import serializers
from .models import Transaction
from apps.categories.models import Category
from apps.categories.serializers import CategorySerializer

class TransactionSerializer(serializers.ModelSerializer):
    """
    Serializer for Transaction model with category details
    """
    category_details = CategorySerializer(source='category', read_only=True)
    category = serializers.CharField(write_only=True)  # Accept category name for creation
    
    class Meta:
        model = Transaction
        fields = [
            'id', 'title', 'description', 'amount', 'type', 'category', 
            'category_details', 'date', 'receipt', 'metadata', 
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def validate_category(self, value):
        """
        Validate that the category exists and belongs to the user
        """
        user = self.context['request'].user
        try:
            category = Category.objects.get(name=value, user=user, is_active=True)
            return category
        except Category.DoesNotExist:
            raise serializers.ValidationError(f"Category '{value}' not found or inactive.")
    
    def validate(self, attrs):
        """
        Validate transaction data
        """
        category = attrs.get('category')
        transaction_type = attrs.get('type')
        
        # Ensure transaction type matches category type
        if category and category.type != transaction_type:
            raise serializers.ValidationError(
                f"Transaction type '{transaction_type}' does not match category type '{category.type}'."
            )
        
        return attrs
    
    def create(self, validated_data):
        """
        Create a new transaction for the current user
        """
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)
    
    def to_representation(self, instance):
        """
        Customize the output representation
        """
        data = super().to_representation(instance)
        # Replace category_details with category for the output
        data['category'] = data.pop('category_details')
        return data

class TransactionCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating transactions
    """
    category = serializers.CharField()
    
    class Meta:
        model = Transaction
        fields = ['title', 'description', 'amount', 'type', 'category', 'date', 'receipt', 'metadata']
    
    def validate_category(self, value):
        """
        Validate and get the category object
        """
        user = self.context['request'].user
        try:
            category = Category.objects.get(name=value, user=user, is_active=True)
            return category
        except Category.DoesNotExist:
            raise serializers.ValidationError(f"Category '{value}' not found or inactive.")
    
    def validate(self, attrs):
        """
        Validate transaction data
        """
        category = attrs.get('category')
        transaction_type = attrs.get('type')
        
        # Ensure transaction type matches category type
        if category and category.type != transaction_type:
            raise serializers.ValidationError(
                f"Transaction type '{transaction_type}' does not match category type '{category.type}'."
            )
        
        return attrs
    
    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)

class TransactionUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer for updating transactions
    """
    category = serializers.CharField(required=False)
    
    class Meta:
        model = Transaction
        fields = ['title', 'description', 'amount', 'type', 'category', 'date', 'receipt', 'metadata']
    
    def validate_category(self, value):
        """
        Validate and get the category object
        """
        user = self.context['request'].user
        try:
            category = Category.objects.get(name=value, user=user, is_active=True)
            return category
        except Category.DoesNotExist:
            raise serializers.ValidationError(f"Category '{value}' not found or inactive.")

# apps/transactions/serializers.py 