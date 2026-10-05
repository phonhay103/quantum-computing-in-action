# Chương 4 — Chồng chập

!!! abstract "Trong một câu"
    **Chồng chập** là khi qubit ở tổ hợp có trọng số của `|0⟩` và `|1⟩` cùng lúc;
    cổng **Hadamard** tạo ra nó, và — vì `H` là nghịch đảo của chính nó — áp `H`
    lần thứ hai sẽ **xoá** nó đưa qubit về `|0⟩`.

## Chồng chập là gì?

Bit cổ điển chắc chắn là `0` hoặc chắc chắn là `1`. Qubit có thể ở *tổ hợp* của cả
hai trạng thái cơ sở cùng một lúc:

$$|\psi\rangle = \alpha\,|0\rangle + \beta\,|1\rangle$$

Các số `α` và `β` được gọi là **biên độ**. Chúng không phải xác suất — có thể âm,
thậm chí là số phức — nhưng bình phương độ lớn của chúng sẽ cho xác suất (xem
[số phức và pha](../foundations.md)).

Điều khiến chuyện này quan trọng là quy mô. Hai bit cổ điển chỉ giữ được một trong
bốn giá trị tại một thời điểm; hai *qubit* có thể giữ tổ hợp có trọng số của cả bốn
(trạng thái chung của chúng được dựng từ **tích tensor** của hai qubit). Thêm qubit,
số biên độ tăng **theo hàm mũ**, trong khi số qubit chỉ tăng tuyến tính. Đó là
nguyên liệu thô mà mọi thuật toán lượng tử khai thác.

!!! note "Bạn không thể đọc hết chúng"
    Có `2^n` biên độ **không** có nghĩa là bạn đọc được `2^n` giá trị cùng lúc.
    Phép đo chỉ trả về một kết quả duy nhất; chồng chập cho thuật toán nhiều biên
    độ để thao tác, nhưng việc của thuật toán là lái các xác suất — qua giao thoa —
    sao cho kết quả bạn *đọc được* chính là đáp án.

Chồng chập còn phụ thuộc **cơ sở**: cùng một trạng thái có thể "xác định" trong cơ
sở này nhưng "chồng chập" trong cơ sở khác. Xuyên suốt ghi chú, cơ sở là
`{|0⟩, |1⟩}` trừ khi nói khác.

## Trạng thái như một vector

Vì một qubit có đúng hai biên độ, ta có thể viết trạng thái của nó thành **vector
cột**:

$$|\psi\rangle = \begin{bmatrix}\alpha\\ \beta\end{bmatrix}, \qquad
  |0\rangle = \begin{bmatrix}1\\ 0\end{bmatrix}, \qquad
  |1\rangle = \begin{bmatrix}0\\ 1\end{bmatrix}$$

Đây là bức tranh *vector trạng thái*: trạng thái là một điểm trong không gian hai
chiều, và **quy tắc Born** biến các phần tử thành xác suất đo:

$$P(0) = |\alpha|^2, \qquad P(1) = |\beta|^2, \qquad |\alpha|^2 + |\beta|^2 = 1$$

Phương trình cuối là **chuẩn hoá**: tổng xác suất phải bằng 1, nên các biên độ bị
ràng buộc — về độ lớn bình phương, chúng cộng lại đúng bằng 1.

## Cổng như những ma trận

Nếu trạng thái là một vector thì cổng là một **ma trận** nhân vào nó. Một quy tắc
đúng cho mọi cổng một-qubit:

$$|\psi'\rangle = U\,|\psi\rangle$$

Cổng **Pauli-X** ở Chương 3 trở thành

$$X = \begin{bmatrix}0 & 1\\ 1 & 0\end{bmatrix}$$

do đó

$$X\begin{bmatrix}\alpha\\ \beta\end{bmatrix} =
  \begin{bmatrix}\beta\\ \alpha\end{bmatrix}$$

`X` chỉ đơn giản **hoán đổi hai biên độ** — đúng bằng phép "lật" ta thấy trên mặt
cầu Bloch.

## Áp X lên một chồng chập

Bức tranh ma trận giúp thấy rõ một điểm tinh tế. Lấy chồng chập đều ở Chương 2 rồi
áp `X`:

$$X\,\frac{1}{\sqrt{2}}\begin{bmatrix}1\\ 1\end{bmatrix} =
  \frac{1}{\sqrt{2}}\begin{bmatrix}1\\ 1\end{bmatrix}$$

Trạng thái **không đổi**. Chồng chập đều đối xứng, nên hoán đổi hai biên độ của nó
không thay đổi gì. `X` lật các trạng thái xác định, nhưng để yên chồng chập đặc
biệt này — một màn xem trước nhỏ cho thấy *cùng một* cổng có thể hành xử rất khác
nhau tuỳ theo trạng thái.

## Cổng Hadamard

Cổng **Hadamard** là cổng *tạo* ra chồng chập. Ma trận của nó là

$$H = \frac{1}{\sqrt{2}}\begin{bmatrix}1 & 1\\ 1 & -1\end{bmatrix}$$

Áp lên `|0⟩`:

$$H\,|0\rangle = \frac{1}{\sqrt{2}}\begin{bmatrix}1\\ 1\end{bmatrix}
  = \frac{|0\rangle + |1\rangle}{\sqrt{2}}$$

hỗn hợp đều, nên đo sẽ ra `0` hoặc `1` với xác suất mỗi bên 50%. Áp lên `|1⟩` cho
hỗn hợp đều *kia*, chỉ khác ở dấu trừ:

$$H\,|1\rangle = \frac{|0\rangle - |1\rangle}{\sqrt{2}} = |-\rangle$$

