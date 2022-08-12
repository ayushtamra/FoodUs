from pickle import TRUE
from django.contrib import messages, auth
from django.http import HttpResponseRedirect

from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, FormView, RedirectView
from .forms import *


class CustRegisterView(CreateView):
    model = User
    form_class = UserRegistrationForm
    template_name = 'accounts/customer_register.html'
    success_url = '/'

    extra_context = {
        'title': 'Register'
    }

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return HttpResponseRedirect(self.get_success_url())
        return super().dispatch(self.request, *args, **kwargs)

    def get_success_url(self):
        return self.success_url

    def post(self, request, *args, **kwargs):
        if User.objects.filter(email=request.POST['email']).exists():
            messages.warning(request, 'This email is already taken')
            return redirect('accounts:customer_register')

        user_form = UserRegistrationForm(data=request.POST)

        if user_form.is_valid():
            user = user_form.save(commit=False)
            password = user_form.cleaned_data.get("password1")
            user.is_customer = True
            user.set_password(password)
            user.save()
            messages.success(request, 'Successfully registered')
            return redirect('accounts:customer_login')
        else:
            print(user_form.errors)
            return render(request, 'accounts/customer_register.html', {'form': user_form})


class CustLoginView(FormView):
    success_url = '/accounts/register/customer/profile'
    form_class = UserLoginForm
    template_name = 'accounts/customer_login.html'

    extra_context = {
        'title': 'Login'
    }

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return HttpResponseRedirect(self.get_success_url())
        return super().dispatch(self.request, *args, **kwargs)

    def get_form_class(self):
        return self.form_class

    def form_valid(self, form):
        auth.login(self.request, form.get_user())
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))


# For restaurants

class RestRegisterView(CreateView):
    model = User
    form_class = UserRegistrationForm
    template_name = 'accounts/restaurant_register.html'
    success_url = '/'

    extra_context = {
        'title': 'Register'
    }

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return HttpResponseRedirect(self.get_success_url())
        return super().dispatch(self.request, *args, **kwargs)

    def get_success_url(self):
        return self.success_url

    def post(self, request, *args, **kwargs):
        if User.objects.filter(email=request.POST['email']).exists():
            messages.warning(request, 'This email is already taken')
            return redirect('accounts:restaurant_register')

        user_form = UserRegistrationForm(data=request.POST)

        if user_form.is_valid():
            user = user_form.save(commit=False)
            password = user_form.cleaned_data.get("password1")
            user.is_restaurant_owner = True
            user.set_password(password)
            user.save()
            messages.success(request, 'Successfully registered')
            return redirect('accounts:restaurant_login')
        else:
            print(user_form.errors)
            return render(request, 'accounts/restaurant_register.html', {'form': user_form})



class RestLoginView(FormView):
    success_url = '/'
    form_class = UserLoginForm
    template_name = 'accounts/restaurant_login.html'

    extra_context = {
        'title': 'Login'
    }

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return HttpResponseRedirect(self.get_success_url())
        return super().dispatch(self.request, *args, **kwargs)

    def get_form_class(self):
        return self.form_class

    def form_valid(self, form):
        auth.login(self.request, form.get_user())
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))




# To change these 2 profile reg methods if required to the class ones

def customer_profile_register(request):
    form = CustomerRegisterProfileForm(request.POST or None)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.user = request.user
        # print(instance)
        instance.location_id = 1
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
    return render(request, 'accounts/customer_profile_register.html', context)



def restaurant_profile_register(request):
    form = RestaurantRegisterProfileForm(request.POST or None)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.user = request.user
        # print(instance)
        instance.location_id = 1
        instance.save()
        return redirect("core:restaurant_detail")
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
    return render(request, 'accounts/restaurant_profile_register.html', context)



class LogoutView(RedirectView):
    """
    Provides users the ability to logout
    """
    url = reverse_lazy('core:index')

    def get(self, request, *args, **kwargs):
        auth.logout(request)
        messages.success(request, 'You are now logged out')
        return super(LogoutView, self).get(request, *args, **kwargs)
