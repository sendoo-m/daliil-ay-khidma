"""
Dashboard Forms
"""

# Import from forms module files
from .business import BusinessForm as BusinessFormOld
from .product import ProductForm as ProductFormOld
from .deal import DealForm as DealFormOld
from .review import ReviewReplyForm

# Import from forms.py (new CRUD forms)
try:
    import sys
    import os
    # Get parent directory
    parent_dir = os.path.dirname(os.path.dirname(__file__))
    # Import forms.py from dashboard
    import importlib.util
    spec = importlib.util.spec_from_file_location(
        "dashboard_forms", 
        os.path.join(os.path.dirname(__file__), '..', 'forms.py')
    )
    if spec and spec.loader:
        dashboard_forms = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(dashboard_forms)
        
        AdminUserCreateForm = dashboard_forms.AdminUserCreateForm
        AdminUserEditForm = dashboard_forms.AdminUserEditForm
        BusinessForm = dashboard_forms.BusinessForm
        ProductForm = dashboard_forms.ProductForm
        CategoryForm = dashboard_forms.CategoryForm
        DealForm = dashboard_forms.DealForm
except:
    # Fallback to old forms
    BusinessForm = BusinessFormOld
    ProductForm = ProductFormOld
    DealForm = DealFormOld
    AdminUserCreateForm = None
    AdminUserEditForm = None
    CategoryForm = None

__all__ = [
    'BusinessForm',
    'ProductForm',
    'DealForm',
    'ReviewReplyForm',
    'AdminUserCreateForm',
    'AdminUserEditForm',
    'CategoryForm',
]
