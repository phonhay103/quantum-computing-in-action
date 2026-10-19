# Chương 7 — HelloWorld của chúng ta, giải thích

!!! abstract "Trong một câu"
    Một chương trình lượng tử không phải một chiếc hộp đen: nó là một danh sách
    **các bước** có thứ tự, và trạng thái mà nó tạo ra có thể đọc được sau *mỗi*
    bước — đó là tất cả những gì "chạy một mạch" có nghĩa.

## Một chương trình là một danh sách các bước

Chương 2 xin một bit ngẫu nhiên và nhận được nó, mà không nói bằng cách nào.
Chương này mở chiếc hộp ra. Thứ ở bên trong không phải một lời gọi hàm, mà là một
**chương trình**: một danh sách các bước có thứ tự, mỗi bước chứa những cổng hoạt
động cùng lúc.

Mẫu ``randombit`` của sách là một chương trình bốn qubit với đúng hai bước:

```text
bước 1:  H(0), X(3)
bước 2:  CNOT(0, 1)
```

![Chương trình bốn qubit](../assets/ch07-randombit-circuit.png){ width="460" }

Đọc từ trái sang phải:

- `H` trên `q0` đưa qubit đó vào chồng chập đều, `( |0⟩ + |1⟩ )/√2`. Đây chính là
  bit ngẫu nhiên của Chương 2.
- `X` trên `q3` lật nó thành `|1⟩` xác định — chương trình được phép đặt những
  giá trị nó đã biết.
- `q2` hoàn toàn không bị đụng tới.
- `CNOT(0, 1)` sau đó lật `q1` đúng khi `q0` bằng `1`.

Hai bước, bốn qubit, và chỉ một trong số chúng thực sự ngẫu nhiên. Nhưng chính sự
*kết hợp* mới là điều quan trọng, và để thấy vì sao, bạn phải nhìn trạng thái di
chuyển.

## Đọc trạng thái sau mỗi bước

Một biểu đồ cột ở cuối cho biết chương trình *trả về cái gì*; nó không cho biết
*mỗi qubit đổi ở đâu*. Mẫu ``randombitdebug`` của sách trả lời điều đó bằng cách
vẽ vector xác suất sau **mỗi** bước. Bộ mô phỏng của nó giữ một đối tượng duy
nhất — trạng thái — từ đầu đến cuối, nên "gỡ lỗi" không gì khác hơn là nhìn vào
đối tượng đó ở mỗi bước.

Đây là cùng chương trình đó, với một vạch ranh giới được vẽ sau mỗi bước:

![Chương trình với ranh giới các bước](../assets/ch07-debug-circuit.png){ width="460" }

Và đây là trạng thái tại mỗi điểm đó. Trước hết là toàn bộ vector xác suất, chỉ
giữ lại những trạng thái cơ sở có thể xảy ra:

| Bước | Trạng thái cơ sở `q0 q1 q2 q3` | Xác suất |
|---|---|---|
| bắt đầu | `0000` | 1.00 |
| `H(0), X(3)` | `0001` | 0.50 |
| | `1001` | 0.50 |
| `CNOT(0, 1)` | `0001` | 0.50 |
| | `1101` | 0.50 |

![Xác suất trạng thái cơ sở sau mỗi bước](../assets/ch07-debug-steps.png){ width="620" }

Không bao giờ có quá hai trạng thái khác không, và cột thứ hai kể toàn bộ câu
chuyện: `X` ghim `q3` bằng `1` ngay lập tức (phần `0001` ở đầu), `H` tách `q0`,
và `CNOT` đưa `q1` từ `0` lên `1` *cùng nhịp* với `q0` (`1001` biến thành `1101`).

Cùng lượng thông tin đó, mỗi qubit một cột, dễ đọc lướt hơn:

| Bước | P(q0=1) | P(q1=1) | P(q2=1) | P(q3=1) |
|---|---|---|---|---|
| bắt đầu | 0.00 | 0.00 | 0.00 | 0.00 |
| `H(0), X(3)` | 0.50 | 0.00 | 0.00 | 1.00 |
| `CNOT(0, 1)` | 0.50 | 0.50 | 0.00 | 1.00 |

