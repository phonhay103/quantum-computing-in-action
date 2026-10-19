# Chương 8 — Truyền thông an toàn bằng điện toán lượng tử

!!! abstract "Tóm lại một câu"
    Alice và Bob có thể thống nhất một **khoá bí mật** qua một đường công khai vì
    một qubit chỉ mang một bit *trong một cơ sở được chọn* — và kẻ nghe lén không
    biết cơ sở buộc phải làm nhiễu trạng thái, để lại tỉ lệ lỗi khoảng 25%.

## Câu hỏi chương này trả lời

Alice và Bob chưa từng gặp nhau riêng tư, vậy mà họ cần một bí mật. Mọi đường
truyền giữa họ đều công khai: thứ gì Alice gửi, một bên thứ ba — gọi là **Eve** —
đều có thể xem. Theo cách cổ điển thì việc này tuyệt vọng theo một nghĩa thú vị:
đọc một bản sao của thông điệp không làm hỏng bản gốc, nên Eve có thể sao chép
lặng lẽ và không ai biết. Chương này hỏi bốn câu về tình huống đó:

1. **Làm sao viết một bit để việc đọc nó là một sự *lựa chọn*?** Một qubit chỉ
   mang bit tương đối với một **cơ sở**, và người đọc dùng sai cơ sở sẽ nhận về
   một đồng xu thay vì bit.
2. **Vì sao các thiết kế hiển nhiên đều thất bại?** Gửi bit trần, giấu chúng
   trong một cơ sở ngẫu nhiên, hay trải chúng ra một chồng chập — mỗi cách đều
   có vẻ hứa hẹn, và mỗi cách thất bại vì một lý do đáng biết trước khi hiểu
   được lời giải.
3. **Một cuộc trò chuyện công khai tạo khoá riêng tư bằng cách nào?** BB84: công
   bố **cơ sở** (không bao giờ công bố bit), giữ những qubit mà hai bên chọn cùng
   cơ sở, và các bit giữ lại giống hệt nhau.
4. **Vì sao Eve không thể ẩn mình?** Cô không thể sao chép một qubit, buộc phải
   đo nó, trong một cơ sở chỉ đoán được — và những lần đoán sai để lại vết tay
   khoảng **25%** trong khoá đã sàng lọc, nơi đường sạch để lại đúng **0**.

Sau chương này bạn sẽ giải thích được:

- **cơ sở** là gì (cơ sở Z với `|0⟩`, `|1⟩` và cơ sở X với `|+⟩`, `|−⟩`) và tính
  được, bằng số cụ thể, phép đo trong mỗi cơ sở trả về gì;
- giải thích `H·H = I` là "cơ sở đúng triệt tiêu, cơ sở sai thì không", qua
  vòng xoay Hadamard;
- nói chính xác vì sao bit trần, một cơ sở không được đối chiếu, và một chồng
  chập đều không tạo ra bí mật;
- đi qua một trao đổi BB84 8 qubit từng dòng một: vị trí nào sống sót qua sàng
  lọc và khoá thu được là gì;
- tính tỉ lệ lỗi của kẻ nghe lén là `1/2 × 1/2 = 1/4`, và giải thích vì sao
  đường sạch nằm đúng ở mức 0.

Bạn cần ba điều từ các chương trước, mỗi điều một dòng: `H` đưa một qubit vào
chồng chập đều 50/50 ([Chương 4](ch04-superposition.md)); đo một chồng chập làm
nó sụp, và một giá trị *lạ* thì không thể sao chép — chỉ có thể rối
([Chương 6](ch06-quantum-networking.md)); và trạng thái của một mạch đọc được
sau mỗi bước ([Chương 7](ch07-helloworld-explained.md)).

!!! note "Cách đọc các bảng trong chương này"
    - Một **cơ sở** là cặp trạng thái mà phép đo so với. Chương này dùng hai:
      **cơ sở Z** (`|0⟩`, `|1⟩` — bit thường) và **cơ sở X** (`|+⟩`, `|−⟩` —
      cách đó đúng một cổng Hadamard). `Z` và `X` tên cơ sở; `0` và `1` tên bit.
    - Bảng vòng xoay hai qubit dùng thứ tự nhãn của Qiskit `q1 q0`: ký tự
      *bên phải* là `q0`, qubit mang bit.
    - Nhãn thanh ghi bốn qubit (ví dụ `0110`) dùng thứ tự của sách, `q0` trước —
      đúng quy ước của [Chương 7](ch07-helloworld-explained.md).
    - Các bảng bit/cơ sở có một dòng cho mỗi vị trí qubit, vị trí `0` trước.

