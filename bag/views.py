from django.shortcuts import render, redirect, reverse, HttpResponse, get_object_or_404
from django.contrib import messages

from products.models import Size

# Create your views here.


def view_bag(request):
    """ A view that renders the bag contents page """

    return render(request, 'bag/bag.html')


def add_to_bag(request, product_id, size_id):
    """ Add a quantity of the specified product to the shopping bag """

    product = get_object_or_404(Size, pk=size_id)
    quantity = int(request.POST.get('quantity'))
    redirect_url = request.POST.get('redirect_url')
    bag = request.session.get('bag', {})

    if size_id in list(bag.keys()):
        bag[size_id] += quantity
        messages.success(
            request, f'Updated {product.product.name} quantity to {bag[size_id]}')
    else:
        bag[size_id] = quantity
        messages.success(request, f'Added {product.product.name} to your bag')

    request.session['bag'] = bag
    print(request.session['bag'])
    return redirect(redirect_url)


def adjust_bag(request, item_id):
    """Adjust the quantity of the specified product to the specified ammout"""

    product = get_object_or_404(Size, pk=item_id)
    quantity = int(request.POST.get('quantity'))
    bag = request.session.get('bag', {})

    if quantity > 0:
        bag[item_id] = quantity
        messages.success(
            request, f'Updated {product.product.name} quantity to {bag[item_id]}')
    else:
        bag.pop(item_id)
        messages.success(
            request, f'Removed {product.product.name} quantity to {bag[item_id]}')

    request.session['bag'] = bag
    print(request.session['bag'])
    return redirect(reverse('view_bag'))


def remove_from_bag(request, item_id):
    """Remove the item from the shopping bag"""

    try:
        product = get_object_or_404(Size, pk=item_id)
        if 'product_size' in request.POST:
            size = request.POST['product_size']
        bag = request.session.get('bag', {})

        bag.pop(item_id)

        request.session['bag'] = bag
        return HttpResponse(status=200)

    except Exception as e:
        messages.error(request, f'Error removing item: {e}')
        return HttpResponse(status=500)