Dấu trừ đó là một **pha tương đối** (xem [số phức và pha](../foundations.md)). Cả
hai trạng thái đều đo 50/50, nhưng chúng khác nhau — và sự khác biệt đó chính là
thứ khiến giao thoa khả thi.

## `H` là nghịch đảo của chính nó

Mọi cổng lượng tử đều khả nghịch, nhưng `H` có tính chất đặc biệt: nó là **nghịch
đảo của chính nó**, viết dưới dạng ma trận là

$$H \cdot H = \begin{bmatrix}1 & 0\\ 0 & 1\end{bmatrix} = I$$

trong đó `I` là ma trận đơn vị (phép "không làm gì"). Hai cổng Hadamard liên tiếp
không làm gì cả: cổng thứ hai *hoàn tác* đúng những gì cổng thứ nhất đã làm.

$$H\,H\,|0\rangle = |0\rangle$$

Vậy cùng một cổng vừa **tạo** vừa **xoá** chồng chập, tuỳ theo nó được áp dụng một
số lẻ hay số chẵn lần.

## Một `H` so với hai `H`

| | Một `H` | Hai `H` (`H·H`) |
|---|---|---|
| Trạng thái | (\|0⟩ + \|1⟩)/√2 | \|0⟩ |
| Có chồng chập? | có | không |
| Xác suất ra `0` | 50 % | 100 % |
| Xác suất ra `1` | 50 % | 0 % |
| Đo lặp nhiều lần | lẫn lộn `0` và `1` | luôn là `0` |

Sự tương phản này là điểm cốt lõi của chương: **áp dụng một cổng hai lần có thể đưa
bạn trở lại điểm xuất phát**, và tính ngẫu nhiên xuất hiện sau một `H` sẽ biến mất
sau cái thứ hai.

!!! info "Sự triệt tiêu đến từ đâu — giao thoa"
    Kết quả một-`H` và hai-`H` là hai nửa của cùng một ý tưởng. Cổng `H` thứ hai cho
    trạng thái hai đường dẫn tới mỗi kết quả, và dấu trừ trong `H|1⟩` khiến một số
    đường đó hướng ngược nhau. Với `|1⟩`, hai đóng góp triệt tiêu; với `|0⟩`, chúng
    cộng hưởng — nên `H·H|0⟩ = |0⟩`. Trên mặt cầu Bloch, một `H` đưa trạng thái từ
    cực xuống đường xích đạo (ngẫu nhiên); `H` thứ hai đưa nó trở lại cực (xác
    định). Theo ngôn ngữ ma trận, chuyến khứ hồi đó đơn giản là `H·H = I`.

## Các sơ đồ

### Mạch một `H`

![Mạch Hadamard đơn](../assets/ch04-hadamard-circuit.png){ width="420" }

Qubit `q` bắt đầu ở `|0⟩`, đi qua một cổng `H`, và phép đo `M` ghi một giá trị ngẫu
nhiên `0` hoặc `1` vào bit cổ điển `c`.

### Mạch `H·H`

![Hai cổng Hadamard](../assets/ch04-hadamard2-circuit.png){ width="420" }

Cùng mạch đó với **cổng `H` thứ hai**. Hai cổng triệt tiêu nhau, nên `M` giờ luôn
đọc ra `0`.

### Trên mặt cầu Bloch

![|0>, sau H, và sau H·H](../assets/ch04-hadamard-bloch.png){ width="640" }

- **`|0⟩`** — cực bắc, điểm xuất phát.
- **sau `H`** — nằm trên đường xích đạo: chồng chập cực đại, ngẫu nhiên 50/50.
- **sau `H·H`** — trở lại cực bắc: chồng chập đã biến mất.

### Các cổng dưới dạng ma trận

![X, H và H·H dưới dạng ma trận](../assets/ch04-gate-matrices.png){ width="640" }

Hai ô `X` và `H` cho thấy ma trận của hai cổng; ô `H·H` là ma trận đơn vị — bằng
chứng trực quan rằng hai Hadamard triệt tiêu nhau.

### Kết quả đo được

![1000 lần chạy H](../assets/ch04-hadamard-counts.png){ width="420" }
![1000 lần chạy H·H](../assets/ch04-hadamard2-counts.png){ width="420" }

Sau một `H`, hai cột gần bằng nhau. Sau hai `H`, một cột chứa toàn bộ 1000 kết quả
còn cột kia trống — không còn chút ngẫu nhiên nào.

## Ghi nhớ chính

- Trạng thái qubit là một **vector** `[α, β]`; quy tắc Born biến nó thành xác suất.
- Cổng là một **ma trận** nhân vào vector trạng thái.
- `X` hoán đổi hai biên độ; `H` biến `|0⟩` thành chồng chập đều.
- `H` là **nghịch đảo của chính nó**: `H·H = I`.
- Một `H` cho kết quả ngẫu nhiên; hai `H` cho kết quả tất định `0`.
- Chồng chập cho phép vài qubit mô tả số biên độ tăng theo hàm mũ.

## Mã nguồn của chương này

Ví dụ vẽ mạch, mặt cầu Bloch, biểu đồ số lần đo và ma trận cổng nằm trong
[`src/quantum_computing_in_action/ch04/hadamard.py`](https://github.com/phonhay103/quantum-computing-in-action/blob/main/src/quantum_computing_in_action/ch04/hadamard.py),
với các hàm ma trận ở
[`src/quantum_computing_in_action/ch04/matrices.py`](https://github.com/phonhay103/quantum-computing-in-action/blob/main/src/quantum_computing_in_action/ch04/matrices.py).
Chạy bằng `make ch04`.
