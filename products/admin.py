from django.contrib import admin
from .models import Category, Product


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug")
    search_fields = ("name",)
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "price", "stock", "is_active", "updated_at")
    list_filter = ("category", "is_active")
    search_fields = ("name", "description")
    list_editable = ("price", "stock", "is_active")
    prepopulated_fields = {"slug": ("name",)}
    readonly_fields = ("created_at", "updated_at")
    list_per_page = 25
    fieldsets = (
        ("Product Information", {
            "fields": ("name", "slug", "category", "description", "image")
        }),
        ("Pricing and Inventory", {
            "fields": ("price", "stock", "is_active")
        }),
        ("Timestamps", {
            "fields": ("created_at", "updated_at"),
            "classes": ("collapse",)
        }),
    )


from .models import SharedProduct


@admin.register(SharedProduct)
class SharedProductAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "category",
        "price",
        "stock",
        "is_active",
        "updated_at",
    )

    list_filter = ("category", "is_active")
    search_fields = ("name", "description")
    list_editable = ("price", "stock", "is_active")
    readonly_fields = ("id", "created_at", "updated_at")
    list_per_page = 25

    fields = (
        "id",
        "name",
        "description",
        "category",
        "price",
        "image_url",
        "stock",
        "is_active",
        "created_at",
        "updated_at",
    )
