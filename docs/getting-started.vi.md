# Bắt đầu

Trang này chỉ đề cập đến việc **chạy các ví dụ** và **vẽ lại sơ đồ**. Các
khái niệm điện toán lượng tử được giới thiệu từng bước ngay trong các
chương; để nghiên cứu chúng, cần bắt đầu từ
[Chương 1](chapters/ch01-evolution-revolution-hype.md), chương đặt nền
móng cho toàn bộ các chương về sau.

## Yêu cầu

- [uv](https://docs.astral.sh/uv/) — quản lý cả trình thông dịch Python
  và các gói phụ thuộc của dự án, do đó là công cụ duy nhất cần có sẵn
  trước khi thiết lập
- Python 3.14 (uv tự động cài đặt, vì vậy không cần một bước cài riêng
  nào khác)

Các ví dụ sử dụng [Qiskit](https://www.ibm.com/quantum/qiskit) để dựng và
mô phỏng mạch lượng tử, [matplotlib](https://matplotlib.org/) để vẽ các
hình mà chúng tạo ra, và [Rich](https://github.com/Textualize/rich) để
định dạng đầu ra in ra console.

## Cài đặt

Một lệnh duy nhất chuẩn bị môi trường:

```bash
uv sync
```

Cụ thể, lệnh này tạo một môi trường độc lập, cài Python 3.14 khi phiên
bản đó chưa có sẵn, và tải mọi gói phụ thuộc đã được khai báo trong dự
án.

## Chạy một chương

Mỗi chương tương ứng với một chương trình mẫu độc lập. Khi chương trình
này được thực thi, nó in ra một phần giải thích ngắn về khái niệm đang
được minh họa, bảng phân tích từng bước quá trình dựng mạch, kết quả số
của mô phỏng, và đường dẫn của các tệp sơ đồ đã được ghi ra. Chương
trình có thể được gọi qua giao diện module hoặc qua mục tiêu make tương
ứng:

```bash
# qua module
uv run python -m quantum_computing_in_action ch01
uv run python -m quantum_computing_in_action ch02
uv run python -m quantum_computing_in_action ch03
uv run python -m quantum_computing_in_action ch04
uv run python -m quantum_computing_in_action ch05
uv run python -m quantum_computing_in_action ch06
uv run python -m quantum_computing_in_action ch07
uv run python -m quantum_computing_in_action ch08
uv run python -m quantum_computing_in_action ch09
uv run python -m quantum_computing_in_action ch10
uv run python -m quantum_computing_in_action ch11

# hoặc qua make
make ch01
make ch02
make ch03
make ch04
make ch05
make ch06
make ch07
make ch08
make ch09
make ch10
make ch11
```

| Chương | Lệnh | Sơ đồ ghi vào `build/` |
|--------|------|------------------------|
| 1 | `make ch01` | `ch01-time-complexity.png`, `ch01-time-complexity-classical.png` |
| 2 | `make ch02` | `ch02-random-bits-circuit.png`, `ch02-random-bits-counts.png`, `ch02-random-bits-bloch.png` |
| 3 | `make ch03` | `ch03-pauli-x.png`, `ch03-pauli-x2-circuit.png`, `ch03-pauli-x-bloch.png`, `ch03-pauli-x-counts.png`, `ch03-pauli-x2-counts.png` |
| 4 | `make ch04` | `ch04-hadamard-circuit.png`, `ch04-hadamard2-circuit.png`, `ch04-hadamard-bloch.png`, `ch04-hadamard-counts.png`, `ch04-hadamard2-counts.png`, `ch04-gate-matrices.png` |
| 5 | `make ch05` | `ch05-bell-circuit.png`, `ch05-cnot-circuit.png`, `ch05-bell-counts.png`, `ch05-independent-counts.png`, `ch05-bell-vs-independent.png`, `ch05-amplitude-matrices.png` |
| 6 | `make ch06` | `ch06-clone-attempt-circuit.png`, `ch06-clone-fidelity.png`, `ch06-clone-agreement.png`, `ch06-cz-circuit.png`, `ch06-cz-vs-bell.png`, `ch06-cz-matrices.png`, `ch06-teleport-circuit.png`, `ch06-teleport-outcomes.png`, `ch06-teleport-fidelity.png`, `ch06-repeater-circuit.png`, `ch06-repeater-consistency.png`, `ch06-repeater-counts.png` |
| 7 | `make ch07` | `ch07-randombit-circuit.png`, `ch07-randombit-counts.png`, `ch07-randombit-qubits.png`, `ch07-debug-circuit.png`, `ch07-debug-steps.png`, `ch07-debug-marginals.png`, `ch07-add1-circuit.png`, `ch07-add2-circuit.png`, `ch07-toffoli-matrices.png`, `ch07-adder-comparison.png` |
| 8 | `make ch08` | `ch08-haha-circuit.png`, `ch08-haha-bloch.png`, `ch08-attempts-error.png`, `ch08-superposition-circuit.png`, `ch08-superposition-states.png`, `ch08-bb84-circuit.png`, `ch08-eavesdropper-error.png` |
| 9 | `make ch09` | `ch09-reversible-circuit.png`, `ch09-oracle-matrices.png`, `ch09-oracle-circuit.png`, `ch09-deutsch-circuit.png`, `ch09-deutsch-outcomes.png`, `ch09-dj-circuit.png`, `ch09-dj-outcomes.png` |
| 10 | `make ch10` | `ch10-classical-tries.png`, `ch10-oracle-matrix.png`, `ch10-step-by-step.png`, `ch10-grover-circuit.png`, `ch10-grover-curve.png`, `ch10-grover-outcomes.png` |
| 11 | `make ch11` | `ch11-classical-factor.png`, `ch11-period-function.png`, `ch11-qft-circuit.png`, `ch11-qft-phase.png`, `ch11-order-circuit.png`, `ch11-order-peaks.png` |

Chương 6 tới 11 mỗi chương đều gồm nhiều mẫu, và việc chạy toàn bộ chương
sẽ thực thi tất cả các mẫu đó lần lượt; do đó, một mẫu đơn lẻ có thể được
xem xét riêng khi gọi trực tiếp module của nó:

```bash
uv run python -m quantum_computing_in_action.ch06.teleportation
uv run python -m quantum_computing_in_action.ch07.full_adder
uv run python -m quantum_computing_in_action.ch08.bb84
uv run python -m quantum_computing_in_action.ch09.deutschjozsa
uv run python -m quantum_computing_in_action.ch10.grover
uv run python -m quantum_computing_in_action.ch11.shor
```

## Phát triển

Makefile cung cấp các tác vụ phát triển thông dụng; mỗi mục tiêu bao bọc
một công cụ duy nhất để tác vụ đó được thực hiện một cách nhất quán:

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

Kho mã tuân theo cấu trúc dự án Python thông thường; sơ đồ dưới đây mô
tả vai trò của từng thư mục và từng tệp:

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
│   ├── ch06/                    # networking, czmeasure, teleportation, repeater, protocol
│   ├── ch07/                    # randombit, debugging, half_adder, full_adder, circuits
│   ├── ch08/                    # protocol, identity, attempts, superposition, bb84
│   ├── ch09/                    # reversible, oracles, deutsch, deutschjozsa
│   ├── ch10/                    # search, oracle, step_by_step, grover
│   └── ch11/                    # classical, qft, shor
└── tests/
```

## Ngôn ngữ tài liệu

Ghi chú này được duy trì bằng **English** (mặc định) và **Tiếng Việt**.
Bộ chọn ngôn ngữ ở thanh trên cùng cho phép chuyển đổi giữa hai bản; các
trang tiếng Việt được phục vụ dưới đường dẫn `/vi/`, và mỗi trang bằng
một ngôn ngữ tương ứng chính xác với đúng một trang bằng ngôn ngữ kia.
