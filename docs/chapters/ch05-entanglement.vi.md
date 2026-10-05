# Chương 5 — Rối lượng tử

!!! abstract "Trong một câu"
    Hai qubit có thể chia sẻ một trạng thái chung **không thể** mô tả từng qubit
    một: cổng **CNOT** biến chồng chập thành một **trạng thái Bell**, mà hai qubit
    của nó luôn đo ra *giống nhau* — tương quan hoàn hảo, dù mỗi qubit đều ngẫu
    nhiên.

## Hai qubit cùng lúc

Chương 4 mô tả một qubit bằng hai biên độ. Hai qubit cần bốn:

$$|\psi\rangle = \alpha_{00}\,|00\rangle + \alpha_{01}\,|01\rangle
  + \alpha_{10}\,|10\rangle + \alpha_{11}\,|11\rangle$$

Đây là **tích tensor** của hai không gian một-qubit (xem
[nhiều qubit và tích tensor](../foundations.md)). Nhãn đọc từ trái sang phải, nên
`|01⟩` nghĩa là qubit thứ nhất là `0` và qubit thứ hai là `1`. Như trước, biên độ
không phải xác suất — quy tắc Born bình phương chúng.

`n` qubit có `2^n` biên độ, nên không gian tăng rất nhanh. Đó cũng chính là mức
tăng mà Chương 4 đánh dấu là nguyên liệu thô của thuật toán lượng tử.

## Cổng CNOT

Thành phần mới là một cổng tác động lên **hai** qubit: **controlled-NOT**
(`CNOT`). Nó có một qubit **điều khiển** và một qubit **đích**, và lật qubit đích
đúng khi qubit điều khiển bằng `1`.

Ta viết trạng thái hai qubit là `|c t⟩` với **điều khiển trước** và **đích sau** —
thứ tự quen thuộc trong giáo trình. Bảng chân trị khi đó là:

| Đầu vào <code>\|c t⟩</code> | Đầu ra <code>\|c t⟩</code> |
|---------|--------|
| <code>\|00⟩</code> | <code>\|00⟩</code> |
| <code>\|01⟩</code> | <code>\|01⟩</code> |
| <code>\|10⟩</code> | <code>\|11⟩</code> |
| <code>\|11⟩</code> | <code>\|10⟩</code> |

Trong `|10⟩`, điều khiển bằng `1`, nên đích bị lật và trạng thái thành `|11⟩`;
khi điều khiển bằng `0` (`|00⟩`, `|01⟩`) thì không có gì xảy ra.

Như mọi cổng lượng tử, `CNOT` **khả nghịch** và **unitary**. Trong thứ tự cơ sở
`|00⟩, |01⟩, |10⟩, |11⟩`, ma trận của nó là

$$CNOT = \begin{bmatrix}1&0&0&0\\ 0&1&0&0\\ 0&0&0&1\\ 0&0&1&0\end{bmatrix}$$

Áp nó hai lần cho ma trận đơn vị, nên `CNOT·CNOT = I`.

!!! note "Lưu ý về thứ tự bit (Qiskit)"
    Qiskit lưu biên độ theo thứ tự bit *ngược lại* (little-endian): trong nhãn
    `Statevector`, ký tự bên phải là qubit 0. Vì vậy ví dụ gọi `cx(1, 0)` — điều
    khiển qubit 1, đích qubit 0 — để có quy ước điều-khiển-trước dùng ở đây. Nhãn
    `|q1 q0⟩` in ra đã đặt điều khiển ở trước, nên không có gì khác thay đổi.

## Trạng thái Bell

Rối lượng tử xuất hiện khi `CNOT` tác động lên một chồng chập. Bắt đầu với cả hai
qubit ở `|00⟩`, áp Hadamard lên **điều khiển**, rồi `CNOT`:

$$H(\text{điều khiển}):\quad \frac{|00\rangle + |10\rangle}{\sqrt{2}}
  \quad\xrightarrow{\;CNOT\;}\quad \frac{|00\rangle + |11\rangle}{\sqrt{2}}$$

Kết quả là một **trạng thái Bell** (còn gọi là cặp EPR). Nó không thể viết thành
`|a⟩|b⟩` với bất kỳ trạng thái một-qubit `a`, `b` nào — đó đúng là ý nghĩa của
"rối".

Có bốn trạng thái Bell, là các trạng thái hai-qubit "rối cực đại":

$$\frac{|00\rangle \pm |11\rangle}{\sqrt{2}}, \qquad
  \frac{|01\rangle \pm |10\rangle}{\sqrt{2}}$$

Trạng thái trên là cái thứ nhất; các cái còn lại có được bằng cách thêm `Z` hoặc
`X` trước `CNOT`.

## Đo một cặp rối

Đo trạng thái Bell và một điều lạ xảy ra. Các kết quả khả dĩ chỉ là `00` và `11`,
mỗi cái với xác suất 50%; `01` và `10` **không bao giờ** xuất hiện.

- Từng qubit riêng lẻ là một đồng xu hoàn hảo: chỉ đo qubit 0 thì được `0` hoặc
  `1` theo tỉ lệ 50/50; qubit 1 cũng vậy.
- Nhưng hai kết quả luôn **bằng nhau**. Tính ngẫu nhiên là thật, nhưng nó được
  *chia sẻ*: hai qubit tương quan với nhau.

Tương quan này không phụ thuộc khoảng cách. Nếu hai qubit bị tách xa, phép đo đầu
tiên vẫn dường như "quyết định" phép đo thứ hai — chính là "hành động kỳ lạ ở
khoảng cách" mà tên chương nhắc tới.