## Một qubit chỉ mang bit trong một cơ sở

Một bit cổ điển có đúng một bảng chữ cái: `0` và `1`, và mọi người đọc đều dùng
nó. Một qubit có (ít nhất) hai bảng chữ cái, và *việc đọc theo bảng nào là một
lựa chọn*. Lựa chọn đó là cả chương này, nên hãy bắt đầu bằng con số cụ thể.

Bốn trạng thái Alice có thể gửi, viết dạng vector:

| Cơ sở | bit `0` | bit `1` |
|---|---|---|
| Z | `|0⟩` = (1, 0) | `|1⟩` = (0, 1) |
| X | `|+⟩` = (1, 1)/√2 | `|−⟩` = (1, −1)/√2 |

**Một phép đo làm sẵn.** Alice gửi `|0⟩` — *bit* là `0`, *cơ sở* là Z.

- Bob đo trong **Z**: xác suất đọc `0` là `|⟨0|0⟩|² = 1`. Chắc chắn. Đây là bit
  thường bạn đã quen.
- Bob đo trong **X**: hai kết quả lúc này là `|+⟩` (bit `0`) và `|−⟩` (bit `1`).
  Xác suất đọc bit `0` là

$$|\langle +|0\rangle|^2 = \left(\tfrac{1}{\sqrt{2}}\right)^2 = \tfrac{1}{2}$$

  Một đồng xu 50/50 — về một trạng thái hoàn toàn xác định.

**Quy tắc chung, giờ ví dụ đã nằm trên bàn.** Đo trong cơ sở đã chuẩn bị trả về
bit *chắc chắn* — đủ cả bốn trạng thái, cả hai bit. Đo trong cơ sở kia trả về
một đồng xu công bằng *dù bit là gì*: `|⟨+|1⟩|² = 1/2` như trên, và
`|⟨0|−⟩|² = |⟨1|−⟩|² = 1/2` cũng vậy. Đã kiểm chứng với simulator
(`protocol.state_probabilities`): mọi phép đo cùng cơ sở là chắc chắn, mọi phép
đo chéo cơ sở là `0.5 / 0.5`.

**Vì sao vòng xoay quan trọng: `H·H = I`.** Cổng Hadamard đưa qubit từ cơ sở
này sang cơ sở kia (`H|0⟩ = |+⟩`, `H|1⟩ = |−⟩`), và nó tự là nghịch đảo của
mình: áp hai lần thì chẳng có gì xảy ra. Mẫu `haha` của sách theo dõi cổng này
từng bước trên hai qubit — `q0` mang bit, `q1` ngồi bên cạnh trong cơ sở X:

$$|0\rangle \xrightarrow{X} |1\rangle \xrightarrow{H} |-\rangle \xrightarrow{H} |1\rangle
\qquad
|0\rangle \xrightarrow{H} |+\rangle \xrightarrow{H} |0\rangle$$

![Vòng xoay Hadamard](../assets/ch08-haha-circuit.png){ width="420" }

Trạng thái ghép, đọc sau mỗi bước (nhãn `q1 q0`, nên `01` nghĩa là `q0 = 1,
q1 = 0`):

| Bước | P(00) | P(01) | P(10) | P(11) |
|---|---|---|---|---|
| bắt đầu: `\|00⟩` | 1.00 | 0.00 | 0.00 | 0.00 |
| `X(0)` | 0.00 | 1.00 | 0.00 | 0.00 |
| `H(0), H(1)` | 0.25 | 0.25 | 0.25 | 0.25 |
| `H(0), H(1)` lần nữa | 0.00 | 1.00 | 0.00 | 0.00 |

![Đi vào một cơ sở rồi rời khỏi nó](../assets/ch08-haha-bloch.png){ width="620" }

Dòng 3 đáng có phép tính. Thanh ghi là `q1` trong `|+⟩` và `q0` trong `|−⟩`, tức
`|+−⟩`:

$$|+\rangle \otimes |-\rangle = \tfrac{1}{2}\,(|00\rangle - |01\rangle + |10\rangle - |11\rangle)$$

Bốn trạng thái cơ sở, biên độ mỗi cái `±1/2`, xác suất mỗi cái `1/4`. *Dấu*
không hiện với phép đo — phép đo chỉ thấy `|biên độ|²` — nhưng không hề mất:
một Hadamard thấy chúng. Áp `H` lên cả hai qubit lần nữa, các số hạng hợp lại
thành đúng `q0 = 1, q1 = 0`, nhãn `01`, xác suất 1.00. Dòng 4 chính là dòng 2
lần nữa, đúng từng con số: **chuyến vòng qua cơ sở X không để lại dấu vết.**

