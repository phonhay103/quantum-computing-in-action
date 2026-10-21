# Chương 5 — Rối lượng tử

!!! abstract "Trong một câu"
    Một cổng **CNOT**, khi được áp lên một chồng chập hai-qubit thích hợp, biến
    nó thành một **trạng thái Bell** — một trạng thái chung trong đó hai qubit
    luôn đo ra *giống nhau*, và không thể mô tả từng qubit một.

## Hai qubit cùng lúc

Chương 4 mô tả một qubit đơn bằng hai biên độ; một cặp qubit thì cần bốn:

$$|\psi\rangle = \alpha_{00}\,|00\rangle + \alpha_{01}\,|01\rangle
  + \alpha_{10}\,|10\rangle + \alpha_{11}\,|11\rangle$$

Xét về mặt hình thức, trạng thái như vậy nằm trong **tích tensor** của hai
không gian một-qubit riêng biệt — một cấu trúc được trình bày chi tiết ở trang
nền tảng (xem [nhiều qubit và tích tensor](../foundations.md)). Các nhãn gồm
bốn ký tự được đọc từ trái sang phải, nên ket `|01⟩` cho biết qubit thứ nhất
mang giá trị `0` trong khi qubit thứ hai mang giá trị `1`. Như trong trường hợp
một qubit, các biên độ không tự chúng là xác suất — chính quy tắc Born bình
phương chúng để cho ra các số liệu đo lường.

Với `n` qubit, việc mô tả trạng thái đòi hỏi `2^n` biên độ, nên không gian tăng
rất nhanh với mỗi qubit được thêm vào. Đây chính là mức tăng theo hàm mũ mà
Chương 4 đã đánh dấu là nguyên liệu thô làm nền cho sức mạnh của các thuật toán
lượng tử.

## Cổng CNOT

Thành phần mới của chương này là một cổng tác động lên **hai** qubit đồng thời:
cổng **controlled-NOT** (`CNOT`). Cổng này phân biệt một qubit **điều khiển**
với một qubit **đích**, và chỉ lật qubit đích đúng khi qubit điều khiển mang
giá trị `1`; mỗi khi điều khiển bằng `0`, qubit đích được giữ nguyên hoàn toàn.

Ta viết trạng thái hai qubit là `|c t⟩`, với **điều khiển trước** và **đích
sau** — thứ tự quen thuộc trong giáo trình. Bảng chân trị khi đó là:

| Đầu vào <code>\|c t⟩</code> | Đầu ra <code>\|c t⟩</code> |
|---------|--------|
| <code>\|00⟩</code> | <code>\|00⟩</code> |
| <code>\|01⟩</code> | <code>\|01⟩</code> |
| <code>\|10⟩</code> | <code>\|11⟩</code> |
| <code>\|11⟩</code> | <code>\|10⟩</code> |

Trong trạng thái `|10⟩`, điều khiển bằng `1`, nên qubit đích bị lật và đầu ra
là `|11⟩`; trong `|11⟩`, cùng thao tác đó trả cặp trạng thái về `|10⟩`. Khi
điều khiển bằng `0` (`|00⟩`, `|01⟩`) thì không có gì xảy ra: trạng thái đi qua
cổng và không bị thay đổi.

Như mọi cổng lượng tử, `CNOT` **khả nghịch** và **unita**. Trong thứ tự cơ sở
`|00⟩, |01⟩, |10⟩, |11⟩`, ma trận của nó là

$$CNOT = \begin{bmatrix}1&0&0&0\\ 0&1&0&0\\ 0&0&0&1\\ 0&0&1&0\end{bmatrix}$$

Áp cổng hai lần cho ra ma trận đơn vị, nên `CNOT·CNOT = I`; nói cách khác, lần
áp thứ hai triệt tiêu hiệu quả của lần áp thứ nhất.

!!! note "Lưu ý về thứ tự bit (Qiskit)"
    Qiskit lưu biên độ theo thứ tự bit *ngược lại* (little-endian): trong nhãn
    `Statevector`, ký tự bên phải là qubit 0, tương phản với thứ tự dùng để viết
    các trạng thái ở trên. Vì vậy mẫu ví dụ gọi `cx(1, 0)` — điều khiển qubit 1,
    đích qubit 0 — nhằm khớp với quy ước điều-khiển-trước được dùng trong chương
    này. Vì các nhãn `|q1 q0⟩` in ra đã đặt điều khiển ở trước nên không có gì
    khác thay đổi: kết quả hiển thị khớp chính xác với phần toán đã trình bày.

## Trạng thái Bell

Rối lượng tử xuất hiện khi `CNOT` tác động lên một chồng chập, chứ không phải
lên một trạng thái cơ sở đơn lẻ. Bắt đầu với cả hai qubit ở `|00⟩`, áp
Hadamard lên **điều khiển**, rồi áp `CNOT`:

