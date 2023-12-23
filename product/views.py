import json
from django.db import IntegrityError
from django.http import JsonResponse
import config
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib import messages
from product.models import Item, Order, OrderItem, Discount, Tax
import stripe

# Create your views here.


def items(request):
    items = Item.objects.all()
    order = Order.objects.first()
    return render(request, "product/items.html", {"items": items, "order": order})


def item(request, item_id):
    item = get_object_or_404(Item, pk=item_id)
    order = Order.objects.first()
    return render(request, "product/item.html", {"item": item, "order": order})


def cart(request):
    order = Order.objects.first()
    return render(request, "product/checkout.html", {"order": order})


def cart_count(request):
    order = Order.objects.first()
    return render(request, "product/update_cart_count.html", {"order": order})


def order_item(request, item_id, quantity=1):
    if request.method == "POST":
        discount = Discount.objects.first()
        tax = Tax.objects.first()
        item = get_object_or_404(Item, pk=item_id)
        order, created = Order.objects.get_or_create(discount=discount, tax=tax)
        try:
            order_item, created = OrderItem.objects.get_or_create(
                order=order, item=item, quantity=quantity
            )
        except IntegrityError:
            return render(
                request, "product/update_cart_count.html", {"order": order, "item": item}
            )
        else:
            return render(
                request, "product/update_cart_count.html", {"order": order, "item": item}
            )
    return render(request, "product/checkout.html", {"order": order})


def order_item_add(request, item_id):
    if request.method == "POST":
        item = get_object_or_404(Item, pk=item_id)
        empty = False
        order_item = OrderItem.objects.get(item=item)
        order_item.quantity += 1
        order_item.save()
        order = Order.objects.first()
        return render(
            request,
            "product/update_count.html",
            {"order_item": order_item, "order": order, "empty": empty},
        )


def order_item_remove(request, item_id):
    if request.method == "POST":
        item = get_object_or_404(Item, pk=item_id)
        order_item = OrderItem.objects.get(item=item)
        empty = False
        if order_item.quantity == 1:
            order_item.delete()
            empty = True
        else:
            order_item.quantity -= 1
            order_item.save()
        order = Order.objects.first()
        return render(
            request,
            "product/update_count.html",
            {"order_item": order_item, "order": order, "empty": empty},
        )


def buy(request, item_id):
    item = get_object_or_404(Item, pk=item_id)
    if item.currency == "usd":
        stripe.api_key = config.STRIPE_SECRET_KEY_USD
    else:
        stripe.api_key = config.STRIPE_SECRET_KEY_POUND

    discount = []
    tax = []

    if item.discount:
        discount_coupon = stripe.Coupon.create(
            percent_off=item.discount * 100,
        )
        discount.append({"coupon": discount_coupon.id})

    if item.tax:
        sales_tax = stripe.TaxRate.create(
            display_name="Sales Tax",
            inclusive=False,
            percentage=item.tax.tax * 100,
        )
        tax.append(sales_tax.id)

    try:
        checkout_session = stripe.checkout.Session.create(
            line_items=[
                {
                    "price_data": {
                        "currency": item.currency,
                        "unit_amount": item.get_price_cent(),
                        "product_data": {
                            "name": item.name,
                            "description": item.description,
                            "images": [item.url],
                        },
                    },
                    "quantity": 1,
                    "tax_rates": tax,
                },
            ],
            mode="payment",
            discounts=discount,
            success_url=request.build_absolute_uri("/success"),
            cancel_url=request.build_absolute_uri("/cancel"),
        )
    except Exception as e:
        return str(e)
    return redirect(checkout_session.url, code=303)


def checkout(request, order_id):
    order = get_object_or_404(Order, pk=order_id)
    currency = "usd"  # Can be modify to suit application need

    if currency == "usd":
        stripe.api_key = config.STRIPE_SECRET_KEY_USD
    else:
        stripe.api_key = config.STRIPE_SECRET_KEY_POUND

    discount = []
    tax = []

    if order.discount.discount:
        discount_coupon = stripe.Coupon.create(
            percent_off=order.discount.discount * 100,
        )
        discount.append({"coupon": discount_coupon.id})

    if order.tax:
        sales_tax = stripe.TaxRate.create(
            display_name="Sales Tax",
            inclusive=False,
            percentage=order.tax.tax * 100,
        )
        tax.append(sales_tax.id)

    # stripe.PromotionCode.create(
    #     coupon=discount_coupon.id,
    #     code="TESTCODE1",
    # )

    products = order.items.all()

    line_items = []
    for product in products:
        line_items.append(
            {
                "price_data": {
                    "currency": currency,
                    "product_data": {
                        "name": product.item.name,
                        "description": product.item.description,
                        "images": [product.item.url],
                    },
                    "unit_amount": product.item.get_price_cent(),
                },
                "quantity": product.quantity,
                "tax_rates": tax,
            }
        )

    try:
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            line_items=line_items,
            discounts=discount,
            # allow_promotion_codes=True,
            mode="payment",
            success_url=request.build_absolute_uri("/success"),
            cancel_url=request.build_absolute_uri("/cancel"),
        )
    except Exception as e:
        return str(e)

    return redirect(checkout_session.url, code=303)


def payment_intent(request, order_id):
    order = get_object_or_404(Order, pk=order_id)
    public_key = config.STRIPE_PUBLIC_KEY_USD
    if request.method == "POST":
        currency = "usd"  # Can be modify to suit application need

        if currency == "usd":
            stripe.api_key = config.STRIPE_SECRET_KEY_USD
        else:
            stripe.api_key = config.STRIPE_SECRET_KEY_POUND

        discount = int((1 - order.discount.discount) * order.get_total_price() * 100)
        tax = int(order.tax.tax * order.get_total_price() * 100)

        total = discount + tax

        req_json = json.loads(request.body)
        customer = stripe.Customer.create(email=req_json["email"])

        try:
            intent = stripe.PaymentIntent.create(
                amount=total,
                currency=currency,
                customer=customer["id"],
                payment_method_types=["card"],
                metadata={"order_id": order.id},
            )
        except Exception as e:
            return JsonResponse({"error": str(e)})

        return JsonResponse(
            {
                "clientSecret": intent["client_secret"],
            }
        )
    return render(
        request, "product/payment.html", {"order": order, "public_key": public_key}
    )


def success(request):
    return render(request, "product/success.html")


def cancel(request):
    return render(request, "product/cancel.html")
