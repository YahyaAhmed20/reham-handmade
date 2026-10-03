import requests

from django.conf import settings


def send_telegram_message(message):
    bot_token = getattr(
        settings,
        "TELEGRAM_BOT_TOKEN",
        ""
    )

    chat_id = getattr(
        settings,
        "TELEGRAM_CHAT_ID",
        ""
    )

    if not bot_token or not chat_id:
        return False

    url = (
        f"https://api.telegram.org/bot"
        f"{bot_token}/sendMessage"
    )

    payload = {
        "chat_id": chat_id,
        "text": message,
        "parse_mode": "HTML",
    }

    try:
        response = requests.post(
            url,
            data=payload,
            timeout=10,
        )

        return response.ok

    except requests.RequestException:
        return False
    
def send_new_order_notification(order):
    lines = [
        "🛍️ <b>طلب جديد</b>",
        "",
        f"🧾 <b>رقم الطلب:</b> #{order.id}",
        f"👤 <b>العميل:</b> {order.customer_name}",
        f"📱 <b>الهاتف:</b> {order.phone}",
        "",
        "📦 <b>المنتجات:</b>",
    ]

    for item in order.items.all():
        lines.append(
            f"• {item.product_name} × {item.quantity}"
            f" — {item.total} ج.م"
        )

        if item.customization_note:
            lines.append(
                f"  ✏️ التخصيص: {item.customization_note}"
            )

    lines.extend([
        "",
        f"💰 <b>إجمالي الطلب:</b> {order.subtotal} ج.م",
        f"💳 <b>العربون:</b> {order.deposit_amount} ج.م",
        f"💵 <b>المتبقي:</b> {order.remaining_amount} ج.م",
        "",
        f"🔢 <b>رقم عملية التحويل:</b> "
        f"{order.payment_reference}",
        "",
        f"📍 <b>العنوان:</b>",
        order.address,
    ])

    if order.notes:
        lines.extend([
            "",
            f"📝 <b>ملاحظات:</b>",
            order.notes,
        ])

    lines.extend([
        "",
        "⏳ <b>الحالة:</b> بانتظار تأكيد العربون",
    ])

    return send_telegram_message(
        "\n".join(lines)
    )