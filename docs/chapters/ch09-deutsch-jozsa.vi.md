# Chương 9 — Thuật toán Deutsch–Jozsa

!!! abstract "Trong một câu"
    Nếu một hàm được hứa là **hằng số** hoặc **cân bằng**, chỉ một truy vấn lượng
    tử là đủ để quyết định — trong khi cách kiểm tra cổ điển có thể cần tới
    `2^(n-1) + 1`.

## Mọi cổng đều khả nghịch

Một mạch lượng tử được dựng từ các cổng **khả nghịch**: áp một cổng rồi, bạn luôn
có thể áp cổng nghịch đảo để trở về đúng trạng thái cũ. Ví dụ đơn giản nhất là
cổng `X` dùng hai lần.

![Hai cổng X](../assets/ch09-reversible-circuit.png){ width="360" }

$$|0\rangle \xrightarrow{X} |1\rangle \xrightarrow{X} |0\rangle$$

Đây không phải một điều thú vị vặt — đó là ràng buộc định hình cả chương. Một cổng
`AND` cổ điển vi phạm điều đó:

| a | b | a AND b | |
|---|---|---|---|
| 0 | 0 | 0 | |
| 0 | 1 | 0 | ba đầu vào, một đầu ra |
| 1 | 0 | 0 | |
| 1 | 1 | 1 | |

Ba đầu vào khác nhau chia sẻ cùng đầu ra `0`, nên đầu vào đã mất và không thể khôi
phục. Mạch lượng tử không thể dùng `AND` như một hộp đen. Nó dùng cổng **Toffoli**
của [Chương 7](ch07-helloworld-explained.md) thay vào đó, cổng ghi `a AND b` lên
qubit *thứ ba* và để nguyên `a` với `b` — khả nghịch, đổi lại là một dây thêm.

## Oracle: hộp đen khả nghịch

Một thuật toán lượng tử không bao giờ nhìn thấy hàm; nó nhìn thấy một **oracle**,
tức mạch khả nghịch đánh giá hàm đó. Với hàm `f` một bit, oracle tác động lên hai
thanh ghi:

$$U_f : |x\rangle|y\rangle \longrightarrow |x\rangle\,|y \oplus f(x)\rangle$$

Đầu vào `x` trở về nguyên vẹn và câu trả lời được XOR lên thanh ghi dự phòng `y`.
Đặt `y = 0` thì thanh dự phòng giữ `f(x)`; đặt `y = 1` thì nó giữ `NOT f(x)`. Dù
cách nào cũng không có gì bị xoá — đúng điều mà tính khả nghịch đòi hỏi.

![Một oracle cân bằng: một cổng CNOT](../assets/ch09-oracle-circuit.png){ width="420" }

## Bốn hàm một bit

Chỉ có bốn hàm một bit, và chúng chia thành hai họ:

| Hàm | f(0) | f(1) | Loại | Mạch oracle |
|---|---|---|---|---|
| hằng 0 | 0 | 0 | hằng số | không làm gì |
| hằng 1 | 1 | 1 | hằng số | `X` lên `y` |
| cân bằng: `f(x) = x` | 0 | 1 | cân bằng | `CNOT(x, y)` |
| cân bằng: `f(x) = NOT x` | 1 | 0 | cân bằng | `X` lên `y`, rồi `CNOT(x, y)` |

![Bốn ma trận oracle](../assets/ch09-oracle-matrices.png){ width="620" }

Mỗi ma trận là một **ma trận hoán vị**: đúng một số `1` trên mỗi hàng và mỗi cột,
nên phép toán khả nghịch. Khác biệt giữa hai họ nằm đúng ở chỗ đầu vào `x` có làm
thay đổi câu trả lời hay không — hàm hằng phớt lờ `x` hoàn toàn, hàm cân bằng trả
lời khác nhau trên `0` và `1`.

## Thuật toán Deutsch

Bài toán Deutsch: bạn được trao một trong các oracle này và chỉ được hỏi *nó thuộc
họ nào*. Cổ điển thì phải truy vấn cả hai đầu vào — hai lần tra cứu. Lượng tử thì
**một** truy vấn là đủ:

![Mạch Deutsch](../assets/ch09-deutsch-circuit.png){ width="460" }

