# Chương 6 — Mạng lượng tử: những điều cơ bản

!!! abstract "Trong một câu"
    Một qubit **không thể** bị nhân bản, nên mạng lượng tử không thể chuyển tiếp
    gói tin như mạng cổ điển — nó phải *dựng lại* trạng thái ở mỗi nút, đó là
    **truyền tải lượng tử** với cặp rối dùng chung và hai bit cổ điển. Chương
    trước tiên chứng minh giới hạn cấm đoán này, rồi phát triển giao thức vượt
    qua được nó bằng cách chuyển **thông tin** của trạng thái chứ không chuyển
    bản thân trạng thái.

## Một byte qua socket

Chương mở đầu bằng mạng đơn giản nhất có thể được, và sự tối giản này là có
chủ ý: sự đối chiếu giữa điều một mạng như vậy làm được với điều một mạng
lượng tử không bao giờ làm được chính là ý tưởng xuyên suốt của toàn bộ phần
còn lại. Một tiến trình nhận chiếm một cổng cụ thể rồi chỉ việc chờ kết nối
đến; một tiến trình gửi kết nối tới cổng đó và ghi một byte dữ liệu:

```
[Receiver] Starting to listen for incoming data at port 9753
[Sender] Create a connection to port 9753
[Sender] Write a byte: 8
[Sender] Wrote a byte: 8
[Receiver] Got a byte 8
```

