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
| 8 | `make ch08` | `ch08-haha-circuit.png`, `ch08-haha-bloch.png`, `ch08-attempts-error.png`, `ch08-bb84-circuit.png`, `ch08-eavesdropper-error.png` |
| 9 | `make ch09` | `ch09-reversible-circuit.png`, `ch09-oracle-matrices.png`, `ch09-oracle-circuit.png`, `ch09-deutsch-circuit.png`, `ch09-deutsch-outcomes.png`, `ch09-dj-circuit.png`, `ch09-dj-outcomes.png` |
| 10 | `make ch10` | `ch10-classical-tries.png`, `ch10-oracle-matrix.png`, `ch10-step-by-step.png`, `ch10-grover-circuit.png`, `ch10-grover-curve.png`, `ch10-grover-outcomes.png` |
| 11 | `make ch11` | `ch11-classical-factor.png`, `ch11-period-function.png`, `ch11-qft-circuit.png`, `ch11-qft-phase.png`, `ch11-order-circuit.png`, `ch11-order-peaks.png` |

Chương 6 tới 11 đều có nhiều mẫu và chạy tất cả. Muốn chạy riêng một mẫu, gọi
trực tiếp:

```bash
uv run python -m quantum_computing_in_action.ch06.teleportation
uv run python -m quantum_computing_in_action.ch07.full_adder
uv run python -m quantum_computing_in_action.ch08.bb84
uv run python -m quantum_computing_in_action.ch09.deutschjozsa
uv run python -m quantum_computing_in_action.ch10.grover
uv run python -m quantum_computing_in_action.ch11.shor
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
│   ├── ch06/                    # networking, czmeasure, teleportation, repeater, protocol
│   ├── ch07/                    # randombit, debugging, half_adder, full_adder, circuits
│   ├── ch08/                    # protocol, identity, attempts, bb84
│   ├── ch09/                    # reversible, oracles, deutsch, deutschjozsa
│   ├── ch10/                    # search, oracle, step_by_step, grover
│   └── ch11/                    # classical, qft, shor
└── tests/
```

## Ngôn ngữ tài liệu

Ghi chú này có bằng **English** (mặc định) và **Tiếng Việt**. Dùng bộ chọn ngôn
ngữ ở thanh trên cùng; các trang tiếng Việt nằm dưới `/vi/`.