1. `X(1)` — thanh ghi dự phòng thành `|1⟩`.
2. `H(0), H(1)` — cả hai thanh ghi vào chồng chập; `q1` giờ là `|−⟩`.
3. oracle — đánh giá `f` một lần.
4. `H(0)` — cho hai nhánh giao thoa.
5. đo `q0`.

Cơ chế là **phase kickback**. Với `q1 = |−⟩`, oracle để nguyên hai thanh ghi nhưng
nhân trạng thái lên `(-1)^f(x)`: nó ghi giá trị của hàm vào **dấu**. Giờ hai nhánh
của `q0` mang `(-1)^f(0)` và `(-1)^f(1)`.

- **Hằng số** — hai dấu bằng nhau. Dấu bằng nhau là một pha toàn cục, vô hình, nên
  Hadamard cuối đưa `q0` về `|0⟩`. Phép đo cho `0`.
- **Cân bằng** — hai dấu khác nhau. Dấu trừ tương đối đó là thứ giao thoa nhìn
  thấy, và Hadamard cuối biến nó thành `|1⟩`. Phép đo cho `1`.

| Hàm | f(0) | f(1) | q0 đo được | Kết luận |
|---|---|---|---|---|
| hằng 0 | 0 | 0 | 0 | hằng số |
| hằng 1 | 1 | 1 | 0 | hằng số |
| f(x) = x | 0 | 1 | 1 | cân bằng |
| f(x) = NOT x | 1 | 0 | 1 | cân bằng |

![Một truy vấn: hằng số đo 0, cân bằng đo 1](../assets/ch09-deutsch-outcomes.png){ width="620" }

Cả hai hàm hằng số đo `0`, cả hai hàm cân bằng đo `1`, luôn luôn và chắc chắn, từ
một lần đánh giá duy nhất.

## Deutsch–Jozsa: một truy vấn cho mọi `n`

Bản tổng quát thay đầu vào một bit bằng đầu vào `n` bit, `f: {0,1}^n → {0,1}`, được
hứa là **hằng số** (cùng một câu trả lời trên mọi đầu vào) hoặc **cân bằng** (0
trên đúng một nửa số đầu vào, 1 trên nửa còn lại). Mạch chính là mạch Deutsch với
nhiều dây hơn:

![Deutsch–Jozsa cho n = 3](../assets/ch09-dj-circuit.png){ width="620" }

1. `X` lên ancilla; Hadamard lên cả `n + 1` qubit.
2. Chạy oracle **một lần** — trên cả `2^n` đầu vào cùng lúc.
3. Hadamard lên `n` qubit đầu vào.
4. Đo thanh ghi đầu vào.

Biên độ của `|0…0⟩` là **tổng** các dấu của mọi nhánh:

- **Hằng số** — mọi dấu giống nhau, các biên độ cộng lại, và `|0…0⟩` có xác suất 1.
- **Cân bằng** — một nửa số dấu là `-1`, các biên độ triệt tiêu, và `|0…0⟩` có xác
  suất 0.

Vậy một kết quả là đủ để kết luận: **toàn số không nghĩa là hằng số; bất kỳ thứ gì
khác nghĩa là cân bằng.**

| n | Oracle | P(0…0) | Kết luận | Cổ điển xấu nhất |
|---|---|---|---|---|
| 1 | hằng 0 | 1.00 | hằng số | 2 |
| 1 | hằng 1 | 1.00 | hằng số | 2 |
| 1 | cân bằng | 0.00 | cân bằng | 2 |
| 2 | hằng 0 | 1.00 | hằng số | 3 |
| 2 | cân bằng | 0.00 | cân bằng | 3 |
| 3 | hằng 0 | 1.00 | hằng số | 5 |
| 3 | cân bằng | 0.00 | cân bằng | 5 |

![n = 2: oracle hằng số trả về 00, oracle cân bằng thì không bao giờ](../assets/ch09-dj-outcomes.png){ width="620" }

Cột cổ điển mới là điểm mấu chốt. Muốn *chắc chắn*, một phép kiểm tra cổ điển có
thể phải đánh giá `2^(n-1) + 1` đầu vào — nửa không gian cộng một, vượt qua điểm mà
một hàm cân bằng vẫn còn có thể đang nấp. Chi phí lượng tử vẫn là **một** truy vấn
dù đầu vào rộng đến đâu.

