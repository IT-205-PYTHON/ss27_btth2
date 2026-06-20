"""
hazardous_product.py
----------------------
HazardousProduct: Hàng hóa nguy hiểm (hóa chất, chất dễ cháy...), kế thừa
từ BaseProduct.

Đặc thù nghiệp vụ:
- Có max_safety_limit (hạn mức lưu trữ tối đa an toàn trong 1 phân khu)
- Tồn kho TUYỆT ĐỐI không được vượt quá max_safety_limit
- import_stock(): nếu stock_quantity + quantity > max_safety_limit
  -> từ chối nhập kho (Edge case - Bẫy 2)
- export_stock(): xuất kho bình thường theo quy trình an toàn
"""

from models.base_product import BaseProduct


class HazardousProduct(BaseProduct):
    def __init__(self, product_code, product_name, stock_quantity=0, max_safety_limit=500):
        super().__init__(product_code, product_name, stock_quantity)
        self.max_safety_limit = max_safety_limit

    # -----------------------------------------------------------
    # METHOD OVERRIDING: import_stock
    # Edge case (Bẫy 2): nếu vượt hạn mức an toàn -> raise ValueError
    # -----------------------------------------------------------
    def import_stock(self, quantity):
        if quantity <= 0:
            raise ValueError("Số lượng nhập kho phải lớn hơn 0.")

        projected_stock = self.stock_quantity + quantity

        if projected_stock > self.max_safety_limit:
            raise ValueError(
                f"Số lượng nhập vào khiến tồn kho vượt quá hạn mức an toàn "
                f"cho phép (Tối đa: {self.max_safety_limit:g})."
            )

        self._update_stock(quantity)
        return {
            "quantity": quantity,
            "new_stock": self.stock_quantity,
        }

    # -----------------------------------------------------------
    # METHOD OVERRIDING: export_stock (xuất kho bình thường, không phụ phí)
    # -----------------------------------------------------------
    def export_stock(self, quantity):
        if quantity <= 0:
            raise ValueError("Số lượng xuất kho phải lớn hơn 0.")

        if quantity > self.stock_quantity:
            raise ValueError("Số lượng tồn kho không đủ để xuất.")

        self._update_stock(-quantity)
        return {
            "quantity": quantity,
            "new_stock": self.stock_quantity,
        }
