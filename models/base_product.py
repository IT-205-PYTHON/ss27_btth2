"""
base_product.py
-----------------
Định nghĩa lớp trừu tượng (Abstract Base Class) BaseProduct.
Đây là "bộ khung chuẩn" cho mọi loại hàng hóa trong hệ thống
Amazon Inventory Simulator Pro.

Kỹ thuật OOP áp dụng:
- abc.ABC + @abstractmethod: ép buộc lớp con phải tự định nghĩa
  import_stock()/export_stock()
- Đóng gói (Encapsulation): __stock_quantity là private attribute,
  chỉ truy cập qua property
- @property: cho phép đọc stock_quantity như thuộc tính nhưng không
  cho ghi trực tiếp từ bên ngoài
- @staticmethod / @classmethod: tiện ích không phụ thuộc / phụ thuộc class
- Operator Overloading: __add__, __lt__
"""

from abc import ABC, abstractmethod


class BaseProduct(ABC):
    """
    Lớp trừu tượng (Abstract Base Class) cho mọi loại hàng hóa.
    Không thể khởi tạo trực tiếp (Edge case - Bẫy 1) vì có @abstractmethod.
    """

    # ---------------------------------------------------------------
    # CLASS ATTRIBUTES
    # Thuộc tính cấp lớp - dùng chung cho TẤT CẢ instance.
    # warehouse_name có thể đổi qua classmethod, ảnh hưởng toàn hệ thống.
    # ---------------------------------------------------------------
    warehouse_name = "Amazon Logistics"
    base_storage_fee = 5000  # Phí lưu kho cơ bản / ngày (VND)

    def __init__(self, product_code, product_name, stock_quantity=0):
        self.product_code = product_code

        # Chuẩn hóa tên sản phẩm ngay từ lúc khởi tạo (in hoa, xóa khoảng
        # trắng thừa) thông qua property setter bên dưới.
        self._product_name = self._normalize_name(product_name)

        # ---------------------------------------------------------------
        # PRIVATE ATTRIBUTE (đóng gói số lượng tồn kho)
        # Python "name-mangle" thành self._BaseProduct__stock_quantity,
        # khiến việc truy cập trực tiếp từ ngoài (obj.__stock_quantity)
        # thất bại. Mọi thay đổi tồn kho BẮT BUỘC đi qua import_stock()/
        # export_stock() hoặc hàm bảo vệ _update_stock() bên dưới.
        # ---------------------------------------------------------------
        self.__stock_quantity = stock_quantity

    # =================================================================
    # PROPERTY: stock_quantity (chỉ có getter, KHÔNG có setter)
    # =================================================================
    @property
    def stock_quantity(self):
        """
        Getter duy nhất để đọc số lượng tồn kho.
        Không có @stock_quantity.setter => không thể gán trực tiếp
        obj.stock_quantity = 9999 từ bên ngoài. Muốn thay đổi tồn kho
        phải gọi nghiệp vụ thực sự: import_stock()/export_stock().
        """
        return self.__stock_quantity

    # ---------------------------------------------------------------
    # PROPERTY: product_name (minh họa setter chuẩn hóa dữ liệu theo
    # đúng yêu cầu nghiệp vụ "Tên sản phẩm tự động in hoa, xóa khoảng
    # trắng thừa")
    # ---------------------------------------------------------------
    @property
    def product_name(self):
        return self._product_name

    @product_name.setter
    def product_name(self, value):
        self._product_name = self._normalize_name(value)

    @staticmethod
    def _normalize_name(name):
        """Chuẩn hóa tên: xóa khoảng trắng thừa 2 đầu + giữa từ, in hoa toàn bộ."""
        return " ".join(name.strip().split()).upper()

    # =================================================================
    # PROTECTED HELPER - cho phép lớp con cập nhật __stock_quantity một
    # cách an toàn, có kiểm soát (thay vì truy cập trực tiếp biến private)
    # =================================================================
    def _update_stock(self, delta):
        """Cộng (delta dương) hoặc trừ (delta âm) vào số lượng tồn kho."""
        self.__stock_quantity += delta

    # =================================================================
    # ABSTRACT METHODS
    # Các lớp con BẮT BUỘC phải override, nếu không Python sẽ ném lỗi
    # TypeError ngay khi cố gắng khởi tạo instance của lớp con đó.
    # =================================================================
    @abstractmethod
    def import_stock(self, quantity):
        """Nhập kho. Mỗi loại sản phẩm có nghiệp vụ kiểm tra riêng."""
        raise NotImplementedError

    @abstractmethod
    def export_stock(self, quantity):
        """Xuất kho. Mỗi loại sản phẩm có nghiệp vụ xử lý riêng."""
        raise NotImplementedError

    # =================================================================
    # OPERATOR OVERLOADING
    # =================================================================
    def __add__(self, other):
        """
        Cộng tồn kho của 2 đối tượng sản phẩm bất kỳ -> trả về SỐ NGUYÊN
        (tổng số lượng), KHÔNG trả về một object sản phẩm mới.

        Edge case (Bẫy 3): nếu other không phải BaseProduct (vd: int, str)
        thì trả về NotImplemented thay vì để lỗi tràn ra ngoài mơ hồ.
        Python sẽ tự thử other.__radd__(self); nếu vẫn thất bại sẽ raise
        TypeError chuẩn của Python.
        """
        if not isinstance(other, BaseProduct):
            return NotImplemented
        return int(self.stock_quantity + other.stock_quantity)

    def __radd__(self, other):
        # Hỗ trợ sum([p1, p2, p3]) bắt đầu bằng 0 + p1
        if other == 0:
            return self.stock_quantity
        return NotImplemented

    def __lt__(self, other):
        """
        So sánh tồn kho: self < other -> True/False.

        Edge case (Bẫy 3): nếu other không phải BaseProduct, trả về
        NotImplemented để Python tự raise TypeError chuẩn khi không
        bên nào so sánh được.
        """
        if not isinstance(other, BaseProduct):
            return NotImplemented
        return self.stock_quantity < other.stock_quantity

    def __repr__(self):
        return (f"{self.__class__.__name__}(product_code='{self.product_code}', "
                f"name='{self.product_name}', stock={self.stock_quantity})")

    # =================================================================
    # STATIC METHOD
    # Không phụ thuộc self hay cls -> hàm tiện ích thuần túy, logic
    # không đổi dù gọi từ class hay từ bất kỳ instance nào.
    # =================================================================
    @staticmethod
    def validate_product_code(product_code):
        """
        Kiểm tra mã sản phẩm: phải có đúng 10 ký tự, bắt đầu bằng chữ cái
        (vd: "AMZ1234567").
        """
        return (
            isinstance(product_code, str)
            and len(product_code) == 10
            and product_code[0].isalpha()
        )

    # =================================================================
    # CLASS METHOD
    # Nhận cls thay vì self -> thay đổi/đọc trạng thái cấp LỚP (class
    # attribute), ảnh hưởng toàn hệ thống, không chỉ 1 object.
    # =================================================================
    @classmethod
    def update_warehouse_name(cls, new_name):
        """Cập nhật tên chuỗi kho hàng dùng chung cho toàn hệ thống."""
        cls.warehouse_name = new_name
