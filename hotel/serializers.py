from rest_framework import serializers

from hotel.models import Dishes,Review

from django.contrib.auth.models import User

class DishSerializer(serializers.Serializer):
    name=serializers.CharField()
    category=serializers.CharField()
    price=serializers.IntegerField()




#url : mdishes/2/get_reviews
# method get
class ReviewSerializer(serializers.ModelSerializer):
    # dish=DishesModelSerializer(many=False,read_only=True)
    class Meta:
        model=Review
        fields=[
                "rating",
                "comment",
                "created_date"]
    def create(self, validated_data):
        user=self.context.get("user")
        dish=self.context.get("dish")
        return Review.objects.create(user=user,dish=dish,**validated_data)


class DishesModelSerializer(serializers.ModelSerializer):
    id=serializers.CharField(read_only=True)
    class Meta:
        model=Dishes
        fields=["id","name","category","price"]
        depth=1
    def validate(self, data):
        cost=data.get("price")
        if cost<0:
            raise serializers.ValidationError("invalid price")
        return data


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=["username","email","password"]

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

