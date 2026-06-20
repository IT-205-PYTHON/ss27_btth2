"""
formatters.py
--------------
Các hàm tiện ích dùng chung: parse số lượng có dấu phẩy phân cách,
format hiển thị VND/đơn vị, đọc input an toàn từ người dùng (CLI).
"""


def parse_quantity(raw_text):
    """
    Chuyển chuỗi nhập từ người dùng (vd: "1,000" hoặc "50") thành float.
    Raise ValueError nếu không phải số hợp lệ.
    """
    cleaned = raw_text.replace(",", "").strip()
    try:
        return float(cleaned)
    except ValueError:
        raise ValueError("Số lượng nhập vào không hợp lệ.")


def format_vnd(amount):
    """Format số tiền dạng 10,000,000 VND."""
    return f"{amount:,.0f} VND"


def format_unit(quantity):
    """Format số lượng dạng '50 đơn vị' hoặc '52.5 đơn vị' (bỏ .0 nếu là số nguyên)."""
    return f"{quantity:g} đơn vị"


def safe_input(prompt):
    """Đọc input, loại bỏ khoảng trắng thừa hai đầu."""
    return input(prompt).strip()