Đó là "vì sao nó hoạt động". Hãy đọc như một quy tắc về cơ sở: nếu Bob đo trong
cơ sở của Alice, Hadamard của anh (vào bảng chữ cái Z, ngay trước phép đo) hoàn
tác Hadamard của cô — `H·H = I`, bit đi qua nguyên vẹn. Nếu anh đo trong cơ sở
*kia*, chỉ một Hadamard tác động: `H` một mình, và trạng thái anh đo là một
chồng chập *trong bảng chữ cái của anh* — một đồng xu. **Cơ sở đúng = `H·H`; cơ
sở sai = `H` một mình.** Một cơ sở là thứ bạn có thể nấp phía sau, vì rời khỏi
nó không tốn gì của chủ nhân, mà lấy đi hết certainty của người lạ.

??? question "Tự kiểm tra — Alice gửi `|−⟩` (bit `1`, cơ sở X). Bob đo trong Z và nhận `0`. Liệu anh ta có thể kết luận bit là `0`?"
    Không — tệ hơn, anh ta *không học được gì*. Dù Alice gửi gì, phép đo Z trên
    một trạng thái cơ sở X cũng là một đồng xu công bằng: `|⟨0|−⟩|² = 1/2` và
    `|⟨1|−⟩|² = 1/2`. Bob nhận `0` cũng khả năng như nếu Alice gửi `|+⟩` (bit
    `0`) hay `|−⟩` (bit `1`), nên nó mang không thông tin. Và phép đo của anh
    đã làm qubit sụp về `|0⟩` — không ai có thể đo lại nó trong cơ sở đúng sau
    đó. Một câu trả lời sai cơ sở không phải bản bản nhiễu của bit; nó là một
    đồng xu phá huỷ bản gốc.

## Hai cách làm không thành công

Trước BB84, sách thử các thiết kế hiển nhiên và xem mỗi cách thất bại vì một lý
do khác nhau. Các con số dưới đây là các lượt chạy thật của chính module trong
chương.

**Cách 1 — không dùng cơ sở nào.** Alice mã hoá mỗi bit trong Z
(`|0⟩`/`|1⟩`) rồi gửi. Bob đo trong Z. Một lượt 64 qubit: tỉ lệ lỗi thô là
**0.00** — mọi bit đến nguyên vẹn. Trông có vẻ hoàn hảo, và đó chính là thất
bại: phép đo một bit trần không làm nhiễu gì, nên không gì ngăn Eve đọc cùng
những bit đó. **Thứ gì Bob đọc được thì Eve cũng đọc được.** Không lỗi ở đây
nghĩa là không bí mật — một cuộc trò chuyện không bị xem, chứ không phải riêng
tư.

**Cách 2 — một cơ sở không ai đối chiếu.** Alice giờ tung đồng xu cho từng
qubit và chuẩn bị nó trong Z hoặc X. Bob, không được báo, đo tất cả trong Z.
Khi Alice dùng Z thì anh đúng; khi cô dùng X thì anh nhận một đồng xu, và một
nửa số đồng xu rơi vào bit sai. Phép tính:

$$\underbrace{\tfrac{1}{2}}_{\text{sai cơ sở}} \times \underbrace{\tfrac{1}{2}}_{\text{đồng xu rơi sai}} = \tfrac{1}{4}$$

Các lượt chạy thật: một lượt 64 qubit ra **0.36** (23/64 bit sai — mẫu nhỏ thì
dao động), và một lượt 800 qubit ra **0.235**, tiệm cận mức một phần tư đã
đoán.

| Cách làm | Tỉ lệ lỗi thô (đo được) | Kết luận |
|---|---|---|
| Ngây thơ (không cơ sở) | 0.00 (64 qubit) | Bob đọc được tất cả — Eve cũng vậy |
| Cơ sở mù (chỉ Z) | 0.36 trong lượt 64 qubit, 0.235 trên 800 | một bit trong bốn bị sai |

![Vì sao phải đối chiếu cơ sở](../assets/ch08-attempts-error.png){ width="560" }

Cách 2 thú vị vì nó thất bại theo hướng *ngược* với Cách 1: giờ có thứ Eve
không biết (cơ sở), nhưng Bob cũng không biết, và một khoá sai một bit trong
bốn thì không dùng được. Cách chữa không phải thêm qubit, mà là một **cuộc trò
chuyện công khai về cơ sở** — chính là điều BB84 thêm vào.

