from django.shortcuts import get_object_or_404, render
from listing.models import Listing
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from listing.choices import bedroom_choices, state_choices, price_choices

def index(request):
    listings = Listing.objects.order_by('-list_date').filter(is_published=True)
    paginator = Paginator(listings, 3)
    page = request.GET.get('page')
    page_lisitng = paginator.get_page(page)
    context = {
        'listings': page_lisitng
    }
    return render(request, 'listing/listings.html', context)


def listing(request, listing_id):
    listing = get_object_or_404(Listing, pk=listing_id)
    context = {
        'listing': listing
    }
    return render(request, 'listing/listing.html',context)


def search(request):
    queryset_list = Listing.objects.order_by('-list_date')

    # searching by description
    if 'keywords' in request.GET:
        keywords = request.GET['keywords']
        if keywords:
            queryset_list = queryset_list.filter(description__icontains=keywords)
    # searching by city
    if 'city' in request.GET:
        city = request.GET['city']
        if city:
            queryset_list = queryset_list.filter(city__iexact=city)
    # searching by state
    if 'state' in request.GET:
        state = request.GET['state']
        if state:
            queryset_list = queryset_list.filter(state__iexact=state)

    # searching by bedroom
    if 'bedrooms' in request.GET:
        bedrooms = request.GET['bedrooms']
        if bedrooms:
            queryset_list = queryset_list.filter(bedrooms__lte=bedrooms)

    # searching by price
    if 'price' in request.GET:
        price = request.GET['price']
        if price:
            queryset_list = queryset_list.filter(price__lte=price)

    context = {
        'bedroom_choices': bedroom_choices,
        'state_choices': state_choices,
        'price_choices': price_choices,
        'listings': queryset_list,
        'values': request.GET,
    }
    return render(request, 'listing/search.html', context)
