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
| [1 — Tiến hoá, cách mạng, hay cường điệu?](chapters/ch01-evolution-revolution-hype.md) | hoàn thành | Điện toán lượng tử là một bước tiến hoá với tăng tốc cách mạng cho một nhóm bài toán hẹp, ví dụ phân tích thừa số | [cổ điển so với Shor, cổ điển riêng](chapters/ch01-evolution-revolution-hype.md) |
| [2 — Hello World kiểu điện toán lượng tử](chapters/ch02-hello-world.md) | hoàn thành | Qubit ở trạng thái chồng chập cho ra `0`/`1` thực sự ngẫu nhiên khi đo | [mạch, biểu đồ, Bloch](chapters/ch02-hello-world.md) |
| [3 — Qubit và cổng lượng tử](chapters/ch03-qubits-and-gates.md) | hoàn thành | Qubit là đơn vị cơ bản và cổng là phép toán khả nghịch; `X` lật `\|0⟩` thành `\|1⟩` tất định | [mạch, Bloch, số lần đo](chapters/ch03-qubits-and-gates.md) |
| [4 — Chồng chập](chapters/ch04-superposition.md) | hoàn thành | Trạng thái là vector và cổng là ma trận; `H` tạo chồng chập đều và `H·H` xoá nó | [mạch, Bloch, số lần đo, ma trận](chapters/ch04-superposition.md) |
| [5 — Rối lượng tử](chapters/ch05-entanglement.md) | dự kiến | Hai qubit có thể chia sẻ một trạng thái chung không thể mô tả riêng từng qubit | — |
| [6 — Mạng lượng tử: những điều cơ bản](chapters/ch06-quantum-networking.md) | dự kiến | Truyền thông tin lượng tử giữa các nút: dịch chuyển, không nhân bản, bộ lặp | — |
| [7 — HelloWorld của chúng ta, giải thích](chapters/ch07-helloworld-explained.md) | dự kiến | Dựng lại mạch tạo bit ngẫu nhiên từng cổng một để thấy nó thực sự hoạt động ra sao | — |
| [8 — Truyền thông an toàn bằng điện toán lượng tử](chapters/ch08-secure-communication.md) | dự kiến | Phân phối khoá lượng tử (BB84) khiến hành vi nghe lén bị phát hiện | — |
| [9 — Thuật toán Deutsch–Jozsa](chapters/ch09-deutsch-jozsa.md) | dự kiến | Quyết định hàm là hằng số hay cân bằng chỉ trong một truy vấn | — |
| [10 — Thuật toán tìm kiếm của Grover](chapters/ch10-grovers-search.md) | dự kiến | Tăng tốc bậc hai cho tìm kiếm không cấu trúc | — |
| [11 — Thuật toán Shor](chapters/ch11-shors-algorithm.md) | dự kiến | Phân tích thừa số thời gian đa thức nhờ tìm bậc và biến đổi Fourier lượng tử | — |

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

## Đi tiếp ở đâu

- Mới bắt đầu? Xem **[Bắt đầu](getting-started.md)** để chạy ví dụ và vẽ lại sơ đồ.
- Mới với các ý nền (bit, biên độ, pha, mặt cầu Bloch)? Đọc lướt trang
  **[Kiến thức nền](foundations.md)**.
- Chỉ muốn phần khái niệm? Đi thẳng tới
  **[Chương 1](chapters/ch01-evolution-revolution-hype.md)**.
- Tìm mã tạo ra một hình? Xem bảng trong **[Tham chiếu](reference.md)**, ánh xạ mỗi
  chương với module, lệnh CLI và sơ đồ của nó.
