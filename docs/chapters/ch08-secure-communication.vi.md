# Chương 8 — Truyền thông an toàn bằng điện toán lượng tử

!!! abstract "Trong một câu"
    Alice và Bob có thể thống nhất một **khoá bí mật** qua một đường công khai vì
    một qubit chỉ mang một bit *trong một cơ sở được chọn* — và kẻ nghe lén không
    biết cơ sở buộc phải làm nhiễu trạng thái, để lại tỉ lệ lỗi khoảng 25%.

## Một qubit chỉ mang bit trong một cơ sở

Mọi qubit trong chương này được viết trong một trong hai **cơ sở**:

- **cơ sở Z**, với các trạng thái `|0⟩` và `|1⟩` — bit thông thường;
- **cơ sở X**, với các trạng thái `|+⟩` và `|−⟩`, cách cơ sở Z đúng một cổng
  Hadamard.

Một cổng Hadamard xoay từ cơ sở này sang cơ sở kia, và — sự thật nhỏ mà cả chương
dựa vào — **`H·H = I`**: xoay vào một cơ sở rồi xoay ngược lại, thì không có gì
thay đổi.

![Vòng xoay Hadamard](../assets/ch08-haha-circuit.png){ width="420" }

Áp một cổng `X` để đặt một bit, rồi một Hadamard và thêm một Hadamard nữa, qubit
trở về đúng chỗ cũ:

$$|0\rangle \xrightarrow{X} |1\rangle \xrightarrow{H} |-\rangle \xrightarrow{H} |1\rangle$$

| Bước | P(00) | P(01) | P(10) | P(11) |
|---|---|---|---|---|
| bắt đầu: `\|00⟩` | 1.00 | 0.00 | 0.00 | 0.00 |
| `X(0)` | 0.00 | 1.00 | 0.00 | 0.00 |
| `H(0), H(1)` | 0.25 | 0.25 | 0.25 | 0.25 |
| `H(0), H(1)` lần nữa | 0.00 | 1.00 | 0.00 | 0.00 |

![Đi vào một cơ sở rồi rời khỏi nó](../assets/ch08-haha-bloch.png){ width="620" }

Chuyến đi vòng qua cơ sở X (hàng 3) trông như một lần tung đồng xu trong cơ sở Z —
mọi kết quả đều cân bằng — vậy mà nó **không để lại dấu vết**: hàng cuối giống hệt
hàng `X`. Một cơ sở là thứ bạn có thể nấp phía sau, vì rời khỏi nó không tốn gì.

## Hai cách làm không thành công

Trước BB84, những thiết kế hiển nhiên đều thất bại, mỗi cái vì một lý do khác nhau.

**Không dùng cơ sở nào.** Alice gửi thẳng `|0⟩`/`|1⟩`, Bob đo trong cơ sở Z và đọc
lại đúng từng bit. Trông có vẻ hoàn hảo, và đó chính là thất bại: việc bị đọc
không làm nhiễu qubit chút nào, nên **thứ gì Bob đọc được thì Eve cũng đọc được**.
Không có bí mật, chỉ có một cuộc trò chuyện không bị ai nghe.

**Một cơ sở không ai đối chiếu.** Alice tung đồng xu cho từng qubit rồi chuẩn bị nó
trong Z hoặc X. Bob, không biết cơ sở nào, đo tất cả trong Z. Khi Alice dùng Z thì
Bob đúng; khi cô dùng X thì anh nhận được một đồng xu công bằng. Một nửa số qubit
sai, một nửa trong đó lật, và tỉ lệ lỗi thô rơi vào khoảng một phần tư:

| Cách làm | Tỉ lệ lỗi thô | Kết luận |
|---|---|---|
| Ngây thơ (không cơ sở) | 0.00 | Bob đọc được tất cả — Eve cũng vậy |
| Cơ sở mù (chỉ Z) | ≈ 0.25 | một bit trong bốn bị sai |

![Vì sao phải đối chiếu cơ sở](../assets/ch08-attempts-error.png){ width="560" }

Cách chữa không phải là thêm qubit, mà là một **cuộc trò chuyện công khai** ngắn
về các cơ sở.

## Dùng chồng chập cũng không đủ

Ý tưởng thứ ba hiển nhiên: nếu bit thuần ai cũng đọc được và một cơ sở giấu kín là
chưa đủ, sao không gửi các bit **trong chồng chập**? Hadamard mọi qubit và thanh ghi
giữ cả `2^n` trạng thái cùng lúc.

Đúng là như vậy — và đó là một khả năng thật, không phải mẹo. Với bốn qubit, thanh
ghi đi qua **mười sáu** trạng thái cơ sở, mỗi trạng thái biên độ `1/4`:

![Một thanh ghi trong chồng chập, và chính thanh ghi đó được khôi phục](../assets/ch08-superposition-states.png){ width="620" }