## Dùng chồng chập cũng không đủ

Ý tưởng thứ ba hiển nhiên: nếu bit trần ai cũng đọc được và cơ sở giấu kín là
chưa đủ, hãy gửi các bit **trong chồng chập** — Hadamard mọi qubit để thanh ghi
giữ cả `2^n` trạng thái cùng lúc. Eve surely không thể đọc một trạng thái vẫn
còn "đang chảy"?

Nó thật sự trải thanh ghi ra — rồi trải thẳng trở lại, vì `H·H = I`. Hãy theo
dõi phép tính trên bốn qubit của mẫu, chuẩn bị với các bit `0110` (một `X` trên
mỗi qubit có bit `1`):

**Đã chuẩn bị.** Một trạng thái cơ sở xác định, `|0110⟩`, xác suất 1.00.

**Sau một vòng `H`.** Mỗi qubit tách với biên độ `1/√2` mỗi số hạng, nên mỗi
trong `2⁴ = 16` trạng thái của thanh ghi mang biên độ `(1/√2)⁴ = 1/4`:

$$\underbrace{\left(\tfrac{1}{\sqrt{2}}\right)^4}_{\text{biên độ}} = \tfrac{1}{4},
\qquad
\text{xác suất mỗi trạng thái} = \left(\tfrac{1}{4}\right)^2 = \tfrac{1}{16} = 0.0625$$

Mười sáu trạng thái mỗi cái `0.0625`, và `16 × 0.0625 = 1`: toàn bộ khối xác
suất, trải đều. Đây là nghĩa *bằng số cụ thể* của "thanh ghi ở trong mọi trạng
thái cùng lúc".

**Sau vòng `H` thứ hai.** Vòng hai là nghịch đảo của vòng một (`H·H = I` trên
mọi qubit), nên các biên độ hợp lại thành đúng trạng thái đã chuẩn bị: `|0110⟩`
với xác suất 1.00, và `0` ở mọi nơi khác.

![Một thanh ghi trong chồng chập, và chính thanh ghi đó được khôi phục](../assets/ch08-superposition-states.png){ width="620" }

![Mạch chồng chập bốn qubit](../assets/ch08-superposition-circuit.png){ width="620" }

| Bước | Phân bố (đã kiểm chứng) |
|---|---|
| đã chuẩn bị | một trạng thái: `0110`, xác suất 1.00 |
| sau một `H` trên mọi qubit | cả 16 trạng thái, mỗi trạng thái xác suất `1/16 = 0.0625` |
| sau hai `H` trên mọi qubit | lại `0110`, xác suất 1.00 |

Vậy Bob — vốn biết công thức, vì Alice chỉ cần áp `H` hai lần — đọc các bit hoàn
hảo. Lượt chạy mẫu của chương: Alice gửi `1000`, Bob nhận `1000`, bốn qubit,
không lỗi. Eve cũng làm được điều đó: trạng thái "trải" không bị giấu, nó bị
*xoay*, và ai biết phép xoay thì đọc được.

Chồng chập là một khả năng thật (Chương 9 sẽ dùng nó mạnh), nhưng nó không phải
bí mật. Bí mật cần đúng một thành phần mà không cách nào ở trên có: một cơ sở do
Alice chọn ngẫu nhiên và chỉ công bố **sau khi các qubit đã đi qua**.

## BB84: giữ lại những qubit có cơ sở khớp nhau

Giao thức là một lần tung đồng xu cho mỗi qubit ở mỗi bên, cộng một thông báo
công khai:

1. **Alice** chọn ngẫu nhiên một bit *và* một cơ sở, rồi chuẩn bị qubit trong cơ
   sở đó — một trong `|0⟩`, `|1⟩`, `|+⟩`, `|−⟩`.
2. **Bob** chọn ngẫu nhiên một cơ sở và đo.
3. Hai người **sàng lọc**: họ công bố **cơ sở** — không bao giờ công bố bit —
   và chỉ giữ những qubit mà cơ sở khớp nhau. Khi khớp, Hadamard đo của Bob
   hoàn tác Hadamard chuẩn bị của Alice (`H·H = I`), nên bit của Bob *chính là*
   bit của Alice, chắc chắn.

![Một mạch BB84](../assets/ch08-bb84-circuit.png){ width="620" }

**Một trao đổi hoàn chỉnh** — 8 qubit, tạo bằng một seed cố định với chính mã
của chương (`bb84.exchange(seed=2)`), nên bạn có thể tái hiện từng ô:

