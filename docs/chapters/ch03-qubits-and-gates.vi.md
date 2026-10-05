# Chương 3 — Qubit và cổng lượng tử

!!! abstract "Trong một câu"
    **Qubit** là đơn vị cơ bản của thông tin lượng tử và **cổng** là một phép toán
    khả nghịch tác động lên nó; cổng đầu tiên cần gặp là **Pauli-X**, lật `|0⟩`
    thành `|1⟩` một cách tất định — chính là `NOT` lượng tử.

## Những đơn vị cơ bản

Chương trình lượng tử được dựng từ hai mảnh rất nhỏ:

- một **qubit** — vật mang thông tin lượng tử, với hai trạng thái cơ sở `|0⟩` và
  `|1⟩`;
- một **cổng** — phép toán áp lên một hay nhiều qubit.

Mọi thứ về sau trong cuốn sách (chồng chập, rối lượng tử, các thuật toán hoàn
chỉnh) đều được lắp từ hai ý tưởng này. Đó là lý do chương này là chương "đơn vị cơ
bản": trước khi làm điều gì tinh vi, ta cần biết qubit là gì và cổng thay đổi nó
ra sao.

## Qubit

Bit cổ điển là `0` hoặc `1`. Qubit có thể là một trong hai, nhưng cũng có thể ở
trạng thái **chồng chập** — tổ hợp có trọng số của cả hai. Chương 2 đã dùng điều
đó để tạo bit ngẫu nhiên. Ở đây ta tập trung vào việc đơn giản nhất mà một cổng có
thể làm: chuyển qubit gọn gàng giữa hai trạng thái cơ sở.

Ghi nhớ một con số về quy mô để dùng sau: `n` qubit được mô tả bởi `2^n` biên độ,
nên số lượng này nhân đôi với mỗi qubit thêm vào. Sự tăng trưởng đó là nguyên liệu
thô của Chương 4 và các chương sau.

## Cổng có tính khả nghịch

Một thuộc tính định hình của cổng lượng tử là chúng **khả nghịch**: thông tin không
bao giờ bị ném đi. Mỗi cổng đều có nghịch đảo khôi phục trạng thái trước đó. Điều
này tương phản với các cổng cổ điển quen thuộc — `AND` nhận hai đầu vào nhưng chỉ
trả một đầu ra, nên không thể khôi phục đầu vào từ đầu ra. Về mặt toán học, tính
khả nghịch nghĩa là cổng là một ma trận **unitary**
(xem [vector, ma trận và cổng unitary](../foundations.md)), điều Chương 4 sẽ trình
bày rõ.

- Nghịch đảo của `X` chính là `X`: `X·X = I`.
- Nghịch đảo của `H` cũng chính là `H` (Chương 4).

Ở đây `I` là phép **đơn vị** — "không làm gì". Tính khả nghịch này không phải chi
tiết vụn; nó là thứ cho phép các mạch lượng tử được dựng lên rồi hoàn tác.

!!! note "Phép đo là ngoại lệ"
    Cổng thì khả nghịch, nhưng **phép đo** thì không: nó làm sụp trạng thái và chỉ
    để lại một kết quả cổ điển duy nhất. Chính sự bất đối xứng đó khiến một thuật
    toán lượng tử được viết dưới dạng mạch khả nghịch rồi mới đo.

## Một cổng NOT cho qubit

Cổng **Pauli-X** là tương tự lượng tử của `NOT` cổ điển:

$$X\,|0\rangle = |1\rangle, \qquad X\,|1\rangle = |0\rangle$$

Nó hoán đổi vai trò của hai trạng thái cơ sở mà vẫn giữ mọi thứ khác nhất quán.
Bắt đầu ở `|0⟩`, áp `X`, qubit giờ chắc chắn là `|1⟩`. Đo nó, bạn được `1` — mọi
lần.

## Các cổng bạn sẽ gặp

`X` là cổng đầu tiên, nhưng chỉ là một trong một họ nhỏ. `H` (Chương 2) tạo chồng
chập, còn cổng **hai qubit** như `CNOT` xuất hiện cùng rối lượng tử ở Chương 5.
Điểm mấu chốt lúc này là mọi cổng đều chung hai quy tắc: nó khả nghịch, và nó đưa
qubit tới một điểm xác định trên mặt cầu Bloch.