Nhưng nó rời khỏi chồng chập dễ như khi bước vào, vì quy tắc ở đầu chương:
**`H·H = I`**. Một vòng Hadamard trải trạng thái ra mười sáu trạng thái; vòng thứ hai
là nghịch đảo của nó, nên thứ đến phép đo đúng là trạng thái đã chuẩn bị — và Bob đọc
bit của Alice hoàn hảo.

![Mạch chồng chập bốn qubit](../assets/ch08-superposition-circuit.png){ width="620" }

| Bước | Phân bố |
|---|---|
| đã chuẩn bị | một trạng thái: chuỗi bit đã chuẩn bị |
| sau một `H` trên mọi qubit | cả 16 trạng thái, mỗi trạng thái xác suất `1/16` |
| sau hai `H` trên mọi qubit | lại đúng chuỗi bit đã chuẩn bị |

Vậy chồng chập không phải là bí mật. Nó là một **phép xoay**, và ai biết cách xoay
ngược lại thì thấy hết. Muốn giữ bí mật cần đúng một thành phần mà BB84 thêm vào: một
cơ sở do Alice chọn ngẫu nhiên và chỉ công bố sau khi các qubit đã đi qua.

## BB84: giữ lại những qubit có cơ sở khớp nhau

Giao thức là một lần tung đồng xu cho mỗi qubit ở mỗi bên, cộng một thông báo công
khai.

1. **Alice** chọn ngẫu nhiên một bit và một cơ sở, rồi chuẩn bị qubit trong cơ sở
   đó — một trong `|0⟩`, `|1⟩`, `|+⟩`, `|−⟩`.
2. **Bob** chọn ngẫu nhiên một cơ sở và đo.
3. Hai người **sàng lọc**: họ công bố **cơ sở** — không bao giờ công bố bit — và
   chỉ giữ những qubit mà cơ sở khớp nhau. Khi khớp, bit của Bob chắc chắn là bit
   của Alice.

![Một mạch BB84](../assets/ch08-bb84-circuit.png){ width="620" }

Một nửa số qubit khớp, nên một trao đổi `N` qubit cho khoảng `N/2` bit khoá. Trong
ví dụ, 8 qubit cho 2 vị trí khớp và cả hai bit đều đồng ý:

| # | Bit Alice | Cơ sở Alice | Cơ sở Bob | Bit Bob | |
|---|---|---|---|---|---|
| 0 | 1 | Z | X | 1 | bỏ (cơ sở khác nhau) |
| 1 | 0 | X | Z | 0 | bỏ (cơ sở khác nhau) |
| 2 | 0 | X | Z | 1 | bỏ (cơ sở khác nhau) |
| 3 | 0 | X | X | 0 | giữ |
| 4 | 0 | X | Z | 1 | bỏ (cơ sở khác nhau) |
| 5 | 1 | Z | X | 1 | bỏ (cơ sở khác nhau) |
| 6 | 0 | X | Z | 0 | bỏ (cơ sở khác nhau) |
| 7 | 0 | Z | Z | 0 | giữ |

## Kẻ nghe lén không thể ẩn mình

Vì sao điều này phát hiện được kẻ nghe lén? Eve không thể **sao chép** một qubit —
[định lý không nhân bản](ch06-quantum-networking.md) cấm điều đó — nên cách tốt
nhất cô có thể làm là **chặn rồi gửi lại**: đo mỗi qubit trong một cơ sở cô đoán,
rồi gửi tiếp đúng trạng thái mà cô đã làm nó sụp về. Cô đoán đúng một nửa số lần.

Khi đoán đúng, cô chuyển tiếp trạng thái đúng và Bob không hề hay biết. Khi đoán
sai, phép đo của cô *đã* phá huỷ trạng thái của Alice, và trạng thái cô gửi đi
khác với trạng thái của Alice khoảng một nửa số lần. Tính trung bình trên các lần
tung đồng xu của cô, một phần tư số bit đã sàng lọc của Bob là sai:

| Đường truyền | Tỉ lệ lỗi trung bình sau sàng lọc |
|---|---|
| Không có kẻ nghe lén | 0.000 |
| Chặn rồi gửi lại | ≈ 0.25 |

![Đường sạch so với một đường bị nghe trộm](../assets/ch08-eavesdropper-error.png){ width="620" }

Hai lần trao đổi 8 qubit không bao giờ giống nhau, nhưng 200 lần thì tách bạch rõ
ràng: đường sạch dồn hết vào **0** lỗi, còn đường bị nghe trộm trải ra quanh mức
một phần tư số bit đã sàng lọc. Alice và Bob so một mẫu khoá của họ; một vài bất
đồng là nhiễu thường, nhưng một phần tư là nghe trộm, và họ vứt khoá đi rồi thử lại.

!!! note "Một khoá, không phải thông điệp"
    BB84 tạo ra một **khoá** ngẫu nhiên dùng chung, không phải thông điệp. Khoá đó
    sau đó dùng với một mật mã thông thường — ví dụ một bảng một lần (one-time
    pad) — nên phần lượng tử chỉ cần giải nửa khó: thống nhất bí mật giữa thanh
    thiên bạch nhật.