| # | Bit Alice | Cơ sở Alice | Cơ sở Bob | Bit Bob | kết luận |
|---|---|---|---|---|---|
| 0 | 1 | Z | X | 1 | bỏ (cơ sở khác nhau) |
| 1 | 0 | X | Z | 0 | bỏ (cơ sở khác nhau) |
| 2 | 0 | X | Z | 1 | bỏ (cơ sở khác nhau) |
| 3 | 0 | X | X | 0 | **giữ** |
| 4 | 0 | X | Z | 1 | bỏ (cơ sở khác nhau) |
| 5 | 1 | Z | X | 1 | bỏ (cơ sở khác nhau) |
| 6 | 0 | X | Z | 0 | bỏ (cơ sở khác nhau) |
| 7 | 0 | Z | Z | 0 | **giữ** |

Đi qua từng dòng:

- **Dòng 0:** Alice gửi bit `1` trong Z (`|1⟩`). Bob chọn X. Bit `1` của anh là
  một đồng xu (`|⟨−|1⟩|² = 1/2`) — nó *tình cờ* khớp, nhưng không phải thông
  tin, nên vị trí này bị loại.
- **Dòng 1, 2, 4, 6:** Alice dùng X, Bob dùng Z. Chú ý dòng 2: bit của Bob là
  `1` trong khi của Alice là `0` — đúng hành xử đồng xu, và đúng lý do những vị
  trí này phải đi.
- **Dòng 3:** cả hai chọn X. Hadamard chuẩn bị của Alice và Hadamard đo của Bob
  triệt tiêu nhau: Bob đọc `0` của cô chắc chắn. Giữ.
- **Dòng 5:** Alice trong Z, Bob trong X — khác nhau, bỏ.
- **Dòng 7:** cả hai chọn Z, không Hadamard đâu cả: bit trần đi qua. Giữ.

Các vị trí được sàng lọc là `3` và `7`, nên khoá là bit của Alice tại đó: `0` và
`0`. Cả hai khoá đều đọc **`00`** — và trên đường sạch chúng luôn khớp (trên
200 lượt trao đổi, tỉ lệ lỗi trung bình sau sàng lọc đúng bằng `0.000`). Hai
trên tám là trượt nhỏ của seed này; trung bình dài hạn vào khoảng một nửa — đo
được `4.0` vị trí giữ mỗi lượt 8 qubit trên 200 lần chạy — nên một trao đổi
`N` qubit cho khoảng `N/2` bit khoá.

??? question "Tự kiểm tra — các bit sai cơ sở của Bob đôi khi đúng nhờ may (dòng 0, 1, 6). Vì sao vứt chúng đi thay vì sửa chúng?"
    Vì "sai" ở đây không phải kiểu sai *sửa được*. Một bit bị bỏ là một đồng xu —
    nó khớp bit của Alice với xác suất 1/2 *dù cô gửi gì*, nên nó không chứa
    thông tin để mà sửa. Muốn sửa, Bob phải biết bit của Alice — thứ hai người
    đang cố chia sẻ. Và anh không thể đo lại qubit trong cơ sở đúng: phép đo sai
    cơ sở đã làm nó sụp rồi. Bỏ đi tốn một nửa qubit và giữ được certainty; "sửa"
    sẽ giữ mọi qubit mà mất hết certainty.

!!! note "Một khoá, không phải thông điệp"
    BB84 tạo ra một **khoá** ngẫu nhiên dùng chung, không phải thông điệp. Khoá đó
    sau đó dùng với một mật mã thông thường — ví dụ một bảng một lần (one-time
    pad) — nên phần lượng tử chỉ cần giải nửa khó: thống nhất bí mật giữa thanh
    thiên bạch nhật.

## Kẻ nghe lén không thể ẩn mình

Giờ là lý do giao thức này *an toàn*, chứ không chỉ là một cuộc trao đổi dễ
thương. Theo cách cổ điển, Eve sao chép thông điệp rồi chuyển bản gốc đi tiếp;
không ai hay biết. Cơ học lượng tử đóng cánh cửa đó: [định lý không nhân
bản](ch06-quantum-networking.md) nói rằng một trạng thái lạ **không thể nhân
bản** — và mọi trạng thái Alice gửi đều là lạ với Eve, vì cô không biết cơ sở.
Muốn biết bất cứ điều gì, Eve buộc phải *đo*, và phép đo trong một cơ sở đoán
thì *làm nhiễu* qubit. Chiến lược tốt nhất của cô là **chặn rồi gửi lại**: đo
mỗi qubit trong một cơ sở cô đoán, rồi gửi tiếp đúng trạng thái mà phép đo của
cô đã làm nó sụp về.

