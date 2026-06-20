# Amazon Inventory Simulator Pro

Hệ thống quản lý kho hàng thông minh, minh họa các kỹ thuật OOP nâng cao
trong Python: Abstract Base Class, Multiple Inheritance & MRO, Duck Typing,
Operator Overloading.

## Cấu trúc thư mục

```
amazon_inventory/
├── main.py                          # Entry point - chương trình CLI chính (menu 1-7)
├── models/
│   ├── __init__.py
│   ├── base_product.py              # BaseProduct (Abstract Base Class)
│   ├── cold_storage_product.py      # ColdStorageProduct (kế thừa BaseProduct)
│   ├── hazardous_product.py         # HazardousProduct (kế thừa BaseProduct)
│   └── hybrid_premium_product.py    # HybridPremiumProduct (đa kế thừa)
├── carriers/
│   ├── __init__.py
│   └── carriers.py                  # FedExCarrier, DHLCarrier, InvalidCarrier (Duck Typing)
├── services/
│   ├── __init__.py
│   └── shipping_service.py          # dispatch_to_carrier() - hàm Duck Typing toàn cục
├── utils/
│   ├── __init__.py
│   └── formatters.py                # Hàm tiện ích: parse số lượng, format hiển thị
└── docs/
    └── DESIGN_DOCUMENT.md           # Phân tích & thiết kế giải pháp
```

## Cách chạy

Yêu cầu Python 3.8+ (không cần cài thêm thư viện ngoài).

```bash
cd amazon_inventory
python3 main.py
```

## Demo nhanh các Edge Cases (không cần nhập liệu tương tác)

Mở `main.py`, bỏ comment dòng `demo_edge_cases()` trong khối `if __name__ == "__main__":`,
hoặc chạy trực tiếp:

```bash
python3 -c "import main; main.demo_edge_cases()"
```

## Tóm tắt kỹ thuật OOP áp dụng

| Kỹ thuật | Vị trí trong code |
|---|---|
| Abstract Base Class | `models/base_product.py` — `BaseProduct(ABC)` |
| Encapsulation (Property) | `BaseProduct.stock_quantity` (get-only) |
| Inheritance + `super()` | `ColdStorageProduct.__init__`, `HazardousProduct.__init__` |
| Multiple Inheritance + MRO | `models/hybrid_premium_product.py` — `HybridPremiumProduct(ColdStorageProduct, HazardousProduct)` |
| Operator Overloading | `BaseProduct.__add__`, `BaseProduct.__lt__` |
| Duck Typing | `carriers/carriers.py` + `services/shipping_service.py` |
| `@staticmethod` | `BaseProduct.validate_product_code` |
| `@classmethod` | `BaseProduct.update_warehouse_name` |

Xem phân tích chi tiết tại `docs/DESIGN_DOCUMENT.md`.
