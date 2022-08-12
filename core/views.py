from collections import Counter
import datetime
from django.shortcuts import render
from pickle import TRUE
from django.contrib import messages, auth
from django.http import HttpResponseRedirect

from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, FormView, RedirectView
from django.contrib.auth.decorators import login_required
from .forms import *
# Create your views here.


def index(request):
    return render(request, 'webapp/index.html')


def restaurant_detail(request):
    form = RestaurantDetailForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        instance = form.save(commit=False)
        print("e")
        restaurantowner = RestaurantOwner.objects.get(user_id=request.user.id)
        instance.owner = restaurantowner
        # print(restaurantowner)
        instance.location_id = 1
        instance.offer_id = 1
        instance.cuisine_id = 1
        instance.save()
        return redirect("core:index")
    loc = Location.objects.all()
    locations = []
    for x in loc:
        lps = [x.LocationId, x.LocationName]
        locations.append(lps)
    context = {
        'locations': locations,
        'form': form,
        'title': "Complete Your profile"
    }
    return render(request, 'webapp/restaurant_detail.html', context)

    # def ajax_is_favorite(request):
    #     if not request.is_ajax() or not request.method == 'POST':
    #         return HttpResponseNotAllowed(['POST'])
    #     else:
    #         # Here you have to get the data and update the object
    #         # update favourite table
    #         fav = Favourite()
    #         # fav.restaurant_id = request.
    #         fav.user_id = request.user.id
    #
    #         return HttpResponse({"success": True})


# def favorite_ajax(request):
#     data = {'success': False}
#     print("a1")
#     if request.method == 'POST':
#         print("a2")
#         user_id = request.POST.get('user_id')
#         rest_id = request.POST.get('rest_id')
#         fav = Favourite()
#         fav.restaurant_id = rest_id
#         fav.user_id = user_id
#         fav.save()
#         data['success'] = True
#     return JsonResponse(data)
def rest_index(request):
    return render(request, 'webapp/rest_index.html', {})


def restaurant_index(request):
    if request.POST:
        rest_id = request.POST['rest_id']
        user_id = request.POST['user_id']
        customer = Customer.objects.get(user_id=user_id)
        # Customer.objects.get(user_id)
        fav = Favourite()
        fav.user_id = int(customer.id)
        fav.restaurant_id = int(rest_id)
        fav.save()
    #     try:
    #         offer = Offer.objects.get(offer_id=offerid)
    #         ownner = RestaurantOwner.objects.get(user_id=request.user.id)
    #         rest = Restaurant.objects.get(owner=ownner)
    #         rest.offer = offer
    #         rest.save()
    #     except Offer.DoesNotExist:
    #         print("i23")
    #     select = request.POST['orderstatus']
    #     print("manas")
    #     print(oid)
    # select = int(

    if request.user.is_authenticated:
        customer = Customer.objects.get(user=request.user)
        r_object = Restaurant.objects.filter(location=customer.location)
        user_id = customer.user_id
        temp = 1
        location = customer.location.LocationName
        fav = Favourite.objects.filter(user_id=customer.id)
    else:
        r_object = None
        user_id = None
        temp = 1
        location = None
        fav = None
        # query = request.GET.get('q')
        # if query:
        #     r_object = Restaurant.objects.filter(Q(location_id__iins=query)).distinct()
    context = {
        'r_object': r_object,
        'location': location,
        'user_id': user_id,
        'temp': temp,
        'fav': fav,
    }
    return render(request, 'webapp/restaurant_index.html', context)


def restaurantProfile(request, pk=None):
    if pk:
        user = User.objects.get(pk=pk)
    else:
        user = request.user

    restaurant_owner = RestaurantOwner.objects.get(user_id=request.user.id)
    restaurant = Restaurant.objects.get(owner_id=restaurant_owner)

    Context = {
        'user': user,
        'restaurant': restaurant,
        'restaurant_owner': restaurant_owner,

    }

    return render(request, 'webapp/rest_profile.html', Context)


def orderplaced(request):
    return render(request, 'webapp/orderplaced.html', {})


