from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .forms import UserAddressForm, UserForm
from .models import UserAddress


@login_required
def profile_view(request):
    user = request.user
    if request.method == 'POST':
        user_form = UserForm(request.POST, request.FILES, instance=user)
        if user_form.is_valid():
            user = user_form.save(commit=False)
            # avatar = request.FILES.get('avatar')
            # if avatar:
            #     filename = default_storage.save(avatar.name, avatar)
            #     user.avatar = filename
            user.save()
            messages.success(request, 'Your profile has been updated.')
            return redirect('user_profile:profile_view')
    else:
        user_form = UserForm(instance=user)
    context = {
        'user_form': user_form,
    }
    return render(request, 'dashboard.html', context)


# if UserAddress.objects.filter(user=request.user).exists():
#     address = UserAddress.objects.get(user=request.user)
#     form = UserAddressForm(instance=address)
# else:
#     address = None
#     form = UserAddressForm()
def update_address(request):
    address = get_object_or_404(UserAddress, user=request.user)
    form = UserAddressForm(request.POST or None, instance=address)
    print(address)
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('user_profile:profile_view')
    if get_object_or_404(UserAddress, user=request.user):
        form = UserAddressForm(request.POST or None, instance=address)
        # form = UserAddressForm()

    else:
        form = UserAddressForm()

    context = {
        'address': address,
        'form': form,
    }

    return render(request, 'dashboard.html', context)


class PreUrl:
    url = None

    def __init__(self, destination) -> None:
        PreUrl.url = destination


def add_address(request):
    dest = request.META.get('HTTP_REFERER')
    if request.method == 'POST':
        form = UserAddressForm(request.POST)
        if form.is_valid():
            address = form.save(commit=False)
            address.user = request.user
            address.save()
            next = PreUrl.url
            return redirect(next)
    else:
        form = UserAddressForm()
    PreUrl(dest)
    context = {
        'form': form,
    }

    return render(request, 'dashboard_address.html', context)


def edit_address(request, address_id):
    dest = request.META.get('HTTP_REFERER')
    # Get the address object based on the ID parameter
    address = get_object_or_404(UserAddress, pk=address_id)

    if request.method == 'POST':
        # If the form has been submitted, process the data
        form = UserAddressForm(request.POST, instance=address)
        if form.is_valid():
            form.save()
            # Redirect to the address list page after editing
            next = PreUrl.url
            return redirect(next)
    else:
        # If the form has not been submitted, display the form
        form = UserAddressForm(instance=address)
    PreUrl(dest)

    return render(request, 'dashboard_address.html', {'form': form})


def addresses(request):
    user_addresses = UserAddress.objects.filter(user=request.user)
    context = {
        'user_addresses': user_addresses
    }
    return render(request, 'dashboard_address_view.html', context)


def delete_address(request, address_id):
    address = get_object_or_404(UserAddress, id=address_id, user=request.user)
    if request.method == 'POST':
        address.delete()
        messages.success(request, 'Address deleted successfully!')
        return redirect('user_profile:addresses')
    return render(request, 'dashboard_address_view.html', {'address': address})
