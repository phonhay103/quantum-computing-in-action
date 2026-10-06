# Bắt đầu

Trang này chỉ nói về cách **chạy các ví dụ** và **vẽ lại sơ đồ**. Muốn hiểu kiến
thức điện toán lượng tử, hãy bắt đầu từ
[Chương 1](chapters/ch01-evolution-revolution-hype.md).

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
uv run python -m quantum_computing_in_action ch04
uv run python -m quantum_computing_in_action ch05
uv run python -m quantum_computing_in_action ch06

# hoặc qua make
make ch01
make ch02
make ch03
make ch04
make ch05
make ch06
```

| Chương | Lệnh | Sơ đồ ghi vào `build/` |
|--------|------|------------------------|
| 1 | `make ch01` | `ch01-time-complexity.png`, `ch01-time-complexity-classical.png` |
| 2 | `make ch02` | `ch02-random-bits-circuit.png`, `ch02-random-bits-counts.png`, `ch02-random-bits-bloch.png` |
| 3 | `make ch03` | `ch03-pauli-x.png`, `ch03-pauli-x2-circuit.png`, `ch03-pauli-x-bloch.png`, `ch03-pauli-x-counts.png`, `ch03-pauli-x2-counts.png` |
| 4 | `make ch04` | `ch04-hadamard-circuit.png`, `ch04-hadamard2-circuit.png`, `ch04-hadamard-bloch.png`, `ch04-hadamard-counts.png`, `ch04-hadamard2-counts.png`, `ch04-gate-matrices.png` |
| 5 | `make ch05` | `ch05-bell-circuit.png`, `ch05-cnot-circuit.png`, `ch05-bell-counts.png`, `ch05-independent-counts.png`, `ch05-bell-vs-independent.png`, `ch05-amplitude-matrices.png` |
| 6 | `make ch06` | `ch06-clone-attempt-circuit.png`, `ch06-clone-fidelity.png`, `ch06-clone-agreement.png`, `ch06-cz-circuit.png`, `ch06-cz-vs-bell.png`, `ch06-cz-matrices.png`, `ch06-teleport-circuit.png`, `ch06-teleport-outcomes.png`, `ch06-teleport-fidelity.png`, `ch06-repeater-circuit.png`, `ch06-repeater-consistency.png`, `ch06-repeater-counts.png` |

Chương 6 có bốn mẫu và chạy tất cả. Muốn chạy riêng một mẫu, gọi trực tiếp:

```bash
uv run python -m quantum_computing_in_action.ch06.teleportation
```

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
│   ├── _diagrams.py             # bộ vẽ mạch / biểu đồ / Bloch / ma trận
│   ├── ch01/time_complexity.py
│   ├── ch02/random_bits.py
│   ├── ch03/pauli_x.py
│   ├── ch04/                    # hadamard.py + matrices.py
│   ├── ch05/                    # entanglement.py + states.py
│   └── ch06/                    # networking, czmeasure, teleportation, repeater, protocol
└── tests/
```

## Ngôn ngữ tài liệu

Ghi chú này có bằng **English** (mặc định) và **Tiếng Việt**. Dùng bộ chọn ngôn
ngữ ở thanh trên cùng; các trang tiếng Việt nằm dưới `/vi/`.