# #
# #
# # # Showing Restaurants list to Customer
# # def restuarent(request):
# #     r_object = Restaurant.objects.all()
# #     query = request.GET.get('q')
# #     if query:
# #         r_object = Restaurant.objects.filter(Q(rname__iins=query)).distinct()
# #         return render(request, 'webapp/restaurents.html', {'r_object': r_object})
# #     return render(request, 'webapp/restaurents.html', {'r_object': r_object})
# #
# #
# logout


# # # customer profile view
# # def customerProfile(request, pk=None):
# #     if pk:
# #         user = User.objects.get(pk=pk)
# #     else:
# #         user = request.user
# #
# #     return render(request, 'webapp/profile.html', {'user': user})
# #
# #
#
# #
# # #  Update customer detail
# # def updateCustomer(request, id):
# #     form = CustomerForm(request.POST or None, instance=request.user.customer)
# #     if form.is_valid():
# #         form.save()
# #         return redirect('profile')
# #     context = {
# #         'form': form,
# #         'title': "Update Your profile"
# #     }
# #     return render(request, 'webapp/customer_profile_register.html', context)
# #
# #
def restuarantMenu(request, pk=None):
    menu = FoodRestaurant.objects.filter(restaurant_id=pk)
    rest = Restaurant.objects.filter(restaurant_id=pk)

    items = []
    for i in menu:
        item = FoodItem.objects.filter(food_item_id=i.food_item_id)
        for content in item:
            ml = ItemType.objects.get(type_id=content.type_id)
            temp = [content.name, content.is_veg, ml.name, i.cost, i.food_item_id]
            items.append(temp)
    context = {
        'items': items,
        'r_id': pk,
        'r_name': rest[0].name,
        'r_ex': rest[0].is_exclusive,
        'r_cost': rest[0].avg_cost,
        'r_time': rest[0].avg_time,
        'r_phone': rest[0].phone,
        'r_logo': rest[0].r_logo,
        'r_cuisine': rest[0].cuisine.cuisine_name,
        'r_add': rest[0].address,
        # 'rlocation': rest[0].location,
    }
    return render(request, 'webapp/menu.html', context)


# #
# #
@login_required
def checkout(request):
    if request.POST:
        ptype = request.POST['submit']
        ordid = request.POST['oid']
        order = Order.objects.get(order_id=ordid)
        order.status = Order.ORDER_STATE_PLACED
        order.payment_hash_id = 1
        order.instructions = request.POST['instruct']
        order.save()
        if ptype == "Pay Later":
            order.payment_mode_online = False
            order.save()
            return render(request, 'webapp/orderplaced.html', {})
        else:
            payment = Payment()
            payment.amount = request.POST['total_price']
            payment.save()
            order.payment_hash_id = payment.hash
            order.save()
            return render(request, 'webapp/online_pay.html', {})
    else:
        cart = request.COOKIES['cart'].split(",")
        cart = dict(Counter(cart))
        items = []
        totalprice = 0
        order = Order()

        # order.save()
        print(order.order_id)
        order.tax = 0.05 * totalprice
        order.user = Customer.objects.get(user_id=request.user.id)
        order.datetime = datetime.now()
        # order.offer = Offer.objects.get(offer_id=1)
        for x, y in cart.items():
            it = FoodItem.objects.get(food_item_id=int(x))
            print(it.name)
            item_rest = FoodRestaurant.objects.get(food_item_id=it.food_item_id)
            order.restaurant = Restaurant.objects.get(restaurant_id=item_rest.restaurant.restaurant_id)
            yu = Offer.objects.get(
                offer_id=Restaurant.objects.get(restaurant_id=item_rest.restaurant.restaurant_id).offer_id)
            print(yu.discount)
            order.offer_id = yu.offer_id
        order.payment_hash_id = 1
        order.save()
        for x, y in cart.items():
            item = []
            it = FoodItem.objects.get(food_item_id=int(x))
            print(it.name)
            item_rest = FoodRestaurant.objects.get(food_item_id=it.food_item_id)

            print(order.order_id)
            order_detail = OrderDetail()
            order_detail.food_item_id = it.food_item_id
            order_detail.order_id = order.order_id
            order_detail.quantity = int(y)
            order_detail.save()
            item.append(it.name)
            item.append(y)
            totalprice += item_rest.cost * y
            item.append(item_rest.cost * y)
            items.append(item)
        order.tax = int(0.05 * totalprice)
        withouttax = totalprice
        totalprice += order.tax
        totalprice -= int(yu.discount)
        if totalprice < order.tax:
            totalprice = order.tax
        order.save()

        context = {
            "items": items,
            "yu": yu,
            "totalprice": totalprice,
            "withouttax": withouttax,
            "order": order,
            "oid": order.order_id

        }
        return render(request, 'webapp/order.html', context)


