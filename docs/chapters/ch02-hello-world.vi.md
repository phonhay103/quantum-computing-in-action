# Chương 2 — Hello World kiểu điện toán lượng tử

!!! abstract "Trong một câu"
    Đưa qubit vào trạng thái **chồng chập** bằng cổng Hadamard rồi tiến hành đo,
    kết quả thu được là `0` hoặc `1` với xác suất bằng nhau — tính ngẫu nhiên
    đến từ bản chất vật lý, không phải từ một thuật toán ẩn.

## Vì sao là "Hello World"?

Mọi ngôn ngữ lập trình đều bắt đầu bằng chương trình in ra `Hello, World!`.
Chương trình này đủ nhỏ để gõ trong vài giây, nhưng đóng vai trò quan trọng:
nó chứng minh toàn bộ chuỗi công cụ — trình biên dịch, môi trường chạy và
đường dẫn xuất kết quả — đều hoạt động đúng. Điện toán lượng tử cũng cần một
chương trình đầu tiên như vậy, tức một thí nghiệm xác nhận môi trường trước
khi bước vào nội dung sâu hơn.

Điểm đáng chú ý là chương trình lượng tử nhỏ nhất mà vẫn *đáng chú ý* lại làm
được điều máy cổ điển không làm được: tạo ra một **bit thực sự ngẫu nhiên**.
Đó chính là "Hello World" lượng tử — một qubit, một cổng, một phép đo. Nói
cách khác, toàn bộ minh hoạ gói gọn trong một đường mạch duy nhất, trong khi
không gì cổ điển có thể sao chép kết quả ấy một cách tất định.

## Bit cổ điển so với qubit

Bit cổ điển luôn là một trong hai giá trị: `0` **hoặc** `1`. Giá trị này được
xác định rõ ở mọi thời điểm, và việc đọc bit chỉ đơn giản là báo cáo điều đã
tồn tại. **Qubit**, ngược lại, có thể còn ở *tổ hợp* của cả hai giá trị cùng
lúc. Viết theo ký hiệu Dirac dùng xuyên suốt cuốn sách, các trạng thái liên
quan là:

- `|0⟩` — trạng thái luôn đo ra `0`
- `|1⟩` — trạng thái luôn đo ra `1`
- một **chồng chập**, ví dụ `(|0⟩ + |1⟩) / √2` — hỗn hợp đều của cả hai

Các ký hiệu `|…⟩` chỉ là quy ước gán nhãn cho trạng thái; nội dung vật lý nằm
ở các hệ số gắn với từng thành phần, vì chính các hệ số này quyết định phép đo
sẽ cho ra kết quả gì. Phần trình bày đầy đủ hơn về bit, qubit và ký hiệu Dirac
có trong chương nền tảng (xem [bit, qubit và ký hiệu Dirac](../foundations.md)).

## Cổng Hadamard

Cổng **Hadamard** (`H`) là cách chuẩn để tạo chồng chập đều. Áp dụng lên
trạng thái ban đầu, cổng này tác động như sau:

$$H\,|0\rangle = \frac{|0\rangle + |1\rangle}{\sqrt{2}}$$

Nếu qubit bắt đầu ở `|0⟩`, một cổng `H` đưa nó vào trạng thái đúng một nửa
`|0⟩` và một nửa `|1⟩`. Các hệ số `1/√2` là **biên độ**, không phải xác suất
(xem [biên độ và quy tắc Born](../foundations.md)). Cần lưu ý rằng việc bình
phương biên độ mới tạo ra xác suất, và chính phép tính này bảo đảm tổng xác
suất của mọi kết quả bằng 1. Do đó, cổng không *chọn* kết quả; nó chỉ chuẩn bị
trạng thái mà từ đó kết quả sẽ được rút ra sau này bằng phép đo.

## Phép đo và quy tắc Born

Chồng chập không bao giờ được *quan sát* trực tiếp. Tại thời điểm qubit được
**đo**, nó sụp về một trong các trạng thái cơ sở, và xác suất của mỗi kết quả
là bình phương hệ số của trạng thái đó — quy định này chính là **quy tắc
Born**:

$$P(0) = \left|\tfrac{1}{\sqrt{2}}\right|^2 = \tfrac{1}{2}, \qquad
  P(1) = \left|\tfrac{1}{\sqrt{2}}\right|^2 = \tfrac{1}{2}$$