**Một lượt trao đổi bị nghe lén** — cùng bộ máy seed cố định, giờ có Eve ở giữa
(`bb84.exchange(seed=0, eavesdropper=True)`):

| # | Bit Alice | Cơ sở Alice | Cơ sở Eve | Bit Eve | Cơ sở Bob | Bit Bob | kết luận |
|---|---|---|---|---|---|---|---|
| 0 | 1 | Z | Z | 1 | X | 0 | bỏ (cơ sở khác nhau) |
| 1 | 1 | X | X | 1 | X | 1 | giữ |
| 2 | 1 | X | X | 1 | X | 1 | giữ |
| 3 | 0 | X | Z | 0 | X | 1 | giữ — **không khớp** |
| 4 | 0 | X | X | 0 | Z | 0 | bỏ (cơ sở khác nhau) |
| 5 | 0 | X | X | 0 | X | 0 | giữ |
| 6 | 0 | X | X | 0 | X | 0 | giữ |
| 7 | 0 | X | Z | 1 | Z | 1 | bỏ (cơ sở khác nhau) |

Eve đoán sai hai lần — dòng 3 và 7. Hãy theo dòng 3 bằng phép tính trạng thái,
vì nó cho thấy toàn bộ sự phát hiện trong đúng một qubit:

1. Alice gửi bit `0` trong cơ sở X: `|−⟩`.
2. Eve đoán Z và đo. `|⟨0|−⟩|² = 1/2`: cô đọc `0` (lượt này), và phép đo của cô
   **làm qubit sụp về `|0⟩`** — `|−⟩` của Alice không còn tồn tại ở đâu nữa.
   Cô gửi lại `|0⟩`.
3. Bob đo trong X (cơ sở của anh khớp Alice, nên vị trí này sống qua sàng
   lọc). Qubit giờ là `|0⟩`, không phải `|−⟩`: anh đọc `1` với xác suất
   `|⟨−|0⟩|² = 1/2` — và đọc đúng `1`. Alice có `0`, Bob có `1`: **một bit khoá
   sai**.

Dòng 7 cho thấy mặt kia: Eve cũng đoán sai ở đó (đọc `1`, gửi lại `|1⟩`) —
nhưng cơ sở của Bob (Z) khác của Alice (X), nên vị trí bị bỏ. Một bit bị làm
nhiễu trong một vị trí bị bỏ thì vô hại.

Kết luận: các vị trí được sàng lọc `(1, 2, 3, 5, 6)`, nên khoá của Alice là
`11000` còn của Bob là `11100` — **1 trên 5 bit sai (20% lượt này)**.

**Con số 25% nói chung.** Lấy một bit đã giữ — vị trí của nó sống sót, nên Alice
và Bob dùng cùng cơ sở. Bit đó đã bị gõ. Eve đoán sai cơ sở với xác suất `1/2`.
Cho một cơ sở sai (tình huống dòng 3), kết quả của Bob là một đồng xu, nên bit
của anh sai với xác suất `1/2`:

$$\underbrace{\tfrac{1}{2}}_{\text{Eve sai cơ sở}} \times \underbrace{\tfrac{1}{2}}_{\text{đồng xu của Bob rơi sai}} = \tfrac{1}{4}$$

Còn đường sạch thì *đúng bằng* 0: không ai chạm vào qubit, mọi bit giữ đi qua
`H·H = I` nguyên vẹn. Đã kiểm chứng bằng chính thống kê của module trên 200
lượt trao đổi 8 qubit (`bb84.mean_error_rate`, `bb84.error_distribution`,
seed 10):

| Đường truyền | Tỉ lệ lỗi trung bình sau sàng lọc | Phân bố lỗi (200 lượt) |
|---|---|---|
| Không có kẻ nghe lén | 0.000 | mọi lượt đều 0 lỗi |
| Chặn rồi gửi lại | 0.237 | 0 lỗi × 73, 1 × 74, 2 × 38, 3 × 13, 4 × 2 |

![Đường sạch so với một đường bị nghe trộm](../assets/ch08-eavesdropper-error.png){ width="620" }

Hai nhận xét trung thực về phân bố đó. Thứ nhất, 8 qubit cố ý là nhỏ: trong 73
trên 200 lượt bị gõ, Eve tình cờ để lại 0 lỗi, nên một lượt ngắn không *bảo
đảm* tóm được cô — thứ tách biệt là trung bình (`0.000` so với `0.237`, khoảng
`0.96` lỗi trên `4.0` bit giữ mỗi lượt), còn khoá thật dài hàng nghìn bit, nơi
một phần tư là không thể bỏ sót. Thứ hai, hai phân bố khác nhau về hình dạng,
không chỉ về trung bình: đường sạch *dồn* vào 0 và không bao giờ nhúc nhích;
đường bị gõ trải quanh mức một phần tư.

