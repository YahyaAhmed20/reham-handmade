from django.contrib import admin
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from django.urls import reverse

from .models import (
    Category,
    Product,
    ProductImage,
    Order,
    OrderItem,
    StoreSettings,
)


# =========================================================
# ADMIN SITE CUSTOMIZATION
# =========================================================

admin.site.site_header = "لوحة تحكم الذكان"
admin.site.site_title = "الذكان - إدارة"
admin.site.index_title = "مرحباً بك في لوحة تحكم الذكان"


# =========================================================
# CATEGORY
# =========================================================

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):

    list_display = (
        "image_preview",
        "name",
        "products_count_display",
        "is_active_badge",
        "order",
        "created_at",
    )

    list_display_links = (
        "image_preview",
        "name",
    )

    list_filter = (
        "is_active",
        "created_at",
    )

    search_fields = (
        "name",
        "description",
    )

    list_editable = (
        "order",
    )

    ordering = (
        "order",
        "-created_at",
    )

    list_per_page = 20

    fieldsets = (
        (
            "البيانات الأساسية",
            {
                "fields": (
                    "name",
                    "description",
                )
            },
        ),
        (
            "الصورة والإعدادات",
            {
                "fields": (
                    "image",
                    "image_preview_large",
                    "is_active",
                    "order",
                )
            },
        ),
        (
            "التواريخ",
            {
                "fields": ("created_at",),
                "classes": ("collapse",),
            },
        ),
    )

    readonly_fields = (
        "created_at",
        "image_preview_large",
    )

    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="width:45px;height:45px;'
                'object-fit:cover;border-radius:8px;" />',
                obj.image.url,
            )
        return format_html(
            '<span style="color:#999;font-size:20px;">📁</span>'
        )

    image_preview.short_description = "الصورة"

    def image_preview_large(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="max-width:200px;border-radius:12px;" />',
                obj.image.url,
            )
        return "—"

    image_preview_large.short_description = "معاينة"

    def is_active_badge(self, obj):
        if obj.is_active:
            return format_html(
                '<span style="background:#4CAF50;color:white;'
                'padding:4px 12px;border-radius:12px;font-size:12px;">'
                '✓ نشط</span>'
            )
        return format_html(
            '<span style="background:#999;color:white;'
            'padding:4px 12px;border-radius:12px;font-size:12px;">'
            '✗ معطّل</span>'
        )

    is_active_badge.short_description = "الحالة"
    is_active_badge.admin_order_field = "is_active"

    def products_count_display(self, obj):
        count = obj.products.count()
        return format_html(
            '<span style="background:#f8f1e7;color:#6f4930;'
            'padding:4px 12px;border-radius:12px;font-size:12px;'
            'font-weight:bold;">{} منتج</span>',
            count,
        )

    products_count_display.short_description = "المنتجات"


# =========================================================
# PRODUCT IMAGE INLINE
# =========================================================

class ProductImageInline(admin.TabularInline):

    model = ProductImage
    extra = 1
    max_num = 8
    min_num = 0

    fields = (
        "image",
        "image_preview_small",
        "order",
    )

    readonly_fields = ("image_preview_small",)

    def image_preview_small(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="width:60px;height:60px;'
                'object-fit:cover;border-radius:8px;" />',
                obj.image.url,
            )
        return "—"

    image_preview_small.short_description = "معاينة"


