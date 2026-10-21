# Tham chiếu

Tham chiếu này cung cấp một bản đồ hệ thống từ mỗi chương của sách tới module mã
nguồn tương ứng, lệnh khi thực thi module đó, và các sơ đồ được sinh ra trong
quá trình chạy. Nó được thiết kế để tra cứu song song với nội dung các chương:
liên kết module trỏ trực tiếp tới mã triển khai, còn phần *khái niệm* đằng sau
mỗi chương trình được trình bày trên trang chương, cần theo liên kết chương để
có phần giải thích khái niệm đầy đủ.

## Các chương trong nháy mắt

| Chương | Chủ đề (tên trong sách) | Module mã nguồn | Lệnh |
|--------|-------------------------|-----------------|------|
| [1](chapters/ch01-evolution-revolution-hype.md) | Tiến hoá, cách mạng, hay cường điệu? | [`ch01/time_complexity.py`](https://github.com/phonhay103/quantum-computing-in-action/blob/main/src/quantum_computing_in_action/ch01/time_complexity.py) | `make ch01` |
| [2](chapters/ch02-hello-world.md) | Hello World kiểu điện toán lượng tử | [`ch02/random_bits.py`](https://github.com/phonhay103/quantum-computing-in-action/blob/main/src/quantum_computing_in_action/ch02/random_bits.py) | `make ch02` |
| [3](chapters/ch03-qubits-and-gates.md) | Qubit và cổng lượng tử | [`ch03/pauli_x.py`](https://github.com/phonhay103/quantum-computing-in-action/blob/main/src/quantum_computing_in_action/ch03/pauli_x.py) | `make ch03` |
| [4](chapters/ch04-superposition.md) | Chồng chập | [`ch04/hadamard.py`](https://github.com/phonhay103/quantum-computing-in-action/blob/main/src/quantum_computing_in_action/ch04/hadamard.py), [`ch04/matrices.py`](https://github.com/phonhay103/quantum-computing-in-action/blob/main/src/quantum_computing_in_action/ch04/matrices.py) | `make ch04` |
| [5](chapters/ch05-entanglement.md) | Rối lượng tử | [`ch05/entanglement.py`](https://github.com/phonhay103/quantum-computing-in-action/blob/main/src/quantum_computing_in_action/ch05/entanglement.py), [`ch05/states.py`](https://github.com/phonhay103/quantum-computing-in-action/blob/main/src/quantum_computing_in_action/ch05/states.py) | `make ch05` |
| [6](chapters/ch06-quantum-networking.md) | Mạng lượng tử: những điều cơ bản | [`ch06/networking.py`](https://github.com/phonhay103/quantum-computing-in-action/blob/main/src/quantum_computing_in_action/ch06/networking.py), [`ch06/czmeasure.py`](https://github.com/phonhay103/quantum-computing-in-action/blob/main/src/quantum_computing_in_action/ch06/czmeasure.py), [`ch06/teleportation.py`](https://github.com/phonhay103/quantum-computing-in-action/blob/main/src/quantum_computing_in_action/ch06/teleportation.py), [`ch06/repeater.py`](https://github.com/phonhay103/quantum-computing-in-action/blob/main/src/quantum_computing_in_action/ch06/repeater.py), [`ch06/protocol.py`](https://github.com/phonhay103/quantum-computing-in-action/blob/main/src/quantum_computing_in_action/ch06/protocol.py) | `make ch06` |
| [7](chapters/ch07-helloworld-explained.md) | HelloWorld của chúng ta, giải thích | [`ch07/randombit.py`](https://github.com/phonhay103/quantum-computing-in-action/blob/main/src/quantum_computing_in_action/ch07/randombit.py), [`ch07/debugging.py`](https://github.com/phonhay103/quantum-computing-in-action/blob/main/src/quantum_computing_in_action/ch07/debugging.py), [`ch07/half_adder.py`](https://github.com/phonhay103/quantum-computing-in-action/blob/main/src/quantum_computing_in_action/ch07/half_adder.py), [`ch07/full_adder.py`](https://github.com/phonhay103/quantum-computing-in-action/blob/main/src/quantum_computing_in_action/ch07/full_adder.py), [`ch07/circuits.py`](https://github.com/phonhay103/quantum-computing-in-action/blob/main/src/quantum_computing_in_action/ch07/circuits.py) | `make ch07` |
| [8](chapters/ch08-secure-communication.md) | Truyền thông an toàn bằng điện toán lượng tử | [`ch08/protocol.py`](https://github.com/phonhay103/quantum-computing-in-action/blob/main/src/quantum_computing_in_action/ch08/protocol.py), [`ch08/identity.py`](https://github.com/phonhay103/quantum-computing-in-action/blob/main/src/quantum_computing_in_action/ch08/identity.py), [`ch08/attempts.py`](https://github.com/phonhay103/quantum-computing-in-action/blob/main/src/quantum_computing_in_action/ch08/attempts.py), [`ch08/superposition.py`](https://github.com/phonhay103/quantum-computing-in-action/blob/main/src/quantum_computing_in_action/ch08/superposition.py), [`ch08/bb84.py`](https://github.com/phonhay103/quantum-computing-in-action/blob/main/src/quantum_computing_in_action/ch08/bb84.py) | `make ch08` |
| [9](chapters/ch09-deutsch-jozsa.md) | Thuật toán Deutsch–Jozsa | [`ch09/reversible.py`](https://github.com/phonhay103/quantum-computing-in-action/blob/main/src/quantum_computing_in_action/ch09/reversible.py), [`ch09/oracles.py`](https://github.com/phonhay103/quantum-computing-in-action/blob/main/src/quantum_computing_in_action/ch09/oracles.py), [`ch09/deutsch.py`](https://github.com/phonhay103/quantum-computing-in-action/blob/main/src/quantum_computing_in_action/ch09/deutsch.py), [`ch09/deutschjozsa.py`](https://github.com/phonhay103/quantum-computing-in-action/blob/main/src/quantum_computing_in_action/ch09/deutschjozsa.py) | `make ch09` |
| [10](chapters/ch10-grovers-search.md) | Thuật toán tìm kiếm của Grover | [`ch10/search.py`](https://github.com/phonhay103/quantum-computing-in-action/blob/main/src/quantum_computing_in_action/ch10/search.py), [`ch10/oracle.py`](https://github.com/phonhay103/quantum-computing-in-action/blob/main/src/quantum_computing_in_action/ch10/oracle.py), [`ch10/step_by_step.py`](https://github.com/phonhay103/quantum-computing-in-action/blob/main/src/quantum_computing_in_action/ch10/step_by_step.py), [`ch10/grover.py`](https://github.com/phonhay103/quantum-computing-in-action/blob/main/src/quantum_computing_in_action/ch10/grover.py) | `make ch10` |
| [11](chapters/ch11-shors-algorithm.md) | Thuật toán Shor | [`ch11/classical.py`](https://github.com/phonhay103/quantum-computing-in-action/blob/main/src/quantum_computing_in_action/ch11/classical.py), [`ch11/qft.py`](https://github.com/phonhay103/quantum-computing-in-action/blob/main/src/quantum_computing_in_action/ch11/qft.py), [`ch11/shor.py`](https://github.com/phonhay103/quantum-computing-in-action/blob/main/src/quantum_computing_in_action/ch11/shor.py) | `make ch11` |

Giao diện dòng lệnh đi kèm nhận id của chương làm đối số. Khi được gọi với một
id chương cụ thể, CLI thực thi chương trình mẫu của chương đó và tạo ra các kết
quả cùng hình vẽ tương ứng:

```bash
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
```

## Các tệp sơ đồ

Mọi sơ đồ do các chương trình mẫu sinh ra đều được ghi vào thư mục `build/` và
có tiền tố là số chương, nhờ đó mỗi hình riêng lẻ luôn có thể được truy ngược về
chương và chương trình đã tạo ra nó. Bảng dưới đây liệt kê từng tệp sinh ra kèm
với phần mô tả nội dung mà hình đó thể hiện.

| Sơ đồ | Chương | Thể hiện |
|-------|--------|----------|
| `ch01-time-complexity.png` | 1 | Đường cong thời gian phân tích thừa số của cách tiếp cận cổ điển so với cách dựa trên thuật toán Shor, đặt cạnh nhau |
| `ch01-time-complexity-classical.png` | 1 | Đường cong thời gian cổ điển, vẽ riêng lẻ |
| `ch02-random-bits-circuit.png` | 2 | Sơ đồ mạch: một cổng `H` duy nhất rồi đến phép đo |
| `ch02-random-bits-counts.png` | 2 | Biểu đồ 10.000 bit đo được, cho thấy hai kết quả xuất hiện với tần suất gần bằng nhau |
| `ch02-random-bits-bloch.png` | 2 | Chồng chập thu được, hiển thị trên mặt cầu Bloch |
| `ch03-pauli-x.png` | 3 | Sơ đồ mạch: một cổng `X` duy nhất rồi đến phép đo |
| `ch03-pauli-x2-circuit.png` | 3 | Sơ đồ mạch: hai cổng `X` liên tiếp rồi đến phép đo |
| `ch03-pauli-x-bloch.png` | 3 | Quá trình biến đổi trạng thái <code>\|0⟩</code> → sau `X` → sau `X·X`, được theo dõi theo từng bước |
| `ch03-pauli-x-counts.png` | 3 | Biểu đồ 1000 lần chạy `X` (mọi lần đều cho kết quả `1`) |
| `ch03-pauli-x2-counts.png` | 3 | Biểu đồ 1000 lần chạy `X·X` (mọi lần đều cho kết quả `0`) |
| `ch04-hadamard-circuit.png` | 4 | Sơ đồ mạch: một cổng `H` duy nhất rồi đến phép đo |
| `ch04-hadamard2-circuit.png` | 4 | Sơ đồ mạch: hai cổng `H` liên tiếp rồi đến phép đo |
| `ch04-hadamard-bloch.png` | 4 | Quá trình biến đổi trạng thái <code>\|0⟩</code> → sau `H` → sau `H·H`, được theo dõi theo từng bước |
| `ch04-hadamard-counts.png` | 4 | Biểu đồ 1000 lần chạy `H`, cho thấy hai kết quả đo được |
| `ch04-hadamard2-counts.png` | 4 | Biểu đồ 1000 lần chạy `H·H` (mọi lần đều cho kết quả `0`) |
| `ch04-gate-matrices.png` | 4 | Các ma trận của `X`, `H` và `H·H`, được vẽ dưới dạng heatmap |
| `ch05-bell-circuit.png` | 5 | Sơ đồ mạch: `H`, `CNOT`, rồi đến phép đo cả hai qubit |
| `ch05-cnot-circuit.png` | 5 | Sơ đồ mạch: một `CNOT(0,1)` trần, áp dụng mà không có bước chuẩn bị thêm nào |
| `ch05-bell-counts.png` | 5 | Biểu đồ 1000 lần chạy trạng thái Bell (chỉ có các kết quả `00` và `11` xuất hiện) |
| `ch05-independent-counts.png` | 5 | Biểu đồ 1000 lần chạy hai qubit, mỗi qubit đi qua cổng `H` độc lập của riêng nó |
| `ch05-bell-vs-independent.png` | 5 | Biểu đồ cột nhóm: kết quả của trường hợp độc lập so với trường hợp rối |
| `ch05-amplitude-matrices.png` | 5 | Ma trận hệ số: trạng thái tích (hạng 1) đặt cạnh trạng thái Bell (hạng 2) |
| `ch06-clone-attempt-circuit.png` | 6 | Sơ đồ mạch: `H` rồi `CNOT`, thể hiện cách thử nhân bản thất bại |
| `ch06-clone-fidelity.png` | 6 | Độ trung thực của bản sao bằng `CNOT`, được đánh giá cho từng trạng thái đầu vào khả dĩ |
| `ch06-clone-agreement.png` | 6 | Nhân bản `\|+⟩`: hai bản sao độc lập đặt cạnh cách thử tương quan bằng `CNOT` |
| `ch06-cz-circuit.png` | 6 | Sơ đồ mạch: `H`, rồi `CZ`, rồi đến phép đo |
| `ch06-cz-vs-bell.png` | 6 | Chứng minh rằng `CZ` khiến cặp qubit rối mà không làm thay đổi xác suất đo nào |
| `ch06-cz-matrices.png` | 6 | Ma trận hệ số: một lần đổi dấu duy nhất đưa hạng từ 1 lên 2 |
| `ch06-teleport-circuit.png` | 6 | Giao thức teleportation: một cặp Bell, phép đo kiểu Bell, và các phép sửa `If X` / `If Z` |
| `ch06-teleport-outcomes.png` | 6 | Kết quả đo của Bob đối với mỗi trạng thái Alice gửi, được đánh chỉ số theo tin nhắn cổ điển |
| `ch06-teleport-fidelity.png` | 6 | Chứng minh rằng mọi tin nhắn đều dựng lại trạng thái được truyền đi một cách chính xác |
| `ch06-repeater-circuit.png` | 6 | Hai đoạn liên kết lặp nối tiếp nhau, được thực hiện trên năm qubit và bốn bit cổ điển |
| `ch06-repeater-consistency.png` | 6 | P(1) khởi đầu của Alice đặt cạnh giá trị P(0) được chuyển đến cho Bob |
| `ch06-repeater-counts.png` | 6 | Giá trị P(1) = 0.4 được gửi qua nút trung gian: phân phối kỳ vọng đặt cạnh phân phối đo được |
| `ch07-randombit-circuit.png` | 7 | Sơ đồ mạch: chương trình bốn qubit, được tạo thành từ `H`, `X` và `CNOT` |
| `ch07-randombit-counts.png` | 7 | Biểu đồ kết quả đo, vốn suy sập về hai kết quả khả dĩ thỏa mãn `q0 = q1` |
| `ch07-randombit-qubits.png` | 7 | Giá trị `P(1)` của từng qubit: `q0`/`q1` bằng 0.50, `q2` bằng 0 và `q3` bằng 1 |
| `ch07-debug-circuit.png` | 7 | Cùng chương trình đó, nhưng có một vạch chắn được chèn vào để đánh dấu mỗi bước |
| `ch07-debug-steps.png` | 7 | Phân phối trên các trạng thái cơ sở sau mỗi bước |
| `ch07-debug-marginals.png` | 7 | `P(1)` biên của từng qubit sau mỗi bước, cho biết bước nào làm thay đổi qubit nào |
| `ch07-add1-circuit.png` | 7 | Bộ bán cộng: `CNOT` áp dụng cho `1 + 1`, cộng theo modulo 2 |
| `ch07-add2-circuit.png` | 7 | Bộ cộng đầy đủ: `Toffoli` (tính số nhớ) theo sau bởi `CNOT` (tính tổng) |
| `ch07-toffoli-matrices.png` | 7 | Các ma trận của `X`, `CNOT` và `Toffoli`: mỗi cổng kế tiếp bổ sung một điều khiển |
| `ch07-adder-comparison.png` | 7 | Bán cộng so với cộng đầy đủ: `1 + 1` cho kết quả 0 khi không có số nhớ, và cho 2 khi có số nhớ |
| `ch08-haha-circuit.png` | 8 | Sơ đồ mạch: `X` rồi `H`, `H` — một cơ sở được đi vào rồi lại rời ra |
| `ch08-haha-bloch.png` | 8 | Quá trình biến đổi tương tự hiển thị trên mặt cầu Bloch, minh hoạ `H·H = I` |
| `ch08-attempts-error.png` | 8 | Tỉ lệ lỗi thô: trường hợp không dùng cơ sở so với trường hợp cơ sở chưa được đối chiếu |
| `ch08-superposition-circuit.png` | 8 | Mạch bốn qubit được dùng để chuẩn bị một chồng chập |
| `ch08-superposition-states.png` | 8 | Cả mười sáu trạng thái hiển thị cùng lúc, theo sau là phần khôi phục lại các bit đã chuẩn bị |
| `ch08-bb84-circuit.png` | 8 | Một trao đổi BB84 đơn lẻ: chuẩn bị trạng thái, lựa chọn cơ sở của Bob, và phép đo |
| `ch08-eavesdropper-error.png` | 8 | Các lỗi sau sàng lọc tích lũy qua 200 trao đổi: kênh sạch so với kênh bị nghe trộm |
| `ch09-reversible-circuit.png` | 9 | Sơ đồ mạch: `X`, `X` — chứng minh rằng mọi cổng trong dãy đều khả nghịch |
| `ch09-oracle-matrices.png` | 9 | Bốn ma trận oracle khả dĩ cho một hàm một bit |
| `ch09-oracle-circuit.png` | 9 | Oracle cân bằng `f(x) = x`, có thể hiện thực bằng một cổng `CNOT` duy nhất |
| `ch09-deutsch-circuit.png` | 9 | Mạch Deutsch, được tạo thành từ `X`, `H`, `H`, oracle và một cổng `H` cuối cùng |
| `ch09-deutsch-outcomes.png` | 9 | Một lần truy vấn oracle: hàm hằng cho kết quả đo 0, hàm cân bằng cho kết quả đo 1 |
| `ch09-dj-circuit.png` | 9 | Mạch Deutsch–Jozsa cho `n = 3` |
| `ch09-dj-outcomes.png` | 9 | Với `n = 2`: oracle hằng trả về `00`, trong khi oracle cân bằng thì không bao giờ như vậy |
| `ch10-classical-tries.png` | 10 | Quét tuyến tính cổ điển: số lần thử cần thiết để tìm ra mục tiêu |
| `ch10-oracle-matrix.png` | 10 | Oracle pha của Grover, được hiện thực bằng một lần lật dấu duy nhất |
| `ch10-step-by-step.png` | 10 | Thuật toán Grover trên 2 qubit: xác suất của từng trạng thái cơ sở sau mỗi vòng |
| `ch10-grover-circuit.png` | 10 | Mạch Grover 3 qubit: một lớp `H` ban đầu, theo sau bởi các cặp oracle/khuếch tán xen kẽ |
| `ch10-grover-curve.png` | 10 | Thuật toán Grover trên 64 mục: xác suất thành công tăng lên rồi vọt quá |
| `ch10-grover-outcomes.png` | 10 | 64 kết quả khả dĩ sau 6 vòng: đáp án đúng chiếm ưu thế trong phân phối |
| `ch11-classical-factor.png` | 11 | Chia thử: lượng công việc tăng lên như `sqrt(n)` |
| `ch11-period-function.png` | 11 | Hàm `2^x mod 15`, hàm lặp lại với chu kỳ 4 |
| `ch11-qft-circuit.png` | 11 | Mạch biến đổi Fourier lượng tử cho ba qubit |
| `ch11-qft-phase.png` | 11 | Trạng thái `QFT\|1⟩`: độ lớn đều kết hợp với dốc pha tuyến tính |
| `ch11-order-circuit.png` | 11 | Mạch tìm bậc gọn cho `2^x mod 15` |
| `ch11-order-peaks.png` | 11 | Đầu ra của QFT nghịch đảo: bốn đỉnh, cách nhau 64 |

## Mẫu trong sách và bản port Python

Các mẫu Java của sách được tổ chức thành một thư mục cho mỗi chương trình
(`quantumjava/chNN/mẫu`). Bảng sau ánh xạ các thư mục này sang các mô-đun Python
của kho lưu trữ này theo từng chương, nhờ đó mỗi chương trình minh hoạ trong
sách đều có thể được xác định trực tiếp dưới dạng bản port của nó.

| Chương sách | Mẫu Java (`quantumjava/chNN/`) | Mô-đun Python |
|---|---|---|
| 1 | `time` | `ch01.time_complexity` |
| 2 | `hellostrange` | `ch02.random_bits` |
| 3 | `paulix`, `paulixui` | `ch03.pauli_x` |
| 4 | `hadamard`, `hadamard2` | `ch04.hadamard`, `ch04.matrices` |
| 5 | `bellstate`, `classiccoin`, `cnot`, `maryqubit`, `quantumcoin` | `ch05.entanglement`, `ch05.states` |
| 6 | `classic`, `classiccopy`, `hczmeasure`, `teleport`, `repeater` | `ch06.networking`, `ch06.czmeasure`, `ch06.teleportation`, `ch06.repeater`, `ch06.protocol` |
| 7 | `randombit`, `randombitdebug`, `add1`, `add2` | `ch07.randombit`, `ch07.debugging`, `ch07.half_adder`, `ch07.full_adder`, `ch07.circuits` |
| 8 | `haha`, `naive`, `guess`, `superposition`, `bb84` | `ch08.identity`, `ch08.attempts`, `ch08.superposition`, `ch08.bb84`, `ch08.protocol` |
| 9 | `reversibleX`, `function`, `oracle`, `applyoracle`, `deutsch`, `deutschjozsa` | `ch09.reversible`, `ch09.oracles`, `ch09.deutsch`, `ch09.deutschjozsa` |
| 10 | `classicsearch`, `quantumsearch`, `groveroracle`, `stepbystepgrover`, `grover` | `ch10.search`, `ch10.oracle`, `ch10.step_by_step`, `ch10.grover` |
| 11 | `classicfactor`, `semiclassicfactor`, `quantumfactor`, `jshell` | `ch11.classical`, `ch11.qft`, `ch11.shor` |

Một số mẫu dùng chung một mô-đun duy nhất: chẳng hạn, bốn mẫu oracle của chương
9 đều nằm trong `ch09.oracles`. Ngoài ra, một số mô-đun cung cấp mã hỗ trợ không
có bản Java tương ứng (`ch07.circuits`, `ch08.protocol`). Cần lưu ý rằng các
snippet `quantumjava/ch11/jshell` tương ứng với phần tính tay trong sách; lời
gọi `ch11.classical.reduction_steps(6, 493)` tái tạo lại các phép tính đó dưới
dạng chương trình.

## Ký hiệu dùng trong ghi chú

Các ký hiệu dưới đây được dùng xuyên suốt trong ghi chú này. Mỗi ký hiệu được
giới thiệu tại vị trí xuất hiện lần đầu, và bảng dưới đây tập hợp các định nghĩa
về một nơi để tiện tra cứu trong lúc đọc.

| Ký hiệu | Ý nghĩa |
|---------|---------|
| <code>\|0⟩</code>, <code>\|1⟩</code> | Hai trạng thái cơ sở tính toán của qubit, tương ứng với hai giá trị bit 0 và 1 |
| <code>\|ψ⟩</code> | Trạng thái một-qubit tổng quát (bất kỳ), không bị hạn chế ở một trạng thái cơ sở nào |
| <code>\|+⟩</code>, <code>\|−⟩</code> | Hai chồng chập đều <code>(\|0⟩ ± \|1⟩)/√2</code>, chỉ khác nhau ở pha tương đối |
| <code>(a\|0⟩ + b\|1⟩)</code> | Chồng chập của <code>\|0⟩</code> và <code>\|1⟩</code> với biên độ `a` và `b` tương ứng |
| `[α, β]` | Cùng trạng thái đó viết dưới dạng vector cột, với các thành phần `α` và `β` |
| `H` | Cổng Hadamard — tạo chồng chập đều từ một trạng thái cơ sở |
| `X` | Cổng Pauli-X — lật <code>\|0⟩ ↔ \|1⟩</code> |
| `CNOT` | Controlled-NOT — lật qubit đích khi qubit điều khiển bằng `1` |
| `Toffoli` | Controlled-controlled-NOT (`CCNOT`) — lật đích khi **cả hai** điều khiển bằng `1`; một cách hiện thực khả nghịch của `AND` |
| `XOR` | Phép hoặc loại trừ — bit tổng của phép cộng modulo 2 |
| `U_f` | Oracle của hàm `f`: `\|x⟩\|y⟩ → \|x⟩\|y ⊕ f(x)⟩` |
| `QFT` | Biến đổi Fourier lượng tử — biến đổi Fourier rời rạc được hiện thực dưới dạng mạch |
| `\|s⟩` | Chồng chập đều trên mọi trạng thái cơ sở `N`, trong đó mọi trạng thái cơ sở đều mang cùng biên độ |
| `Z` | Cổng Pauli-Z — lật **pha** mà không đổi bit |
| `CZ` | Controlled-Z — áp dụng `Z` lên qubit đích khi qubit điều khiển bằng `1` |
| `⊗` | Tích tensor — ghép các trạng thái một qubit thành trạng thái chung của nhiều qubit |
| Trạng thái Bell | Cặp rối cực đại, ví dụ <code>(\|00⟩ + \|11⟩)/√2</code> |
| `I` | Phép đơn vị — "không làm gì", tức là phép toán giữ nguyên mọi trạng thái |
| `U` | Cổng tổng quát, viết dưới dạng ma trận 2×2 |
| `P(0)`, `P(1)` | Xác suất đo (quy tắc Born: biên độ bình phương) |
| Mặt cầu Bloch | Hình học mô tả trạng thái của một qubit |
| Độ trung thực | Độ chồng lấn của hai trạng thái, <code>\|⟨a\|b⟩\|²</code>; bằng 1 nghĩa là hai trạng thái trùng nhau |
| Hạng Schmidt | 1 ứng với trạng thái tích còn 2 ứng với trạng thái rối (xem phần về [ma trận hệ số](chapters/ch05-entanglement.md#trang-thai-tich-so-voi-trang-thai-roi)) |
