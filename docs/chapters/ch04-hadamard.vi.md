# Chương 4 — Cổng Hadamard

!!! abstract "Trong một câu"
    Cổng **Hadamard** biến một qubit xác định thành chồng chập đều, và — vì nó là
    nghịch đảo của chính nó — áp dụng lần thứ hai sẽ **xoá chồng chập** và đưa
    qubit trở về `|0⟩`.

## Cổng tạo ra chồng chập

Chương 3 dùng cổng Pauli-X, vốn chỉ di chuyển qubit giữa hai cực `|0⟩` và `|1⟩`.
Cổng **Hadamard** (`H`) thì khác: nó lấy một trạng thái xác định và đặt nó đúng
vào *khoảng giữa* hai cực.

$$H\,|0\rangle = \frac{|0\rangle + |1\rangle}{\sqrt{2}}, \qquad
  H\,|1\rangle = \frac{|0\rangle - |1\rangle}{\sqrt{2}}$$

Áp dụng lên `|0⟩`, qubit trở thành hỗn hợp đều: đo nó, bạn nhận `0` hoặc `1` với
xác suất bằng nhau. Đây chính là trạng thái chồng chập mà Chương 2 dùng để tạo bit
ngẫu nhiên — Chương 4 xem xét bản thân cổng kỹ hơn.

## `H` là nghịch đảo của chính nó

Mọi cổng lượng tử đều có tính thuận nghịch, nhưng `H` có một tính chất đặc biệt: nó
là **nghịch đảo của chính nó**,

$$H \cdot H = I$$

trong đó `I` là toán tử đơn vị (phép "không làm gì"). Hai cổng Hadamard liên tiếp
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

!!! info "Đọc hai sơ đồ cùng nhau"
    Kết quả một-`H` và hai-`H` là hai nửa của cùng một ý tưởng. Nếu `H` quay trạng
    thái 90° trên mặt cầu Bloch, thì một `H` hạ cánh xuống đường xích đạo (ngẫu
    nhiên), còn hai `H` quay tổng cộng 180°, trở lại cực (xác định).

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

### Kết quả đo được

![1000 lần chạy H](../assets/ch04-hadamard-counts.png){ width="420" }
![1000 lần chạy H·H](../assets/ch04-hadamard2-counts.png){ width="420" }

Sau một `H`, hai cột gần bằng nhau. Sau hai `H`, một cột chứa toàn bộ 1000 kết quả
còn cột kia trống — không còn chút ngẫu nhiên nào.

## Ghi nhớ chính

- Cổng Hadamard **tạo** chồng chập đều từ `|0⟩`.
- `H` là **nghịch đảo của chính nó**: `H·H = I`.
- Một `H` cho kết quả ngẫu nhiên; hai `H` cho kết quả tất định `0`.
- Trên mặt cầu Bloch, `H` quay trạng thái về phía đường xích đạo (rồi trở lại).

## Mã nguồn của chương này

Ví dụ vẽ mạch, mặt cầu Bloch và biểu đồ số lần đo nằm trong
[`src/quantum_computing_in_action/ch04/hadamard.py`](https://github.com/phonhay103/quantum-computing-in-action/blob/main/src/quantum_computing_in_action/ch04/hadamard.py).
Chạy bằng `make ch04`.