Một lần chạy thí nghiệm chỉ cho ra một bit duy nhất, và không thể suy luận
thêm điều gì từ lần thử đơn lẻ đó. Khi thí nghiệm được lặp lại nhiều lần — mỗi
lần chạy gọi là một **lần chạy** (shot) — hai kết quả xuất hiện với số lượng
gần bằng nhau, đúng như dự đoán thống kê của quy tắc Born.

!!! info "Vì sao đây là ngẫu nhiên *thực sự*"
    Hàm `random()` cổ điển thường là **giả ngẫu nhiên**: kết quả trông ngẫu
    nhiên, nhưng toàn bộ chuỗi được xác định hoàn toàn bởi một hạt giống ẩn,
    nên có thể tái tạo nếu biết cùng điều kiện xuất phát. Qubit đã đo không có
    giá trị ẩn nào đang chờ được lộ ra — kết quả không được xác định trước khi
    phép đo diễn ra. Vì vậy, tính ngẫu nhiên ở đây không thể quy về bất kỳ cơ
    chế tất định ngầm nào, và đó là lý do "hello world" này là ví dụ đầu tiên
    phù hợp cho một chương trình lượng tử.

## Các sơ đồ {#cac-so-do}

### Mạch

![Mạch tạo bit ngẫu nhiên](../assets/ch02-random-bits-circuit.png){ width="420" }

Mạch được đọc từ trái sang phải (xem [mô hình mạch](../foundations.md)). Trong
sơ đồ trên, qubit `q` bắt đầu ở `|0⟩`, cổng `H` đưa nó vào chồng chập, và phép
đo `M` ghi giá trị đã sụp vào bit cổ điển `c`. Có thể suy ra rằng chỉ bit cổ
điển `c` mang một giá trị xác định sau khi chạy; vai trò của qubit là sinh ra
giá trị đó thông qua bước đo.

### Kết quả thực tế

![Biểu đồ 10000 bit đo được](../assets/ch02-random-bits-counts.png){ width="420" }

Đo 10.000 lần cho ra hai cột gần bằng nhau. Sai lệch nhỏ so với đúng
5.000/5.000 là điều dự kiến và không phải dấu hiệu lỗi — đó là cùng kiểu dao
động thống kê như khi tung 10.000 đồng xu cân đối; hơn nữa, sai lệch này được
kỳ vọng sẽ thu nhỏ khi số lần chạy tăng lên.

### Trạng thái trên mặt cầu Bloch

![Chồng chập trên mặt cầu Bloch](../assets/ch02-random-bits-bloch.png){ width="420" }

**Mặt cầu Bloch** là hình học mô tả trạng thái của một qubit, được xác định
bởi hai góc `θ` và `φ` (xem [mặt cầu Bloch](../foundations.md)). Cực bắc biểu
diễn `|0⟩` và cực nam biểu diễn `|1⟩`. Trạng thái `H|0⟩` hạ cánh đúng trên
đường xích đạo, hướng theo trục **+X** — dấu hiệu thị giác của chồng chập đều
50/50. Có thể suy ra rằng một trạng thái nằm trên đường xích đạo chính là thứ
bảo đảm kết quả đo cân bằng, vì không bán cầu nào được ưu tiên; khoảng cách
tới hai cực mã hoá mức độ nghiêng của kết quả về phía `0` hay `1`.

## Những điều cần nhớ

- Qubit có thể ở chồng chập, không chỉ `0` hay `1`.
- `H` biến `|0⟩` thành hỗn hợp đều `(|0⟩ + |1⟩)/√2`.
- Phép đo làm sụp trạng thái; **quy tắc Born** cho xác suất.
- Bit thu được là ngẫu nhiên thực sự, khác với bộ sinh giả ngẫu nhiên.
- Trên mặt cầu Bloch, chồng chập đều nằm trên đường xích đạo.

## Mã nguồn của chương này

Ví dụ trong sách dùng lệnh cấp cao `Classic.randomBit()`; bản Python mở lệnh
đó thành mạch `H` rồi đo tường minh, nhờ đó cơ chế bên dưới hiện rõ thay vì
bị giấu bên trong một hàm thư viện. Mã nằm trong
[`src/quantum_computing_in_action/ch02/random_bits.py`](https://github.com/phonhay103/quantum-computing-in-action/blob/main/src/quantum_computing_in_action/ch02/random_bits.py).
Chạy bằng `make ch02`.
