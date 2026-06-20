"""
main.py
-------
AMAZON INVENTORY SIMULATOR PRO
Chương trình CLI chính, điều phối toàn bộ menu nghiệp vụ (1-7).

Chạy chương trình:
    python main.py
"""

from models import BaseProduct, ColdStorageProduct, HazardousProduct, HybridPremiumProduct
from carriers import FedExCarrier, DHLCarrier, InvalidCarrier
from services import dispatch_to_carrier
from utils import parse_quantity, format_vnd, format_unit, safe_input

# Danh sách toàn bộ sản phẩm trong kho & sản phẩm đang được chọn (active)
products = []
current_product = None


# =====================================================================
# CHỨC NĂNG 1: ĐĂNG KÝ MÃ HÀNG HÓA MỚI
# =====================================================================
def register_product():
    global current_product

    print("\n--- CHỌN LOẠI SẢN PHẨM KHỞI TẠO ---")
    print("1. Cold Storage Product (Hàng Đông Lạnh)")
    print("2. Hazardous Product (Hàng Nguy Hiểm)")
    print("3. Hybrid Premium Product (Hàng Lai Cao Cấp)")
    choice = safe_input("Chọn loại sản phẩm (1-3): ")

    if choice not in ("1", "2", "3"):
        print("Lựa chọn không hợp lệ.")
        return

    product_code = safe_input("Nhập mã sản phẩm 10 ký tự: ")

    # ---------------------------------------------------------------
    # Edge case: dùng @staticmethod validate_product_code để kiểm tra
    # ---------------------------------------------------------------
    if not BaseProduct.validate_product_code(product_code):
        print("Mã sản phẩm không hợp lệ! Phải gồm đúng 10 ký tự và bắt đầu bằng chữ cái.")
        return

    # Kiểm tra trùng mã sản phẩm trong hệ thống
    if any(p.product_code == product_code for p in products):
        print("Mã sản phẩm đã tồn tại trong hệ thống.")
        return

    product_name = safe_input("Nhập tên sản phẩm: ")
    if not product_name:
        print("Tên sản phẩm không được để trống.")
        return

    try:
        if choice == "1":
            temp_text = safe_input("Nhập nhiệt độ bảo quản yêu cầu (độ C): ")
            required_temperature = float(temp_text)
            new_product = ColdStorageProduct(
                product_code, product_name, stock_quantity=0,
                required_temperature=required_temperature
            )
            print("\nĐăng ký sản phẩm Đông Lạnh thành công!")

        elif choice == "2":
            limit_text = safe_input("Nhập hạn mức lưu trữ an toàn tối đa (vd: 500): ")
            max_safety_limit = parse_quantity(limit_text)
            new_product = HazardousProduct(
                product_code, product_name, stock_quantity=0,
                max_safety_limit=max_safety_limit
            )
            print("\nĐăng ký sản phẩm Nguy Hiểm thành công!")

        else:  # choice == "3"
            temp_text = safe_input("Nhập nhiệt độ bảo quản yêu cầu (độ C): ")
            required_temperature = float(temp_text)
            limit_text = safe_input("Nhập hạn mức lưu trữ an toàn tối đa (vd: 200): ")
            max_safety_limit = parse_quantity(limit_text)
            new_product = HybridPremiumProduct(
                product_code, product_name, stock_quantity=0,
                required_temperature=required_temperature,
                max_safety_limit=max_safety_limit
            )
            print("\nĐăng ký sản phẩm Lai Cao Cấp (Hybrid) thành công!")

    except ValueError:
        print("Dữ liệu nhập vào không hợp lệ. Hủy đăng ký sản phẩm.")
        return

    products.append(new_product)
    current_product = new_product
    print(f"Tên sản phẩm: {new_product.product_name}")


