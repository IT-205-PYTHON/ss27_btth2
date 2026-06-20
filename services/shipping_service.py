"""
shipping_service.py
---------------------
Chứa hàm toàn cục dispatch_to_carrier(carrier_agent, product, quantity).

Đây là "trái tim" của minh họa Duck Typing: hàm này không kiểm tra
isinstance(carrier_agent, SomeBaseCarrier) - nó chỉ cố gắng GỌI
carrier_agent.ship_package(...) và bắt lỗi nếu phương thức đó không
tồn tại (Edge case - Bẫy 4: AttributeError).
"""


def dispatch_to_carrier(carrier_agent, product, quantity):
    """
    Điều phối vận chuyển một lô hàng qua đối tác thứ ba bất kỳ.

    Tham số:
        carrier_agent: bất kỳ object nào, miễn là có method
                        ship_package(product, quantity)
        product: đối tượng hàng hóa (BaseProduct hoặc lớp con)
        quantity: số lượng hàng hóa bàn giao

    Edge case (Bẫy 4): nếu carrier_agent không có ship_package(),
    bắt AttributeError và thông báo "Đơn vị vận chuyển không hợp lệ
    hoặc chưa ký kết hợp đồng kỹ thuật".
    """
    try:
        carrier_agent.ship_package(product, quantity)
        print("Xác thực đối tác bằng Duck Typing thành công!")
        print(f"Đơn vị vận chuyển đã tiếp nhận đơn hàng số lượng: {quantity:g} đơn vị.")
        print(f"Số lượng tồn kho cập nhật: {product.stock_quantity:g} đơn vị.")
        return True
    except AttributeError:
        print("Lỗi: Đơn vị vận chuyển không hợp lệ hoặc chưa ký kết hợp đồng kỹ thuật.")
        return False
    except ValueError as e:
        print(f"Lỗi giao dịch: {e}")
        return False
