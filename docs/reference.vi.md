# Tham chiếu

Bảng tra nhanh từ mỗi chương tới module mã nguồn, lệnh CLI và các sơ đồ. Liên kết
module trỏ tới mã; muốn hiểu *khái niệm*, hãy theo liên kết chương.

## Các chương trong nháy mắt

| Chương | Chủ đề | Module mã nguồn | Lệnh |
|--------|--------|-----------------|------|
| [1](chapters/ch01-time-complexity.md) | Độ phức tạp thời gian phân tích thừa số | [`ch01/time_complexity.py`](https://github.com/phonhay103/quantum-computing-in-action/blob/main/src/quantum_computing_in_action/ch01/time_complexity.py) | `make ch01` |
| [2](chapters/ch02-random-bits.md) | Bit ngẫu nhiên từ chồng chập | [`ch02/random_bits.py`](https://github.com/phonhay103/quantum-computing-in-action/blob/main/src/quantum_computing_in_action/ch02/random_bits.py) | `make ch02` |
| [3](chapters/ch03-pauli-x.md) | Cổng Pauli-X | [`ch03/pauli_x.py`](https://github.com/phonhay103/quantum-computing-in-action/blob/main/src/quantum_computing_in_action/ch03/pauli_x.py) | `make ch03` |
| [4](chapters/ch04-hadamard.md) | Cổng Hadamard | [`ch04/hadamard.py`](https://github.com/phonhay103/quantum-computing-in-action/blob/main/src/quantum_computing_in_action/ch04/hadamard.py) | `make ch04` |

CLI nhận id của chương:

```bash
uv run python -m quantum_computing_in_action ch01
uv run python -m quantum_computing_in_action ch02
uv run python -m quantum_computing_in_action ch03
```

## Các tệp sơ đồ

Mọi sơ đồ được ghi vào `build/` và có tiền tố là số chương để một hình luôn cho
biết nó đến từ đâu.

| Sơ đồ | Chương | Thể hiện |
|-------|--------|----------|
| `ch01-time-complexity.png` | 1 | Đường cong thời gian phân tích thừa số cổ điển so với Shor |
| `ch02-random-bits-circuit.png` | 2 | Mạch: `H` rồi đo |
| `ch02-random-bits-counts.png` | 2 | Biểu đồ 10.000 bit đo được |
| `ch02-random-bits-bloch.png` | 2 | Chồng chập trên mặt cầu Bloch |
| `ch03-pauli-x.png` | 3 | Mạch: `X` rồi đo |
| `ch03-pauli-x-bloch.png` | 3 | Qubit trước và sau khi lật |
| `ch04-hadamard-circuit.png` | 4 | Mạch: một `H` rồi đo |
| `ch04-hadamard2-circuit.png` | 4 | Mạch: `H`, `H`, rồi đo |
| `ch04-hadamard-bloch.png` | 4 | (\|0⟩ → sau `H` → sau `H·H`) |
| `ch04-hadamard-counts.png` | 4 | Biểu đồ 1000 lần chạy `H` |
| `ch04-hadamard2-counts.png` | 4 | Biểu đồ 1000 lần chạy `H·H` (toàn `0`) |

## Ký hiệu dùng trong ghi chú

| Ký hiệu | Ý nghĩa |
|---------|---------|
| `\|0⟩`, `\|1⟩` | Hai trạng thái cơ sở của qubit |
| `(a\|0⟩ + b\|1⟩)` | Chồng chập với biên độ `a` và `b` |
| `H` | Cổng Hadamard — tạo chồng chập đều |
| `X` | Cổng Pauli-X — lật `\|0⟩ ↔ \|1⟩` |
| `P(0)`, `P(1)` | Xác suất đo (quy tắc Born: biên độ bình phương) |
| Mặt cầu Bloch | Hình học mô tả trạng thái của một qubit |
