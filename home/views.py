import json
from decimal import Decimal
from django.shortcuts import redirect, render
from django.http import JsonResponse
from .models import (
    Category,
    Product,
    Order,
    OrderItem,
    StoreSettings,
)
from .telegram_service import send_new_order_notification


def home(request):
    categories = Category.objects.filter(
        is_active=True
    )

    featured_products = Product.objects.filter(
        is_active=True,
        is_featured=True
    ).select_related(
        "category"
    )[:6]

    context = {
        "categories": categories,
        "featured_products": featured_products,
    }

    return render(
        request,
        "home/home.html",
        context
    )


from django.shortcuts import get_object_or_404


def category_detail(request, category_id):

    category = get_object_or_404(
        Category,
        id=category_id,
        is_active=True
    )

    products = category.products.filter(
        is_active=True
    )

    context = {
        "category": category,
        "products": products,
    }

    return render(
        request,
        "home/category_detail.html",
        context
    )


def product_detail_api(request, product_id):
    product = get_object_or_404(
        Product,
        id=product_id,
        is_active=True
    )

    images = [
        image.image.url
        for image in product.images.all()
    ]

    # الصورة الرئيسية أول صورة
    if product.image:
        images.insert(0, product.image.url)

    return JsonResponse({
        "id": product.id,
        "name": product.name,
        "description": product.description,
        "price": str(product.price),
        "images": images,
        "allow_customization": product.allow_customization,
    })


def add_to_cart(request):
    if request.method != "POST":
        return JsonResponse({
            "success": False,
            "message": "طريقة الطلب غير صحيحة."
        }, status=405)

    try:
        data = json.loads(request.body)

        product_id = int(data.get("product_id"))
        quantity = int(data.get("quantity", 1))
        note = data.get("note", "").strip()

    except (ValueError, TypeError, json.JSONDecodeError):
        return JsonResponse({
            "success": False,
            "message": "بيانات المنتج غير صحيحة."
        }, status=400)

    if quantity < 1:
        return JsonResponse({
            "success": False,
            "message": "الكمية يجب أن تكون أكبر من صفر."
        }, status=400)

    product = get_object_or_404(
        Product,
        id=product_id,
        is_active=True
    )

    cart = request.session.get("cart", {})

    product_key = str(product.id)

    if product_key in cart:
        cart[product_key]["quantity"] += quantity

        if note:
            cart[product_key]["note"] = note

    else:
        cart[product_key] = {
            "quantity": quantity,
            "note": note,
        }

    request.session["cart"] = cart
    request.session.modified = True

    return JsonResponse({
        "success": True,
        "message": "تم إضافة المنتج إلى السلة بنجاح.",
        "cart_count": sum(
            item["quantity"]
            for item in cart.values()
        )
    })


def cart_added(request):

    cart = request.session.get("cart", {})

    if not cart:
        return redirect("home")

    product_id = next(iter(cart))

    product = get_object_or_404(
        Product,
        id=int(product_id),
        is_active=True
    )

    item = cart[product_id]

    quantity = item["quantity"]

    total = product.price * quantity

    context = {
        "product": product,
        "quantity": quantity,
        "total": total,
    }

    return render(
        request,
        "home/cart_added.html",
        context
    )


def update_cart(request):

    if request.method != "POST":
        return JsonResponse({
            "success": False,
            "message": "طريقة الطلب غير صحيحة."
        }, status=405)

    try:
        data = json.loads(request.body)

        product_id = str(
            int(data.get("product_id"))
        )

        action = data.get("action")

    except (ValueError, TypeError, json.JSONDecodeError):

        return JsonResponse({
            "success": False,
            "message": "بيانات غير صحيحة."
        }, status=400)


    cart = request.session.get("cart", {})


    if product_id not in cart:

        return JsonResponse({
            "success": False,
            "message": "المنتج غير موجود في السلة."
        }, status=404)


    current_quantity = cart[product_id]["quantity"]


    if action == "increase":

        cart[product_id]["quantity"] += 1


    elif action == "decrease":

        if current_quantity > 1:

            cart[product_id]["quantity"] -= 1

        else:

            del cart[product_id]


    else:

        return JsonResponse({
            "success": False,
            "message": "عملية غير معروفة."
        }, status=400)


    request.session["cart"] = cart
    request.session.modified = True


    return JsonResponse({
        "success": True
    })


def remove_from_cart(request):

    if request.method != "POST":
        return JsonResponse({
            "success": False,
            "message": "طريقة الطلب غير صحيحة."
        }, status=405)


    try:

        data = json.loads(request.body)

        product_id = str(
            int(data.get("product_id"))
        )

    except (ValueError, TypeError, json.JSONDecodeError):

        return JsonResponse({
            "success": False,
            "message": "بيانات غير صحيحة."
        }, status=400)


    cart = request.session.get("cart", {})


    if product_id in cart:

        del cart[product_id]


    request.session["cart"] = cart
    request.session.modified = True


    return JsonResponse({
        "success": True
    })