def pay(request):
    if request.POST:
        # return redirect('/orderplaced/')
        return render(request, 'webapp/orderplaced.html', {})


# #
# #
# # ####### ------------------- Restaurant Side ------------------- #####
# #
# # # creating restuarant account
# # def restRegister(request):
# #     form = RestuarantSignUpForm(request.POST or None)
# #     if form.is_valid():
# #         user = form.save(commit=False)
# #         username = form.cleaned_data['username']
# #         password = form.cleaned_data['password']
# #         user.is_restaurant = True
# #         user.set_password(password)
# #         user.save()
# #         user = authenticate(username=username, password=password)
# #         if user is not None:
# #             if user.is_active:
# #                 login(request, user)
# #                 return redirect("rcreate")
# #     context = {
# #         'form': form
# #     }
# #     return render(request, 'webapp/restsignup.html', context)
# #
# #
# # # restuarant login
# # def restLogin(request):
# #     if request.method == "POST":
# #         username = request.POST['username']
# #         password = request.POST['password']
# #         user = authenticate(username=username, password=password)
# #         if user is not None:
# #             if user.is_active:
# #                 login(request, user)
# #                 return redirect("rprofile")
# #             else:
# #                 return render(request, 'webapp/restlogin.html', {'error_message': 'Your account disable'})
# #         else:
# #             return render(request, 'webapp/restlogin.html', {'error_message': 'Invalid Login'})
# #     return render(request, 'webapp/restlogin.html')
# #
# #
# # # restaurant profile view
# # def restaurantProfile(request, pk=None):
# #     if pk:
# #         user = User.objects.get(pk=pk)
# #     else:
# #         user = request.user
# #
# #     return render(request, 'webapp/rest_profile.html', {'user': user})
# #
# #
# # # create restaurant detail
# # @login_required(login_url='/login/restaurant/')
# # def createRestaurant(request):
# #     form = RestuarantForm(request.POST or None, request.FILES or None)
# #     if form.is_valid():
# #         instance = form.save(commit=False)
# #         instance.user = request.user
# #         instance.save()
# #         return redirect("rprofile")
# #     context = {
# #         'form': form,
# #         'title': "Complete Your Restaurant profile"
# #     }
# #     return render(request, 'webapp/rest_profile_form.html', context)
# #
# #
# # # Update restaurant detail
# # @login_required(login_url='/login/restaurant/')
# # def updateRestaurant(request, id):
# #     form = RestuarantForm(request.POST or None, request.FILES or None, instance=request.user.restaurant)
# #     if form.is_valid():
# #         form.save()
# #         return redirect('rprofile')
# #     context = {
# #         'form': form,
# #         'title': "Update Your Restaurant profile"
# #     }
# #     return render(request, 'webapp/rest_profile_form.html', context)
# #
# #
# add  menu item for restaurant
@login_required(login_url='/login/restaurant/')
def menu_manipulation(request):
    if not request.user.is_authenticated:
        return redirect("rlogin")
    rest = Restaurant.objects.get(owner=RestaurantOwner.objects.get(user_id=request.user.id))
    if request.POST:
        print("8")
        rtype = request.POST['submit']
        print(rtype)
        if rtype == "Modify":
            print("23")
            foodid = int(request.POST['fooditemid'])
            food = FoodRestaurant.objects.get(food_item_id=foodid)
            food.cost = int(request.POST['cost'])
            foodItem = FoodItem.objects.get(food_item_id=foodid)
            foodItem.name = request.POST['name']
            is_veg = request.POST['is_veg']
            print(is_veg)
            if is_veg:
                foodItem.is_veg = True
            else:
                foodItem.is_veg = False

            ittype = ItemType.objects.get(type_id=request.POST['type'])
            foodItem.type = ittype
            foodItem.save()
            food.save()

        elif rtype == "Add":
            print("13")
            foodrest = FoodRestaurant()
            name = request.POST['name']
            try:
                item = FoodItem.objects.get(name=name)
            except FoodItem.DoesNotExist:
                item = None
            if item is not None:
                print("6")
                foodrest.food_item_id = item.food_item_id
            else:
                print("2")
                fooditem = FoodItem()
                fooditem.name = name
                is_veg = request.POST['is_veg']
                if int(is_veg) == 1:
                    print("3")
                    fooditem.is_veg = True
                else:
                    print("4")
                    fooditem.is_veg = False
                fooditem.type_id = int(request.POST['type_id'])
                fooditem.save()
                foodrest.food_item_id = fooditem.food_item_id
                print("5")
            print("7")

            foodrest.restaurant_id = rest.restaurant_id
            foodrest.cost = request.POST['cost']
            foodrest.save()
        elif rtype == "Select":
            offerid = int(request.POST['offerid'])
            try:
                offer = Offer.objects.get(offer_id=offerid)
                ownner = RestaurantOwner.objects.get(user_id=request.user.id)
                rest = Restaurant.objects.get(owner=ownner)
                rest.offer = offer
                rest.save()
            except Offer.DoesNotExist:
                print("i23")

        else:

            foodid = int(request.POST['fooditemid'])
            try:
                food = FoodRestaurant.objects.get(food_item_id=foodid)
                food.delete()
            except FoodRestaurant.DoesNotExist:
                print("d")

    food = FoodRestaurant.objects.filter(restaurant=rest)
    menu = []
    for x in food:
        y = FoodItem.objects.get(food_item_id=x.food_item_id)
        cmenu = []
        cmenu.append(x.food_item_id)
        cmenu.append(y.name)
        cmenu.append(x.cost)
        cmenu.append(x.restaurant)
        cmenu.append(y.is_veg)

        print("yello")
        print(y.type)
        itype = ItemType.objects.get(type_id=y.type.type_id)
        cmenu.append(itype.name)
        cmenu.append(itype.type_id)
        if y.is_veg == 1:
            cmenu.append("veg")
        else:
            cmenu.append("non veg")
        menu.append(cmenu)
    offers = Offer.objects.all()
    appliedoffer = Offer.objects.get(offer_id=rest.offer_id)
    i1 = ItemType.objects.all()
    itemtypes = []
    vegarray = [[0, "non veg"], [1, "veg"]]
    for x in i1:
        itemtypes.append([x.type_id, x.name])
    context = {
        "menu": menu,
        "user": request.user,
        "itemtypes": itemtypes,
        "vegarray": vegarray,
        "offer": offers,
        "applied": appliedoffer
    }
    return render(request, 'webapp/menu_modify.html', context)


