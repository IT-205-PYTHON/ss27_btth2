"""
cold_storage_product.py
-------------------------
ColdStorageProduct: Hàng đông lạnh, kế thừa từ BaseProduct.

Đặc thù nghiệp vụ:
- Có required_temperature (nhiệt độ bảo quản yêu cầu, vd: -18 độ C)
- import_stock(): nhập kho bình thường
- export_stock(): chịu thêm 5% hao hụt bảo quản trên số lượng xuất
  (vd: xuất 50 -> hao hụt 2.5 -> tổng khấu trừ trong kho là 52.5)
- apply_cooling_cost(): tính chi phí vận hành máy lạnh phát sinh dựa
  trên số lượng tồn kho hiện tại
"""

from models.base_product import BaseProduct

# Tỷ lệ hao hụt bảo quản khi xuất kho hàng đông lạnh (5%)
COLD_STORAGE_LOSS_RATE = 0.05

# Đơn giá chi phí làm lạnh tính trên mỗi đơn vị tồn kho / ngày (VND)
COOLING_COST_PER_UNIT = 3000


class ColdStorageProduct(BaseProduct):
    def __init__(self, product_code, product_name, stock_quantity=0, required_temperature=-18):
        # super().__init__() để tái sử dụng logic khởi tạo của lớp cha
        # (gán product_code, chuẩn hóa product_name, khởi tạo __stock_quantity)
        super().__init__(product_code, product_name, stock_quantity)
        self.required_temperature = required_temperature

    # -----------------------------------------------------------
    # METHOD OVERRIDING: import_stock
    # -----------------------------------------------------------
    def import_stock(self, quantity):
        if quantity <= 0:
            raise ValueError("Số lượng nhập kho phải lớn hơn 0.")
        self._update_stock(quantity)
        return {
            "quantity": quantity,
            "new_stock": self.stock_quantity,
        }

    # -----------------------------------------------------------
    # METHOD OVERRIDING: export_stock
    # Hàng đông lạnh xuất kho -> chịu thêm 5% hao hụt bảo quản
    # tính trên số lượng xuất.
    # -----------------------------------------------------------
    def export_stock(self, quantity):
        if quantity <= 0:
            raise ValueError("Số lượng xuất kho phải lớn hơn 0.")

        loss = quantity * COLD_STORAGE_LOSS_RATE
        total_deduct = quantity + loss

        if total_deduct > self.stock_quantity:
            raise ValueError("Số lượng tồn kho không đủ để xuất (đã bao gồm hao hụt bảo quản).")

        self._update_stock(-total_deduct)
        return {
            "quantity": quantity,
            "loss": loss,
            "total_deduct": total_deduct,
            "new_stock": self.stock_quantity,
        }

    # -----------------------------------------------------------
    # INSTANCE METHOD: apply_cooling_cost
    # -----------------------------------------------------------
    def apply_cooling_cost(self):
        """Tính chi phí làm lạnh phát sinh trong ngày = tồn kho * đơn giá/đv."""
        cooling_cost = self.stock_quantity * COOLING_COST_PER_UNIT
        return cooling_cost