# =====================================================================
# CHỨC NĂNG 2: XEM THÔNG TIN & KIỂM TRA MRO
# =====================================================================
def view_product_info():
    if current_product is None:
        print("\nHệ thống chưa có thông tin sản phẩm. Vui lòng đăng ký ở Chức năng 1 trước.")
        return

    p = current_product
    print("\n--- THÔNG TIN SẢN PHẨM HIỆN TẠI ---")
    print(f"Loại sản phẩm: {p.__class__.__name__}")
    print(f"Chuỗi kho: {p.warehouse_name}")
    print(f"Mã sản phẩm: {p.product_code}")
    print(f"Tên sản phẩm: {p.product_name}")
    print(f"Số lượng tồn kho: {format_unit(p.stock_quantity)}")

    if isinstance(p, ColdStorageProduct):
        print(f"Nhiệt độ yêu cầu: {p.required_temperature:g} độ C")

    if isinstance(p, HazardousProduct):
        print(f"Hạn mức an toàn tối đa: {format_unit(p.max_safety_limit)}")

    # ---------------------------------------------------------------
    # Kiểm tra MRO (Method Resolution Order) - đặc biệt ý nghĩa với
    # HybridPremiumProduct vì đây là lớp đa kế thừa từ 2 nhánh cha.
    # ---------------------------------------------------------------
    print("\n--- MRO (Method Resolution Order) ---")
    mro_names = [cls.__name__ for cls in p.__class__.__mro__]
    print(" -> ".join(mro_names))


# =====================================================================
# CHỨC NĂNG 3: GIAO DỊCH NHẬP / XUẤT KHO (ĐA HÌNH)
# =====================================================================
def transaction():
    if current_product is None:
        print("\nHệ thống chưa có thông tin sản phẩm. Vui lòng đăng ký ở Chức năng 1 trước.")
        return

    print("\n--- GIAO DỊCH NHẬP / XUẤT KHO ---")
    print("1. Nhập kho")
    print("2. Xuất kho")
    choice = safe_input("Chọn giao dịch (1-2): ")

    if choice not in ("1", "2"):
        print("Lựa chọn không hợp lệ.")
        return

    try:
        if choice == "1":
            quantity = parse_quantity(safe_input("Nhập số lượng nhập kho: "))
            # ĐA HÌNH: cùng lời gọi .import_stock() nhưng hành vi khác nhau
            # tùy current_product thực sự là ColdStorageProduct /
            # HazardousProduct / HybridPremiumProduct
            result = current_product.import_stock(quantity)
            print("\nNhập kho thành công!")
            print(f"Số lượng nhập: {format_unit(result['quantity'])}")
            print(f"Số lượng tồn kho cập nhật: {format_unit(current_product.stock_quantity)}")

        else:
            quantity = parse_quantity(safe_input("Nhập số lượng cần xuất: "))
            # ĐA HÌNH: ColdStorageProduct/HybridPremiumProduct hao hụt 5%,
            # HazardousProduct xuất bình thường.
            result = current_product.export_stock(quantity)
            print("\nXuất kho thành công!")
            print(f"Số lượng yêu cầu: {format_unit(result['quantity'])}")

            if "loss" in result:
                print(f"Số lượng hao hụt bảo quản (5%): {format_unit(result['loss'])}")
                print(f"Tổng số lượng khấu trừ trong kho: {format_unit(result['total_deduct'])}")

            print(f"Số lượng tồn kho cập nhật: {format_unit(current_product.stock_quantity)}")

    except ValueError as e:
        print(f"\nGiao dịch thất bại! {e}")


