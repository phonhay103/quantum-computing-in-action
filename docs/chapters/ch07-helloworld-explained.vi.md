# Chương 7 — HelloWorld của chúng ta, giải thích

!!! abstract "Trong một câu"
    Một chương trình lượng tử không phải hộp đen: nó là một danh sách **các bước**
    có thứ tự, và trạng thái mà nó tạo ra đọc được sau *mỗi* bước — đó là tất cả
    ý nghĩa của việc "chạy một mạch". Các chương sau chỉ thêm bước vào danh sách
    ấy; bức tranh về sự thực thi nêu ở đây không hề thay đổi.

## Câu hỏi chương này trả lời

Chương 2 đã hỏi simulator xin một bit ngẫu nhiên và nhận được, chỉ bằng một lời
gọi: một dòng mã trả về kết quả mà không để lộ gì về cơ chế đã sinh ra nó. Nhìn
từ bên ngoài, lời gọi ấy trông như một hành động không thể phân chia. Chương
này mở lời gọi đó ra và hỏi hai câu mà lập trình viên cuối cùng buộc phải đặt ra
cho mọi trò ảo thuật:

1. **Cái gì đã thực sự chạy?** Không phải một lời gọi hàm theo nghĩa thông
   thường. Đó là một *chương trình*: một danh sách **các bước** có thứ tự, mỗi
   bước chứa các cổng tác động cùng lúc. Nói cách khác, thứ simulator thực thi
   không phải một thao tác đơn khối mà là một lịch chạy có cấu trúc gồm các
   thao tác đồng thời, và cấu trúc đó có tên, có thể ghi ra và kiểm tra được.
   Đó chính là nghĩa của "mạch lượng tử" từ đầu đến giờ.
2. **Liệu có thể nhìn vào trong khi nó chạy?** Được. Simulator giữ đúng một
   đối tượng — **trạng thái** — từ cổng đầu đến cổng cuối, và đối tượng ấy vẫn
   sẵn dùng ở mọi thời điểm trung gian chứ không bị vứt bỏ ngay sau khi một
   cổng đã tác động. Do đó, "gỡ lỗi" chẳng gì hơn là đọc trạng thái đó sau mỗi
   bước, hệt như việc in một biến ở giữa một vòng lặp thông thường; không cần
   một thiết bị đo bổ sung nào.

Mở hộp xong, chương dùng nó để làm việc thực: **phép tính số học**. Cộng số là
bài kiểm tra kinh điển đầu tiên của mọi mô hình tính toán, và sự lựa chọn là
chủ ý: phép cộng quen đến mức kết quả kiểm chứng được bằng tay, nhưng lại có
cấu trúc đủ để bộc lộ những gì mô hình biểu diễn được và không biểu diễn được.
Mạch lượng tử cộng được — nhưng theo một quy tắc lạ định hình mọi thứ từ đây
trở đi: *cổng lượng tử không bao giờ được phép làm mất thông tin*.

Sau chương này, những năng lực sau sẽ được xác lập:

- sơ đồ mạch được đọc như một chương trình: cổng nào chạm qubit nào, ở bước
  nào;
- trạng thái sau mỗi bước được viết ra **bằng số cụ thể**, chứ không chỉ quan
  sát ở cuối;
- giải thích được vì sao `CNOT` cộng "modulo 2" (`1 + 1 = 0`), và chính xác
  điều gì bị mất trong quá trình ấy;
- giải thích được cổng **Toffoli**, cùng cách nó vá lại chỗ mất mát để cuối
  cùng `1 + 1 = 2` giữ đúng.

Ba kết quả từ các chương trước là cần thiết, và mỗi kết quả được cô thành một
dòng: `H` đưa một qubit vào chồng chập đều 50/50, nội dung của
[Chương 4](ch04-superposition.md); `CNOT` lật qubit đích khi điều khiển là `1`,
cổng được xét kỹ trong [Chương 5](ch05-entanglement.md); và một giá trị *lạ*
thì không thể sao chép — chỉ có thể rối, như đã chứng minh trong
[Chương 6](ch06-quantum-networking.md).

