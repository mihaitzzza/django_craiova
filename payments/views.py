import stripe
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.contrib.sites.models import Site
from django.shortcuts import render, Http404, reverse, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from payments.models import StripeCard
from django.contrib import messages


@login_required
def view_cards(request):
    cards_detail = stripe.Customer.list_sources(
        request.user.stripe_data.customer_id,
        api_key=settings.STRIPE_SECRET_KEY,
    )

    return render(request, 'payments/view_cards.html', {
        'cards': cards_detail['data']
    })


@login_required
def add_card(request):
    if request.method == 'GET':
        return render(request, 'payments/add_card.html', {
            'stripe_key': settings.STRIPE_PUBLIC_KEY
        })
    else:
        if 'stripeToken' in request.POST:
            stripe_customer = request.user.stripe_data
            stripe_token = request.POST['stripeToken']

            card = stripe.Customer.create_source(
                stripe_customer.customer_id,
                source=stripe_token,
                api_key=settings.STRIPE_SECRET_KEY
            )

            StripeCard(customer=stripe_customer, card_id=card['id']).save()

            return HttpResponseRedirect(reverse('payments:view_cards'))

        raise Http404


@login_required
def delete_card(request, card_id):
    if request.method == 'POST':
        stripe_customer = request.user.stripe_data

        card = get_object_or_404(StripeCard, customer=stripe_customer, card_id=card_id)

        stripe.Customer.delete_source(
            stripe_customer.customer_id,
            card_id,
            api_key=settings.STRIPE_SECRET_KEY,
        )

        card.delete()

        return HttpResponseRedirect(reverse('payments:view_cards'))

    raise Http404


@login_required
def handle_payment(request):
    payment_process_url = f"{Site.objects.get_current().domain}{reverse('payments:process')}"
    stripe_customer = request.user.stripe_data

    payment_intent = stripe.PaymentIntent.create(
        amount=200,
        currency='ron',
        customer=stripe_customer.customer_id,
        payment_method=stripe_customer.cards.last().card_id,
        confirm=True,
        return_url=payment_process_url,
        api_key=settings.STRIPE_SECRET_KEY
    )

    print('payment_intent', payment_intent)

    if payment_intent['next_action']:
        return HttpResponseRedirect(payment_intent['next_action']['redirect_to_url']['url'])

    return HttpResponseRedirect(reverse('payments:process'))


@login_required
def handle_payment_process(request):
    payment_intent_id = request.GET.get('payment_intent', None)

    if payment_intent_id:
        payment_intent = stripe.PaymentIntent.retrieve(
            payment_intent_id,
            api_key=settings.STRIPE_SECRET_KEY
        )

        if payment_intent['last_payment_error']:
            stripe.PaymentIntent.cancel(
                payment_intent_id,
                api_key=settings.STRIPE_SECRET_KEY
            )

            return HttpResponseRedirect(reverse('payments:failed'))

    return HttpResponseRedirect(reverse('payments:done'))


@login_required
def payment_done(request):
    return HttpResponse('Payment done! Congrats.')


@login_required
def payment_failed(request):
    return HttpResponse('Payment failed! Try again :)')


def xz(request):
    print(f'{request.user.first_name} {request.user.last_name}')
    request.session['fullname'] = f'{request.user.first_name} {request.user.last_name}'
    return render(request, 'payments/template1.html', {
        'has_bathroom': False
    })


def y(request):
    return render(request, 'payments/template2.html')


def change_cart(request):
    request.session['cart_items'] = int(request.session['cart_items']) + 1
    messages.add_message(request, messages.ERROR, 'Incremented cart items.')
    return HttpResponseRedirect(reverse('payments:y'))