# =====================================================================
# CHỨC NĂNG 4: KIỂM TRA ĐIỀU KIỆN BẢO QUẢN / TÍNH CHI PHÍ PHỤ TRỘI
# =====================================================================
def apply_cooling_cost():
    if current_product is None:
        print("\nHệ thống chưa có thông tin sản phẩm. Vui lòng đăng ký ở Chức năng 1 trước.")
        return

    # ColdStorageProduct & HybridPremiumProduct (vì HybridPremiumProduct
    # kế thừa ColdStorageProduct)
    if not isinstance(current_product, ColdStorageProduct):
        print("\nTính năng này không hỗ trợ cho loại sản phẩm hiện tại "
              "(chỉ áp dụng cho Đông Lạnh/Hybrid).")
        return

    print("\n--- TÍNH PHÍ BẢO QUẢN ĐÔNG LẠNH ---")
    print(f"Số lượng tồn kho hiện tại: {format_unit(current_product.stock_quantity)}")
    print(f"Nhiệt độ yêu cầu: {current_product.required_temperature:g} độ C")

    cooling_cost = current_product.apply_cooling_cost()
    print(f"Chi phí làm lạnh phát sinh trong ngày: +{format_vnd(cooling_cost)}")


# =====================================================================
# CHỨC NĂNG 5: GỘP LÔ HÀNG & SO SÁNH TỒN KHO (OPERATOR OVERLOADING)
# =====================================================================
def compare_and_merge():
    if current_product is None:
        print("\nHệ thống chưa có thông tin sản phẩm. Vui lòng đăng ký ở Chức năng 1 trước.")
        return

    other_products = [p for p in products if p is not current_product]
    if not other_products:
        print("\nKhông có sản phẩm nào khác trong hệ thống để so sánh.")
        return

    print("\n--- ĐỒNG BỘ & SO SÁNH TỒN KHO (OPERATOR OVERLOADING) ---")
    print(f"Sản phẩm hiện tại (A): {current_product.product_name} "
          f"(Tồn kho: {format_unit(current_product.stock_quantity)})")

    print("\nDanh sách sản phẩm khác trong hệ thống:")
    for idx, p in enumerate(other_products, start=1):
        print(f"{idx}. {p.product_code} ({p.product_name} - Tồn kho: {format_unit(p.stock_quantity)})")

    choice = safe_input("Chọn sản phẩm đối ứng (B) theo số thứ tự: ")
    if not choice.isdigit() or not (1 <= int(choice) <= len(other_products)):
        print("Lựa chọn không hợp lệ.")
        return

    other_product = other_products[int(choice) - 1]

    # __lt__ overloading
    if current_product < other_product:
        print("\n[Kết quả So sánh (__lt__)]: Tồn kho sản phẩm A ÍT HƠN tồn kho sản phẩm B.")
    elif other_product < current_product:
        print("\n[Kết quả So sánh (__lt__)]: Tồn kho sản phẩm A NHIỀU HƠN tồn kho sản phẩm B.")
    else:
        print("\n[Kết quả So sánh (__lt__)]: Tồn kho sản phẩm A BẰNG tồn kho sản phẩm B.")

    # __add__ overloading -> trả về SỐ NGUYÊN, không phải object
    total = current_product + other_product
    print(f"[Kết quả Tổng hợp (__add__)]: Tổng số lượng tồn kho của cả 2 mã sản phẩm là: "
          f"{format_unit(total)}.")


# =====================================================================
# CHỨC NĂNG 6: ĐIỀU PHỐI VẬN CHUYỂN QUA ĐỐI TÁC THỨ BA (DUCK TYPING)
# =====================================================================
def ship_package():
    if current_product is None:
        print("\nHệ thống chưa có thông tin sản phẩm. Vui lòng đăng ký ở Chức năng 1 trước.")
        return

    print("\n--- ĐIỀU PHỐI ĐƠN VỊ VẬN CHUYỂN NGOÀI ---")
    print("1. Vận chuyển qua đối tác FedEx")
    print("2. Vận chuyển qua đối tác DHL")
    choice = safe_input("Chọn đối tác vận chuyển (1-2): ")

    carrier_map = {
        "1": FedExCarrier(),
        "2": DHLCarrier(),
    }

    carrier = carrier_map.get(choice)
    if carrier is None:
        print("Lựa chọn không hợp lệ.")
        return

    try:
        quantity = parse_quantity(safe_input("Nhập số lượng hàng hóa bàn giao: "))
    except ValueError as e:
        print(f"Lỗi: {e}")
        return

    # dispatch_to_carrier() không quan tâm carrier là class gì - Duck Typing
    dispatch_to_carrier(carrier, current_product, quantity)


