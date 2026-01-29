"""
Dashboard Views
"""

from .main import dashboard_home, dashboard_stats
from .business import (
    business_list, business_create, business_update, 
    business_detail, business_delete
)
from .product import (
    product_list, product_create, product_update, product_delete
)
from .deal import (
    deal_list, deal_create, deal_update, deal_delete
)
from .review import review_list, review_reply

__all__ = [
    'dashboard_home',
    'dashboard_stats',
    'business_list',
    'business_create',
    'business_update',
    'business_detail',
    'business_delete',
    'product_list',
    'product_create',
    'product_update',
    'product_delete',
    'deal_list',
    'deal_create',
    'deal_update',
    'deal_delete',
    'review_list',
    'review_reply',
]
