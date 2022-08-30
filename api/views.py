from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from api.models import menu_items

#url :localhost:8000/hotels/dishes?category=veg

class DishesView(APIView):
    def get(self,request,*args,**kwargs):
        print(request.query_params)
        all_items=menu_items
        if "category" in request.query_params:
            all_items=[ item for item in all_items if item["category"]==request.query_params.get("category")]
        if "limit" in request.query_params:
            limit=int(request.query_params.get("limit"))
            all_items=all_items[0:limit]
        return Response(data=all_items)
      #request.query_params={"category":"veg",limit:2}


    def post(self,request,*args,**kwargs):
        item=request.data
        menu_items.append(item)
        return Response(data=item)

#url localhost:8000/hotels/dishes/1
# method :get
# return details of specific product

class DishDetailView(APIView):
    def get(self,request,*args,**kwargs):
        code=kwargs.get("dcode")
        dish=[item for item in menu_items if item["code"]==code].pop()
        return Response(data=dish)

    def put(self,request,*args,**kwargs):
        code=kwargs.get("dcode")
        dish=[item for item in menu_items if item["code"]==code].pop()
        data=request.data
        dish.update(data)
        return Response(data=data)

    def delete(self,request,*args,**kwargs):
        code=kwargs.get("dcode")
        dish=[item for item in menu_items if item["code"]==code].pop()
        menu_items.remove(dish)
        return Response(data=dish)





