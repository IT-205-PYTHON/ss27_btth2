"""
models package
---------------
Gom toàn bộ các lớp Sản phẩm để import gọn:
    from models import BaseProduct, ColdStorageProduct, HazardousProduct, HybridPremiumProduct
"""

from models.base_product import BaseProduct
from models.cold_storage_product import ColdStorageProduct
from models.hazardous_product import HazardousProduct
from models.hybrid_premium_product import HybridPremiumProduct

__all__ = [
    "BaseProduct",
    "ColdStorageProduct",
    "HazardousProduct",
    "HybridPremiumProduct",
]