## Sơ đồ

### Vòng xoay Hadamard

![Vòng xoay Hadamard](../assets/ch08-haha-circuit.png){ width="420" }

![Đi vào một cơ sở rồi rời khỏi nó](../assets/ch08-haha-bloch.png){ width="620" }

`H·H = I`: trạng thái ở giữa trải trên cả bốn kết quả, và trạng thái cuối lại là
hàng `X` — một cơ sở được đi vào rồi rời ra miễn phí.

### Những cách làm thất bại

![Vì sao phải đối chiếu cơ sở](../assets/ch08-attempts-error.png){ width="560" }

Không lỗi nào từ một kênh không cơ sở không phải là thành công — đó là sự vắng
mặt của một bí mật.

### Chồng chập: cả mười sáu trạng thái, rồi chính thanh ghi đó trở lại

![Mạch chồng chập bốn qubit](../assets/ch08-superposition-circuit.png){ width="620" }

![Một thanh ghi trong chồng chập, và chính thanh ghi đó được khôi phục](../assets/ch08-superposition-states.png){ width="620" }

### BB84 và kẻ nghe trộm

![Một mạch BB84](../assets/ch08-bb84-circuit.png){ width="620" }

Phần chuẩn bị của Alice (một `X` cho bit `1`, một Hadamard cho cơ sở X), phép xoay
cơ sở của Bob, và phép đo.

![Đường sạch so với một đường bị nghe trộm](../assets/ch08-eavesdropper-error.png){ width="620" }

## Những điều cần nhớ

- Một qubit chỉ mang bit tương đối với một **cơ sở**. Cơ sở Z chứa `|0⟩`,`|1⟩`; cơ
  sở X chứa `|+⟩`,`|−⟩`; một Hadamard chuyển giữa chúng, và `H·H = I`.
- Một kênh bit thuần tuý thì ai cũng đọc được — cả Bob **và** Eve. Không lỗi nào
  không phải là bí mật.
- Thêm một cơ sở ngẫu nhiên không tự cứu được: nếu Bob không bao giờ biết cơ sở
  đó, một phần tư số bit sẽ sai.
- Gửi các bit **trong chồng chập** cũng không phải bí mật: thanh ghi thật sự trải
  trên cả `2^n` trạng thái, nhưng `H·H = I` đưa đúng các bit đã chuẩn bị trở lại,
  nên Bob đọc chúng hoàn hảo.
- **BB84** khắc phục bằng cách sàng lọc theo **cơ sở**: công bố cơ sở, giữ những
  qubit khớp nhau, và các bit giữ lại là giống hệt nhau.
- **Không nhân bản** nghĩa là kẻ nghe lén buộc phải làm nhiễu trạng thái. Một đòn
  chặn-rồi-gửi-lại để lại tỉ lệ lỗi **~25%** nơi đường sạch để lại 0 — nên việc
  nghe trộm là phát hiện được, và Alice với Bob có thể từ chối một khoá đã bị lộ.

## Mã nguồn của chương này

Ba mẫu, mỗi mẫu cho một mục của sách, cùng một mô hình dùng chung nhỏ:

- [`ch08/identity.py`](https://github.com/phonhay103/quantum-computing-in-action/blob/main/src/quantum_computing_in_action/ch08/identity.py)
  — mẫu ``haha``: `X` rồi `H`, `H`, và trạng thái trở về (8.2).
- [`ch08/attempts.py`](https://github.com/phonhay103/quantum-computing-in-action/blob/main/src/quantum_computing_in_action/ch08/attempts.py)
  — hai cách làm ``naive`` và ``guess`` thất bại.
- [`ch08/superposition.py`](https://github.com/phonhay103/quantum-computing-in-action/blob/main/src/quantum_computing_in_action/ch08/superposition.py)
  — mẫu ``superposition``: cả thanh ghi trong `2^n` trạng thái cùng lúc, và `H·H = I`
  đưa đúng các bit đã chuẩn bị trở lại.
- [`ch08/bb84.py`](https://github.com/phonhay103/quantum-computing-in-action/blob/main/src/quantum_computing_in_action/ch08/bb84.py)
  — giao thức đúng, với kẻ nghe lén chặn-rồi-gửi-lại và sự tách biệt tỉ lệ lỗi.
- [`ch08/protocol.py`](https://github.com/phonhay103/quantum-computing-in-action/blob/main/src/quantum_computing_in_action/ch08/protocol.py)
  — mô hình qubit dùng chung: bốn trạng thái, một quy tắc đo duy nhất (cùng cơ sở =
  bit, khác cơ sở = đồng xu công bằng), phép sàng lọc, và mạch đáng để vẽ.

Chạy toàn bộ bằng `make ch08`, hoặc từng mẫu một:

```bash
uv run python -m quantum_computing_in_action.ch08.bb84
```
