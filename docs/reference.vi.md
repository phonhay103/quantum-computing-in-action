# Tham chiếu

Bảng tra nhanh từ mỗi chương tới module mã nguồn, lệnh CLI và các sơ đồ. Liên kết
module trỏ tới mã; muốn hiểu *khái niệm*, hãy theo liên kết chương.

## Các chương trong nháy mắt

| Chương | Chủ đề (tên trong sách) | Module mã nguồn | Lệnh |
|--------|-------------------------|-----------------|------|
| [1](chapters/ch01-evolution-revolution-hype.md) | Tiến hoá, cách mạng, hay cường điệu? | [`ch01/time_complexity.py`](https://github.com/phonhay103/quantum-computing-in-action/blob/main/src/quantum_computing_in_action/ch01/time_complexity.py) | `make ch01` |
| [2](chapters/ch02-hello-world.md) | Hello World kiểu điện toán lượng tử | [`ch02/random_bits.py`](https://github.com/phonhay103/quantum-computing-in-action/blob/main/src/quantum_computing_in_action/ch02/random_bits.py) | `make ch02` |
| [3](chapters/ch03-qubits-and-gates.md) | Qubit và cổng lượng tử | [`ch03/pauli_x.py`](https://github.com/phonhay103/quantum-computing-in-action/blob/main/src/quantum_computing_in_action/ch03/pauli_x.py) | `make ch03` |
| [4](chapters/ch04-superposition.md) | Chồng chập | [`ch04/hadamard.py`](https://github.com/phonhay103/quantum-computing-in-action/blob/main/src/quantum_computing_in_action/ch04/hadamard.py), [`ch04/matrices.py`](https://github.com/phonhay103/quantum-computing-in-action/blob/main/src/quantum_computing_in_action/ch04/matrices.py) | `make ch04` |
| [5](chapters/ch05-entanglement.md) | Rối lượng tử | [`ch05/entanglement.py`](https://github.com/phonhay103/quantum-computing-in-action/blob/main/src/quantum_computing_in_action/ch05/entanglement.py), [`ch05/states.py`](https://github.com/phonhay103/quantum-computing-in-action/blob/main/src/quantum_computing_in_action/ch05/states.py) | `make ch05` |
| [6](chapters/ch06-quantum-networking.md) | Mạng lượng tử: những điều cơ bản | [`ch06/networking.py`](https://github.com/phonhay103/quantum-computing-in-action/blob/main/src/quantum_computing_in_action/ch06/networking.py), [`ch06/czmeasure.py`](https://github.com/phonhay103/quantum-computing-in-action/blob/main/src/quantum_computing_in_action/ch06/czmeasure.py), [`ch06/teleportation.py`](https://github.com/phonhay103/quantum-computing-in-action/blob/main/src/quantum_computing_in_action/ch06/teleportation.py), [`ch06/repeater.py`](https://github.com/phonhay103/quantum-computing-in-action/blob/main/src/quantum_computing_in_action/ch06/repeater.py), [`ch06/protocol.py`](https://github.com/phonhay103/quantum-computing-in-action/blob/main/src/quantum_computing_in_action/ch06/protocol.py) | `make ch06` |
| [7](chapters/ch07-helloworld-explained.md) | HelloWorld của chúng ta, giải thích | — | dự kiến |
| [8](chapters/ch08-secure-communication.md) | Truyền thông an toàn bằng điện toán lượng tử | — | dự kiến |
| [9](chapters/ch09-deutsch-jozsa.md) | Thuật toán Deutsch–Jozsa | — | dự kiến |
| [10](chapters/ch10-grovers-search.md) | Thuật toán tìm kiếm của Grover | — | dự kiến |
| [11](chapters/ch11-shors-algorithm.md) | Thuật toán Shor | — | dự kiến |

CLI nhận id của chương:

```bash
uv run python -m quantum_computing_in_action ch01
uv run python -m quantum_computing_in_action ch02
uv run python -m quantum_computing_in_action ch03
uv run python -m quantum_computing_in_action ch04
uv run python -m quantum_computing_in_action ch05
uv run python -m quantum_computing_in_action ch06
```

## Các tệp sơ đồ

Mọi sơ đồ được ghi vào `build/` và có tiền tố là số chương để một hình luôn cho
biết nó đến từ đâu.

| Sơ đồ | Chương | Thể hiện |
|-------|--------|----------|
| `ch01-time-complexity.png` | 1 | Đường cong thời gian phân tích thừa số cổ điển so với Shor |
| `ch01-time-complexity-classical.png` | 1 | Đường cổ điển riêng lẻ |
| `ch02-random-bits-circuit.png` | 2 | Mạch: `H` rồi đo |
| `ch02-random-bits-counts.png` | 2 | Biểu đồ 10.000 bit đo được |
| `ch02-random-bits-bloch.png` | 2 | Chồng chập trên mặt cầu Bloch |
| `ch03-pauli-x.png` | 3 | Mạch: `X` rồi đo |
| `ch03-pauli-x2-circuit.png` | 3 | Mạch: `X`, `X`, rồi đo |
| `ch03-pauli-x-bloch.png` | 3 | (\|0⟩ → sau `X` → sau `X·X`) |
| `ch03-pauli-x-counts.png` | 3 | Biểu đồ 1000 lần chạy `X` (toàn `1`) |
| `ch03-pauli-x2-counts.png` | 3 | Biểu đồ 1000 lần chạy `X·X` (toàn `0`) |
| `ch04-hadamard-circuit.png` | 4 | Mạch: một `H` rồi đo |
| `ch04-hadamard2-circuit.png` | 4 | Mạch: `H`, `H`, rồi đo |
| `ch04-hadamard-bloch.png` | 4 | (\|0⟩ → sau `H` → sau `H·H`) |
| `ch04-hadamard-counts.png` | 4 | Biểu đồ 1000 lần chạy `H` |
| `ch04-hadamard2-counts.png` | 4 | Biểu đồ 1000 lần chạy `H·H` (toàn `0`) |
| `ch04-gate-matrices.png` | 4 | Ma trận `X`, `H` và `H·H` dưới dạng heatmap |
| `ch05-bell-circuit.png` | 5 | Mạch: `H`, `CNOT`, rồi đo cả hai qubit |
| `ch05-cnot-circuit.png` | 5 | Mạch: `CNOT(0,1)` trần |
| `ch05-bell-counts.png` | 5 | Biểu đồ 1000 lần chạy trạng thái Bell (chỉ `00`, `11`) |
| `ch05-independent-counts.png` | 5 | Biểu đồ 1000 lần chạy hai qubit `H` độc lập |
| `ch05-bell-vs-independent.png` | 5 | Cột nhóm: kết quả độc lập so với rối |
| `ch05-amplitude-matrices.png` | 5 | Ma trận hệ số: trạng thái tích (hạng 1) so với Bell (hạng 2) |
| `ch06-clone-attempt-circuit.png` | 6 | Mạch: `H` rồi `CNOT`, cách thử nhân bản thất bại |
| `ch06-clone-fidelity.png` | 6 | Độ trung thành của bản sao bằng `CNOT` theo từng trạng thái đầu vào |
| `ch06-clone-agreement.png` | 6 | Nhân bản `\|+>`: hai bản độc lập so với cách thử tương quan bằng `CNOT` |
| `ch06-cz-circuit.png` | 6 | Mạch: `H` rồi `CZ`, rồi đo |
| `ch06-cz-vs-bell.png` | 6 | `CZ` rối cặp qubit mà không đổi xác suất nào |
| `ch06-cz-matrices.png` | 6 | Ma trận hệ số: một dấu đổi đưa hạng từ 1 lên 2 |
| `ch06-teleport-circuit.png` | 6 | Teleportation: cặp Bell, đo kiểu Bell, phép sửa `If X` / `If Z` |
| `ch06-teleport-outcomes.png` | 6 | Kết quả của Bob theo trạng thái Alice gửi, gắn với tin nhắn |
| `ch06-teleport-fidelity.png` | 6 | Mọi tin nhắn đều dựng lại trạng thái chính xác |
| `ch06-repeater-circuit.png` | 6 | Hai mắt xích nối qua năm qubit và bốn bit cổ điển |
| `ch06-repeater-consistency.png` | 6 | P(1) khởi đầu của Alice so với P(0) Bob nhận được |
| `ch06-repeater-counts.png` | 6 | Gửi P(1) = 0.4 qua nút trung gian: kỳ vọng so với đo được |

## Ký hiệu dùng trong ghi chú

| Ký hiệu | Ý nghĩa |
|---------|---------|
| <code>\|0⟩</code>, <code>\|1⟩</code> | Hai trạng thái cơ sở của qubit |
| <code>\|ψ⟩</code> | Trạng thái một-qubit tổng quát (bất kỳ) |
| <code>\|+⟩</code>, <code>\|−⟩</code> | Hai chồng chập đều <code>(\|0⟩ ± \|1⟩)/√2</code> |
| <code>(a\|0⟩ + b\|1⟩)</code> | Chồng chập với biên độ `a` và `b` |
| `[α, β]` | Cùng trạng thái đó viết dưới dạng vector cột |
| `H` | Cổng Hadamard — tạo chồng chập đều |
| `X` | Cổng Pauli-X — lật <code>\|0⟩ ↔ \|1⟩</code> |
| `CNOT` | Controlled-NOT — lật đích khi điều khiển bằng `1` |
| `Z` | Cổng Pauli-Z — lật **pha** mà không đổi bit |
| `CZ` | Controlled-Z — áp dụng `Z` lên đích khi điều khiển bằng `1` |
| `⊗` | Tích tensor — ghép các qubit thành trạng thái chung |
| Trạng thái Bell | Cặp rối cực đại, ví dụ <code>(\|00⟩ + \|11⟩)/√2</code> |
| `I` | Phép đơn vị — "không làm gì" |
| `U` | Cổng tổng quát, viết dưới dạng ma trận 2×2 |
| `P(0)`, `P(1)` | Xác suất đo (quy tắc Born: biên độ bình phương) |
| Mặt cầu Bloch | Hình học mô tả trạng thái của một qubit |
| Độ trung thành | Độ chồng lấn của hai trạng thái, <code>\|⟨a\|b⟩\|²</code>; bằng 1 nghĩa là giống hệt |
| Hạng Schmidt | 1 = trạng thái tích, 2 = rối (xem [ma trận hệ số](chapters/ch05-entanglement.md#trang-thai-tich-so-voi-trang-thai-roi)) |
