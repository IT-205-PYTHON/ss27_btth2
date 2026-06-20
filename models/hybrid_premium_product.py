"""
hybrid_premium_product.py
---------------------------
HybridPremiumProduct: Dòng sản phẩm lai cao cấp, áp dụng ĐA KẾ THỪA
(Multiple Inheritance) từ CẢ HAI lớp cụ thể: ColdStorageProduct và
HazardousProduct.

Đây là điểm KHÁC BIỆT quan trọng so với mô hình Mixin thông thường:
cả 2 lớp cha (ColdStorageProduct, HazardousProduct) đều là lớp CỤ THỂ,
ĐỀU TỰ OVERRIDE import_stock() và export_stock() của BaseProduct.
=> Khi HybridPremiumProduct gọi super().import_stock(...) hay không
   override gì cả, Python phải dùng MRO (C3 Linearization) để quyết
   định gọi phiên bản của lớp cha nào trước.

MRO của lớp này (theo thứ tự khai báo
`class HybridPremiumProduct(ColdStorageProduct, HazardousProduct)`):

    HybridPremiumProduct -> ColdStorageProduct -> HazardousProduct
    -> BaseProduct -> ABC -> object

=> Nếu HybridPremiumProduct KHÔNG tự override import_stock()/export_stock(),
   Python sẽ ưu tiên gọi ColdStorageProduct.import_stock() trước (vì đứng
   trước trong MRO), bỏ qua HazardousProduct.import_stock() hoàn toàn.

Theo yêu cầu đề bài, sản phẩm Hybrid phải đồng thời:
   (a) chịu hao hụt bảo quản 5% khi xuất (đặc tính ColdStorageProduct)
   (b) bị chặn nhập kho nếu vượt hạn mức an toàn (đặc tính HazardousProduct)

=> Do đó HybridPremiumProduct PHẢI tự override cả import_stock() và
   export_stock(), rồi chủ động gọi rõ ràng đến từng lớp cha tương ứng
   bằng cách gọi method không-bound qua tên lớp cha
   (HazardousProduct.import_stock(self, ...) / ColdStorageProduct.export_stock(self, ...))
   thay vì chỉ dùng super() đơn thuần (super() chỉ trỏ đến lớp NGAY SAU
   trong MRO, không đủ để gọi rõ ràng "lớp cha thứ 2").
"""

from models.cold_storage_product import ColdStorageProduct
from models.hazardous_product import HazardousProduct


class HybridPremiumProduct(ColdStorageProduct, HazardousProduct):
    """
    Đa kế thừa: ColdStorageProduct (quản lý nhiệt độ, hao hụt bảo quản)
    + HazardousProduct (chặn hạn mức an toàn tuyệt đối).
    """

    def __init__(self, product_code, product_name, stock_quantity=0,
                 required_temperature=-18, max_safety_limit=500):
        # Không thể chỉ gọi super().__init__() một lần vì 2 lớp cha có
        # __init__ khác chữ ký (signature) và đều set thuộc tính riêng
        # (required_temperature / max_safety_limit). Ta gọi trực tiếp
        # __init__ của BaseProduct (gốc chung) một lần để tránh khởi tạo
        # __stock_quantity 2 lần, sau đó tự gán 2 thuộc tính đặc thù.
        ColdStorageProduct.__init__(
            self, product_code, product_name, stock_quantity, required_temperature
        )
        # max_safety_limit là thuộc tính riêng của HazardousProduct,
        # ColdStorageProduct.__init__ ở trên không gán nó -> gán bổ sung.
        self.max_safety_limit = max_safety_limit

    # -----------------------------------------------------------
    # METHOD OVERRIDING: import_stock
    # Tích hợp cơ chế chặn hạn mức an toàn (HazardousProduct) - vì đây
    # là điều kiện AN TOÀN bắt buộc, ưu tiên cao nhất khi nhập kho.
    # -----------------------------------------------------------
    def import_stock(self, quantity):
        # Gọi tường minh đến HazardousProduct.import_stock để đảm bảo
        # logic chặn vượt hạn mức an toàn LUÔN được áp dụng, bất kể MRO
        # ưu tiên ColdStorageProduct đứng trước.
        return HazardousProduct.import_stock(self, quantity)

    # -----------------------------------------------------------
    # METHOD OVERRIDING: export_stock
    # Tích hợp cơ chế hao hụt bảo quản 5% (ColdStorageProduct) - vì
    # đây là đặc tính vật lý của hàng đông lạnh, áp dụng khi xuất kho.
    # -----------------------------------------------------------
    def export_stock(self, quantity):
        # Gọi tường minh đến ColdStorageProduct.export_stock để đảm bảo
        # hao hụt bảo quản 5% luôn được tính đúng theo MRO mong muốn.
        return ColdStorageProduct.export_stock(self, quantity)
