# Bắt đầu

Trang này chỉ nói về cách **chạy các ví dụ** và **vẽ lại sơ đồ**. Muốn hiểu kiến
thức điện toán lượng tử, hãy bắt đầu từ
[Chương 1](chapters/ch01-time-complexity.md).

## Yêu cầu

- [uv](https://docs.astral.sh/uv/) — quản lý Python và các gói phụ thuộc
- Python 3.14 (uv tự động cài)

Các ví dụ dùng [Qiskit](https://www.ibm.com/quantum/qiskit) để dựng mạch,
[matplotlib](https://matplotlib.org/) để vẽ hình, và
[Rich](https://github.com/Textualize/rich) để in ra console.

## Cài đặt

```bash
uv sync
```

## Chạy một chương

Mỗi chương in ra phần giải thích ngắn, bảng từng bước, kết quả số, và đường dẫn
các sơ đồ đã lưu.

```bash
# qua module
uv run python -m quantum_computing_in_action ch01
uv run python -m quantum_computing_in_action ch02
uv run python -m quantum_computing_in_action ch03

# hoặc qua make
make ch01
make ch02
make ch03
```

| Chương | Lệnh | Sơ đồ ghi vào `build/` |
|--------|------|------------------------|
| 1 | `make ch01` | `ch01-time-complexity.png` |
| 2 | `make ch02` | `ch02-random-bits-circuit.png`, `ch02-random-bits-counts.png`, `ch02-random-bits-bloch.png` |
| 3 | `make ch03` | `ch03-pauli-x.png`, `ch03-pauli-x-bloch.png` |

## Phát triển

```bash
make sync       # cài phụ thuộc
make lint       # ruff + ty
make format     # định dạng bằng ruff
make test       # pytest
make docs       # dựng trang tài liệu này vào site/
make docs-serve # xem trước tài liệu tại http://127.0.0.1:8000
make clean      # xoá cache và sản phẩm đã sinh
```

## Cấu trúc dự án

```
.
├── Makefile
├── pyproject.toml
├── mkdocs.yml
├── build/                       # sơ đồ đã sinh (được commit)
├── docs/                        # trang tài liệu này
│   └── assets/                  # sơ đồ được sao chép vào đây khi dựng docs
├── src/quantum_computing_in_action/
│   ├── __main__.py              # CLI: python -m quantum_computing_in_action <chapter>
│   ├── _console.py              # giao diện console tối dùng chung
│   ├── _diagrams.py             # bộ vẽ mạch / biểu đồ / Bloch
│   ├── ch01/time_complexity.py
│   ├── ch02/random_bits.py
│   └── ch03/pauli_x.py
└── tests/
```

## Ngôn ngữ tài liệu

Ghi chú này có bằng **English** (mặc định) và **Tiếng Việt**. Dùng bộ chọn ngôn
ngữ ở thanh trên cùng; các trang tiếng Việt nằm dưới `/vi/`.
