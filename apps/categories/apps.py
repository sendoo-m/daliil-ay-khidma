"""
Categories App Configuration
============================
"""

from django.apps import AppConfig


class CategoriesConfig(AppConfig):
    """إعدادات تطبيق التصنيفات"""
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.categories'
    verbose_name = 'Categories Management'
    verbose_name_plural = 'Categories'