Alice và Bob kết thúc bằng cách so một mẫu các bit đã sàng lọc qua kênh công
khai. Vài bất đồng có thể là nhiễu đường truyền thường; một phần tư là nghe
trộm, nên họ vứt khoá đi rồi thử lại.

??? question "Tự kiểm tra — vì sao Eve không thể sao chép qubit, chuyển bản gốc cho Bob, rồi phân tích bản sao sau?"
    [Định lý không nhân bản](ch06-quantum-networking.md): một trạng thái lượng tử
    lạ không thể nhân đôi. "Sao chép trước, đọc sau" đòi Eve phải biết *cái gì*
    để sao — nhưng phép sao chép phải giữ nguyên biên độ của cả bốn trạng thái
    khả dĩ mà không biết cái nào được gửi, và [Chương 7](ch07-helloworld-explained.md)
    đã cho thấy `CNOT` "nhân bản" một chồng chập thực sự làm gì: nó rối, không
    nhân đôi. Nên con đường duy nhất đến thông tin của Eve là đo — và đo trong
    cơ sở đoán làm qubit sụp, thứ cô buộc phải gửi lại. Làm nhiễu không phải
    hiệu ứng phụ cô tránh được; nó là nước đi duy nhất của cô.

??? question "Tự kiểm tra — liệu 25% có thể chỉ là xui? Vì sao Eve (hoặc nhiễu) không thể giải thích một phần tư khoá bị sai?"
    Nhiễu không thể ngồi ở mức 25%. Nhiễu đường truyền thực tế tệ lắm cũng chỉ
    vài phần trăm, và phép tính nhị thức khiến "nhiễu tạo ra một phần tư" khó
    tin đến mức thiên văn: kể cả cho một sàn nhiễu hào phóng 1%, xác suất để
    ≥ 25 trong 100 bit đã sàng lọc lật vì may là khoảng `10⁻²⁷` — còn 250
    trong 1000 bit thì nhỏ đến mức số học dấu phẩy động không diễn tả nổi. Eve
    cũng không thể lấy trung bình mà thoát: con 25% đến từ `1/2 × 1/2`, và mọi
    chiến lược đọc *nhiều* khoá hơn thì làm nhiễu *nhiều* hơn. Alice và Bob so
    một mẫu, thấy tỉ lệ, và từ chối khoá. Đòn tấn công không chỉ phát hiện được —
    nó còn không lời.

## Sơ đồ

### Vòng xoay Hadamard

![Vòng xoay Hadamard](../assets/ch08-haha-circuit.png){ width="420" }

![Đi vào một cơ sở rồi rời khỏi nó](../assets/ch08-haha-bloch.png){ width="620" }

`H·H = I`: trạng thái ở giữa trải trên cả bốn kết quả (biên độ mỗi cái `±1/2`),
và trạng thái cuối lại là hàng `X` — một cơ sở được đi vào rồi rời ra miễn phí.

### Những cách làm thất bại

![Vì sao phải đối chiếu cơ sở](../assets/ch08-attempts-error.png){ width="560" }

Không lỗi nào từ một kênh không cơ sở không phải là thành công — đó là sự vắng
mặt của một bí mật. Cơ sở mù rơi vào khoảng một phần tư — một khoá sai một bit
trong bốn.

### Chồng chập: cả mười sáu trạng thái, rồi chính thanh ghi đó trở lại

![Mạch chồng chập bốn qubit](../assets/ch08-superposition-circuit.png){ width="620" }

![Một thanh ghi trong chồng chập, và chính thanh ghi đó được khôi phục](../assets/ch08-superposition-states.png){ width="620" }

Mười sáu trạng thái mỗi cái `1/16 = 0.0625` ở giữa, còn `0110` đã chuẩn bị với
xác suất 1.00 ở hai đầu.

### BB84 và kẻ nghe trộm

![Một mạch BB84](../assets/ch08-bb84-circuit.png){ width="620" }

Phần chuẩn bị của Alice (một `X` cho bit `1`, một Hadamard cho cơ sở X), phép
xoay cơ sở của Bob, và phép đo.

![Đường sạch so với một đường bị nghe trộm](../assets/ch08-eavesdropper-error.png){ width="620" }