!!! note "Một chút sổ sách: thứ tự bit"
    Một nhãn như `1001` trong chương này luôn đọc **`q0` trước**, trái sang
    phải: `q0 q1 q2 q3`. Vậy `1001` nghĩa là `q0 = 1, q1 = 0, q2 = 0, q3 = 1` —
    đúng thứ tự của sách, khớp với `Qubit[0] … Qubit[3]`. Cần lưu ý rằng chính
    Qiskit in chỉ số cao nhất bên trái, tức quy ước ngược lại; vì vậy mọi kết
    quả ở đây đã được lật sẵn về thứ tự của sách, và người đọc không phải hiệu
    chỉnh thêm gì.

## Một chương trình là một danh sách các bước

Mẫu ``randombit`` của sách là một chương trình bốn qubit với đúng hai bước —
gọn đủ để viết ra trọn vẹn và kiểm chứng bằng tay ở mọi thời điểm trung gian,
đúng như các đoạn dưới đây thực hiện:

```text
bước 1:  H(0), X(3)
bước 2:  CNOT(0, 1)
```

![Chương trình bốn qubit](../assets/ch07-randombit-circuit.png){ width="460" }

Mạch được đọc từng cổng một, và sau mỗi cổng đặt cùng câu hỏi: "trạng thái bây
giờ là gì?" Không cần gì thêm để bám theo chương trình từ đầu đến cuối.

**Khởi đầu.** Mọi qubit bắt đầu ở `|0⟩`, nên trạng thái bốn qubit là đúng một
trạng thái cơ sở `|0000⟩` — chắc chắn, xác suất 1.00. Ở thời điểm này thanh ghi
chẳng chứa tí ngẫu nhiên nào; mọi kết quả khác `0000` đều có xác suất bằng
không.

**Bước 1 — `H(0)` và `X(3)`.** Hai cổng tác động cùng lúc, trên hai qubit khác
nhau, và không cổng nào phụ thuộc kết quả của cổng kia:

- `H` trên `q0` tách nó thành `( |0⟩ + |1⟩ )/√2` — hỗn hợp đều 50/50, cái bit
  ngẫu nhiên mà Chương 2 thu được. Nó không *quyết định* gì cả; nó chỉ làm hai
  tương lai cùng khả năng, còn phán quyết thực sự được dồn cho phép đo lúc
  cuối.
- `X` trên `q3` lật qubit đó thành `|1⟩` chắc chắn. Chương trình được phép đặt
  những giá trị nó đã biết — `X` chính là lệnh "gán bằng 1", khả nghịch; vì
  không sinh thông tin mới nào nên nó không vi phạm quy tắc lượng tử nào.
- `q1` và `q2` hoàn toàn không có trong bước này, nên chúng không nhúc nhích:
  biên độ của chúng giữ nguyên như lúc khởi đầu.

Vậy sau bước 1 cả thanh ghi là

$$\frac{1}{\sqrt{2}}\,(|0001\rangle + |1001\rangle)$$

Hai trạng thái cơ sở, biên độ mỗi cái `1/√2`, xác suất mỗi cái `1/2`. Đọc nhãn
theo thứ tự của sách: `0001` là "`q0=0` còn `q3=1`", `1001` là "`q0=1` còn
`q3=1`". Chỉ mỗi `q0` khác nhau giữa hai nhãn — đúng qubit mà `H` đã tác động —
còn chữ `1` cuối cùng trong cả hai nhãn ghi lại `X` trên `q3`.

**Bước 2 — `CNOT(0, 1)`.** Cổng này nhìn điều khiển `q0` và lật đích `q1` khi
điều khiển là `1`. Nó tác động lên từng nhánh một, và trong mỗi nhánh nó là tất
định:

- nhánh `0001`: điều khiển `q0` là `0`, nên điều kiện không thỏa và đích không
  hề bị chạm;
- nhánh `1001`: điều khiển `q0` là `1`, nên điều kiện thỏa và `q1` lật
  `0 → 1`, thành `1101`.

$$\frac{1}{\sqrt{2}}\,(|0001\rangle + |1001\rangle)
\;\xrightarrow{\;\mathrm{CNOT}\;}
\frac{1}{\sqrt{2}}\,(|0001\rangle + |1101\rangle)$$

Vẫn hai nhánh, mỗi nhãn vẫn xác suất `1/2`. Nói cách khác, `CNOT` không làm gì
*thêm* ngẫu nhiên; điều nó làm là *liên kết* `q1` với `q0`, sao cho giá trị của
một qubit trở thành chỉ báo đáng tin về giá trị qubit kia.

