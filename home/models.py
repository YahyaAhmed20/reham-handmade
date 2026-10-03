from django.db import models
from django.core.exceptions import ValidationError
from cloudinary.models import CloudinaryField


# =========================================================
# IMAGE VALIDATORS
# =========================================================

def validate_image_size(image):
    """
    التحقق من حجم الصورة
    بيتعامل مع UploadedFile بس (الصور الجديدة)
    """
    # لو الصورة محفوظة على Cloudinary → نتخطى التحقق
    if not hasattr(image, "size"):
        return

    if not image.size:
        return

    max_size = 5 * 1024 * 1024  # 5 MB

    if image.size > max_size:
        size_mb = image.size / 1024 / 1024
        raise ValidationError(
            f"❌ حجم الصورة كبير جداً ({size_mb:.1f} MB). "
            f"الحد الأقصى المسموح هو 5 MB. "
            f"اضغط الصورة من tinypng.com وحاول تاني."
        )


def validate_file_extension(image):
    """
    التحقق من امتداد الصورة
    بيتعامل مع UploadedFile بس (الصور الجديدة)
    """
    # لو الصورة محفوظة على Cloudinary → نتخطى التحقق
    if not hasattr(image, "name"):
        return

    if not image.name:
        return

    import os

    ext = os.path.splitext(image.name)[1].lower()
    valid_extensions = [".jpg", ".jpeg", ".png", ".webp"]

    if ext not in valid_extensions:
        raise ValidationError(
            f"❌ امتداد الصورة غير مدعوم ({ext}). "
            f"المسموح: JPG, JPEG, PNG, WEBP"
        )


# =========================================================
# CATEGORY
# =========================================================

class Category(models.Model):
    name = models.CharField(
        max_length=150,
        verbose_name="اسم التصنيف"
    )

    image = CloudinaryField(
        "صورة التصنيف",
        folder="dakkan/categories/",
        blank=True,
        null=True,
        validators=[validate_image_size, validate_file_extension],
    )

    description = models.TextField(
        blank=True,
        verbose_name="الوصف"
    )

    is_active = models.BooleanField(
        default=True,
        verbose_name="نشط"
    )

    order = models.PositiveIntegerField(
        default=0,
        verbose_name="ترتيب الظهور"
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        ordering = ["order", "-created_at"]
        verbose_name = "تصنيف"
        verbose_name_plural = "التصنيفات"

    def __str__(self):
        return self.name


# =========================================================
# PRODUCT
# =========================================================

class Product(models.Model):
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name="products",
        verbose_name="التصنيف"
    )

    name = models.CharField(
        max_length=200,
        verbose_name="اسم المنتج"
    )

    description = models.TextField(
        blank=True,
        verbose_name="الوصف"
    )

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="السعر"
    )

    old_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name="السعر القديم"
    )

    image = CloudinaryField(
        "الصورة الرئيسية",
        folder="dakkan/products/",
        blank=True,
        null=True,
        validators=[validate_image_size, validate_file_extension],
    )

    is_active = models.BooleanField(
        default=True,
        verbose_name="نشط"
    )

    is_featured = models.BooleanField(
        default=False,
        verbose_name="منتج مميز"
    )

    is_new = models.BooleanField(
        default=False,
        verbose_name="جديد"
    )

    allow_customization = models.BooleanField(
        default=False,
        verbose_name="يسمح بالتخصيص"
    )

    order = models.PositiveIntegerField(
        default=0,
        verbose_name="ترتيب الظهور"
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        ordering = ["order", "-created_at"]
        verbose_name = "منتج"
        verbose_name_plural = "المنتجات"

    def __str__(self):
        return self.name


# =========================================================
# PRODUCT IMAGE
# =========================================================

class ProductImage(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="images",
        verbose_name="المنتج"
    )

    image = CloudinaryField(
        "الصورة",
        folder="dakkan/products/gallery/",
        blank=True,
        null=True,
        validators=[validate_image_size, validate_file_extension],
    )

    order = models.PositiveIntegerField(
        default=0,
        verbose_name="ترتيب الصورة"
    )

    class Meta:
        ordering = ["order"]
        verbose_name = "صورة منتج"
        verbose_name_plural = "صور المنتجات"

    def __str__(self):
        return f"{self.product.name} - {self.order}"


# =========================================================
# ORDER
# =========================================================

class Order(models.Model):
    STATUS_CHOICES = [
        ("pending", "طلب جديد"),
        ("deposit_pending", "بانتظار تأكيد العربون"),
        ("deposit_confirmed", "تم تأكيد العربون"),
        ("processing", "قيد التنفيذ"),
        ("ready", "جاهز"),
        ("delivered", "تم التسليم"),
        ("cancelled", "ملغي"),
    ]

    customer_name = models.CharField(
        max_length=150,
        verbose_name="اسم العميل"
    )

    phone = models.CharField(
        max_length=30,
        verbose_name="رقم الهاتف"
    )

    address = models.TextField(
        verbose_name="العنوان"
    )

    notes = models.TextField(
        blank=True,
        verbose_name="ملاحظات الطلب"
    )

    subtotal = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="إجمالي الطلب"
    )

    deposit_percentage = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=50,
        verbose_name="نسبة العربون %"
    )

    deposit_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="قيمة العربون"
    )

    remaining_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="المبلغ المتبقي"
    )

    payment_reference = models.CharField(
        max_length=100,
        blank=True,
        verbose_name="رقم عملية التحويل"
    )

    payment_proof = CloudinaryField(
        "إثبات التحويل",
        folder="dakkan/orders/payment_proofs/",
        blank=True,
        null=True,
        validators=[validate_image_size, validate_file_extension],
    )

    status = models.CharField(
        max_length=30,
        choices=STATUS_CHOICES,
        default="pending",
        verbose_name="حالة الطلب"
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="تاريخ الطلب"
    )

    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="آخر تحديث"
    )

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "طلب"
        verbose_name_plural = "الطلبات"

    def __str__(self):
        return f"طلب #{self.id} - {self.customer_name}"


# =========================================================
# ORDER ITEM
# =========================================================

class OrderItem(models.Model):
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name="items",
        verbose_name="الطلب"
    )

    product = models.ForeignKey(
        Product,
        on_delete=models.PROTECT,
        related_name="order_items",
        verbose_name="المنتج"
    )

    product_name = models.CharField(
        max_length=200,
        verbose_name="اسم المنتج وقت الطلب"
    )

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="سعر المنتج"
    )

    quantity = models.PositiveIntegerField(
        default=1,
        verbose_name="الكمية"
    )

    customization_note = models.TextField(
        blank=True,
        verbose_name="ملاحظات التخصيص"
    )

    total = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="الإجمالي"
    )

    def __str__(self):
        return f"{self.product_name} × {self.quantity}"


# =========================================================
# STORE SETTINGS
# =========================================================

class StoreSettings(models.Model):
    wallet_number = models.CharField(
        max_length=30,
        default="01001404850",
        verbose_name="رقم المحفظة"
    )

    deposit_percentage = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=50,
        verbose_name="نسبة العربون %"
    )

    is_active = models.BooleanField(
        default=True,
        verbose_name="الإعدادات مفعلة"
    )

    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="آخر تحديث"
    )

    class Meta:
        verbose_name = "إعدادات المتجر"
        verbose_name_plural = "إعدادات المتجر"

    def __str__(self):
        return "إعدادات المتجر"