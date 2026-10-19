# Quantum Computing in Action — ghi chú đồng hành

Trang này giải thích các **ý tưởng** trong sách
[_Quantum Computing in Action_](https://www.manning.com/books/quantum-computing-in-action)
của Johan Vos, cho những chương đã được chuyển sang Python với
[Qiskit](https://www.ibm.com/quantum/qiskit).

Sách dạy điện toán lượng tử bằng bộ mô phỏng [Strange](https://github.com/gluonhq/strange)
viết bằng Java. Kho mã này giữ nguyên mạch kể chuyện đó nhưng dùng Qiskit, và vẽ
kết quả của mỗi ví dụ thành sơ đồ để bạn *nhìn thấy* điều mà toán học mô tả. Nó chỉ
dùng hai nguồn công khai: **mã nguồn** của sách và
[trang Manning](https://www.manning.com/books/quantum-computing-in-action) của sách
(bao gồm cả mục lục).

!!! note "Ghi chú này là gì — và không phải là gì"
    Các trang này trình bày **kiến thức điện toán lượng tử** của từng chương:
    qubit là gì, cổng lượng tử làm gì, phép đo trả về gì, và vì sao điều đó quan
    trọng. Chúng **không** đi qua từng dòng mã nguồn. Mỗi trang có liên kết tới
    module tương ứng nếu bạn muốn đọc phần cài đặt.

## Các chương được trình bày

Tên chương bám theo mục lục của sách.

| Chương | Trạng thái | Ý tưởng trong một câu | Sơ đồ |
|--------|-----------|-----------------------|-------|
| [1 — Tiến hoá, cách mạng, hay cường điệu?](chapters/ch01-evolution-revolution-hype.md) | hoàn thành | Điện toán lượng tử là một bước tiến hoá với tăng tốc cách mạng cho một nhóm bài toán hẹp, ví dụ phân tích thừa số | [cổ điển so với Shor, cổ điển riêng](chapters/ch01-evolution-revolution-hype.md#cac-so-do) |
| [2 — Hello World kiểu điện toán lượng tử](chapters/ch02-hello-world.md) | hoàn thành | Qubit ở trạng thái chồng chập cho ra `0`/`1` thực sự ngẫu nhiên khi đo | [mạch, biểu đồ, Bloch](chapters/ch02-hello-world.md#cac-so-do) |
| [3 — Qubit và cổng lượng tử](chapters/ch03-qubits-and-gates.md) | hoàn thành | Qubit là đơn vị cơ bản và cổng là phép toán khả nghịch; `X` lật <code>\|0⟩</code> thành <code>\|1⟩</code> tất định | [mạch, Bloch, số lần đo](chapters/ch03-qubits-and-gates.md#cac-so-do) |
| [4 — Chồng chập](chapters/ch04-superposition.md) | hoàn thành | Trạng thái là vector và cổng là ma trận; `H` tạo chồng chập đều và `H·H` xoá nó | [mạch, Bloch, số lần đo, ma trận](chapters/ch04-superposition.md#cac-so-do) |
| [5 — Rối lượng tử](chapters/ch05-entanglement.md) | hoàn thành | Hai qubit có thể chia sẻ một trạng thái chung không thể mô tả riêng từng qubit | [mạch, số lần đo, so sánh, ma trận](chapters/ch05-entanglement.md#cac-so-do) |
| [6 — Mạng lượng tử: những điều cơ bản](chapters/ch06-quantum-networking.md) | hoàn thành | Một qubit không thể nhân bản, nên nó phải được *dựng lại ở nơi khác*: truyền tải lượng tử tái tạo một trạng thái từ cặp rối dùng chung cộng hai bit cổ điển, và trạm lặp nối các liên kết lại | [không nhân bản, CZ, truyền tải, trạm lặp](chapters/ch06-quantum-networking.md#cac-so-do) |
| [7 — HelloWorld của chúng ta, giải thích](chapters/ch07-helloworld-explained.md) | hoàn thành | Một mạch là danh sách các bước có thứ tự, và có thể đọc trạng thái sau mỗi bước — cùng ý tưởng đó tạo nên một bộ cộng khả nghịch từ `CNOT` và `Toffoli` | [mạch, từng bước, bộ cộng, Toffoli](chapters/ch07-helloworld-explained.md#cac-so-do) |
| [8 — Truyền thông an toàn bằng điện toán lượng tử](chapters/ch08-secure-communication.md) | hoàn thành | Một qubit chỉ mang bit trong một **cơ sở** được chọn, nên Alice và Bob có thể sàng lọc các cơ sở khớp nhau thành khoá bí mật — và phép đo của kẻ nghe lén để lại tỉ lệ lỗi ~25% | [vòng xoay, các cách thử, chồng chập, BB84, nghe trộm](chapters/ch08-secure-communication.md#cac-so-do) |
| [9 — Thuật toán Deutsch–Jozsa](chapters/ch09-deutsch-jozsa.md) | hoàn thành | Một truy vấn lượng tử quyết định hàm được hứa là hằng số hay cân bằng, nơi kiểm tra cổ điển có thể cần `2^(n-1) + 1` | [khả nghịch, oracle, Deutsch, DJ](chapters/ch09-deutsch-jozsa.md#cac-so-do) |
| [10 — Thuật toán tìm kiếm của Grover](chapters/ch10-grovers-search.md) | hoàn thành | Oracle lật một dấu; khuếch tán phản xạ quanh trung bình; `(π/4)√N` vòng tìm ra mục — tăng tốc bậc hai | [cổ điển, oracle, từng bước, 64 mục](chapters/ch10-grovers-search.md#cac-so-do) |
| [11 — Thuật toán Shor](chapters/ch11-shors-algorithm.md) | hoàn thành | Phân tích thừa số quy giản về tìm bậc, và biến đổi Fourier lượng tử đọc chu kỳ từ vài đỉnh — thời gian đa thức | [cổ điển, QFT, tìm bậc](chapters/ch11-shors-algorithm.md#cac-so-do) |

## Thư viện sơ đồ

Mỗi ví dụ ghi hình của nó vào `build/`, với tiền tố là số chương để một hình luôn
cho biết nó đến từ đâu.

### Chương 1 — cổ điển so với Shor

![Độ phức tạp cổ điển so với Shor](assets/ch01-time-complexity.png){ width="460" }
![Đường cổ điển riêng lẻ](assets/ch01-time-complexity-classical.png){ width="460" }

### Chương 2 — bit ngẫu nhiên

![Mạch tạo bit ngẫu nhiên](assets/ch02-random-bits-circuit.png){ width="360" }
![Số lần đo được](assets/ch02-random-bits-counts.png){ width="360" }
![Chồng chập trên mặt cầu Bloch](assets/ch02-random-bits-bloch.png){ width="360" }

### Chương 3 — qubit và cổng

![Mạch Pauli-X](assets/ch03-pauli-x.png){ width="360" }
![Hai cổng Pauli-X](assets/ch03-pauli-x2-circuit.png){ width="360" }
![Qubit trước, sau X, và sau X·X](assets/ch03-pauli-x-bloch.png){ width="620" }

### Chương 4 — chồng chập

![Mạch Hadamard đơn](assets/ch04-hadamard-circuit.png){ width="360" }
![Hai cổng Hadamard](assets/ch04-hadamard2-circuit.png){ width="360" }
![Chồng chập được tạo và xoá trên mặt cầu Bloch](assets/ch04-hadamard-bloch.png){ width="560" }
![X, H và H·H dưới dạng ma trận](assets/ch04-gate-matrices.png){ width="560" }

### Chương 5 — rối lượng tử

![Mạch trạng thái Bell](assets/ch05-bell-circuit.png){ width="360" }
![Mạch CNOT](assets/ch05-cnot-circuit.png){ width="360" }
![Qubit độc lập so với rối](assets/ch05-bell-vs-independent.png){ width="560" }
![Ma trận hệ số](assets/ch05-amplitude-matrices.png){ width="560" }

### Chương 6 — mạng lượng tử

![Cách thử nhân bản thất bại](assets/ch06-clone-attempt-circuit.png){ width="360" }
![Bản sao hoàn hảo so với cách thử bằng CNOT](assets/ch06-clone-agreement.png){ width="560" }
![Mạch teleportation](assets/ch06-teleport-circuit.png){ width="620" }
![Hai đoạn liên kết nối qua một nút trung gian](assets/ch06-repeater-circuit.png){ width="620" }

### Chương 7 — HelloWorld của chúng ta, giải thích

![Chương trình bốn qubit](assets/ch07-randombit-circuit.png){ width="360" }
![Xác suất trạng thái cơ sở sau mỗi bước](assets/ch07-debug-steps.png){ width="560" }
![Bộ bán cộng cho 1 + 1](assets/ch07-add1-circuit.png){ width="360" }
![Bộ cộng đầy đủ cho 1 + 1](assets/ch07-add2-circuit.png){ width="420" }
![Từ X tới CNOT tới Toffoli](assets/ch07-toffoli-matrices.png){ width="560" }
![Bán cộng so với cộng đầy đủ](assets/ch07-adder-comparison.png){ width="560" }

### Chương 8 — truyền thông an toàn

![Vòng xoay Hadamard](assets/ch08-haha-circuit.png){ width="360" }
![Đường sạch so với một đường bị nghe trộm](assets/ch08-eavesdropper-error.png){ width="560" }
![Một thanh ghi trong chồng chập, và chính thanh ghi đó được khôi phục](assets/ch08-superposition-states.png){ width="560" }
![Một mạch BB84](assets/ch08-bb84-circuit.png){ width="620" }

### Chương 9 — Deutsch–Jozsa

![Bốn ma trận oracle](assets/ch09-oracle-matrices.png){ width="560" }
![Mạch Deutsch](assets/ch09-deutsch-circuit.png){ width="360" }
![Một truy vấn: hằng số đo 0, cân bằng đo 1](assets/ch09-deutsch-outcomes.png){ width="560" }
![Deutsch–Jozsa cho n = 3](assets/ch09-dj-circuit.png){ width="620" }

### Chương 10 — tìm kiếm của Grover

![Oracle của Grover](assets/ch10-oracle-matrix.png){ width="360" }
![Grover trên 2 qubit](assets/ch10-step-by-step.png){ width="560" }
![Grover trên 64 mục: xác suất tăng rồi vọt quá](assets/ch10-grover-curve.png){ width="560" }

### Chương 11 — thuật toán Shor

![Chia thử cổ điển](assets/ch11-classical-factor.png){ width="560" }
![QFT|1>: dốc pha tuyến tính](assets/ch11-qft-phase.png){ width="560" }
![Một mạch tìm bậc gọn](assets/ch11-order-circuit.png){ width="620" }
![QFT nghịch đảo của thanh ghi tuần hoàn: bốn đỉnh](assets/ch11-order-peaks.png){ width="560" }

## Đi tiếp ở đâu

- Mới bắt đầu? Xem **[Bắt đầu](getting-started.md)** để chạy ví dụ và vẽ lại sơ đồ.
- Mới với các ý nền (bit, biên độ, pha, mặt cầu Bloch)? Đọc lướt trang
  **[Kiến thức nền](foundations.md)**.
- Vướng một từ như *độ trung thực*, *hạng Schmidt*, hay *dưới hàm mũ*? Tra trong
  bảng **[Thuật ngữ](glossary.md)**.
- Chỉ muốn phần khái niệm? Đi thẳng tới
  **[Chương 1](chapters/ch01-evolution-revolution-hype.md)**.
- Tìm mã tạo ra một hình? Xem bảng trong **[Tham chiếu](reference.md)**, ánh xạ mỗi
  chương với module, lệnh CLI và sơ đồ của nó.
