# Quantum Computing in Action — ghi chú đồng hành

Trang này giải thích các **ý tưởng** trong sách
[_Quantum Computing in Action_](https://www.manning.com/books/quantum-computing-in-action)
của Johan Vos, cho những chương đã được chuyển sang Python với
[Qiskit](https://www.ibm.com/quantum/qiskit).

Sách dạy điện toán lượng tử bằng bộ mô phỏng [Strange](https://github.com/gluonhq/strange)
viết bằng Java. Kho mã này giữ nguyên mạch kể chuyện đó nhưng dùng Qiskit, và vẽ
kết quả của mỗi ví dụ thành sơ đồ để bạn *nhìn thấy* điều mà toán học mô tả.

!!! note "Ghi chú này là gì — và không phải là gì"
    Các trang này trình bày **kiến thức điện toán lượng tử** của từng chương:
    qubit là gì, cổng lượng tử làm gì, phép đo trả về gì, và vì sao điều đó quan
    trọng. Chúng **không** đi qua từng dòng mã nguồn. Mỗi trang có liên kết tới
    module tương ứng nếu bạn muốn đọc phần cài đặt.

## Các chương được trình bày

| Chương | Ý tưởng trong một câu | Sơ đồ |
|--------|-----------------------|-------|
| [1 — Độ phức tạp thời gian phân tích thừa số](chapters/ch01-time-complexity.md) | Máy tính lượng tử hứa hẹn tăng tốc vì thuật toán Shor có độ phức tạp đa thức, còn phương pháp cổ điển tốt nhất là hàm mũ | [cổ điển so với Shor](chapters/ch01-time-complexity.md) |
| [2 — Bit ngẫu nhiên](chapters/ch02-random-bits.md) | Qubit ở trạng thái chồng chập cho ra `0`/`1` thực sự ngẫu nhiên khi đo | [mạch, biểu đồ, Bloch](chapters/ch02-random-bits.md) |
| [3 — Cổng Pauli-X](chapters/ch03-pauli-x.md) | Một cổng một-qubit lật `\|0⟩` thành `\|1⟩` một cách tất định | [mạch, Bloch](chapters/ch03-pauli-x.md) |

## Thư viện sơ đồ

Mỗi ví dụ ghi hình của nó vào `build/`, với tiền tố là số chương để một hình luôn
cho biết nó đến từ đâu.

### Chương 1 — cổ điển so với Shor

![Độ phức tạp cổ điển so với Shor](assets/ch01-time-complexity.png){ width="520" }

### Chương 2 — bit ngẫu nhiên

![Mạch tạo bit ngẫu nhiên](assets/ch02-random-bits-circuit.png){ width="360" }
![Số lần đo được](assets/ch02-random-bits-counts.png){ width="360" }
![Chồng chập trên mặt cầu Bloch](assets/ch02-random-bits-bloch.png){ width="360" }

### Chương 3 — cổng Pauli-X

![Mạch Pauli-X](assets/ch03-pauli-x.png){ width="360" }
![Qubit trước và sau cổng X](assets/ch03-pauli-x-bloch.png){ width="520" }

## Đi tiếp ở đâu

- Mới bắt đầu? Xem **[Bắt đầu](getting-started.md)** để chạy ví dụ và vẽ lại sơ đồ.
- Chỉ muốn phần khái niệm? Đi thẳng tới **[Chương 1](chapters/ch01-time-complexity.md)**.
- Tìm mã tạo ra một hình? Xem bảng trong **[Tham chiếu](reference.md)**, ánh xạ mỗi
  chương với module, lệnh CLI và sơ đồ của nó.
