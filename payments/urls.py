from django.urls import path
from payments.views import (
    view_cards,
    add_card,
    delete_card,
    handle_payment,
    handle_payment_process,
    payment_done,
    payment_failed,
    x,
    y,
    change_cart
)


app_name = 'payments'


urlpatterns = [
    path('cards/', view=view_cards, name='view_cards'),
    path('cards/add/', view=add_card, name='add_card'),
    path('cards/delete/<str:card_id>/', view=delete_card, name='delete_card'),
    path('pay/', view=handle_payment, name='pay'),
    path('process/', view=handle_payment_process, name='process'),
    path('done/', view=payment_done, name='done'),
    path('failed/', view=payment_failed, name='failed'),
    path('x/', view=x, name='x'),
    path('y/', view=y, name='y'),
    path('change/', view=change_cart, name='change_cart'),
]