$$H(\text{điều khiển}):\quad \frac{|00\rangle + |10\rangle}{\sqrt{2}}
  \quad\xrightarrow{\;CNOT\;}\quad \frac{|00\rangle + |11\rangle}{\sqrt{2}}$$

Kết quả của quy trình hai bước này là một **trạng thái Bell** (còn gọi là cặp
EPR). Nó không thể viết thành dạng tích `|a⟩|b⟩` với bất kỳ trạng thái
một-qubit `a`, `b` nào, và chính điều bất khả tách này là ý nghĩa của chữ
"rối".

Có bốn trạng thái Bell, và gộp lại chúng bao trọn các trạng thái hai-qubit
"rối cực đại":

$$\frac{|00\rangle \pm |11\rangle}{\sqrt{2}}, \qquad
  \frac{|01\rangle \pm |10\rangle}{\sqrt{2}}$$

Trạng thái thu được ở trên là cái thứ nhất trong bốn; ba cái còn lại có được
bằng cách chèn một cổng `Z` hoặc `X` trước `CNOT`, vốn biến đổi chồng chập
Hadamard mà CNOT rồi sẽ tương quan.

## Đo một cặp rối

Khi trạng thái Bell được đo, một điều đáng chú ý xảy ra. Các kết quả khả dĩ chỉ
là `00` và `11`, mỗi cái với xác suất 50%; các kết quả `01` và `10` **không bao
giờ** xuất hiện.

- Xét riêng từng qubit thì qubit đó giống một đồng xu hoàn hảo: việc đo riêng
  qubit 0 cho ra `0` hoặc `1` với tỉ lệ 50/50, và điều tương tự cũng đúng với
  qubit 1.
- Tuy vậy, hai kết quả đo luôn **bằng nhau**. Tính ngẫu nhiên là thật, nhưng nó
  được *chia sẻ* giữa hai qubit: các kết quả tương quan với nhau.

Tương quan này không phụ thuộc khoảng cách giữa các qubit. Nếu hai qubit bị
đưa ra xa nhau, phép đo đầu tiên vẫn dường như "quyết định" phép đo thứ hai —
chính là "hành động kỳ lạ ở khoảng cách" mà tên chương nhắc tới.

!!! warning "Rối lượng tử không truyền được thông điệp"
    Dễ tưởng rằng phép đo thứ nhất *báo* cho qubit thứ hai biết phải làm gì,
    nhanh hơn ánh sáng. Không phải vậy. Không nhà thí nghiệm nào có thể chọn
    được kết quả thu được — nó hoàn toàn ngẫu nhiên — và để so sánh hai kết
    quả, thông tin cổ điển vẫn phải được gửi giữa hai bên, nhanh nhất là bằng
    tốc độ ánh sáng. Vì vậy rối lượng tử cho *tương quan*, không phải truyền
    thông.

## Trạng thái tích so với trạng thái rối {#trang-thai-tich-so-voi-trang-thai-roi}

Sự tương phản với tính ngẫu nhiên thông thường là điểm chính của chương. Áp
Hadamard lên **mỗi** qubit và không dùng `CNOT`:

$$H(0), H(1):\quad \frac{|00\rangle + |01\rangle + |10\rangle + |11\rangle}{2}$$

Giờ cả bốn kết quả đều xuất hiện, mỗi cái khoảng 25% — đúng như mẫu hình kỳ
vọng từ việc tung hai đồng xu độc lập. Đây là một **trạng thái tích**: biết giá
trị của qubit 0 không hề cung cấp thông tin nào về qubit 1.

Một phép thử gọn gàng phân biệt hai trường hợp. Xếp bốn biên độ thành ma trận
2×2. Trạng thái tích cho ma trận **hạng 1** — mọi hàng là bội của hàng kia,
nên trạng thái tách ra được thành tích của hai thành phần. Trạng thái Bell cho
**hạng 2** — các hàng độc lập với nhau, và do đó trạng thái không tách được.

