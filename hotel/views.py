from django.shortcuts import render

# Create your views here.

from rest_framework.views import  APIView
from rest_framework.response import Response
from hotel.models import Dishes,Review
from hotel.serializers import DishSerializer,DishesModelSerializer,UserSerializer,ReviewSerializer
from django.contrib.auth.models import User
from rest_framework import permissions,authentication
from rest_framework.decorators import  action
class DishesView(APIView):

    def get(self,request,*args,**kwargs):
        all_dishes=Dishes.objects.all()
        serializer=DishSerializer(all_dishes,many=True)
        return Response(data=serializer.data)
    def post(self,request,*args,**kwargs):
      serializer=DishSerializer(data=request.data)
      if serializer.is_valid():
          category=serializer.validated_data.get("category")
          name=serializer.validated_data.get("name")
          price=serializer.validated_data.get("price")
          Dishes.objects.create(name=name,
                                category=category,
                                price=price)
          return Response(data=serializer.data)

class DishDetailsView(APIView):
    def get(self,request,*args,**kwargs):
        id=kwargs.get("id")
        dish=Dishes.objects.get(id=id)
        serializer=DishSerializer(dish)
        return Response(data=serializer.data)
    def put(self,request,*args,**kwargs):
        id = kwargs.get("id")
        instance = Dishes.objects.get(id=id)
        serializer=DishSerializer(data=request.data)
        if serializer.is_valid():
            category = serializer.validated_data.get("category")
            name = serializer.validated_data.get("name")
            price = serializer.validated_data.get("price")
            instance.name=name
            instance.price=price
            instance.category=category
            instance.save()
            return Response(data=serializer.data)

    def delete(self,request,*args,**kwargs):
        id=kwargs.get("id")
        dish=Dishes.objects.get(id=id)
        dish.delete()
        return Response({"msg":"deleted"})


class MenuItemsView(APIView):
    serilalizer_class=DishesModelSerializer

    def get(self,request,*args,**kwargs):
        all_dishes=Dishes.objects.all()
        serializer=self.serilalizer_class(all_dishes,many=True)
        return Response(data=serializer.data)
    def post(self,request,*args,**kwargs):
        serializer=DishesModelSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data)
        else:
            return Response(data=serializer.errors)




class MenuItemDetailsView(APIView):
    serializer_class=DishesModelSerializer
    def get(self,request,*args,**kwargs):
        id=kwargs.get("id")
        dish=Dishes.objects.get(id=id)
        serializer=DishesModelSerializer(dish)
        return Response(data=serializer.data)
    def delete(self, request, *args, **kwargs):
        id = kwargs.get("id")
        dish = Dishes.objects.get(id=id)
        dish.delete()
        return Response(data=dish)
    def put(self,request,*args,**kwargs):
        id = kwargs.get("id")
        instance = Dishes.objects.get(id=id)
        serializer=self.serializer_class(data=request.data,instance=instance)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data)
        else:
            return Response(serializer.errors)


class SingnUpView(APIView):

    def post(self,request,*args,**kwargs):
        serializer=UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data)

#APIView
# ViewSets

from rest_framework import viewsets
class DishViewsetView(viewsets.ViewSet):
    serializer_class = DishesModelSerializer
    def list(self,request,*args,**kwargs):
        qs=Dishes.objects.all()
        if "category" in request.query_params:
            category=request.query_params.get("category")
            qs=qs.filter(category=category)
        if "price_lt" in request.query_params:
            price=request.query_params.get("price_lt")
            qs=qs.filter(price__lte=price)
        serializer=DishesModelSerializer(qs,many=True)
        return Response(serializer.data)






    def create(self,request,*args,**kwargs):
        serializer=DishesModelSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data)
        else:
            return Response(data=serializer.errors)

    def retrieve(self, request, *args, **kwargs):
        id = kwargs.get("pk")
        dish = Dishes.objects.get(id=id)
        serializer = DishesModelSerializer(dish)
        return Response(data=serializer.data)

    def destroy(self, request, *args, **kwargs):
        id = kwargs.get("pk")
        dish = Dishes.objects.get(id=id)
        dish.delete()
        return Response(data=dish)

    def update(self, request, *args, **kwargs):
        id = kwargs.get("pk")
        instance = Dishes.objects.get(id=id)
        serializer = self.serializer_class(data=request.data, instance=instance)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data)
        else:
            return Response(serializer.errors)


class DishModelViewsetView(viewsets.ModelViewSet):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = DishesModelSerializer
    queryset = Dishes.objects.all()
    model=Dishes

    @action(detail=True,methods=["get"])
    def get_reviews(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        dish=Dishes.objects.get(id=id)
        qs=Review.objects.filter(dish=dish)
        serializer=ReviewSerializer(qs,many=True)
        return Response(data=serializer.data)

    @action(detail=True,methods=["post"])
    def add_review(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        dish=Dishes.obejcts.get(id=id)
        user=request.user
        serializer=ReviewSerializer(data=request.data,context={"user":user,"dish":dish})
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data)
        else:
            return Response(data=serializer.errors)