## Vì sao kết quả là tất định

So sánh trực tiếp hai chương:

| | Chương 2 (Hadamard) | Chương 3 (Pauli-X) |
|---|---|---|
| Trạng thái sau cổng | (\|0⟩ + \|1⟩)/√2 | \|1⟩ |
| Xác suất ra `0` | 50 % | 0 % |
| Xác suất ra `1` | 50 % | 100 % |
| Đo lặp nhiều lần | lẫn lộn `0` và `1` | luôn là `1` |

Khác biệt nằm ở trạng thái, không phải ở thiết bị đo. Trạng thái xác định cho kết
quả xác định; chồng chập đều cho kết quả ngẫu nhiên. (Xuyên suốt ghi chú, "đo"
nghĩa là đo trong cơ sở tính toán `{|0⟩, |1⟩}` — chính trục Z mà các cực của mặt
cầu Bloch biểu diễn.)

## Các sơ đồ

### Mạch

![Mạch Pauli-X](../assets/ch03-pauli-x.png){ width="420" }

Từ trái sang phải: qubit `q` bắt đầu ở `|0⟩`, ô `X` lật nó, và phép đo `M` ghi kết
quả vào bit cổ điển `c`. Sơ đồ nhỏ này là toàn bộ câu chuyện của chương.

### Hai cổng `X` triệt tiêu nhau

![Hai cổng Pauli-X](../assets/ch03-pauli-x2-circuit.png){ width="420" }

Vì `X·X = I`, cổng `X` thứ hai hoàn tác cổng thứ nhất. Một mạch chỉ là các cổng
xếp theo thứ tự, và chuỗi `X, X` tương đương với không làm gì.

### Trước, sau một `X`, sau hai `X`

![Qubit trước, sau X, và sau X·X](../assets/ch03-pauli-x-bloch.png){ width="720" }

**Mặt cầu Bloch** làm phép lật trở nên trực quan:

- **Trước** — mũi tên chỉ cực bắc, `|0⟩`.
- **Sau một `X`** — mũi tên chỉ cực nam, `|1⟩`.
- **Sau hai `X`** — trở lại cực bắc, `|0⟩`.

Về hình học, `X` là một **phép quay 180° quanh trục X** của mặt cầu. Vì trạng thái
đi từ cực này sang cực kia và không bao giờ chạm đường xích đạo, nên không có chồng
chập và do đó không có ngẫu nhiên trong kết quả.

### Kết quả đo được

![1000 lần chạy X](../assets/ch03-pauli-x-counts.png){ width="420" }
![1000 lần chạy X·X](../assets/ch03-pauli-x2-counts.png){ width="420" }

Sau một `X`, cả 1000 kết quả đều là `1`; sau hai `X`, cả 1000 kết quả đều là `0`.
Tất định trong cả hai trường hợp — nguồn ngẫu nhiên duy nhất trong các chương này
đến từ cổng Hadamard.

## Ghi nhớ chính

- Qubit và cổng là hai **đơn vị cơ bản** của chương trình lượng tử.
- Cổng lượng tử **khả nghịch**; mỗi cổng đều có nghịch đảo.
- Cổng Pauli-X là tương tự lượng tử của `NOT`.
- `X|0⟩ = |1⟩` và `X|1⟩ = |0⟩`; hai cổng `X` triệt tiêu nhau (`X·X = I`).
- Áp `X` lên `|0⟩` rồi đo luôn trả về `1` — tất định, không ngẫu nhiên.
- Trên mặt cầu Bloch, `X` là phép quay 180° quanh trục X.

## Mã nguồn của chương này

Ví dụ vẽ mạch, mặt cầu Bloch trước/sau và biểu đồ số lần đo nằm trong
[`src/quantum_computing_in_action/ch03/pauli_x.py`](https://github.com/phonhay103/quantum-computing-in-action/blob/main/src/quantum_computing_in_action/ch03/pauli_x.py).
Chạy bằng `make ch03`.
