# Chương 6 — Mạng lượng tử: những điều cơ bản

!!! abstract "Trong một câu"
    Một qubit **không thể** bị nhân bản, nên mạng lượng tử không thể chuyển tiếp
    gói tin như mạng cổ điển. Nó phải *dựng lại* trạng thái ở mỗi nút — đó là
    **dịch chuyển lượng tử** (teleportation) với cặp rối dùng chung và hai bit
    cổ điển, và đó là **bộ lặp** (repeater) nối các mắt xích lại.

## Một byte qua socket

Chương mở đầu bằng mạng đơn giản nhất có thể có. Một tiến trình thu nhận chiếm
một cổng và chờ; một tiến trình gửi kết nối và ghi một byte:

```
[Receiver] Starting to listen for incoming data at port 9753
[Sender] Create a connection to port 9753
[Sender] Write a byte: 8
[Sender] Wrote a byte: 8
[Receiver] Got a byte 8
```

Mẫu trong
[`ch06/networking.py`](https://github.com/phonhay103/quantum-computing-in-action/blob/main/src/quantum_computing_in_action/ch06/networking.py)
làm đúng điều đó với module `socket` của Python. Không có gì ghê gớm ở đây —
và đó chính là điểm. Mọi mạng cổ điển đều làm vậy, và làm đi lặp đi lặp lại
bằng cùng một mẹo: **đọc một gói tin, sao chép nó, chuyển tiếp bản sao.**

## Vì sao không thể nhân bản một qubit

Mẫu `classiccopy` của sách sao chép một bit cổ điển. Chuyện này tầm thường:

```python
source = True
copy = classic_copy(source)      # cả hai cùng tồn tại và dùng được
copy = not copy                  # đổi bản sao không ảnh hưởng bản gốc
```

Nó hoạt động vì **đọc** một bit cổ điển không làm nhiễu nó. Điều đó **không**
đúng với qubit, và không phải vì thiếu cố gắng — **định lý không nhân bản**
(no-cloning) nói rằng không máy nào có thể sao chép một trạng thái lượng tử
chưa biết.

Lập luận rất ngắn. Giả sử có một máy sao chép được mọi trạng thái `|ψ>` mà vẫn
để nguyên bản gốc.

1. Cho nó vào `|+>`. Bản sao ra cũng là `|+>`, chưa thấy vấn đề gì.
2. Cho nó vào `( |0> + |1> ) / √2`. Vì việc sao chép phải là một phép *tuyến
   tính* trên các biên độ, bản sao bị buộc phải là
   `( |00> + |11> ) / √2`.
3. Nhưng đo **một** qubit của `( |00> + |11> ) / √2` cho kết quả 0 hoặc 1 chắc
   chắn, khiến qubit còn lại sụp về `|0>` hoặc `|1>`.
4. Vậy "bản sao" chỉ là `|0>` hoặc `|1>` — không bao giờ là `|+>`. Mâu thuẫn.

### Một lần thử thất bại trông như thế nào

Cách thử hiển nhiên nhất là một `CNOT`: chuẩn bị `|+>` trên `q0`, rồi `CNOT`
sang `q1`. Qiskit sẽ vui vẻ dựng và chạy nó. Kết quả sai một cách âm thầm:

![Cách thử nhân bản](../assets/ch06-clone-attempt-circuit.png){ width="420" }

Qubit điều khiển không hề bị đụng tới, nên `q0` **vẫn** giữ trạng thái gốc. Nhưng
`q1` lại rối với nó chứ không phải là một bản sao:

$$H(0),\; CNOT(0,1) \quad\longrightarrow\quad \frac{|00\rangle + |11\rangle}{\sqrt{2}}$$

Đó là một **trạng thái Bell**, không phải hai trạng thái `|+>`. Đo cặp này ra,
kết quả **tương quan** hoàn hảo — `01` và `10` không bao giờ xuất hiện — trong
khi hai bản sao thật sẽ độc lập và cho cả bốn kết quả ở mức 25%:

![Bản sao hoàn hảo so với cách thử bằng CNOT](../assets/ch06-clone-agreement.png){ width="620" }

Mẫu còn thử cả mẹo đối xứng: quên chuyện sao chép đi, chỉ cần tự chuẩn bị một
`|+>` mới bằng `H`. Không chiến lược nào phủ hết mọi đầu vào.

| Đầu vào | `CNOT`: bản sao | `CNOT`: bản gốc | `H` mới trên bản sao | Một bản sao thật |
|---|---|---|---|---|
| <code>\|0⟩</code> | 1.00 | 1.00 | 0.50 | 1.00 |
| <code>\|1⟩</code> | 1.00 | 1.00 | 0.50 | 1.00 |
| <code>\|+⟩</code> | 0.50 | 0.50 | 1.00 | 1.00 |
| <code>\|−⟩</code> | 0.50 | 0.50 | 0.00 | 1.00 |

Đọc cột `CNOT`: nó sao chép được trạng thái cơ sở và hỏng trên chồng chập. Đọc cột
`H`: ngược lại. **Không chiến lược nào đúng cho cả bốn đầu vào.** Chính khoảng
trống đó là định lý không nhân bản, đo được.

![Độ trung thành của bản sao bằng CNOT](../assets/ch06-clone-fidelity.png){ width="420" }

!!! note "Cái giá phải trả trên một mạng thật"
    Mạng cổ điển tạo một bản sao của mỗi gói tin để phòng khi đường truyền đứt.
    Mạng lượng tử không thể làm vậy. Nó buộc phải *tạo lại* trạng thái ở mỗi
    mắt xích, và phần còn lại của chương nói về điều đó.

## Một pha mà bạn không nhìn thấy

Bài tập của Chương 6 ("Pauli-Z gate and Measurement") hỏi rằng *cổng hai qubit*
còn lại làm gì. `CZ`, cổng controlled-Z, giống `CNOT` ở một điểm: khi qubit
điều khiển bằng `1`, nó lật **pha** của qubit đích thay vì lật bit của nó.

![Mạch H + CZ](../assets/ch06-cz-circuit.png){ width="420" }

Hãy đặt cả hai qubit vào chồng chập trước, rồi áp dụng `CZ`:

$$H(0),\, H(1) \quad\longrightarrow\quad \frac{|00\rangle + |01\rangle + |10\rangle + |11\rangle}{2}
\qquad\text{(trạng thái tích)}$$
$$\xrightarrow{\;CZ\;}\quad \frac{|00\rangle + |01\rangle + |10\rangle - |11\rangle}{2}
\qquad\text{(đã rối)}$$

Chỉ một dấu đổi đã thay đổi hoàn toàn bản chất trạng thái: ma trận hệ số đi từ
hạng 1 lên hạng 2, nên hai qubit không còn độc lập. (Xem
[trạng thái tích so với rối](ch05-entanglement.md#trang-thai-tich-so-voi-trang-thai-roi)
để biết cách kiểm tra hạng.)

Và giờ hãy đo cả hai qubit. Bạn nhận được **cả bốn kết quả ở mức 25% mỗi loại** —
đúng biểu đồ cột giống hệt trạng thái khi chưa có `CZ`:

![CZ so với trạng thái Bell](../assets/ch06-cz-vs-bell.png){ width="620" }

Quy tắc Born *bình phương* các biên độ, nên `|−½|² = |+½|²`. Dấu ở đó, sự rối
là thật, và một phép đo theo cơ sở tính toán không báo gì cả. Muốn phân biệt hai
trạng thái này cần một **cơ sở đo khác** — và đó chính xác là mẹo mà
teleportation dùng.

![Các ma trận hệ số](../assets/ch06-cz-matrices.png){ width="620" }

Hai trường hợp đối chiếu. `CZ` sau một `H` đơn lẻ là **vô tác dụng hoàn toàn**,
vì qubit 1 vẫn ở `|0>` nên điều khiển không bao giờ kích hoạt. Và `CZ` trên trạng
thái Bell chỉ lật cùng một dấu, còn tập kết quả `{00, 11}` không đổi, vì `CNOT`
đã làm phần tương quan từ trước rồi.

## Dịch chuyển lượng tử: chuyển trạng thái, không phải hạt

Giờ đến phần chính. Alice không thể đọc qubit của mình, và cũng không thể gửi
một bản sao. Nhưng cô ấy có thể *hủy* bản gốc và dựng lại một trạng thái giống
hệt ở phía Bob, nhờ các tương quan mà hai người đã chia sẻ từ trước.

| Qubit | Thuộc về |
|---|---|
| `q0` | Alice — trạng thái cần gửi |
| `q1` | Nửa của cặp Bell mà Alice chia sẻ với Bob |
| `q2` | Nửa còn lại của cặp đó — trạng thái kết thúc ở đây |

![Mạch teleportation](../assets/ch06-teleport-circuit.png){ width="620" }

Giao thức:

1. **Chia sẻ một cặp Bell.** `H(2)`, `CNOT(2,1)` — quay lại Chương 5.
2. **Trải rộng trạng thái.** `CNOT(0,1)`, `H(0)`. Trạng thái của Alice giờ nằm
   rải trên cả hai qubit của cô ấy.
3. **Đo kiểu Bell.** Alice đo `q0` và `q1`. Điều này hủy `q0` — và chính sự hủy
   đó là điều cho phép trạng thái xuất hiện lại ở phía Bob.
4. **Gửi hai bit cổ điển.** Qua một kênh thông thường, với tốc độ ánh sáng.
5. **Sửa sai.** Bob áp dụng `X` lên `q2` nếu bit của anh ấy cho `q1` là `1`, và
   `Z` nếu bit cho `q0` là `1`.

| Tin nhắn của Alice | Bob áp dụng | Qubit của Bob khi Alice gửi <code>\|0⟩</code> | Độ trung thành |
|---|---|---|---|
| `00` | không làm gì | <code>\|0⟩</code> | 1.000 |
| `01` | `X` | <code>\|0⟩</code> | 1.000 |
| `10` | `Z` | <code>\|0⟩</code> | 1.000 |
| `11` | `X` rồi `Z` | <code>\|0⟩</code> | 1.000 |

Cả bốn tin nhắn đều xảy ra với xác suất ¼, và **cả bốn đều dựng lại trạng thái
chính xác**. Đó là toàn bộ điều giao thức khẳng định, và nó đúng cho mọi đầu vào:

| Alice gửi | Bob đo | Độ trung thành |
|---|---|---|
| <code>\|0⟩</code> | P(0) = 1.00 | 1.000 |
| <code>\|1⟩</code> | P(1) = 1.00 | 1.000 |
| <code>\|+⟩</code> | P(0) = 0.50, P(1) = 0.50 | 1.000 |
| <code>\|−⟩</code> | P(0) = 0.50, P(1) = 0.50 | 1.000 |

![Mọi tin nhắn đều dựng lại trạng thái](../assets/ch06-teleport-fidelity.png){ width="620" }

Hãy chú ý điều mà độ trung thành bằng 1.0 *không* có nghĩa: Bob không thể tự tạo
ra `|+>` từ `|0>`, cũng không thể tự tạo ra `|0>` từ `|+>`. Anh ấy chỉ *dựng
lại* một trạng thái vốn đã tồn tại ở phía Alice. Teleportation chuyển **thông
tin**, không chuyển hạt — dù sao thì `q0` của Alice vẫn mất.

![Kết quả của Bob theo trạng thái Alice gửi](../assets/ch06-teleport-outcomes.png){ width="620" }

!!! warning "Không truyền tín hiệu nhanh hơn ánh sáng"
    Bước 4 là một tin nhắn cổ điển thông thường, bị giới hạn bởi tốc độ ánh
    sáng. Không có hai bit đó, Bob chỉ có một trạng thái với lỗi pha ngẫu nhiên
    và không cách nào sửa. Đó là hai "bit cổ điển" trong tên của giao thức, và đó
    là lý do teleportation **không** vượt ánh sáng.

## Từ mạch tới mạng: bộ lặp

Teleportation chuyển trạng thái qua **một** mắt xích. **Bộ lặp** (repeater) nối
nhiều mắt xích lại để trạng thái vượt được khoảng cách xa hơn nhiều, với một nút
ở giữa đóng vai trò vừa là nơi nhận vừa là nơi gửi:

```
Alice (q0)  ---  mắt 1  ---  relay (q2)  ---  mắt 2  ---  Bob (q4)
                        với q1                    với q3
```

![Hai mắt xích nối qua một nút trung gian](../assets/ch06-repeater-circuit.png){ width="620" }

Nút trung gian là phần thú vị. Nó **đo** các qubit của mình ở mắt xích đầu tiên,
đúng như Alice đo vậy, nên nó không bao giờ giữ trạng thái một cách sạch sẽ ở
giữa chừng. Thứ thực sự di chuyển không phải là trạng thái: đó là chuỗi các
**tương quan** cộng với *bốn* bit cổ điển — hai từ Alice, hai từ nút trung gian.

Để chứng minh trạng thái thực sự đến nơi, Alice khởi tạo một qubit không phải
`|0>` cũng không phải `|1>`: một phép quay với `P(1) = 0.4`. Nếu nút trung gian
chỉ chuyển tiếp bit cổ điển, Bob sẽ chỉ thấy 0 và 1. Thay vào đó, thống kê của
anh ấy khớp với thống kê của cô ấy, cho mọi đầu vào:

| Qubit của Alice | P(1) ở Alice | P(1) ở Bob |
|---|---|---|
| P(1) = 0.0 | 0.00 | 0.00 |
| P(1) = 0.2 | 0.20 | 0.20 |
| P(1) = 0.4 | 0.40 | 0.40 |
| P(1) = 0.6 | 0.60 | 0.60 |
| P(1) = 0.8 | 0.80 | 0.80 |
| P(1) = 1.0 | 1.00 | 1.00 |

![Thống kê sống sót qua chuyến đi](../assets/ch06-repeater-consistency.png){ width="620" }

![Kỳ vọng so với đo được ở Bob](../assets/ch06-repeater-counts.png){ width="620" }

Một hỗn hợp thật sự đã đến với Bob, sau khi được dựng lại hai lần trên đường đi.
Và hãy chú ý rằng nút trung gian buộc phải *đo* mới chuyển tiếp được — trạng
thái không bao giờ nằm trên đường dưới dạng bản sao, và đó chính xác là lý do
mọi thứ vẫn hoạt động dù không thể sao chép.

!!! note "Hướng đi tiếp"
    Trong một mạng lượng tử thật, khoảng cách bị giới hạn bởi **suy hao** chứ
    không phải bởi tốc độ ánh sáng: một trạng thái đã mất tính toàn vẹn thì
    không thể sửa, vì không có bản sao nào để dựa vào. Bộ lặp không khuếch đại
    tín hiệu yếu như bộ lặp cổ điển — nó *tạo lại* trạng thái ở mỗi nút từ cặp
    rối dùng chung cộng một tin nhắn cổ điển.
    [Chương 8](ch08-secure-communication.md) biến cùng ý tưởng đó thành truyền
    thông an toàn.

## Sơ đồ

### Định lý không nhân bản

![Cách thử nhân bản](../assets/ch06-clone-attempt-circuit.png){ width="420" }

`CNOT` không nhân bản: nó rối. Qubit điều khiển được giữ nguyên, còn qubit đích
chứa một đối tác Bell chứ không phải một bản sao.

![Bản sao hoàn hảo so với cách thử bằng CNOT](../assets/ch06-clone-agreement.png){ width="620" }

Hai bản sao thật của `|+>` sẽ độc lập (mỗi kết quả 25%); cách thử lại tương quan
hoàn hảo, và `01`/`10` biến mất.

![Độ trung thành của bản sao bằng CNOT](../assets/ch06-clone-fidelity.png){ width="420" }

Đúng với trạng thái cơ sở, sai hoàn toàn với chồng chập.

### Controlled-Z

![Mạch H + CZ](../assets/ch06-cz-circuit.png){ width="420" }

![CZ so với trạng thái Bell](../assets/ch06-cz-vs-bell.png){ width="620" }

Hai chuỗi đầu không thể phân biệt bằng phép đo, dù một cái là trạng thái tích và
cái kia đã rối.

![Các ma trận hệ số](../assets/ch06-cz-matrices.png){ width="620" }

Một dấu đổi đưa hạng từ 1 lên 2.

### Dịch chuyển lượng tử

![Mạch teleportation](../assets/ch06-teleport-circuit.png){ width="620" }

Các hộp `If X` và `If Z` là những phép sửa cổ điển, do kết quả đo của Alice điều
khiển.

![Mọi tin nhắn đều dựng lại trạng thái](../assets/ch06-teleport-fidelity.png){ width="620" }

![Kết quả của Bob theo trạng thái Alice gửi](../assets/ch06-teleport-outcomes.png){ width="620" }

### Bộ lặp

![Hai mắt xích nối qua một nút trung gian](../assets/ch06-repeater-circuit.png){ width="620" }

Hai cặp Bell, hai phép đo kiểu Bell, bốn phép sửa cổ điển.

![Thống kê sống sót qua chuyến đi](../assets/ch06-repeater-consistency.png){ width="620" }

![Kỳ vọng so với đo được ở Bob](../assets/ch06-repeater-counts.png){ width="620" }

## Những điều cần nhớ

- Mạng cổ điển chuyển tiếp gói tin bằng cách **sao chép** chúng; mạng lượng tử
  thì không, vì **định lý không nhân bản** cấm sao chép một trạng thái chưa biết.
- `CNOT` không nhân bản: nó rối. Cách thử thành công trên trạng thái cơ sở và
  hỏng trên chồng chập, và không biến thể nào phủ được cả hai.
- `CZ` lật một pha, còn quy tắc Born bình phương các biên độ — nên `CZ` có thể
  biến một trạng thái tích thành trạng thái rối **mà không đổi một xác suất đo
  nào**.
- **Teleportation** chuyển một trạng thái bằng cách hủy bản gốc rồi dựng lại nó
  từ cặp rối dùng chung cộng **hai bit cổ điển**. Nó chuyển thông tin, không
  chuyển hạt, và không vượt ánh sáng.
- Một **bộ lặp** nối các mắt xích teleportation; một nút trung gian mà phải
  *đo* vẫn có thể chuyển tiếp trạng thái, và qubit nhận được giữ nguyên thống
  kê ban đầu.
- Vì không thể sửa từ một bản sao dự phòng khi bị mất tính toàn vẹn, mạng lượng
  tử thật bị giới hạn bởi hiệu ứng mất coherence — cái giá của mẹo không-có-bản-sao.

## Mã nguồn của chương này

Bốn mẫu, mỗi mẫu cho một mục của sách, cùng một bộ mô phỏng nhỏ dùng chung:

- [`ch06/networking.py`](https://github.com/phonhay103/quantum-computing-in-action/blob/main/src/quantum_computing_in_action/ch06/networking.py)
  — byte qua TCP (6.2.1) và phần minh hoạ định lý không nhân bản (6.2.2).
- [`ch06/czmeasure.py`](https://github.com/phonhay103/quantum-computing-in-action/blob/main/src/quantum_computing_in_action/ch06/czmeasure.py)
  — bài tập Chương 6 về `CZ` và phép đo.
- [`ch06/teleportation.py`](https://github.com/phonhay103/quantum-computing-in-action/blob/main/src/quantum_computing_in_action/ch06/teleportation.py)
  — mạch teleportation và bảng phép sửa của nó.
- [`ch06/repeater.py`](https://github.com/phonhay103/quantum-computing-in-action/blob/main/src/quantum_computing_in_action/ch06/repeater.py)
  — chuỗi hai mắt xích qua một nút trung gian.
- [`ch06/protocol.py`](https://github.com/phonhay103/quantum-computing-in-action/blob/main/src/quantum_computing_in_action/ch06/protocol.py)
  — bộ mô phỏng nhánh dùng chung. Teleportation cần một phép **đo giữa mạch**
  mà kết quả của nó điều khiển các cổng cổ điển, và `Statevector` của Qiskit
  từ chối các mạch chứa control flow. Module này thay vào đó giữ một *frame* cho
  mỗi kết quả đo, áp các cổng lên mọi frame và rẽ nhánh khi một qubit được đo.

Chạy toàn bộ bằng `make ch06`, hoặc từng mẫu một:

```bash
uv run python -m quantum_computing_in_action.ch06.teleportation
```

!!! note "Cách đọc nhãn trên mạch"
    Các mạch được *vẽ ra* là mạch Qiski bình thường có khối `if_test`, đúng như
    cách bạn sẽ viết. Các con số đến từ bộ mô phỏng nhánh, vốn tính ra cùng phân
    phối mà không cần thực thi control flow. Các qubit được đánh số theo chỉ số
    thuần (`q0`, `q1`, ...), khớp với mẫu Java của sách, nên `q0` là qubit ở
    `q[0]`.