![P(qubit = 1) sau mỗi bước](../assets/ch07-debug-marginals.png){ width="620" }

Đọc theo cột: `q0` nhảy lên `0.50` ở **bước đầu** (`H`), `q1` nhảy ở **bước hai**
(`CNOT`), còn `q2` và `q3` giữ nguyên giá trị suốt quá trình. Một biểu đồ cột của
trạng thái cuối không thể cho bạn biết điều đó; trạng thái trung gian thì có.

Vậy chương trình *trả về* cái gì? Đo cả bốn qubit thì chỉ có hai chuỗi xuất hiện:

| Kết quả `q0 q1 q2 q3` | Số lần (1000 lần chạy) |
|---|---|
| `0001` | ≈ 500 |
| `1101` | ≈ 500 |

![Chỉ hai kết quả, và q1 đi theo q0](../assets/ch07-randombit-counts.png){ width="620" }

`q2` luôn bằng `0` và `q3` luôn bằng `1`; tính ngẫu nhiên nằm hoàn toàn ở `q0`, và
`q1` **luôn đồng ý** với nó. Sự đồng ý đó là một cặp Bell trên cặp `(q0, q1)` —
tương quan của [Chương 5](ch05-entanglement.md) — và đó là cách trung thực duy
nhất để một mạch chia sẻ một giá trị chưa biết. Nó không phải một bản sao:
[Chương 6](ch06-quantum-networking.md) đã cho thấy không thể sao chép, và một
`CNOT` "nhân bản" một chồng chập lại tạo ra đúng sự rối này thay vì bản sao.

## Cộng hai qubit

Khi chương trình đã mở ra, sách chuyển sang **số học** — phép thử đầu tiên kinh
điển của mọi mô hình tính toán. Mạch cổ điển cộng bằng các cổng `AND` và `OR`.
Mạch lượng tử thì không thể, vì mọi cổng lượng tử đều phải **khả nghịch**: bạn
không bao giờ được phép xoá một bit.

Vì thế phép toán nhỏ nhất mà một mạch lượng tử làm được là một `CNOT`, cổng lật
qubit đích đúng khi qubit điều khiển bằng `1`:

![Bộ bán cộng cho 1 + 1](../assets/ch07-add1-circuit.png){ width="420" }

Với `a` nạp vào `q0` và `b` vào `q1`, một `CNOT(0, 1)` duy nhất để lại **tổng**
trên `q1`:

| a | b | a + b (mod 2) |
|---|---|---|
| 0 | 0 | 0 |
| 0 | 1 | 1 |
| 1 | 0 | 1 |
| 1 | 1 | **0** |

Ba dòng đầu là phép cộng thông thường. Dòng thứ tư thì không: `1 + 1` quấn về `0`,
vì `CNOT` chỉ lật qubit đích *qua lại* giữa `0` và `1`. Không gì trong mạch nhớ
rằng nó đã nhớ. Đây là một **bộ bán cộng** (half-adder): đúng chừng nào kết quả
còn vừa trong một bit.

## Cổng đem lại số nhớ

Thứ còn thiếu là một phép **AND** logic — một bit chỉ bằng `1` khi cả hai đầu vào
bằng `1`. Một `AND` thường phá huỷ các đầu vào của nó, nên không được phép. Bản
thay thế khả nghịch của nó là cổng **Toffoli** (còn viết là `CCNOT`): một cổng ba
qubit, lật qubit đích chỉ khi **cả hai** qubit điều khiển bằng `1`.

| Vào `q0 q1 q2` | Ra `q0 q1 q2` | |
|---|---|---|
| `000` | `000` | |
| `001` | `001` | |
| `010` | `010` | |
| `011` | `011` | |
| `100` | `100` | |
| `101` | `101` | |
| `110` | `111` | bị lật |
| `111` | `110` | bị lật |