!!! note "Song song lượng tử, và điều nó không phải"
    Oracle thật sự đánh giá `f` trên cả `2^n` đầu vào trong một lượt — đó là **song
    song lượng tử**. Nhưng bạn không thể đọc hết các giá trị đó ra: một phép đo chỉ
    trả về một trạng thái cơ sở. Thứ mạch trích ra không phải các câu trả lời, mà là
    một bit **toàn cục** về `f` (ở đây là tính hằng số của nó). Giao thoa là thứ
    biến việc đánh giá song song thành bit đó, và đó là lý do các tăng tốc lượng tử
    nói về *câu hỏi*, không phải về việc tính mọi thứ cùng lúc.

## Sơ đồ

### Tính khả nghịch

![Hai cổng X](../assets/ch09-reversible-circuit.png){ width="360" }

### Oracle

![Một oracle cân bằng: một cổng CNOT](../assets/ch09-oracle-circuit.png){ width="420" }

![Bốn ma trận oracle](../assets/ch09-oracle-matrices.png){ width="620" }

### Deutsch

![Mạch Deutsch](../assets/ch09-deutsch-circuit.png){ width="460" }

![Một truy vấn: hằng số đo 0, cân bằng đo 1](../assets/ch09-deutsch-outcomes.png){ width="620" }

### Deutsch–Jozsa

![Deutsch–Jozsa cho n = 3](../assets/ch09-dj-circuit.png){ width="620" }

![n = 2: oracle hằng số trả về 00, oracle cân bằng thì không bao giờ](../assets/ch09-dj-outcomes.png){ width="620" }

## Những điều cần nhớ

- Mọi cổng lượng tử đều **khả nghịch**. Các cổng cổ điển bất khả nghịch như `AND`
  không dùng trực tiếp được; bản thay thế khả nghịch là cổng **Toffoli**.
- Một **oracle** đánh giá hàm một cách khả nghịch:
  `U_f : |x⟩|y⟩ → |x⟩|y ⊕ f(x)⟩`. Nó giữ đầu vào và ghi câu trả lời lên thanh ghi
  dự phòng.
- Hàm một bit là **hằng số** (`f(0) = f(1)`) hoặc **cân bằng** (`f(0) ≠ f(1)`); có
  bốn hàm như vậy và mỗi hàm có một oracle một cổng.
- **Phase kickback** biến giá trị của hàm thành một *dấu*: với thanh ghi dự phòng ở
  `|−⟩`, oracle nhân mỗi nhánh với `(-1)^f(x)`.
- **Deutsch** dùng một truy vấn để phân loại hàm một bit; **Deutsch–Jozsa** làm
  điều đó cho `n` bit, vẫn trong **một** truy vấn, nơi kiểm tra cổ điển cần tới
  `2^(n-1) + 1`.
- Thuật toán không đọc `2^n` câu trả lời; nó trích ra một bit **toàn cục** — tính
  hằng số — nhờ giao thoa.

## Mã nguồn của chương này

Bốn mẫu, từ quy tắc nền tới thuật toán:

- [`ch09/reversible.py`](https://github.com/phonhay103/quantum-computing-in-action/blob/main/src/quantum_computing_in_action/ch09/reversible.py)
  — mẫu ``reversibleX``: `X·X = I`, và vì sao `AND` không thể làm oracle.
- [`ch09/oracles.py`](https://github.com/phonhay103/quantum-computing-in-action/blob/main/src/quantum_computing_in_action/ch09/oracles.py)
  — bốn hàm một bit, mạch oracle và ma trận của chúng, cùng các oracle `n` bit cho
  Deutsch–Jozsa.
- [`ch09/deutsch.py`](https://github.com/phonhay103/quantum-computing-in-action/blob/main/src/quantum_computing_in_action/ch09/deutsch.py)
  — mạch Deutsch và phép phân loại một truy vấn của nó.
- [`ch09/deutschjozsa.py`](https://github.com/phonhay103/quantum-computing-in-action/blob/main/src/quantum_computing_in_action/ch09/deutschjozsa.py)
  — thuật toán tổng quát, phép thử toàn số không, và so sánh cổ điển.

Chạy toàn bộ bằng `make ch09`, hoặc từng mẫu một:

```bash
uv run python -m quantum_computing_in_action.ch09.deutschjozsa
```