# =========================================================
# PRODUCT
# =========================================================

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):

    list_display = (
        "image_preview",
        "name",
        "category_link",
        "price_display",
        "badges",
        "is_active_badge",
        "order",
    )

    list_display_links = (
        "image_preview",
        "name",
    )

    list_filter = (
        "category",
        "is_active",
        "is_featured",
        "is_new",
        "allow_customization",
        "created_at",
    )

    search_fields = (
        "name",
        "description",
    )

    list_editable = (
        "order",
    )

    ordering = (
        "order",
        "-created_at",
    )

    list_per_page = 25

    inlines = [ProductImageInline]

    save_on_top = True

    fieldsets = (
        (
            "البيانات الأساسية",
            {
                "fields": (
                    "name",
                    "category",
                    "description",
                )
            },
        ),
        (
            "السعر",
            {
                "fields": (
                    "price",
                    "old_price",
                )
            },
        ),
        (
            "الصورة الرئيسية",
            {
                "fields": (
                    "image",
                    "image_preview_large",
                )
            },
        ),
        (
            "الحالة والمميزات",
            {
                "fields": (
                    "is_active",
                    "is_featured",
                    "is_new",
                    "allow_customization",
                    "order",
                )
            },
        ),
        (
            "التواريخ",
            {
                "fields": ("created_at",),
                "classes": ("collapse",),
            },
        ),
    )

    readonly_fields = (
        "created_at",
        "image_preview_large",
    )

    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="width:50px;height:50px;'
                'object-fit:cover;border-radius:8px;" />',
                obj.image.url,
            )
        return format_html(
            '<span style="color:#999;font-size:20px;">📁</span>'
        )

    image_preview.short_description = "الصورة"

    def image_preview_large(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="max-width:250px;border-radius:12px;" />',
                obj.image.url,
            )
        return "—"

    image_preview_large.short_description = "معاينة"

    def category_link(self, obj):
        if obj.category:
            url = reverse("admin:home_category_change", args=[obj.category.id])
            return format_html(
                '<a href="{}" style="color:#6f4930;font-weight:bold;">'
                '{}</a>',
                url,
                obj.category.name,
            )
        return "—"

    category_link.short_description = "التصنيف"
    category_link.admin_order_field = "category"

    def price_display(self, obj):
        if obj.old_price:
            return format_html(
                '<div>'
                '<span style="color:#b8894d;font-weight:bold;">{} ج.م</span><br>'
                '<span style="color:#999;text-decoration:line-through;'
                'font-size:11px;">{} ج.م</span>'
                '</div>',
                obj.price,
                obj.old_price,
            )
        return format_html(
            '<span style="color:#b8894d;font-weight:bold;">{} ج.م</span>',
            obj.price,
        )

    price_display.short_description = "السعر"
    price_display.admin_order_field = "price"

    def badges(self, obj):
        badges = []
        if obj.is_new:
            badges.append(
                '<span style="background:#b8894d;color:white;'
                'padding:2px 8px;border-radius:10px;font-size:10px;'
                'margin-left:3px;">جديد</span>'
            )
        if obj.is_featured:
            badges.append(
                '<span style="background:#6f4930;color:white;'
                'padding:2px 8px;border-radius:10px;font-size:10px;'
                'margin-left:3px;">مميز</span>'
            )
        if obj.allow_customization:
            badges.append(
                '<span style="background:#4CAF50;color:white;'
                'padding:2px 8px;border-radius:10px;font-size:10px;'
                'margin-left:3px;">تخصيص</span>'
            )
        return mark_safe("".join(badges)) if badges else "—"

    badges.short_description = "الشارات"

    def is_active_badge(self, obj):
        if obj.is_active:
            return format_html(
                '<span style="background:#4CAF50;color:white;'
                'padding:4px 12px;border-radius:12px;font-size:12px;">'
                '✓</span>'
            )
        return format_html(
            '<span style="background:#999;color:white;'
            'padding:4px 12px;border-radius:12px;font-size:12px;">'
            '✗</span>'
        )

    is_active_badge.short_description = "نشط"
    is_active_badge.admin_order_field = "is_active"

    actions = ["make_featured", "make_new", "activate", "deactivate"]

    def make_featured(self, request, queryset):
        updated = queryset.update(is_featured=True)
        self.message_user(request, f"تم تمييز {updated} منتج بنجاح.")

    make_featured.short_description = "⭐ تمييز المنتجات المختارة"

    def make_new(self, request, queryset):
        updated = queryset.update(is_new=True)
        self.message_user(request, f"تم تحديد {updated} منتج كجديد.")

    make_new.short_description = "🆕 تحديد كـ جديد"

    def activate(self, request, queryset):
        updated = queryset.update(is_active=True)
        self.message_user(request, f"تم تفعيل {updated} منتج.")

    activate.short_description = "✅ تفعيل"

    def deactivate(self, request, queryset):
        updated = queryset.update(is_active=False)
        self.message_user(request, f"تم تعطيل {updated} منتج.")

    deactivate.short_description = "🚫 تعطيل"


# =========================================================
# ORDER ITEM INLINE
# =========================================================

class OrderItemInline(admin.TabularInline):

    model = OrderItem
    extra = 0

    fields = (
        "product_link",
        "product_name",
        "price_display",
        "quantity",
        "customization_note",
        "total_display",
    )

    readonly_fields = (
        "product_link",
        "product_name",
        "price_display",
        "quantity",
        "customization_note",
        "total_display",
    )

    can_delete = False

    def product_link(self, obj):
        if obj.product:
            url = reverse("admin:home_product_change", args=[obj.product.id])
            return format_html(
                '<a href="{}" style="color:#6f4930;font-weight:bold;">'
                '{}</a>',
                url,
                obj.product.name,
            )
        return obj.product_name

    product_link.short_description = "المنتج"

    def price_display(self, obj):
        return format_html(
            '<span style="color:#b8894d;font-weight:bold;">{} ج.م</span>',
            obj.price,
        )

    price_display.short_description = "السعر"

    def total_display(self, obj):
        return format_html(
            '<span style="color:#4CAF50;font-weight:bold;">{} ج.م</span>',
            obj.total,
        )

    total_display.short_description = "الإجمالي"