# =====================================================================
# MENU CHÍNH
# =====================================================================
MENU_TEXT = """
===== AMAZON INVENTORY SIMULATOR PRO =====
1. Đăng ký mã hàng hóa mới (Chọn loại sản phẩm)
2. Xem thông tin & Kiểm tra thứ tự kế thừa (MRO)
3. Giao dịch Nhập / Xuất kho (Đa hình)
4. Kiểm tra điều kiện bảo quản / Tính chi phí phụ trội
5. Kiểm tra tính năng gộp lô hàng & So sánh tồn kho (Overloading)
6. Điều phối vận chuyển qua Đối tác thứ ba (Duck Typing)
7. Thoát chương trình
==========================================
"""


def main():
    while True:
        print(MENU_TEXT)
        choice = safe_input("Chọn chức năng (1-7): ")

        if choice == "1":
            register_product()
        elif choice == "2":
            view_product_info()
        elif choice == "3":
            transaction()
        elif choice == "4":
            apply_cooling_cost()
        elif choice == "5":
            compare_and_merge()
        elif choice == "6":
            ship_package()
        elif choice == "7":
            print("\nCảm ơn đã sử dụng hệ thống Amazon Inventory Simulator Pro!")
            break
        else:
            print("\nLựa chọn không hợp lệ. Vui lòng chọn từ 1-7.")


# =====================================================================
# DEMO EDGE CASES (chạy độc lập để kiểm chứng các bẫy dữ liệu)
# Có thể bỏ comment để chạy thử nhanh không cần tương tác CLI.
# =====================================================================
def demo_edge_cases():
    print("\n========== DEMO EDGE CASES ==========")

    # Bẫy 1: Khởi tạo trực tiếp lớp trừu tượng
    try:
        BaseProduct("AMZ0000001", "TEST")
    except TypeError as e:
        print(f"[Bẫy 1 OK] Không thể khởi tạo BaseProduct trực tiếp -> TypeError: {e}")

    # Bẫy 2: Vượt quá giới hạn lưu kho an toàn (HazardousProduct & Hybrid)
    hazardous = HazardousProduct("AMZ1111111", "Sulfuric Acid", stock_quantity=480, max_safety_limit=500)
    try:
        hazardous.import_stock(50)
    except ValueError as e:
        print(f"[Bẫy 2 OK - Hazardous] {e}")

    hybrid = HybridPremiumProduct(
        "AMZ2222222", "Special Vaccine Lo A", stock_quantity=180,
        required_temperature=-70, max_safety_limit=200
    )
    try:
        hybrid.import_stock(50)
    except ValueError as e:
        print(f"[Bẫy 2 OK - Hybrid] {e}")

    # Bẫy 3: Cộng/so sánh sản phẩm với kiểu dữ liệu khác
    # __add__/__lt__ trả về NotImplemented khi other không phải BaseProduct;
    # Python sau đó tự động raise TypeError chuẩn khi dùng trong biểu thức.
    cold = ColdStorageProduct("AMZ3333333", "Salmon Fillet", stock_quantity=100)
    try:
        cold + 100
    except TypeError as e:
        print(f"[Bẫy 3 OK] Cộng sản phẩm với int -> TypeError: {e}")

    try:
        cold < "some_string"
    except TypeError as e:
        print(f"[Bẫy 3 OK] So sánh sản phẩm với string -> TypeError: {e}")

    # Bẫy 4: Đối tác vận chuyển không hợp lệ (thiếu ship_package)
    invalid_carrier = InvalidCarrier()
    dispatch_to_carrier(invalid_carrier, cold, 10)

    print("========== KẾT THÚC DEMO ==========\n")


if __name__ == "__main__":
    # Bỏ comment dòng dưới để xem demo edge cases trước khi vào menu chính
    # demo_edge_cases()
    main()