??? question "Tự kiểm tra — bốn qubit có mười sáu kết quả khả dĩ. Vì sao chỉ hai kết quả xuất hiện?"
    Mười sáu chỉ là số *nhãn khả dĩ*; một chương trình chỉ đạt tới những trạng
    thái mà cổng của nó tạo ra. Ở đây `q3` bị `X` ghim vào `1`, `q2` không bao
    giờ bị chạm nên giữ `0`, và nhánh tách duy nhất trong cả chương trình là
    lần `H` tách `q0` — hai nhánh. Rồi `CNOT` đưa mỗi nhánh tới đúng một nhánh
    mới; nó không tách thêm gì. Hai nhánh vào, hai nhánh ra: `0001` và `1101`.

## Đọc trạng thái sau mỗi bước

Biểu đồ ở *cuối* cho biết chương trình trả về gì; nó không cho biết *ở đâu* mỗi
qubit thay đổi trên đường đi — mà đó thường mới là câu hỏi thú vị khi chương
trình chạy sai. Mẫu ``randombitdebug`` của sách trả lời điều đó bằng cách vẽ
vector xác suất sau **mỗi** bước — và vì trạng thái của simulator là một đối
tượng duy nhất suốt cuộc chạy, đây không phải mẹo gì: nó chỉ là "in biến ra" ở
ba thời điểm, hệt như khi gỡ lỗi mã cổ điển.

Đây là cùng chương trình đó, với ranh giới vẽ sau mỗi bước:

![Chương trình với ranh giới bước](../assets/ch07-debug-circuit.png){ width="460" }

Trước hết là vector xác suất đầy đủ, chỉ giữ các trạng thái cơ sở có thể xảy
ra — những trạng thái chưa bao giờ có biên độ khác không được lược bỏ cho gọn:

| Bước | Trạng thái cơ sở `q0 q1 q2 q3` | Xác suất |
|---|---|---|
| khởi đầu | `0000` | 1.00 |
| `H(0), X(3)` | `0001` | 0.50 |
| | `1001` | 0.50 |
| `CNOT(0, 1)` | `0001` | 0.50 |
| | `1101` | 0.50 |

![Xác suất các trạng thái cơ sở sau mỗi bước](../assets/ch07-debug-steps.png){ width="620" }

Cách đọc: bảng là toàn bộ trạng thái ở ba thời điểm, và mỗi điều thay đổi
giữa các thời điểm là điều do một bước cụ thể gây ra. Ở khởi đầu có một dòng,
vì thanh ghi đang ở một trạng thái xác định. Sau bước 1 có hai dòng — `H` tách
thanh ghi thành hai tương lai, mỗi tương lai cùng xác suất, và chữ `1` cuối cả
hai nhãn là `X` trên `q3`. Bước 2 vẫn hai dòng nhưng *đổi tên* một dòng:
`1001 → 1101`, đó là `CNOT` lật `q1` bên trong nhánh mà `q0 = 1`. Không còn gì
khác trong bảng di chuyển nữa.

Cùng thông tin đó, mỗi cột một qubit, dễ liếc hơn:

| Bước | P(q0=1) | P(q1=1) | P(q2=1) | P(q3=1) |
|---|---|---|---|---|
| khởi đầu | 0.00 | 0.00 | 0.00 | 0.00 |
| `H(0), X(3)` | 0.50 | 0.00 | 0.00 | 1.00 |
| `CNOT(0, 1)` | 0.50 | 0.50 | 0.00 | 1.00 |

![P(qubit = 1) sau mỗi bước](../assets/ch07-debug-marginals.png){ width="620" }

Đọc bảng theo cột, rồi theo dòng; mỗi dòng chính là "cuộc đời trong chương
trình" của một qubit:

- `q0`: nhảy lên `0.50` ngay **bước đầu** (`H`) và không tự nhúc nhích nữa —
  tính ngẫu nhiên gán cho `q0` được sinh một lần rồi để nguyên.
- `q1`: ngồi im ở `0` cho đến khi `CNOT` ở **bước hai** kéo lên `0.50`; nghĩa
  là tính ngẫu nhiên của nó được thừa hưởng từ `q0`, không tự sinh tại chỗ.