def orderlist(request):
    if request.POST:
        oid = request.POST['orderid']
        select = request.POST['orderstatus']
        print("manas")
        print(oid)
        select = int(select)
        print(select)

        try:
            order = Order.objects.get(order_id=oid)
        except Order.DoesNotExist:
            order = None

        # print(order.restaurant.name)
        if order is not None:
            # x = Order.ORDER_STATE_WAITING

            if select == 1:
                x = Order.ORDER_STATE_PLACED
            elif select == 2:
                x = Order.ORDER_STATE_ACKNOWLEDGED
            elif select == 3:
                x = Order.ORDER_STATE_COMPLETED
            elif select == 4:
                x = Order.ORDER_STATE_DISPATCHED
            elif select == 5:
                x = Order.ORDER_STATE_CANCELLED
            else:
                x = 1
            order.status = x
            print("ml")
            order.save()
    ownner = RestaurantOwner.objects.get(user_id=request.user.id)
    restaurant = Restaurant.objects.get(owner=ownner)
    orders = Order.objects.filter(restaurant=restaurant).order_by('-datetime')
    print("hi")
    # print(orders[0].instructions)
    corders = []

    for order in orders:

        # user = User.objects.get(id=order.user_id)
        corder = []
        customer = Customer.objects.get(id=order.user_id)
        # print('cust')
        # print(customer.f_name)
        corder.append(customer.f_name + ' ' + customer.l_name)
        corder.append(customer.phone)
        items_list = OrderDetail.objects.filter(order_id=order.order_id)
        print("item")
        # print(items_list[0].)

        items = []
        without_tax = 0
        for item in items_list:
            citem = []
            item_name = FoodItem.objects.get(food_item_id=item.food_item_id)
            citem.append(item_name.name)
            citem.append(item.quantity)
            fooditem = FoodRestaurant.objects.get(food_item_id=item.food_item_id)
            print("ok")
            print(fooditem.cost)
            without_tax += fooditem.cost * item.quantity
            citem.append(fooditem.cost * item.quantity)
            items.append(citem)

        corder.append(items)
        yu = Offer.objects.get(
            offer_id=order.offer_id)

        if (int(without_tax) + int(order.tax) - int(yu.discount)) < int(order.tax):
            corder.append(int(order.tax))
        else:
            corder.append(int(without_tax) + int(order.tax) - int(yu.discount))
        # corder.append(without_tax + order.tax)
        corder.append(without_tax)
        corder.append(order.tax)
        corder.append(order.instructions)
        corder.append(order.order_id)

        x = order.status
        if x == Order.ORDER_STATE_PLACED:
            x = 1
        elif x == Order.ORDER_STATE_ACKNOWLEDGED:
            x = 2
        elif x == Order.ORDER_STATE_COMPLETED:
            x = 3
        elif x == Order.ORDER_STATE_DISPATCHED:
            x = 4
        elif x == Order.ORDER_STATE_CANCELLED:
            x = 5
        else:
            continue
        # x = 1
        print('i am here')

        corder.append(x)
        corder.append(order.review)
        corder.append(yu.discount)
        corders.append(corder)

    context = {
        "orders": corders,
    }

    return render(request, "webapp/order-list.html", context)


