# Chương 2 — Hello World kiểu điện toán lượng tử

!!! abstract "Trong một câu"
    Đưa qubit vào trạng thái **chồng chập** bằng cổng Hadamard rồi đo, bạn nhận
    `0` hoặc `1` với xác suất bằng nhau — tính ngẫu nhiên đến từ vật lý, không
    phải từ một thuật toán ẩn.

## Vì sao là "Hello World"?

Mọi ngôn ngữ lập trình đều bắt đầu bằng chương trình in ra `Hello, World!`: đủ nhỏ
để gõ, nhưng chứng minh cả chuỗi công cụ hoạt động. Điện toán lượng tử cũng cần
một chương trình đầu tiên như vậy.

Điểm thú vị là chương trình lượng tử nhỏ nhất mà *thú vị* lại làm được điều máy cổ
điển không làm được: tạo ra một **bit thực sự ngẫu nhiên**. Đó là "Hello World"
lượng tử — một qubit, một cổng, một phép đo.

## Bit cổ điển so với qubit

Bit cổ điển luôn là một trong hai giá trị: `0` **hoặc** `1`. **Qubit** có thể còn
ở *tổ hợp* của cả hai. Viết theo ký hiệu Dirac dùng xuyên suốt cuốn sách:

- `|0⟩` — trạng thái luôn đo ra `0`
- `|1⟩` — trạng thái luôn đo ra `1`
- một **chồng chập**, ví dụ `(|0⟩ + |1⟩) / √2` — hỗn hợp đều của cả hai

Các ký hiệu `|…⟩` chỉ là quy ước gán nhãn; vật lý nằm ở các hệ số.

## Cổng Hadamard

Cổng **Hadamard** (`H`) là cách chuẩn để tạo chồng chập đều:

$$H\,|0\rangle = \frac{|0\rangle + |1\rangle}{\sqrt{2}}$$

Nếu qubit bắt đầu ở `|0⟩`, một cổng `H` đưa nó vào trạng thái đúng một nửa `|0⟩`
và một nửa `|1⟩`. Các hệ số `1/√2` chính là thứ khiến xác suất cộng lại bằng 1
(xem quy tắc Born bên dưới).

## Phép đo và quy tắc Born

Bạn không bao giờ *nhìn thấy* chồng chập trực tiếp. Khoảnh khắc bạn **đo** qubit,
nó sụp về một trong các trạng thái cơ sở, và xác suất của mỗi kết quả là bình
phương hệ số của trạng thái đó — **quy tắc Born**:

$$P(0) = \left|\tfrac{1}{\sqrt{2}}\right|^2 = \tfrac{1}{2}, \qquad
  P(1) = \left|\tfrac{1}{\sqrt{2}}\right|^2 = \tfrac{1}{2}$$

Chạy thí nghiệm một lần, bạn được một bit. Chạy hàng nghìn lần, hai kết quả xuất
hiện với số lượng gần bằng nhau.

!!! info "Vì sao đây là ngẫu nhiên *thực sự*"
    Hàm `random()` cổ điển thường là **giả ngẫu nhiên**: trông ngẫu nhiên nhưng
    hoàn toàn xác định bởi một hạt giống ẩn, và có thể tái tạo. Qubit đã đo không
    có giá trị ẩn nào đang chờ được lộ ra — kết quả không được xác định trước khi
    đo. Đó là lý do "hello world" này là ví dụ đầu tiên phù hợp cho một chương
    trình lượng tử.

## Các sơ đồ

### Mạch

![Mạch tạo bit ngẫu nhiên](../assets/ch02-random-bits-circuit.png){ width="420" }

Đọc từ trái sang phải: qubit `q` bắt đầu ở `|0⟩`, cổng `H` đưa nó vào chồng chập,
và phép đo `M` ghi giá trị đã sụp vào bit cổ điển `c`.

### Kết quả thực tế

![Biểu đồ 10000 bit đo được](../assets/ch02-random-bits-counts.png){ width="420" }

Đo 10.000 lần cho ra hai cột gần bằng nhau. Sai lệch nhỏ so với đúng 5.000/5.000 là
điều dự kiến — đó là cùng kiểu dao động thống kê như khi tung 10.000 đồng xu cân
đối.

### Trạng thái trên mặt cầu Bloch

![Chồng chập trên mặt cầu Bloch](../assets/ch02-random-bits-bloch.png){ width="420" }

**Mặt cầu Bloch** là hình học mô tả trạng thái của một qubit. Cực bắc là `|0⟩` và
cực nam là `|1⟩`. `H|0⟩` hạ cánh đúng trên đường xích đạo, hướng theo trục **+X**
— dấu hiệu thị giác của chồng chập đều 50/50. Một trạng thái nằm trên đường xích
đạo chính là thứ bảo đảm kết quả đo cân bằng.

## Ghi nhớ chính

- Qubit có thể ở chồng chập, không chỉ `0` hay `1`.
- `H` biến `|0⟩` thành hỗn hợp đều `(|0⟩ + |1⟩)/√2`.
- Phép đo làm sụp trạng thái; **quy tắc Born** cho xác suất.
- Bit thu được là ngẫu nhiên thực sự, khác với bộ sinh giả ngẫu nhiên.
- Trên mặt cầu Bloch, chồng chập đều nằm trên đường xích đạo.

## Mã nguồn của chương này

Ví dụ trong sách dùng lệnh cấp cao `Classic.randomBit()`; bản Python mở lệnh đó
thành mạch `H` rồi đo tường minh để thấy rõ cơ chế. Mã nằm trong
[`src/quantum_computing_in_action/ch02/random_bits.py`](https://github.com/phonhay103/quantum-computing-in-action/blob/main/src/quantum_computing_in_action/ch02/random_bits.py).
Chạy bằng `make ch02`.