- `q2`: `0.00` suốt — không có gì trong chương trình chạm nó, nên nó không
  đóng vai trò nào trong bất kỳ kết quả nào.
- `q3`: nhảy lên `1.00` ngay bước đầu (`X`) và giữ nguyên, hành xử như một
  hằng số cổ điển mà chương trình chủ ý đặt.

Đây là thông tin gỡ lỗi mà biểu đồ cuối không thể cho: *bước nào đã đổi qubit
nào*.

??? question "Tự kiểm tra — sau bước 2, P(q1 = 1) là 0.50. Liệu `q1` tự nó có phải một đồng xu ngẫu nhiên?"
    Nếu đo **riêng** `q1`, kết quả thu được là một đồng xu công bằng — 50/50,
    ở mức này không phân biệt được với một bit ngẫu nhiên thực sự. Nhưng nó
    không *độc lập*: hai dòng `0001` và `1101` nói rằng `q1` **luôn bằng**
    `q0`. Xác suất nửa-nửa đến từ việc chia sẻ hai nhánh, không phải từ `q1`
    tự quyết. Khác biệt đó — ngẫu nhiên ở bìa so với tương quan chung — chính
    là điểm của [Chương 5](ch05-entanglement.md).

Vậy chương trình *trả về* gì? Đo cả bốn qubit, lặp bao nhiêu lần cũng chỉ hai
chuỗi từng xuất hiện:

| Kết quả `q0 q1 q2 q3` | Số lần (1000 shots) |
|---|---|
| `0001` | ≈ 500 |
| `1101` | ≈ 500 |

![Chỉ hai kết quả, và q1 bám theo q0](../assets/ch07-randombit-counts.png){ width="620" }

`q2` luôn `0` và `q3` luôn `1`; tính ngẫu nhiên nằm trọn trong `q0`, còn `q1`
**luôn khớp** với nó. Sự khớp nhau đó là một cặp Bell trên cặp `(q0, q1)` — và
đó là cách trung thực duy nhất để một mạch chia sẻ một giá trị lạ. Nó không
phải bản sao: [Chương 6](ch06-quantum-networking.md) đã cho thấy sao chép một
giá trị lạ là bất khả thi về nguyên tắc, và `CNOT` "nhân bản" một chồng chập
tạo ra đúng kiểu rối lượng tử này thay thế.

## Cộng hai qubit

Mở xong hộp, sách quay sang số học — bài kiểm tra kinh điển đầu tiên của mọi
mô hình tính toán, đúng nội dung chương này đặt ra để vượt qua. Đáng chú ý là
xét kỹ xem một phép quen thuộc, đời thường hành xử thế nào khi quy tắc "không
được làm mất gì" được thi hành.

Mạch cổ điển cộng bằng cổng `AND` và `OR`. Mạch lượng tử thì không, và lý do
đáng nói cẩn thận: mọi cổng lượng tử phải **khả nghịch** — luôn phải chạy
ngược được cổng đó và lấy lại đúng đầu vào đã nạp. Một cổng vứt thông tin đi
(ba đầu vào, một đầu ra, như `AND`) thì không chạy ngược được, vì hai đầu vào
khác nhau cho cùng một đầu ra và sự khác biệt giữa chúng đã mất; vì vậy nó bị
cấm hẳn.

Phép số học nhỏ nhất mà mạch lượng tử *làm được* là một `CNOT`, lật đích đúng
khi điều khiển là `1`. Với `a` nạp trên `q0` và `b` trên `q1`, đầu ra của
`CNOT(0, 1)` trên `q1` trả lời câu hỏi *"hai bit có khác nhau không?"*:

| a | b | "khác nhau?" | a + b (mod 2) |
|---|---|---|---|
| 0 | 0 | không | 0 |
| 0 | 1 | có | 1 |
| 1 | 0 | có | 1 |
| 1 | 1 | **không** | **0** |

"Khác nhau hay không" chính là phép **XOR**, và nó cũng là phép cộng **modulo
2** — đếm các số 1 rồi chỉ giữ tính lẻ-chẵn, như bật công tắc đèn hai lần rồi
thấy đèn tắt. Ba dòng đầu là phép cộng thường: số `1` đó nhỏ đủ để vừa trong
một bit. Dòng thứ tư không: `1 + 1 = 2`, mà `2` không vừa trong một bit, nên
kết quả quay vòng về `0`.