Đường sạch dồn hết vào 0 lỗi; đường bị gõ trải quanh mức một phần tư số bit đã
sàng lọc.

## Những điều cần nhớ

- Một qubit chỉ mang bit tương đối với một **cơ sở**: cơ sở Z chứa `|0⟩`,
  `|1⟩`; cơ sở X chứa `|+⟩`, `|−⟩`. Cùng cơ sở = bit chắc chắn
  (`|⟨0|0⟩|² = 1`); khác cơ sở = đồng xu công bằng (`|⟨+|0⟩|² = 1/2`).
- `H·H = I` là toàn bộ cơ chế: cơ sở đúng triệt tiêu (`H·H`), cơ sở sai để lại
  một `H` đơn độc và một đồng xu. Một cơ sở vào ra miễn phí — với chủ nhân của
  nó.
- Một kênh bit trần đọc hoàn hảo — cả Bob **và** Eve. Không lỗi nào không phải
  là bí mật; đó là một cuộc trò chuyện không bị xem.
- Một cơ sở ngẫu nhiên không được đối chiếu cho Bob một phần tư số bit sai
  (`1/2 × 1/2`), còn chồng chập là một *phép xoay*, không phải bí mật: thanh ghi
  thật sự trải trên cả `2^n` trạng thái (biên độ `1/4`, xác suất mỗi trạng thái
  `1/16` với bốn qubit), nhưng `H·H = I` đưa nó trở lại — và ai biết phép xoay
  thì đọc được.
- **BB84**: công bố cơ sở, không bao giờ bit; giữ các vị trí khớp (khoảng một
  nửa — trung bình `4.0` trên 8). Các bit giữ lại giống hệt nhau chắc chắn, nên
  một trao đổi `N` qubit cho một khoá dùng chung khoảng `N/2` bit.
- **Không nhân bản** buộc Eve phải đo, và phép đo sai cơ sở làm sụp qubit mà cô
  phải gửi lại. Nửa sai của cô × nửa đồng xu của Bob = **~25%** khoá đã sàng
  lọc bị sai, nơi đường sạch đúng bằng **0** — nên việc nghe trộm phát hiện được
  (và không lời), và Alice với Bob có thể từ chối một khoá đã bị lộ.

## Mã nguồn của chương này

Bốn mẫu, mỗi mẫu một mục sách, cùng một mô hình dùng chung nhỏ. Mỗi mẫu in một
bảng hướng dẫn rồi đến các con số cần theo dõi:

- [`ch08/identity.py`](https://github.com/phonhay103/quantum-computing-in-action/blob/main/src/quantum_computing_in_action/ch08/identity.py)
  — mẫu ``haha``: `X` rồi `H`, `H`, và trạng thái trở về (8.2). Hãy theo bảng
  xác suất: dòng 2 và dòng 4 giống hệt nhau, dòng 3 toàn `0.25`.
- [`ch08/attempts.py`](https://github.com/phonhay103/quantum-computing-in-action/blob/main/src/quantum_computing_in_action/ch08/attempts.py)
  — hai cách làm ``naive`` và ``guess`` thất bại. Hãy theo các tỉ lệ lỗi thô:
  `0.00` cho ngây thơ, `0.36` (64 qubit) cho cơ sở mù, với lượt dài tiệm cận
  `1/4`.
- [`ch08/superposition.py`](https://github.com/phonhay103/quantum-computing-in-action/blob/main/src/quantum_computing_in_action/ch08/superposition.py)
  — mẫu ``superposition``: cả 16 trạng thái mỗi cái `0.0625` sau một vòng `H`,
  và `0110` đã chuẩn bị được khôi phục sau vòng hai.
- [`ch08/bb84.py`](https://github.com/phonhay103/quantum-computing-in-action/blob/main/src/quantum_computing_in_action/ch08/bb84.py)
  — giao thức đúng: bảng sàng lọc 8 qubit, rồi sự tách biệt tỉ lệ lỗi, `0.000`
  sạch so với `0.237` bị gõ trên 200 lượt trao đổi.
- [`ch08/protocol.py`](https://github.com/phonhay103/quantum-computing-in-action/blob/main/src/quantum_computing_in_action/ch08/protocol.py)
  — mô hình qubit dùng chung: bốn trạng thái, một quy tắc đo duy nhất (cùng cơ sở
  = bit, khác cơ sở = đồng xu công bằng), phép sàng lọc, và mạch đáng để vẽ.

Chạy toàn bộ bằng `make ch08`, hoặc từng mẫu một:

```bash
uv run python -m quantum_computing_in_action.ch08.bb84
```
