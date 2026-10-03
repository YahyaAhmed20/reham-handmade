from django.urls import path

from . import views

app_name = "home"


urlpatterns = [

    path(
        "",
        views.home,
        name="home"
    ),

    path(
        "category/<int:category_id>/",
        views.category_detail,
        name="category_detail"
    ),

    path(
        "product/<int:product_id>/",
        views.product_detail_api,
        name="product_detail_api"
    ),

    # =========================
    # CART
    # =========================

    path(
        "cart/add/",
        views.add_to_cart,
        name="add_to_cart"
    ),

    path(
        "cart/added/",
        views.cart_added,
        name="cart_added"
    ),

    path(
        "cart/",
        views.cart,
        name="cart"
    ),

    path(
        "cart/update/",
        views.update_cart,
        name="update_cart"
    ),

    path(
        "cart/remove/",
        views.remove_from_cart,
        name="remove_from_cart"
    ),
    path(
    "checkout/",
    views.checkout,
    name="checkout"
),
    path(
    "order/success/<int:order_id>/",
    views.order_success,
    name="order_success"
),
]