!!! warning "Rối lượng tử không truyền được thông điệp"
    Dễ tưởng rằng phép đo thứ nhất *báo* cho qubit thứ hai biết phải làm gì, nhanh
    hơn ánh sáng. Không phải vậy. Bạn không thể chọn kết quả mình nhận được — nó
    ngẫu nhiên — và để so sánh hai kết quả, hai bên vẫn phải gửi thông tin cổ điển
    cho nhau, nhanh nhất là bằng tốc độ ánh sáng. Rối lượng tử cho *tương quan*,
    không phải truyền thông.

## Trạng thái tích so với trạng thái rối

Sự tương phản với tính ngẫu nhiên thường là điểm chính của chương. Áp Hadamard lên
**mỗi** qubit và không dùng `CNOT`:

$$H(0), H(1):\quad \frac{|00\rangle + |01\rangle + |10\rangle + |11\rangle}{2}$$

Giờ cả bốn kết quả đều xuất hiện, mỗi cái khoảng 25% — y hệt việc tung hai đồng
xu độc lập. Đây là một **trạng thái tích**: biết qubit 0 không cho bạn biết gì về
qubit 1.

Một phép thử gọn gàng phân biệt hai trường hợp. Xếp bốn biên độ thành ma trận 2×2.
Trạng thái tích cho ma trận **hạng 1** (mọi hàng là bội của hàng kia); trạng thái
Bell cho **hạng 2**. Các [ma trận hệ số](#ma-tran-he-so) bên dưới cho thấy hai cái
cạnh nhau.

| | Hai qubit `H` (tích) | Trạng thái Bell (rối) |
|---|---|---|
| Kết quả | cả bốn | chỉ `00`, `11` |
| Từng qubit riêng | 50/50 | 50/50 |
| Kết quả chung | độc lập | tương quan hoàn hảo |
| Ma trận biên độ | hạng 1 | hạng 2 |

Cả hai hệ đều trông "ngẫu nhiên" nếu bạn chỉ liếc một qubit. Khác biệt nằm ở các
**tương quan**.

## Các sơ đồ

### Mạch Bell

![Mạch trạng thái Bell](../assets/ch05-bell-circuit.png){ width="460" }

Qubit **điều khiển** nhận một Hadamard, rồi `CNOT` tương quan nó với qubit
**đích**, và cả hai được đo. Mạch nhỏ này là cách chuẩn để *tạo* rối lượng tử.

### Mạch CNOT

![Mạch CNOT](../assets/ch05-cnot-circuit.png){ width="460" }

`CNOT` trần. Một mình nó không bao giờ tạo chồng chập — nó chỉ tương quan các qubit
vốn đã ở trong chồng chập.

### Đo ra gì (trạng thái Bell)

![1000 lần chạy trạng thái Bell](../assets/ch05-bell-counts.png){ width="420" }

Chỉ hai cột `00` và `11` có chiều cao. Hai kết quả còn lại hoàn toàn vắng mặt —
dấu hiệu thị giác của rối lượng tử.

### Đo ra gì (hai qubit độc lập)

![1000 lần chạy hai qubit H độc lập](../assets/ch05-independent-counts.png){ width="420" }

Hai Hadamard độc lập lấp đầy cả bốn cột gần như đều nhau. Mỗi qubit ngẫu nhiên,
nhưng các kết quả **không tương quan**.

### Độc lập so với rối

![Qubit độc lập so với rối](../assets/ch05-bell-vs-independent.png){ width="640" }

Cùng bốn kết quả, đặt cạnh nhau. Các qubit độc lập trải đều; cặp rối dồn về hai
kết quả khớp nhau.

### Ma trận hệ số

![Trạng thái tích so với trạng thái rối](../assets/ch05-amplitude-matrices.png){ width="640" }

Xếp các biên độ thành ma trận 2×2 khiến khác biệt trở nên trực quan. Trạng thái
tích cho ma trận hạng 1 (mọi phần tử `0.50`); trạng thái Bell cho ma trận chéo hạng
2. Hạng 1 nghĩa là "phân tích được thành tích"; hạng 2 nghĩa là "rối".

## Điểm cốt lõi

- Hai qubit sống trong không gian bốn chiều sinh bởi `|00⟩, |01⟩, |10⟩, |11⟩`.
- `CNOT` lật **đích** khi **điều khiển** bằng `1`; nó khả nghịch và unitary.
- `H` rồi `CNOT` tạo trạng thái Bell `(|00⟩ + |11⟩)/√2`.
- Đo trạng thái Bell chỉ cho `00` hoặc `11` — kết quả tương quan hoàn hảo.
- Từng qubit riêng vẫn 50/50, nên tính ngẫu nhiên nằm ở các *tương quan*.
- Rối lượng tử cho tương quan, **không** truyền thông nhanh hơn ánh sáng.
- Hai qubit `H` độc lập cho **trạng thái tích** (cả bốn kết quả, hạng 1); trạng
  thái Bell là **rối** (hạng 2).

## Mã nguồn của chương này

Ví dụ vẽ mạch, biểu đồ số lần đo, so sánh và các ma trận hệ số nằm trong
[`src/quantum_computing_in_action/ch05/entanglement.py`](https://github.com/phonhay103/quantum-computing-in-action/blob/main/src/quantum_computing_in_action/ch05/entanglement.py),
với các helper tích tensor và CNOT trong
[`src/quantum_computing_in_action/ch05/states.py`](https://github.com/phonhay103/quantum-computing-in-action/blob/main/src/quantum_computing_in_action/ch05/states.py).
Chạy bằng `make ch05`.
