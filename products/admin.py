from django import forms
from django.conf import settings
from django.contrib import admin
from django.core.files.storage import default_storage
from django.utils.html import format_html

from .models import Category, Product, SharedProduct


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug")
    search_fields = ("name",)
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        "name", "category", "price", "stock", "is_active", "updated_at"
    )
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


class SharedProductUploadForm(forms.ModelForm):
    image_upload = forms.ImageField(
        required=False,
        label="Upload product image",
        help_text="Choose an image from your computer. Maximum size: 5 MB."
    )

    class Meta:
        model = SharedProduct
        fields = (
            "name",
            "description",
            "category",
            "price",
            "stock",
            "is_active",
        )

    def clean_image_upload(self):
        image = self.cleaned_data.get("image_upload")

        if image and image.size > 5 * 1024 * 1024:
            raise forms.ValidationError("Image size must not exceed 5 MB.")

        return image


@admin.register(SharedProduct)
class SharedProductAdmin(admin.ModelAdmin):
    form = SharedProductUploadForm

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
    readonly_fields = (
        "id",
        "image_url",
        "image_preview",
        "created_at",
        "updated_at",
    )
    list_per_page = 25

    fields = (
        "id",
        "name",
        "description",
        "category",
        "price",
        "stock",
        "is_active",
        "image_upload",
        "image_url",
        "image_preview",
        "created_at",
        "updated_at",
    )

    @admin.display(description="Current product image")
    def image_preview(self, obj):
        if obj and obj.image_url:
            return format_html(
                '<img src="{}" style="max-width:180px;max-height:180px;'
                'object-fit:contain;border-radius:8px;" />',
                obj.image_url
            )
        return "No image uploaded"

    def save_model(self, request, obj, form, change):
        uploaded_image = form.cleaned_data.get("image_upload")

        if uploaded_image:
            filename = default_storage.save(
                f"products/{uploaded_image.name}",
                uploaded_image,
            )
            obj.image_url = default_storage.url(filename)

        super().save_model(request, obj, form, change)