Chỉ hai dòng thay đổi, và chỉ qubit thứ ba thay đổi trong đó — nhưng đó chính xác
là `AND`. Áp lên `(a, b, 0)`, cổng Toffoli để nguyên `a` và `b` rồi ghi `a AND b`
lên qubit đích. Không gì bị xoá, nên cổng khả nghịch; cái giá là các đầu vào vẫn
còn đó về sau, và vì vậy kết quả cần một qubit riêng.

```text
Toffoli(0, 1, 2)   q2 = q0 AND q1   (số nhớ)
CNOT(0, 1)         q1 = q0 XOR q1   (tổng)
```

Cổng Toffoli phải chạy **trước** `CNOT`, vì `CNOT` sắp ghi đè lên qubit điều
khiển thứ hai của nó.

![Bộ cộng đầy đủ cho 1 + 1](../assets/ch07-add2-circuit.png){ width="460" }

Giờ thì `1 + 1 = 2` đã thành sự thật: bit tổng vẫn quấn về `0`, còn qubit mới `q2`
giữ số `1` mà bộ bán cộng đã đánh rơi.

| a | b | tổng | số nhớ | a + b |
|---|---|---|---|---|
| 0 | 0 | 0 | 0 | 0 |
| 0 | 1 | 1 | 0 | 1 |
| 1 | 0 | 1 | 0 | 1 |
| 1 | 1 | 0 | 1 | **2** |

![Bán cộng so với cộng đầy đủ](../assets/ch07-adder-comparison.png){ width="620" }

Hai mạch đồng ý ở ba đầu vào và khác nhau ở đầu vào thứ tư. Khoảng cách — số nhớ —
chính là lý do cổng Toffoli tồn tại trong hộp đồ nghề lượng tử, và nó là mẫu hình
mà mọi thuật toán lượng tử lớn hơn dựng lên: thêm một qubit, thêm một cổng, và
một phép toán trước đây bất khả nghịch trở nên khả nghịch.

![Từ X tới CNOT tới Toffoli](../assets/ch07-toffoli-matrices.png){ width="620" }

Các ma trận cho thấy rõ cả họ cổng. `X` một qubit lật qubit đích duy nhất của nó
vô điều kiện; `CNOT` lật qubit đích theo một qubit điều khiển; `Toffoli` theo
hai. Mỗi cổng thêm một điều khiển và một qubit, và tập các cổng nhiều qubit *khả
nghịch* chính là thứ để viết nên một thuật toán.

## Sơ đồ

### Chương trình

![Chương trình bốn qubit](../assets/ch07-randombit-circuit.png){ width="460" }

`q0` ở trên cùng, rồi `q1`, `q2`, `q3` — đúng thứ tự của sách, khớp với
`Qubit[0] … Qubit[3]`. `H` tách `q0`, `X` đặt `q3`, và `CNOT(0, 1)` buộc `q1`
vào `q0`. `q2` được vẽ ra nhưng không hề bị đụng tới.

### Gỡ lỗi, từng bước

![Chương trình với ranh giới các bước](../assets/ch07-debug-circuit.png){ width="460" }

Các vạch chắn đánh dấu nơi một bước kết thúc và bước kế tiếp bắt đầu — đúng vai
trò mà các cổng xác suất của sách đảm nhiệm trong hình.

![Xác suất trạng thái cơ sở sau mỗi bước](../assets/ch07-debug-steps.png){ width="620" }

Vector xác suất tại ba thời điểm: một trạng thái, rồi hai, rồi hai — và lần thứ
hai đổi thành viên của qubit `q1`.

![P(qubit = 1) sau mỗi bước](../assets/ch07-debug-marginals.png){ width="620" }

Cùng sự thật đó, mỗi qubit một cột: `q0` đổi ở bước 1, `q1` ở bước 2, `q2` và
`q3` không bao giờ.

### Các bộ cộng

![Bộ bán cộng cho 1 + 1](../assets/ch07-add1-circuit.png){ width="420" }

Trường hợp `1 + 1`: cả hai đầu vào được đặt, và tổng đọc ra `0` vì không có chỗ
để chứa số nhớ.

![Bộ cộng đầy đủ cho 1 + 1](../assets/ch07-add2-circuit.png){ width="460" }