# =========================================================
# ORDER
# =========================================================

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):

    list_display = (
        "order_id_badge",
        "customer_info",
        "total_display",
        "deposit_display",
        "remaining_display",
        "status_badge",
        "payment_proof_preview",
        "created_at",
    )

    list_display_links = (
        "order_id_badge",
        "customer_info",
    )

    list_filter = (
        "status",
        "created_at",
    )

    search_fields = (
        "customer_name",
        "phone",
        "payment_reference",
    )

    ordering = ("-created_at",)

    list_per_page = 20

    readonly_fields = (
        "subtotal",
        "deposit_percentage",
        "deposit_amount",
        "remaining_amount",
        "created_at",
        "updated_at",
        "payment_proof_preview_large",
    )

    fieldsets = (
        (
            "🧾 بيانات العميل",
            {
                "fields": (
                    "customer_name",
                    "phone",
                    "address",
                    "notes",
                )
            },
        ),
        (
            "💰 بيانات الطلب",
            {
                "fields": (
                    "subtotal",
                    "deposit_percentage",
                    "deposit_amount",
                    "remaining_amount",
                    "status",
                )
            },
        ),
        (
            "💳 بيانات التحويل",
            {
                "fields": (
                    "payment_reference",
                    "payment_proof",
                    "payment_proof_preview_large",
                )
            },
        ),
        (
            "📅 التواريخ",
            {
                "fields": (
                    "created_at",
                    "updated_at",
                ),
                "classes": ("collapse",),
            },
        ),
    )

    inlines = [OrderItemInline]

    save_on_top = True

    def order_id_badge(self, obj):
        return format_html(
            '<span style="background:#6f4930;color:white;'
            'padding:6px 14px;border-radius:20px;font-size:12px;'
            'font-weight:bold;">#{}</span>',
            obj.id,
        )

    order_id_badge.short_description = "رقم الطلب"
    order_id_badge.admin_order_field = "id"

    def customer_info(self, obj):
        return format_html(
            '<div>'
            '<strong style="color:#2e7d32;font-size:14px;font-weight:bold;">'
            '👤 {}</strong><br>'
            '<span style="color:#806f61;font-size:12px;">📱 {}</span>'
            '</div>',
            obj.customer_name,
            obj.phone,
        )

    customer_info.short_description = "العميل"

    def total_display(self, obj):
        return format_html(
            '<span style="color:#b8894d;font-weight:bold;font-size:14px;">'
            '{} ج.م</span>',
            obj.subtotal,
        )

    total_display.short_description = "الإجمالي"
    total_display.admin_order_field = "subtotal"

    def deposit_display(self, obj):
        return format_html(
            '<span style="color:#4CAF50;font-weight:bold;">{} ج.م</span>',
            obj.deposit_amount,
        )

    deposit_display.short_description = "العربون"

    def remaining_display(self, obj):
        return format_html(
            '<span style="color:#FF9800;font-weight:bold;">{} ج.م</span>',
            obj.remaining_amount,
        )

    remaining_display.short_description = "المتبقي"

    def status_badge(self, obj):
        colors = {
            "pending":            ("#FF9800", "⏳ طلب جديد"),
            "deposit_pending":    ("#FFC107", "💳 بانتظار تأكيد العربون"),
            "deposit_confirmed":  ("#8BC34A", "✓ تم تأكيد العربون"),
            "processing":         ("#2196F3", "📦 قيد التنفيذ"),
            "ready":              ("#9C27B0", "🎁 جاهز"),
            "delivered":          ("#4CAF50", "✅ تم التسليم"),
            "cancelled":          ("#F44336", "✗ ملغي"),
        }
        color, text = colors.get(
            obj.status,
            ("#999", obj.get_status_display()),
        )

        return format_html(
            '<span style="background:{};color:white;'
            'padding:6px 12px;border-radius:20px;font-size:12px;'
            'font-weight:bold;white-space:nowrap;">{}</span>',
            color,
            text,
        )

    status_badge.short_description = "الحالة"
    status_badge.admin_order_field = "status"

    def payment_proof_preview(self, obj):
        if obj.payment_proof:
            return format_html(
                '<a href="{}" target="_blank" '
                'style="text-decoration:none;">'
                '<img src="{}" style="width:50px;height:50px;'
                'object-fit:cover;border-radius:8px;'
                'border:2px solid #b8894d;" />'
                '</a>',
                obj.payment_proof.url,
                obj.payment_proof.url,
            )
        return format_html(
            '<span style="color:#999;">—</span>'
        )

    payment_proof_preview.short_description = "الإثبات"

    def payment_proof_preview_large(self, obj):
        if obj.payment_proof:
            return format_html(
                '<a href="{}" target="_blank">'
                '<img src="{}" style="max-width:400px;border-radius:12px;'
                'box-shadow:0 4px 12px rgba(0,0,0,0.15);" />'
                '</a>'
                '<br><small style="color:#666;">'
                'اضغط على الصورة لعرضها بحجم كامل</small>',
                obj.payment_proof.url,
                obj.payment_proof.url,
            )
        return "—"

    payment_proof_preview_large.short_description = "معاينة الإثبات"

    # =========================
    # ACTIONS
    # =========================

    actions = [
        "mark_pending",
        "mark_deposit_pending",
        "mark_deposit_confirmed",
        "mark_processing",
        "mark_ready",
        "mark_delivered",
        "mark_cancelled",
    ]

    def mark_pending(self, request, queryset):
        updated = queryset.update(status="pending")
        self.message_user(request, f"تم تحويل {updated} طلب لـ طلب جديد.")

    mark_pending.short_description = "⏳ طلب جديد"

    def mark_deposit_pending(self, request, queryset):
        updated = queryset.update(status="deposit_pending")
        self.message_user(request, f"تم تحويل {updated} طلب لـ بانتظار تأكيد العربون.")

    mark_deposit_pending.short_description = "💳 بانتظار تأكيد العربون"

    def mark_deposit_confirmed(self, request, queryset):
        updated = queryset.update(status="deposit_confirmed")
        self.message_user(request, f"تم تأكيد العربون لـ {updated} طلب.")

    mark_deposit_confirmed.short_description = "✓ تم تأكيد العربون"

    def mark_processing(self, request, queryset):
        updated = queryset.update(status="processing")
        self.message_user(request, f"تم تحويل {updated} طلب لـ قيد التنفيذ.")

    mark_processing.short_description = "📦 قيد التنفيذ"

    def mark_ready(self, request, queryset):
        updated = queryset.update(status="ready")
        self.message_user(request, f"تم تحويل {updated} طلب لـ جاهز.")

    mark_ready.short_description = "🎁 جاهز"

    def mark_delivered(self, request, queryset):
        updated = queryset.update(status="delivered")
        self.message_user(request, f"تم تسليم {updated} طلب.")

    mark_delivered.short_description = "✅ تم التسليم"

    def mark_cancelled(self, request, queryset):
        updated = queryset.update(status="cancelled")
        self.message_user(request, f"تم إلغاء {updated} طلب.")

    mark_cancelled.short_description = "✗ ملغي"

    # =========================
    # PERMISSIONS
    # =========================

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser


# =========================================================
# STORE SETTINGS
# =========================================================

@admin.register(StoreSettings)
class StoreSettingsAdmin(admin.ModelAdmin):

    list_display = (
        "wallet_number_display",
        "deposit_percentage_display",
        "is_active_badge",
        "updated_at",
    )

    fieldsets = (
        (
            "💳 بيانات الدفع",
            {
                "fields": (
                    "wallet_number",
                    "deposit_percentage",
                )
            },
        ),
        (
            "⚙️ الإعدادات",
            {
                "fields": ("is_active",)
            },
        ),
        (
            "📅 التاريخ",
            {
                "fields": ("updated_at",),
                "classes": ("collapse",),
            },
        ),
    )

    readonly_fields = ("updated_at",)

    def wallet_number_display(self, obj):
        return format_html(
            '<span style="font-family:monospace;font-size:15px;'
            'font-weight:bold;color:#6f4930;">{}</span>',
            obj.wallet_number,
        )

    wallet_number_display.short_description = "رقم المحفظة"

    def deposit_percentage_display(self, obj):
        return format_html(
            '<span style="background:#b8894d;color:white;'
            'padding:4px 12px;border-radius:12px;font-size:12px;'
            'font-weight:bold;">{}%</span>',
            obj.deposit_percentage,
        )

    deposit_percentage_display.short_description = "نسبة العربون"

    def is_active_badge(self, obj):
        if obj.is_active:
            return format_html(
                '<span style="background:#4CAF50;color:white;'
                'padding:4px 12px;border-radius:12px;font-size:12px;">'
                '✓ نشط</span>'
            )
        return format_html(
            '<span style="background:#999;color:white;'
            'padding:4px 12px;border-radius:12px;font-size:12px;">'
            '✗ معطّل</span>'
        )

    is_active_badge.short_description = "الحالة"

    def has_add_permission(self, request):
        return not StoreSettings.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False