Hạng là số hàng độc lập; với ma trận 2×2 nó chỉ là 1 hoặc 2. Con số này chính
là **hạng Schmidt** của trạng thái: 1 là trạng thái tích, 2 là rối. Các
[ma trận hệ số](#ma-tran-he-so) bên dưới cho thấy hai trường hợp cạnh nhau.

Bảng dưới đây đặt hai trạng thái đối chọi nhau, mỗi hàng một câu hỏi; hàng cuối
là phép kiểm tra mà các sơ đồ cuối chương minh hoạ trực quan:

| | Hai qubit `H` (tích) | Trạng thái Bell (rối) |
|---|---|---|
| Kết quả | cả bốn | chỉ `00`, `11` |
| Từng qubit riêng | 50/50 | 50/50 |
| Kết quả chung | độc lập | tương quan hoàn hảo |
| Ma trận biên độ | hạng 1 | hạng 2 |

Cả hai hệ đều trông "ngẫu nhiên" khi chỉ xét riêng một qubit; khác biệt nằm ở
các **tương quan** giữa các kết quả.

??? question "Tự kiểm tra — từng qubit riêng đều 50/50 ở cả hai trạng thái. Một thí nghiệm nào đó phân biệt được chúng?"
    Cần đếm xem hai kết quả đo *khớp nhau* bao nhiêu lần. Với hai qubit `H` độc
    lập, cả bốn kết quả chung đều ngang nhau, nên hai kết quả khớp xảy ra khoảng
    một nửa số lần (`00` và `11` là 2 trong 4 kết quả). Với trạng thái Bell, tỉ
    lệ khớp là 100% — `00` và `11` là *hai kết quả duy nhất*. Riêng một con số
    đó đã là khác biệt giữa hai đồng xu ngẫu nhiên và một đồng xu chia sẻ.

## Các sơ đồ {#cac-so-do}

### Mạch Bell

![Mạch trạng thái Bell](../assets/ch05-bell-circuit.png){ width="460" }

Qubit **điều khiển** nhận một Hadamard, `CNOT` rồi tương quan nó với qubit
**đích**, và cả hai qubit được đo. Mạch nhỏ này là quy trình chuẩn để *tạo*
rối lượng tử từ một cặp vốn chưa tương quan.

### Mạch CNOT

![Mạch CNOT](../assets/ch05-cnot-circuit.png){ width="460" }

Cổng `CNOT` trần, xét riêng lẻ. Một mình nó không bao giờ tạo chồng chập — nó
chỉ tương quan các qubit vốn đã ở trong chồng chập.

### Đo ra gì (trạng thái Bell)

![1000 lần chạy trạng thái Bell](../assets/ch05-bell-counts.png){ width="420" }

Chỉ hai cột `00` và `11` có chiều cao; hai kết quả còn lại hoàn toàn vắng mặt.
Sự vắng mặt này là dấu hiệu thị giác của rối lượng tử.

### Đo ra gì (hai qubit độc lập)

![1000 lần chạy hai qubit H độc lập](../assets/ch05-independent-counts.png){ width="420" }

Hai Hadamard độc lập lấp đầy cả bốn cột gần như đều nhau. Mỗi qubit ngẫu nhiên
riêng lẻ, nhưng các kết quả **không tương quan**.

### Độc lập so với rối

![Qubit độc lập so với rối](../assets/ch05-bell-vs-independent.png){ width="640" }

Cùng bốn kết quả, đặt cạnh nhau. Các qubit độc lập trải đều trên mọi khả năng,
trong khi cặp rối dồn về hai kết quả khớp nhau.

### Ma trận hệ số {#ma-tran-he-so}

![Trạng thái tích so với trạng thái rối](../assets/ch05-amplitude-matrices.png){ width="640" }

Xếp các biên độ thành ma trận 2×2 khiến khác biệt trở nên trực quan. Trạng thái
tích cho ma trận hạng 1 (mọi phần tử `0.50`); trạng thái Bell cho ma trận chéo
hạng 2. Hạng 1 nghĩa là trạng thái phân tích được thành tích; hạng 2 nghĩa là
trạng thái rối.

## Những điều cần nhớ

- Hai qubit sống trong không gian bốn chiều sinh bởi `|00⟩, |01⟩, |10⟩, |11⟩`, với một biên độ cho mỗi trạng thái cơ sở.
- `CNOT` lật **đích** đúng khi **điều khiển** bằng `1`; cổng này khả nghịch và unita.
- `H` rồi `CNOT` tạo trạng thái Bell `(|00⟩ + |11⟩)/√2`.
- Đo trạng thái Bell chỉ cho `00` hoặc `11` — kết quả tương quan hoàn hảo.
- Từng qubit riêng vẫn 50/50, nên tính ngẫu nhiên nằm ở các *tương quan* thay vì ở riêng qubit nào.
- Rối lượng tử cho tương quan, **không** truyền thông nhanh hơn ánh sáng: việc so sánh hai kết quả vẫn cần nhắn tin cổ điển.
- Hai qubit `H` độc lập cho **trạng thái tích** (cả bốn kết quả, hạng 1); trạng thái Bell là **rối** (hạng 2).

## Mã nguồn của chương này

Ví dụ vẽ mạch, biểu đồ số lần đo, so sánh và các ma trận hệ số nằm trong
[`src/quantum_computing_in_action/ch05/entanglement.py`](https://github.com/phonhay103/quantum-computing-in-action/blob/main/src/quantum_computing_in_action/ch05/entanglement.py),
với các helper tích tensor và CNOT trong
[`src/quantum_computing_in_action/ch05/states.py`](https://github.com/phonhay103/quantum-computing-in-action/blob/main/src/quantum_computing_in_action/ch05/states.py).
Cả phần trình bày có thể tái tạo cục bộ bằng cách chạy `make ch05`.