Và vấn đề nằm ở đó: mạch *biết* là có số nhớ — cả hai đầu vào đều `1`, nên một
phép cộng đúng thực thụ sẽ cho `10` trong nhị phân — nhưng nó **không có chỗ
để đặt**. `CNOT` chỉ lật đích giữa `0` và `1`; không gì trong mạch nhớ rằng nó
đã nhớ. Đây là một **bộ bán cộng**: cấu trúc đúng chỉ khi mọi kết quả vừa
trong một bit, phần tràn bị lặng lẽ bỏ đi.

??? question "Tự kiểm tra — `1 + 1 = 0` có phải lỗi không?"
    Không — đó là hợp đồng. `CNOT` tính `a XOR b`, tức `a + b` *modulo 2*: tổng
    cộng với số nhớ bị bỏ đi. Với ba trong bốn đầu vào, số nhớ vốn bằng
    không, nên kết quả đó là đáp án đầy đủ; với `1 + 1`, cổng lặng lẽ vứt mất
    con `2`. Mạch chưa từng hứa lưu số nhớ — chính sự bỏ trống ấy là khuyết
    điểm mà mục sau sẽ vá.

## Cổng đem lại số nhớ

Cái còn thiếu là một phép **AND** logic: một bit chỉ bằng `1` khi *cả hai*
đầu vào đều `1`. `AND` thường không dùng được — nó phá đầu vào, như quy tắc
khả nghịch đã nói. Bản thay thế khả nghịch của nó là cổng **Toffoli** (viết
tắt `CCNOT`). Cách hình dung dễ nhất: **một `CNOT` cần hai lần xin phép.**
Đích chỉ lật khi *cả hai* điều khiển đều `1`.

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

Chỉ hai dòng di chuyển, và trong hai dòng ấy chỉ qubit thứ ba di chuyển — nhưng
đó chính là `AND` được ghi lên `q2`: khi cả hai điều khiển đều `1`, đích trở
thành `1`; khi một trong hai là `0`, đích quay về `0`. Vì các đầu vào vẫn còn
nguyên sau đó, không gì bị xóa, nên cổng khả nghịch (ma trận của nó là một
hoán vị: chạy bảng ngược lại là hoàn tác). Cái giá của tính khả nghịch là kết
quả cần **qubit riêng của nó** — không thể ghi đè lên đầu vào, vì một đầu vào
đã bị ghi đè là một đầu vào không thể khôi phục nữa.

Giờ bộ cộng là hai cổng, và thứ tự không phải khẩu vị:

```text
Toffoli(0, 1, 2)   q2 = q0 AND q1   (số nhớ)   -- trước
CNOT(0, 1)         q1 = q0 XOR q1   (tổng)     -- sau
```

![Bộ cộng đầy đủ cho 1 + 1](../assets/ch07-add2-circuit.png){ width="460" }

Trường hợp khó nhất, `1 + 1`, đáng được bám sát — xuất phát với `a = 1` trên
`q0`, `b = 1` trên `q1`, và một qubit nháp chứa số nhớ, `q2 = 0`, tức trạng
thái `|110⟩`:

1. **Toffoli(0, 1, 2)** — cả hai điều khiển đều `1`, nên đích lật:
   `|110⟩ → |111⟩`. Số nhớ giờ tồn tại: `q2 = 1`.
2. **CNOT(0, 1)** — điều khiển `q0` là `1`, nên đích lật:
   `|111⟩ → |101⟩`. Bit tổng hạ cánh lên `q1 = 0`.

Đọc kết quả: `q1 = 0` (tổng), `q2 = 1` (số nhớ) — và `10` trong nhị phân là
`2`. Cuối cùng `1 + 1 = 2`, và cả hai phần của đáp án đều hiện hữu vật lý trong
thanh ghi.

