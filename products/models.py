from django.db import models
from django.utils.text import slugify


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=120, unique=True, blank=True)
    description = models.TextField(blank=True)

    class Meta:
        ordering = ["name"]
        verbose_name_plural = "Categories"

    def save(self, *args, **kwargs):
        if not self.slug:
            base = slugify(self.name)
            candidate = base
            n = 2
            while Category.objects.filter(slug=candidate).exclude(pk=self.pk).exists():
                candidate = f"{base}-{n}"
                n += 1
            self.slug = candidate
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name="products")
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=220, unique=True, blank=True)
    price = models.DecimalField(max_digits=12, decimal_places=2)
    description = models.TextField(blank=True)
    stock = models.PositiveIntegerField(default=0)
    image = models.ImageField(upload_to="products/", blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def save(self, *args, **kwargs):
        if not self.slug:
            base = slugify(self.name)
            candidate = base
            n = 2
            while Product.objects.filter(slug=candidate).exclude(pk=self.pk).exists():
                candidate = f"{base}-{n}"
                n += 1
            self.slug = candidate
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class SharedProduct(models.Model):
    name = models.CharField(max_length=150)
    description = models.TextField(blank=True, null=True)
    category = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=12, decimal_places=2)
    image_url = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    stock = models.IntegerField(default=0)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = "products"
        ordering = ["-created_at"]
        verbose_name = "Shared Product"
        verbose_name_plural = "Shared Products"

    def __str__(self):
        return self.name
