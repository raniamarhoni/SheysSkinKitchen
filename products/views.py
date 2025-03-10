from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q, F, Avg, Min
from django.db.models.functions import Lower
from datetime import datetime

from .models import Product, Category, Size, Review
from .forms import ProductForm, SizeForm, ReviewForm

# Create your views here.


def all_products(request):
    """ A view to show all products, including sorting and search queries """

    products = Product.objects.all()
    query = None
    categories = Category.objects.all()
    sort = None
    direction = None

    if request.GET:
        if 'sort' in request.GET:
            sortkey = request.GET['sort']
            sort = sortkey
            if sortkey == 'name':
                sortkey = 'lower_name'
                products = products.annotate(lower_name=Lower('name'))
            if sortkey == 'category':
                sortkey = 'category__name'
            if sortkey == 'rating':
                sortkey = 'avgreview'
                products = products.annotate(avgreview=Avg('review__star'))
            if sortkey == 'price':
                sortkey = 'minprice'
                products = products.annotate(minprice=Min('size__price'))
            if 'direction' in request.GET:
                direction = request.GET['direction']
                if direction == 'desc':
                    sortkey = f'{sortkey}'
                    products = products.order_by(
                        F(sortkey).desc(nulls_last=True))
                else:
                    products = products.order_by(sortkey)

        if 'category' in request.GET:
            categories = request.GET['category'].split(',')
            products = products.filter(category__name__in=categories)
            categories = Category.objects.filter(name__in=categories)

        if 'q' in request.GET:
            query = request.GET['q']
            if not query:
                messages.error(request,
                               ("You didn't enter any search criteria!"))
                return redirect(reverse('products'))

            queries = Q(name__icontains=query) | Q(
                description__icontains=query)
            products = products.filter(queries)

    current_sorting = f'{sort}_{direction}'

    context = {
        'products': products,
        'search_term': query,
        'current_categories': categories,
        'current_sorting': current_sorting,
    }

    return render(request, 'products/products.html', context)


def product_detail(request, product_id):
    """ A view to show individual product details """

    product = get_object_or_404(Product, pk=product_id)
    reviews = Review.objects.filter(product=product_id)

    context = {
        'product': product,
        'reviews': reviews,
    }

    return render(request, 'products/product_detail.html', context)


def product_size(request, product_id, size_id):
    """ A view to show individual product details """

    product = get_object_or_404(Product, pk=product_id)
    size = get_object_or_404(Size, pk=size_id)
    reviews = Review.objects.filter(product=product_id)

    context = {
        'product': product,
        'size': size,
        'reviews': reviews,
    }

    return render(request, 'products/product_size.html', context)



@login_required
def add_product(request):
    """ Add a product to the store """
    if not request.user.is_superuser:
        messages.error(request, 'Sorry, only store owners can do that.')
        return redirect(reverse('home'))

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save()
            messages.success(request, 'Successfully added product!')
            return redirect(reverse('product_detail', args=[product.id]))
        else:
            messages.error(request,
                           ('Failed to add product. '
                            'Please ensure the form is valid.'))
    else:
        form = ProductForm()

    template = 'products/add_product.html'
    context = {
        'form': form,
    }

    return render(request, template, context)


@login_required
def edit_product(request, product_id):
    """ Edit a product in the store """
    if not request.user.is_superuser:
        messages.error(request, 'Sorry, only store owners can do that.')
        return redirect(reverse('home'))

    product = get_object_or_404(Product, pk=product_id)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, 'Successfully updated product!')
            return redirect(reverse('product_detail', args=[product.id]))
        else:
            messages.error(request,
                           ('Failed to update product. '
                            'Please ensure the form is valid.'))
    else:
        form = ProductForm(instance=product)
        messages.info(request, f'You are editing {product.name}')

    template = 'products/edit_product.html'
    context = {
        'form': form,
        'product': product,
    }

    return render(request, template, context)

@login_required
def delete_product(request, product_id):
    """ Delete a product from the store """
    if not request.user.is_superuser:
        messages.error(request, 'Sorry, only store owners can do that.')
        return redirect(reverse('home'))

    product = get_object_or_404(Product, pk=product_id)
    product.delete()
    messages.success(request, 'Product deleted!')
    return redirect(reverse('products'))

@login_required
def add_size(request, product_id):
    if not request.user.is_superuser:
        messages.error(request, 'Sorry, only store owners can do that.')
        return redirect(reverse('home'))

    product = get_object_or_404(Product, pk=product_id)
    if request.method == 'POST':
        form = SizeForm(request.POST)
        if form.is_valid():
            a = form.save(commit=False)
            a.product = product
            a.save()
            messages.success(request, 'Successfully added size!')
            return redirect(reverse('product_detail', args=[product.id]))
        else:
            messages.error(request,
                           ('Failed to update size. '
                            'Please ensure the form is valid.'))
    else:
        form = SizeForm(instance=product)
        messages.info(request, f'You are adding a size to {product.name}')

    template = 'products/add_size.html'
    context = {
        'form': form,
        'product': product,
    }

    return render(request, template, context)


@login_required
def edit_size(request, product_id, size_id):
    if not request.user.is_superuser:
        messages.error(request, 'Sorry, only store owners can do that.')
        return redirect(reverse('home'))

    product = get_object_or_404(Product, pk=product_id)
    size = get_object_or_404(Size, pk=size_id)
    form = SizeForm(request.POST, request.FILES, instance=size)
    if request.method == 'POST':
        if form.is_valid():
            a = form.save(commit=False)
            a.product = product
            a.save()
            messages.success(request, 'Successfully edited size!')
            return redirect(reverse('product_detail', args=[product.id]))
        else:
            messages.error(request,
                           ('Failed to edit size. '
                            'Please ensure the form is valid.'))
    else:
        form = SizeForm(instance=size)
        messages.info(request, f'You are editing size {size.size} for {product.name}')

    template = 'products/edit_size.html'
    context = {
        'form': form,
        'product': product,
        'size': size,
    }

    return render(request, template, context)

@login_required
def delete_size(request, product_id, size_id):
    """ Delete a product from the store """
    if not request.user.is_superuser:
        messages.error(request, 'Sorry, only store owners can do that.')
        return redirect(reverse('home'))

    product = get_object_or_404(Product, pk=product_id)
    size = get_object_or_404(Size, pk=size_id)
    size.delete()
    messages.success(request, 'Size deleted!')
    return redirect(reverse('product_detail', args=[product.id]))


def add_review(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            a = form.save(commit=False)
            a.product = product
            a.date_created = default=datetime.now()
            a.save()
            messages.success(request, 'Successfully added review!')
            return redirect(reverse('product_detail', args=[product.id]))
        else:
            messages.error(request,
                           ('Failed to update review. '
                            'Please ensure the form is valid.'))
    else:
        form = ReviewForm(instance=product)
        messages.info(request, f'You are adding a review to {product.name}')

    template = 'products/add_review.html'
    context = {
        'form': form,
        'product': product,
    }

    return render(request, template, context)