??? question "Tự kiểm tra — vì sao Toffoli phải chạy *trước* CNOT?"
    Vì `CNOT` ghi đè lên một trong hai đầu vào mà Toffoli cần đọc. Chạy ngược
    thứ tự trên `1 + 1`: `CNOT` trước cho `|110⟩ → |100⟩` (tổng hạ cánh,
    `q1 = 0`). Giờ Toffoli thấy điều khiển `1` và `0` — không phải cả hai đều
    1 — nên nó không làm gì, và số nhớ không bao giờ được ghi. `|100⟩` nói
    "tổng 0, số nhớ 0": con `2` biến mất. Nói cách khác, thứ tự quan trọng mỗi
    khi một cổng đọc thứ cổng khác vừa ghi; ở đây CNOT phá đúng thông tin mà
    Toffoli cần trước khi kịp tác động.

Bức tranh đầy đủ trên cả bốn đầu vào:

| a | b | tổng | số nhớ | a + b |
|---|---|---|---|---|
| 0 | 0 | 0 | 0 | 0 |
| 0 | 1 | 1 | 0 | 1 |
| 1 | 0 | 1 | 0 | 1 |
| 1 | 1 | 0 | 1 | **2** |

![Bộ bán cộng so với bộ cộng đầy đủ](../assets/ch07-adder-comparison.png){ width="620" }

Hai mạch đồng ý trên ba đầu vào và phân kỳ ở dòng thứ tư. Khoảng trống đó — số
nhớ — là toàn bộ lý do Toffoli tồn tại trong hộp công cụ lượng tử, và là khuôn
mẫu mà mọi thuật toán lượng tử lớn hơn đều xây trên: **thêm một qubit, thêm
một điều khiển, và một phép vốn bất khả nghịch trở thành khả nghịch.**

![Từ X đến CNOT đến Toffoli](../assets/ch07-toffoli-matrices.png){ width="620" }

Các ma trận làm rõ khuôn mẫu của cả gia đình. `X` một qubit lật đích duy nhất
của nó vô điều kiện; `CNOT` lật đích theo một điều khiển; `Toffoli` theo hai.
Mỗi thành viên thêm một điều khiển và một qubit so với thành viên trước, và
chính gia đình *khả nghịch* này là chất liệu cấu thành các thuật toán lượng tử
— kể cả các oracle của [Chương 9](ch09-deutsch-jozsa.md), vốn được dựng từ
chính những cổng đa-điều khiển như vậy.

## Các sơ đồ {#cac-so-do}

### Chương trình

![Chương trình bốn qubit](../assets/ch07-randombit-circuit.png){ width="460" }

`q0` ở trên cùng, rồi `q1`, `q2`, `q3` từ trên xuống — thứ tự của sách, khớp
`Qubit[0] … Qubit[3]`. `H` tách `q0`, `X` đặt `q3`, và `CNOT(0, 1)` buộc `q1`
vào `q0`; đường nối dọc giữa hai quy tắc chính là thứ làm cổng trở nên có điều
kiện. `q2` được vẽ nhưng không bao giờ bị chạm, và một dây không cổng nào
chạm thì đơn thuần mang giá trị khởi đầu của nó đến cuối chương trình.

### Gỡ lỗi, từng bước

![Chương trình với ranh giới bước](../assets/ch07-debug-circuit.png){ width="460" }

Các đường chặn đánh dấu chỗ một bước kết thúc và bước kế bắt đầu — đúng việc
mà cổng xác suất của sách từng làm trong hình. Vậy mỗi vùng giữa hai đường
chặn đều có thể được truy vấn độc lập, và đó chính là điều khiến trạng thái
đọc được ở từng thời điểm.

![Xác suất các trạng thái cơ sở sau mỗi bước](../assets/ch07-debug-steps.png){ width="620" }

Vector xác suất tại ba thời điểm: đầu tiên một trạng thái, rồi hai, rồi hai —
và lần chuyển thứ hai đổi thành phần của qubit `q1` trong nhánh mang
`q0 = 1`, mà không hề sinh nhánh mới nào.

![P(qubit = 1) sau mỗi bước](../assets/ch07-debug-marginals.png){ width="620" }

Cùng sự thật đó, mỗi cột một qubit: `q0` nhúc nhích ở bước 1, `q1` ở bước 2,
còn `q2` và `q3` không bao giờ. Đọc lần lượt các cột thì thu được, xét cho
cùng, tiểu sử từng qubit trong chương trình.

### Các bộ cộng

![Bộ bán cộng cho 1 + 1](../assets/ch07-add1-circuit.png){ width="420" }