Mẫu trong
[`ch06/networking.py`](https://github.com/phonhay103/quantum-computing-in-action/blob/main/src/quantum_computing_in_action/ch06/networking.py)
làm đúng giao dịch đó với module `socket` của Python, và không có gì ghê gớm
trong cơ chế của nó — thật ra, chính sự thiếu ghê gớm này là điểm mấu chốt.
Mọi mạng cổ điển đều thực hiện dịch vụ như vậy, và đều làm bằng một quy tắc
được lặp đi lặp lại: **đọc một gói tin, sao chép nó, chuyển tiếp bản sao.**
Phần tiếp theo sẽ chứng minh rằng quy tắc nền tảng này không có đối ứng nào
giới lượng tử, và rằng nguyên nhân cấm đoán kia là một định lý chứ không phải
một khó khăn kỹ thuật.

## Vì sao không thể nhân bản một qubit

Mẫu `classiccopy` của sách sao chép một bit cổ điển, và thủ tục này thành công
vì thông tin cổ điển cho phép nhân bản mà không phải trả giá nào:

```python
source = True
copy = classic_copy(source)  # cả hai cùng tồn tại và dùng được
copy = not copy  # đổi bản sao không ảnh hưởng bản gốc
```

Cách xây dựng này hoạt động vì thao tác **đọc** một bit cổ điển không làm nhiễu
nó: một bit cổ điển vốn đã nằm ở một trong hai giá trị xác định, và việc xem
biết nó đang giữ giá trị nào không hề thay đổi chính giá trị đó. Điều đó
**không** đúng với qubit, và không phải vì thiếu cố gắng — **định lý không
nhân bản** (no-cloning) phát biểu rằng không có thiết bị vật lý nào, dù tinh vi
đến đâu, sao chép được một trạng thái lượng tử chưa biết.

Lập luận rất ngắn, và nó đi theo hướng phản chứng. Giả sử có một máy sao chép
được mọi trạng thái `|ψ⟩` mà vẫn để nguyên bản gốc.

1. Cho máy vào `|0⟩` và `|1⟩` cho ra các bản sao đúng, và ở giai đoạn này thiết
   bị giả định vẫn hoàn toàn nhất quán với định nghĩa của nó.
2. Cho máy vào `|+⟩ = ( |0⟩ + |1⟩ ) / √2` thay vào đó sẽ bộc lộ khó khăn: vì
   việc sao chép phải là một phép *tuyến tính* trên các biên độ, kết quả bị
   buộc phải là
   `( |00⟩ + |11⟩ ) / √2` — một cặp rối, không phải hai bản sao độc lập của
   `|+⟩`.
3. Nhưng đo **một** qubit của `( |00⟩ + |11⟩ ) / √2` lại cho một giá trị `0`
   hoặc `1` xác định, khiến qubit còn lại sụp về `|0⟩` hoặc `|1⟩`.
4. Do đó "bản sao" chỉ là `|0⟩` hoặc `|1⟩` — không bao giờ là `|+⟩`. Đây là
   một mâu thuẫn.

### Một lần thử thất bại trông như thế nào

Cách thử hiển nhiên nhất là một `CNOT`: chuẩn bị `|+⟩` trên `q0`, rồi áp dụng
`CNOT` sang `q1`. Qiskit dựng và chạy mạch này mà không phản đối gì, và chính
điều đó khiến kết quả sai một cách âm thầm trở nên đáng để suy ngẫm hơn là
nhận ra ngay:

![Cách thử nhân bản](../assets/ch06-clone-attempt-circuit.png){ width="420" }

Qubit điều khiển không hề bị phép biến đổi đụng tới, nên `q0` **vẫn** giữ
trạng thái gốc. Nhưng `q1` lại rối với nó chứ không phải là một bản sao độc
lập:

$$H(0),\; CNOT(0,1) \quad\longrightarrow\quad \frac{|00\rangle + |11\rangle}{\sqrt{2}}$$

Thứ đã tạo ra là một **trạng thái Bell**, không phải hai trạng thái `|+⟩`. Đo
cặp này ta thu được các kết quả **tương quan** hoàn hảo — `01` và `10` không
bao giờ xuất hiện — trong khi hai bản sao thật sẽ độc lập và cho cả bốn kết quả
ở mức 25%:

![Bản sao hoàn hảo so với cách thử bằng CNOT](../assets/ch06-clone-agreement.png){ width="620" }

Mẫu còn thử cả chiến lược đối xứng: bỏ hẳn chuyện sao chép, chỉ tự chuẩn bị một
`|+⟩` mới trên bản sao bằng `H`. Như bảng dưới đây cho thấy, không chiến lược
nào phủ hết mọi đầu vào.

| Đầu vào | `CNOT`: bản sao | `CNOT`: bản gốc | `H` mới trên bản sao | Một bản sao thật |
|---|---|---|---|---|
| <code>\|0⟩</code> | 1.00 | 1.00 | 0.50 | 1.00 |
| <code>\|1⟩</code> | 1.00 | 1.00 | 0.50 | 1.00 |
| <code>\|+⟩</code> | 0.50 | 0.50 | 1.00 | 1.00 |
| <code>\|−⟩</code> | 0.50 | 0.50 | 0.00 | 1.00 |

Đọc dọc các cột `CNOT` cho thấy một chiến lược sao chép được trạng thái cơ sở
nhưng hỏng trên chồng chập. Đọc cột `H` cho thấy trật tự ngược lại.
**Không chiến lược nào đúng cho cả bốn đầu vào.** Khoảng trống đo được giữa
điều mỗi chiến lược đạt được và điều một bản sao thật đòi hỏi — chính là định
lý không nhân bản được trình bày dưới dạng dữ liệu chứ không phải dạng chứng
minh.

![Độ trung thực của bản sao bằng CNOT](../assets/ch06-clone-fidelity.png){ width="420" }

!!! note "Cái giá phải trả trên một mạng thật"
    Mạng cổ điển tạo một bản sao của mỗi gói tin để phòng khi liên kết đứt
    giữa chừng thì bản gốc vẫn được truyền lại an toàn. Mạng lượng tử không
    thể làm vậy, vì định lý không nhân bản đã gỡ bỏ tấm lưới an toàn đó ngay ở
    cấp nền tảng. Nó buộc phải *dựng lại* trạng thái ở mỗi liên kết từ những
    gì còn lại, và phần còn lại của chương nói về chính điều đó.

## Một pha mà bạn không nhìn thấy

Bài tập của Chương 6 ("Pauli-Z gate and Measurement") hỏi rằng *cổng hai qubit*
còn lại làm gì. `CZ`, cổng controlled-Z, chỉ khác `CNOT` ở một điểm: khi qubit
điều khiển bằng `1`, nó lật **pha** của qubit đích thay vì lật bit của nó. Sự
thay đổi tác động hoàn toàn vào cấu trúc dấu của các biên độ và không đụng đến
cấp độ nào cả, và điều này sẽ có vai trò ở phần dưới.

![Mạch H + CZ](../assets/ch06-cz-circuit.png){ width="420" }

Thí nghiệm được thực hiện bằng cách đặt cả hai qubit vào chồng chập cân bằng
trước, rồi áp dụng `CZ`:

$$H(0),\, H(1) \quad\longrightarrow\quad \frac{|00\rangle + |01\rangle + |10\rangle + |11\rangle}{2}
\qquad\text{(trạng thái tích)}$$
$$\xrightarrow{\;CZ\;}\quad \frac{|00\rangle + |01\rangle + |10\rangle - |11\rangle}{2}
\qquad\text{(đã rối)}$$

Chỉ một dấu đổi đã thay đổi hoàn toàn bản chất của trạng thái: ma trận hệ số
đi từ hạng 1 lên hạng 2, và có thể suy ra rằng hai qubit không còn độc lập.
(Xem
[trạng thái tích so với rối](ch05-entanglement.md#trang-thai-tich-so-voi-trang-thai-roi),
mục này trình bày chi tiết cách kiểm tra hạng.)

Đo cả hai qubit ở thời điểm này cho **cả bốn kết quả ở mức 25% mỗi loại** —
đúng biểu đồ cột giống hệt trạng thái khi chưa có `CZ`:

![CZ so với trạng thái Bell](../assets/ch06-cz-vs-bell.png){ width="620" }

Quy tắc Born *bình phương* các biên độ khi chuyển chúng thành xác suất, nên
`|−½|² = |+½|²`. Dấu vẫn ở đó trong trạng thái, sự rối là thật, và một phép đo
theo cơ sở tính toán không báo gì để phân biệt hai tình huống. Muốn phân biệt
hai trạng thái này theo đó cần một **cơ sở đo khác** — và đó chính xác là mẹo
mà teleportation dựa vào ở phần tiếp theo.

![Các ma trận hệ số](../assets/ch06-cz-matrices.png){ width="620" }

Hai trường hợp đối chiếu hoàn thiện bức tranh. `CZ` sau một `H` đơn lẻ là
**vô tác dụng hoàn toàn**, vì qubit 1 vẫn ở `|0⟩` nên điều khiển không bao giờ
kích hoạt. Và `CZ` trên trạng thái Bell chỉ lật cùng một dấu, còn tập kết quả
`{00, 11}` không đổi, vì `CNOT` đã thực hiện phần tương quan mà phép lật pha
sẽ tác động từ trước rồi.

## Dịch chuyển lượng tử: chuyển trạng thái, không phải hạt

Chương giờ đến kết quả chính. Alice không thể đọc qubit của mình, và cũng
không thể gửi một bản sao, vì phần trước đã chứng minh không bản sao như vậy
có thể tồn tại. Nhưng cô ấy có thể *hủy* bản gốc một cách chủ ý và dựng lại
một trạng thái giống hệt ở phía Bob, nhờ các tương quan mà hai bên đã chia
sẻ từ trước:

| Qubit | Thuộc về |
|---|---|
| `q0` | Alice — trạng thái cần gửi |
| `q1` | Nửa của cặp Bell mà Alice chia sẻ với Bob |
| `q2` | Nửa còn lại của cặp đó — trạng thái kết thúc ở đây |

![Mạch teleportation](../assets/ch06-teleport-circuit.png){ width="620" }

Giao thức triển khai theo năm bước:

1. **Chia sẻ một cặp Bell.** `H(2)`, `CNOT(2,1)` — quay lại Chương 5, vì đây
   là cách dựng cặp rối làm tài nguyên của toàn bộ giao thức.
2. **Trải rộng trạng thái.** `CNOT(0,1)`, `H(0)`. Trạng thái của Alice giờ nằm
   rải trên cả hai qubit của cô ấy dưới dạng các tương quan, thay vì còn giữ
   nguyên trong một thanh ghi.
3. **Đo kiểu Bell.** Alice đo `q0` và `q1`. Điều này hủy `q0` — và chính sự hủy
   đó là điều cho phép trạng thái xuất hiện lại ở phía Bob, vì một trạng thái
   lượng tử không thể tồn tại đồng thời ở hai qubit.
4. **Gửi hai bit cổ điển.** Qua một kênh thông thường, với tốc độ ánh sáng —
   một tin nhắn cổ điển chỉ mang hai kết quả đo của Alice.
5. **Sửa sai.** Bob áp dụng `X` lên `q2` nếu bit của anh ấy cho `q1` là `1`, và
   `Z` nếu bit cho `q0` là `1`, hoá giải đúng lỗi trong bốn lỗi có thể mà phép
   đo đã gây ra.

| Tin nhắn của Alice | Bob áp dụng | Qubit của Bob khi Alice gửi <code>\|0⟩</code> | Độ trung thực |
|---|---|---|---|
| `00` | không làm gì | <code>\|0⟩</code> | 1.000 |
| `01` | `X` | <code>\|0⟩</code> | 1.000 |
| `10` | `Z` | <code>\|0⟩</code> | 1.000 |
| `11` | `X` rồi `Z` | <code>\|0⟩</code> | 1.000 |

Cả bốn tin nhắn đều xảy ra với xác suất ¼, và **cả bốn đều dựng lại trạng thái
chính xác**. Đó là toàn bộ điều giao thức khẳng định, và nó đúng cho mọi đầu
vào.

Cột **độ trung thực** dưới đây đo hai trạng thái giống nhau đến đâu, trên thang
chạy từ 0 đến 1. Độ trung thực bằng 1.0 nghĩa là hai trạng thái giống hệt nhau
đối với mọi mục đích đo lường:

| Alice gửi | Bob đo | Độ trung thực |
|---|---|---|
| <code>\|0⟩</code> | P(0) = 1.00 | 1.000 |
| <code>\|1⟩</code> | P(1) = 1.00 | 1.000 |
| <code>\|+⟩</code> | P(0) = 0.50, P(1) = 0.50 | 1.000 |
| <code>\|−⟩</code> | P(0) = 0.50, P(1) = 0.50 | 1.000 |

![Mọi tin nhắn đều dựng lại trạng thái](../assets/ch06-teleport-fidelity.png){ width="620" }

Cần lưu ý điều mà độ trung thực bằng 1.0 *không* có nghĩa ở đây: Bob không thể
tự tạo ra `|+⟩` từ `|0⟩`, cũng không thể tự tạo ra `|0⟩` từ `|+⟩`. Anh ấy chỉ
*dựng lại* một trạng thái vốn đã tồn tại ở phía Alice. Teleportation chuyển
**thông tin**, không chuyển hạt — dù sao thì `q0` của Alice vẫn mất, trong
mọi nhánh của giao thức.

![Kết quả của Bob theo trạng thái Alice gửi](../assets/ch06-teleport-outcomes.png){ width="620" }

!!! warning "Không truyền tín hiệu nhanh hơn ánh sáng"
    Bước 4 là một tin nhắn cổ điển thông thường, và nó bị giới hạn bởi tốc độ
    ánh sáng y như mọi luồng dữ liệu mạng khác. Không có hai bit đó, Bob chỉ
    giữ một trạng thái với lỗi pha ngẫu nhiên và không cách nào xác định hay
    sửa được. Đó là hai "bit cổ điển" trong tên của giao thức, và đó là lý do
    teleportation **không** vượt ánh sáng: phần lượng tử của cuộc chuyển giao
    không làm được gì hữu ích cho tới khi tin nhắn cổ điển kịp đến.

??? question "Tự kiểm tra — bước 3 nói phép đo của Alice *hủy* `q0`. Chẳng phải trạng thái đã mất trước khi Bob dựng lại được sao?"
    `q0` mất rồi, nhưng thông tin của trạng thái thì không: bước 2 đã trải nó
    lên các tương quan giữa cả ba qubit từ trước. Sau khi Alice đo, `q2` của
    Bob theo đó đã giữ trạng thái được gửi kèm một trong bốn lỗi đã biết — có
    thể bị lật (`X`), có thể bị lật pha (`Z`), có thể cả hai. Bốn tin nhắn của
    Alice, mỗi cái xác suất như nhau, ghi đúng lỗi đang xảy ra — vì vậy hai bit
    là đủ để sửa trạng thái, và cũng vì thế chúng là cần thiết, bởi thiếu hai
    bit đó lỗi vẫn còn ẩn danh và không thể sửa.

## Từ mạch tới mạng: trạm lặp

Teleportation chuyển trạng thái qua **một** liên kết. **Trạm lặp** (repeater)
nối nhiều liên kết lại để trạng thái vượt được khoảng cách xa hơn nhiều, với
một nút ở giữa đóng vai trò vừa là nơi nhận vừa là nơi gửi cho các liên
kết tiếp theo:

```
Alice (q0)  ---  mắt 1  ---  relay (q2)  ---  mắt 2  ---  Bob (q4)
                        với q1                    với q3
```

![Hai đoạn liên kết nối qua một nút trung gian](../assets/ch06-repeater-circuit.png){ width="620" }

Nút trung gian là phần thú vị của chuỗi. Nó **đo** các qubit của mình ở liên
kết đầu tiên, đúng như Alice đo vậy, nên nó không bao giờ giữ trạng thái một
cách sạch sẽ ở giữa hai liên kết. Thứ thực sự di chuyển từ đầu tới cuối không
phải là trạng thái: đó là chuỗi các **tương quan** cộng với *bốn* bit cổ điển
— hai từ Alice, hai từ nút trung gian.

Để chứng minh trạng thái thực sự đến nơi, Alice khởi tạo một qubit không phải
`|0⟩` cũng không phải `|1⟩`: một phép quay với `P(1) = 0.4`. Nếu nút trung gian
chỉ chuyển tiếp bit cổ điển, Bob sẽ không nhìn thấy gì ngoài 0 và 1. Thay vào
đó, thống kê của anh ấy khớp với thống kê của cô ấy, cho mọi đầu vào:

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

Một hỗn hợp thật sự đã đến với Bob, sau khi được dựng lại hai lần trên đường
đi. Cần lưu ý thêm rằng nút trung gian buộc phải *đo* mới chuyển tiếp được —
trạng thái không bao giờ nằm trên đường đi dưới dạng bản sao, và đó chính xác
là lý do quy trình vẫn hoạt động dù việc sao chép là bất khả thi.

!!! note "Hướng đi tiếp"
    Trong một mạng lượng tử, khoảng cách bị giới hạn bởi hao mất, chứ không
    phải bởi tốc độ ánh sáng. Có hai cơ chế khác nhau cùng tác động:

    - **Suy hao** — trạng thái bị hấp thụ hoặc tán xạ dọc đường và không bao
      giờ tới được nút nhận.
    - **Mất tính toàn vẹn** (decoherence) — trạng thái vẫn tới nơi nhưng chồng
      chập và pha của nó đã bị nhiễu làm hỗn loạn trên đường đi.

    Cả hai đều không sửa được, vì không có bản sao nào để dựa vào. Đó là lý do
    trạm lặp không khuếch đại tín hiệu yếu như trạm lặp cổ điển — thay vào đó,
    nó *dựng lại* trạng thái ở mỗi nút từ cặp rối dùng chung cộng một tin nhắn
    cổ điển. [Chương 8](ch08-secure-communication.md) biến cùng ý tưởng đó
    thành truyền thông an toàn.

## Các sơ đồ {#cac-so-do}

### Định lý không nhân bản

![Cách thử nhân bản](../assets/ch06-clone-attempt-circuit.png){ width="420" }

`CNOT` không nhân bản: nó rối. Qubit điều khiển đi qua cổng không bị đụng tới,
còn qubit đích chứa một đối tác Bell chứ không phải một bản sao — dấu hiệu
trực quan của định lý không nhân bản.

![Bản sao hoàn hảo so với cách thử bằng CNOT](../assets/ch06-clone-agreement.png){ width="620" }

Hai bản sao thật của `|+⟩` sẽ độc lập, cho mỗi kết quả 25%; cách thử lại tương
quan hoàn hảo, và các tổ hợp `01`/`10` biến mất hẳn khỏi biểu đồ.

![Độ trung thực của bản sao bằng CNOT](../assets/ch06-clone-fidelity.png){ width="420" }

Cách thử đúng đến từng chút với trạng thái cơ sở và sai hoàn toàn với chồng
chập, gói gọn cả định lý trong một biểu đồ duy nhất.

### Controlled-Z

![Mạch H + CZ](../assets/ch06-cz-circuit.png){ width="420" }

![CZ so với trạng thái Bell](../assets/ch06-cz-vs-bell.png){ width="620" }

Hai chuỗi đầu không thể phân biệt bằng phép đo, dù một cái là trạng thái tích
và cái kia đã rối — minh hoạ trực tiếp cho việc cơ sở tính toán che giấu nhiều
đến đâu.

![Các ma trận hệ số](../assets/ch06-cz-matrices.png){ width="620" }

Chỉ một dấu đổi là khác biệt giữa hai ma trận, và nó đã đủ đưa hạng của ma trận
hệ số từ 1 lên 2.

### Dịch chuyển lượng tử

![Mạch teleportation](../assets/ch06-teleport-circuit.png){ width="620" }

Các hộp `If X` và `If Z` là những phép sửa cổ điển, do kết quả đo của Alice
điều khiển và chỉ được áp lên qubit của Bob ở nơi tin nhắn yêu cầu.

![Mọi tin nhắn đều dựng lại trạng thái](../assets/ch06-teleport-fidelity.png){ width="620" }

![Kết quả của Bob theo trạng thái Alice gửi](../assets/ch06-teleport-outcomes.png){ width="620" }

### Bộ lặp

![Hai đoạn liên kết nối qua một nút trung gian](../assets/ch06-repeater-circuit.png){ width="620" }

Hai cặp Bell được tiêu hao, hai phép đo kiểu Bell được thực hiện, và bốn phép
sửa cổ điển dẫn dắt cả đoạn đường qua nút trung gian.

![Thống kê sống sót qua chuyến đi](../assets/ch06-repeater-consistency.png){ width="620" }

![Kỳ vọng so với đo được ở Bob](../assets/ch06-repeater-counts.png){ width="620" }

## Những điều cần nhớ

- Mạng cổ điển chuyển tiếp gói tin bằng cách **sao chép** chúng; mạng lượng tử
  không thể làm vậy, vì **định lý không nhân bản** cấm sao chép một trạng thái
  chưa biết.
- `CNOT` không nhân bản: nó rối. Cách thử thành công trên trạng thái cơ sở và
  hỏng trên chồng chập, và không biến thể nào phủ được cả hai.
- `CZ` lật một pha, còn quy tắc Born bình phương các biên độ — nên `CZ` có thể
  biến một trạng thái tích thành trạng thái rối **mà không đổi một xác suất đo
  nào**.
- **Teleportation** chuyển một trạng thái bằng cách hủy bản gốc rồi dựng lại
  nó từ cặp rối dùng chung cộng **hai bit cổ điển**. Nó chuyển thông tin, không
  chuyển hạt, và không vượt ánh sáng.
- Một **trạm lặp** nối các liên kết truyền tải; một nút trung gian mà phải
  *đo* vẫn có thể chuyển tiếp trạng thái, và qubit nhận được giữ nguyên thống
  kê ban đầu.
- Vì không thể sửa từ một bản sao dự phòng khi bị mất tính toàn vẹn, mạng lượng
  tử thật bị giới hạn bởi hiệu ứng mất coherence — cái giá của mẹo
  không-có-bản-sao.

## Mã nguồn của chương này

Bốn mẫu, mỗi mẫu cho một mục của sách, cùng một bộ mô phỏng nhỏ dùng chung:

- [`ch06/networking.py`](https://github.com/phonhay103/quantum-computing-in-action/blob/main/src/quantum_computing_in_action/ch06/networking.py)
  — byte qua TCP (6.2.1) và phần minh hoạ định lý không nhân bản (6.2.2).
- [`ch06/czmeasure.py`](https://github.com/phonhay103/quantum-computing-in-action/blob/main/src/quantum_computing_in_action/ch06/czmeasure.py)
  — bài tập Chương 6 về `CZ` và phép đo.
- [`ch06/teleportation.py`](https://github.com/phonhay103/quantum-computing-in-action/blob/main/src/quantum_computing_in_action/ch06/teleportation.py)
  — mạch teleportation và bảng phép sửa của nó.
- [`ch06/repeater.py`](https://github.com/phonhay103/quantum-computing-in-action/blob/main/src/quantum_computing_in_action/ch06/repeater.py)
  — chuỗi hai đoạn liên kết qua một nút trung gian.
- [`ch06/protocol.py`](https://github.com/phonhay103/quantum-computing-in-action/blob/main/src/quantum_computing_in_action/ch06/protocol.py)
  — bộ mô phỏng nhánh dùng chung. Teleportation cần một phép **đo giữa mạch**
  mà kết quả của nó điều khiển các cổng cổ điển, và `Statevector` của Qiskit
  từ chối các mạch chứa control flow. Module này thay vào đó giữ một *frame*
  cho mỗi kết quả đo, áp các cổng lên mọi frame và rẽ nhánh khi một qubit được
  đo.

Chạy toàn bộ bằng `make ch06`, hoặc từng mẫu một:

```bash
uv run python -m quantum_computing_in_action.ch06.teleportation
```

!!! note "Cách đọc nhãn trên mạch"
    Các mạch được *vẽ ra* là mạch Qiskit bình thường có khối `if_test`, đúng
    như cách viết bằng tay. Các con số đến từ bộ mô phỏng nhánh, vốn tính ra
    cùng phân phối mà không cần thực thi control flow. Các qubit được đánh số
    theo chỉ số thuần (`q0`, `q1`, ...), khớp với mẫu Java của sách, nên `q0`
    là qubit ở `q[0]`.