Cổng `Toffoli` ghi số nhớ lên `q2`, còn `CNOT` ghi tổng lên `q1`.

![Bán cộng so với cộng đầy đủ](../assets/ch07-adder-comparison.png){ width="620" }

![Từ X tới CNOT tới Toffoli](../assets/ch07-toffoli-matrices.png){ width="620" }

## Những điều cần nhớ

- Một chương trình lượng tử là một danh sách **các bước** có thứ tự. Chạy nó là
  một trạng thái tiến hoá từ `|0…0>` tới phép đo cuối cùng — không hơn.
- Có thể đọc trạng thái sau **mỗi** bước; đó là tất cả ý nghĩa của "gỡ lỗi một
  mạch", và đó là cách bạn thấy *bước nào* đã đổi *qubit nào*.
- Trong chương trình HelloWorld, `q0` trở nên ngẫu nhiên ở cổng `H`, `q1` nhận
  giá trị ở cổng `CNOT`, còn `q2` và `q3` không hề nhúc nhích. Một biểu đồ cột
  cuối cùng sẽ giấu hết những điều đó.
- `CNOT` tính `a XOR b`: phép cộng **modulo 2**, không có số nhớ. Riêng nó là một
  **bộ bán cộng**, và `1 + 1 = 0`.
- Mọi cổng lượng tử đều **khả nghịch**, nên cổng `AND` cổ điển bị cấm. Bản thay
  thế của nó là **Toffoli** (`CCNOT`), lật qubit đích chỉ khi hai qubit điều khiển
  bằng `1` — một phép `AND` khả nghịch giữ nguyên các đầu vào.
- `Toffoli` cho số nhớ cộng với `CNOT` cho tổng tạo nên một **bộ cộng đầy đủ**, và
  `1 + 1 = 2`. Thêm một qubit và một cổng là đủ để phép toán trở nên khả nghịch.

## Mã nguồn của chương này

Bốn mẫu, mỗi mẫu cho một mục của sách, cùng một bộ trợ giúp nhỏ dùng chung:

- [`ch07/randombit.py`](https://github.com/phonhay103/quantum-computing-in-action/blob/main/src/quantum_computing_in_action/ch07/randombit.py)
  — chương trình bốn qubit, hai bước của nó, và các kết quả đo (7.5.1).
- [`ch07/debugging.py`](https://github.com/phonhay103/quantum-computing-in-action/blob/main/src/quantum_computing_in_action/ch07/debugging.py)
  — cùng chương trình đó với trạng thái được báo cáo sau mỗi bước (7.5.2).
- [`ch07/half_adder.py`](https://github.com/phonhay103/quantum-computing-in-action/blob/main/src/quantum_computing_in_action/ch07/half_adder.py)
  — bộ bán cộng bằng `CNOT`, modulo 2, không có số nhớ (7.6.2).
- [`ch07/full_adder.py`](https://github.com/phonhay103/quantum-computing-in-action/blob/main/src/quantum_computing_in_action/ch07/full_adder.py)
  — bộ cộng đầy đủ `Toffoli` + `CNOT`, và ma trận `Toffoli` (7.6.3).
- [`ch07/circuits.py`](https://github.com/phonhay103/quantum-computing-in-action/blob/main/src/quantum_computing_in_action/ch07/circuits.py)
  — các trợ giúp dùng chung: đọc trạng thái sau một bước, vector xác suất, và việc
  chỉnh thứ tự bit giữa Qiskit và sách.

Chạy toàn bộ bằng `make ch07`, hoặc từng mẫu một:

```bash
uv run python -m quantum_computing_in_action.ch07.full_adder
```

!!! note "Một chút sổ sách: thứ tự bit"
    Qiskit in một kết quả với qubit có **chỉ số cao nhất** ở bên trái — khoá bốn
    qubit đọc là `q3 q2 q1 q0`. Sách viết `q0 q1 q2 q3`. Mọi kết quả ở đây đã
    được lật về thứ tự của sách, nên một nhãn trong chương này đọc đúng như
    `Qubit[0] … Qubit[3]` của sách.