Trường hợp `1 + 1`: cả hai đầu vào được đặt, và tổng đọc `0` vì đầu ra một bit
không có chỗ chứa số nhớ. Điều thiếu trong bức tranh này không phải một cổng
mà là một chỗ — một qubit riêng cho phần tràn.

![Bộ cộng đầy đủ cho 1 + 1](../assets/ch07-add2-circuit.png){ width="460" }

`Toffoli` ghi số nhớ lên `q2` và `CNOT` ghi tổng lên `q1`; nhờ cặp cổng ấy, cả
hai nửa của tổng hai bit đều hiện diện như những giá trị qubit thường ở cuối
chương trình.

![Bộ bán cộng so với bộ cộng đầy đủ](../assets/ch07-adder-comparison.png){ width="620" }

![Từ X đến CNOT đến Toffoli](../assets/ch07-toffoli-matrices.png){ width="620" }

## Những điều cần nhớ

- Một chương trình lượng tử là một danh sách **các bước** có thứ tự. Chạy nó
  chẳng gì hơn là một trạng thái tiến hoá từ `|0…0>` dưới danh sách bước đó
  cho đến phép đo cuối cùng.
- Trạng thái đọc được sau **mỗi** bước; đó là tất cả ý nghĩa của "gỡ lỗi
  mạch", và đó là cách xác định *bước nào* đã đổi *qubit nào* — câu hỏi mà
  biểu đồ cuối không thể trả lời.
- Trong chương trình HelloWorld, `q0` trở nên ngẫu nhiên ở `H`, `q1` nhận giá
  trị ở `CNOT`, còn `q2` và `q3` không di chuyển. Mọi sự thật như vậy đều bị
  biểu đồ cuối che mất, vì nó chỉ thể hiện trạng thái kết thúc.
- `CNOT` tính `a XOR b`: cộng **modulo 2**, không số nhớ. Tự thân nó là một
  **bộ bán cộng**, và trên `1 + 1` nó trả về `0`.
- Mọi cổng lượng tử đều **khả nghịch**, nên `AND` cổ điển bị cấm. Bản thay thế
  là **Toffoli** (`CCNOT`) — "một `CNOT` cần hai lần xin phép" — một `AND`
  khả nghịch giữ nguyên đầu vào.
- `Toffoli` cho số nhớ cộng `CNOT` cho tổng lập thành **bộ cộng đầy đủ**, và
  `1 + 1 = 2`. Thêm một qubit và một cổng là đủ để phép tính trở nên khả
  nghịch — và *thứ tự cổng* quan trọng, vì `CNOT` ghi đè đúng giá trị mà
  Toffoli cần đọc.

## Mã nguồn của chương này

Bốn mẫu, mỗi mẫu một mục sách, cộng một trợ giúp dùng chung nhỏ:

- [`ch07/randombit.py`](https://github.com/phonhay103/quantum-computing-in-action/blob/main/src/quantum_computing_in_action/ch07/randombit.py)
  — chương trình bốn qubit, hai bước của nó, và các kết quả đo được (7.5.1).
- [`ch07/debugging.py`](https://github.com/phonhay103/quantum-computing-in-action/blob/main/src/quantum_computing_in_action/ch07/debugging.py)
  — cùng chương trình đó, với trạng thái được báo cáo sau mỗi bước (7.5.2).
- [`ch07/half_adder.py`](https://github.com/phonhay103/quantum-computing-in-action/blob/main/src/quantum_computing_in_action/ch07/half_adder.py)
  — bộ bán cộng `CNOT`, modulo 2, không lưu số nhớ (7.6.2).
- [`ch07/full_adder.py`](https://github.com/phonhay103/quantum-computing-in-action/blob/main/src/quantum_computing_in_action/ch07/full_adder.py)
  — bộ cộng đầy đủ `Toffoli` + `CNOT`, và ma trận `Toffoli` (7.6.3).
- [`ch07/circuits.py`](https://github.com/phonhay103/quantum-computing-in-action/blob/main/src/quantum_computing_in_action/ch07/circuits.py)
  — các trợ giúp dùng chung: đọc trạng thái sau một bước, vector xác suất, và
  cách lật thứ tự bit Qiskit ↔ sách.

Chạy tất cả bằng `make ch07`, hoặc từng cái một:

```bash
uv run python -m quantum_computing_in_action.ch07.full_adder
```