def cart(request):

    cart_data = request.session.get("cart", {})

    items = []
    grand_total = Decimal("0")

    for product_id, item in cart_data.items():

        product = get_object_or_404(
            Product,
            id=int(product_id),
            is_active=True
        )

        quantity = item.get("quantity", 1)
        note = item.get("note", "")

        total = product.price * quantity

        grand_total += total

        items.append({
            "product": product,
            "quantity": quantity,
            "note": note,
            "total": total,
        })

    context = {
        "items": items,
        "grand_total": grand_total,
    }

    return render(
        request,
        "home/cart.html",
        context
    )


def checkout(request):
    cart_data = request.session.get("cart", {})

    if not cart_data:
        return redirect("home:home")

    settings = StoreSettings.objects.filter(
        is_active=True
    ).first()

    if settings:
        wallet_number = settings.wallet_number
        deposit_percentage = settings.deposit_percentage
    else:
        wallet_number = "01001404850"
        deposit_percentage = Decimal("50")

    items = []
    subtotal = Decimal("0")

    for product_id, item in cart_data.items():
        product = get_object_or_404(
            Product,
            id=int(product_id),
            is_active=True
        )

        quantity = int(item.get("quantity", 1))
        note = item.get("note", "")

        total = product.price * quantity
        subtotal += total

        items.append({
            "product": product,
            "quantity": quantity,
            "note": note,
            "total": total,
        })

    deposit_amount = (
        subtotal * deposit_percentage / Decimal("100")
    ).quantize(Decimal("0.01"))

    remaining_amount = subtotal - deposit_amount

    if request.method == "POST":

        customer_name = request.POST.get(
            "customer_name", ""
        ).strip()

        phone = request.POST.get(
            "phone", ""
        ).strip()

        address = request.POST.get(
            "address", ""
        ).strip()

        notes = request.POST.get(
            "notes", ""
        ).strip()

        payment_reference = request.POST.get(
            "payment_reference", ""
        ).strip()

        payment_proof = request.FILES.get(
            "payment_proof"
        )

        # التحقق من البيانات
        if not customer_name:
            return render(
                request,
                "home/checkout.html",
                {
                    "items": items,
                    "subtotal": subtotal,
                    "deposit_percentage": deposit_percentage,
                    "deposit_amount": deposit_amount,
                    "remaining_amount": remaining_amount,
                    "wallet_number": wallet_number,
                    "error": "من فضلك اكتب الاسم بالكامل.",
                }
            )

        if not phone:
            return render(
                request,
                "home/checkout.html",
                {
                    "items": items,
                    "subtotal": subtotal,
                    "deposit_percentage": deposit_percentage,
                    "deposit_amount": deposit_amount,
                    "remaining_amount": remaining_amount,
                    "wallet_number": wallet_number,
                    "error": "من فضلك اكتب رقم الهاتف.",
                }
            )

        if not address:
            return render(
                request,
                "home/checkout.html",
                {
                    "items": items,
                    "subtotal": subtotal,
                    "deposit_percentage": deposit_percentage,
                    "deposit_amount": deposit_amount,
                    "remaining_amount": remaining_amount,
                    "wallet_number": wallet_number,
                    "error": "من فضلك اكتب العنوان.",
                }
            )

        if not payment_reference:
            return render(
                request,
                "home/checkout.html",
                {
                    "items": items,
                    "subtotal": subtotal,
                    "deposit_percentage": deposit_percentage,
                    "deposit_amount": deposit_amount,
                    "remaining_amount": remaining_amount,
                    "wallet_number": wallet_number,
                    "error": "من فضلك اكتب رقم عملية التحويل.",
                }
            )

        if not payment_proof:
            return render(
                request,
                "home/checkout.html",
                {
                    "items": items,
                    "subtotal": subtotal,
                    "deposit_percentage": deposit_percentage,
                    "deposit_amount": deposit_amount,
                    "remaining_amount": remaining_amount,
                    "wallet_number": wallet_number,
                    "error": "من فضلك ارفع صورة إثبات التحويل.",
                }
            )

        # إنشاء الطلب
        order = Order.objects.create(
            customer_name=customer_name,
            phone=phone,
            address=address,
            notes=notes,
            subtotal=subtotal,
            deposit_percentage=deposit_percentage,
            deposit_amount=deposit_amount,
            remaining_amount=remaining_amount,
            payment_reference=payment_reference,
            payment_proof=payment_proof,
            status="deposit_pending",
        )

        # إنشاء المنتجات داخل الطلب
        for item in items:
            product = item["product"]

            OrderItem.objects.create(
                order=order,
                product=product,
                product_name=product.name,
                price=product.price,
                quantity=item["quantity"],
                customization_note=item["note"],
                total=item["total"],
            )

        # إرسال الطلب إلى Telegram
        send_new_order_notification(order)

        # تفريغ السلة
        request.session["cart"] = {}
        request.session.modified = True

        return redirect(
            "home:order_success",
            order_id=order.id
        )

    context = {
        "items": items,
        "subtotal": subtotal,
        "deposit_percentage": deposit_percentage,
        "deposit_amount": deposit_amount,
        "remaining_amount": remaining_amount,
        "wallet_number": wallet_number,
    }

    return render(
        request,
        "home/checkout.html",
        context
    )


def order_success(request, order_id):
    order = get_object_or_404(
        Order,
        id=order_id
    )

    return render(
        request,
        "home/order_success.html",
        {
            "order": order
        }
    )