def myorders(request):
    if request.POST:
        oid = request.POST['orderid']
        review = request.POST.get('review', '')
        print(review)
        print('review')
        rate = request.POST.get('rating', 4)

        try:
            order = Order.objects.get(order_id=oid)
        except Order.DoesNotExist:
            order = None
        print('order')
        if order is not None:
            order.review = review
            order.rating = int(rate)
        order.save()

    customer = Customer.objects.get(user_id=request.user.id)
    orders = Order.objects.filter(user_id=customer.id).order_by('-datetime')
    corders = []
    for order in orders:

        corder = []
        rest = Restaurant.objects.get(restaurant_id=order.restaurant_id)

        corder.append(rest.name)
        corder.append(customer.phone)
        items_list = OrderDetail.objects.filter(order_id=order.order_id)

        items = []
        without_tax = 0
        for item in items_list:
            citem = []
            item_name = FoodItem.objects.get(food_item_id=item.food_item_id)
            citem.append(item_name.name)
            citem.append(item.quantity)
            fooditem = FoodRestaurant.objects.get(food_item_id=item.food_item_id)

            without_tax += fooditem.cost * item.quantity
            citem.append(fooditem.cost * item.quantity)
            items.append(citem)

        corder.append(items)
        yu = Offer.objects.get(
            offer_id=order.offer_id)

        if (int(without_tax) + int(order.tax) - int(yu.discount)) < int(order.tax):
            corder.append(int(order.tax))
        else:
            corder.append(int(without_tax) + int(order.tax) - int(yu.discount))

        corder.append(without_tax)
        corder.append(order.tax)
        corder.append(order.instructions)
        corder.append(order.order_id)
        corder.append(order.rating)
        corder.append(order.review)

        x = order.status

        corder.append(x)
        corder.append(yu.discount)
        corders.append(corder)

    context = {
        "orders": corders,
    }
    return render(request, "webapp/my_order.html", context)
