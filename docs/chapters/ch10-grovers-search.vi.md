# Chương 10 — Thuật toán tìm kiếm của Grover

!!! abstract "Trong một câu"
    Với một danh sách không có cấu trúc và chỉ có một phép thử nhận ra đáp án,
    Grover tìm ra nó trong khoảng `(π/4)·√N` bước thay vì `N/2` của cổ điển — một
    tăng tốc **bậc hai**, và là mức tốt nhất mà một danh sách không sắp xếp cho
    phép.

## Câu hỏi chương này trả lời

Chương 9 kết thúc với một oracle có thể được hỏi đúng một câu hỏi toàn cục về
một hàm — hằng số hay cân bằng — chỉ trong một lần hỏi. Chương này hỏi câu mà
mọi người dùng cơ sở dữ liệu thực sự có, theo ba bước:

1. **Làm sao tìm một mục cần tìm trong một danh sách không có cấu trúc?** Không
   có khoá đã sắp xếp, không có gì để khai thác — chỉ một đống mục và một phép
   thử nói "có" với đúng một mục. Cổ điển chỉ có một kế hoạch: nhìn, lần lượt
   từng mục, với giá `N/2` lần thử trung bình.
2. **Một dấu trừ ẩn làm sao trở thành một mục được tìm thấy?** Trên thanh ghi
   lượng tử, phép thử trở thành một oracle chỉ được phép lật **dấu** của trạng
   thái cần tìm — mà một dấu không đổi xác suất nào cả, nên vô hình với mọi phép
   đo. Câu trả lời của Grover là một **điệu nhảy hai bước**, oracle rồi khuếch
   tán, lặp lại đúng số lần được đếm sẵn.
3. **Vì sao điệu nhảy phải dừng đúng lúc?** Mỗi vòng xoay vector biên độ một
   bước cố định về phía đáp án; vượt qua đáp án rồi thì cùng một phép xoay lại
   chỉ *ra khỏi* nó, nên xoay *quá* làm xác suất thành công *giảm*.

Sau chương này bạn sẽ giải thích được:

- nói chi phí cổ điển của một **tìm kiếm không cấu trúc** là bao nhiêu, và biện
  minh cho mức trung bình `N/2`;
- giải thích oracle là "lật dấu của trạng thái được đánh dấu — và không làm gì
  khác", và vì sao lật dấu là một **phản xạ**;
- tính tay một vòng Grover **trên bốn trạng thái**: biên độ mỗi trạng thái
  `0.5` → oracle → trung bình `0.25` → trạng thái đánh dấu lên `1.0` sau đúng
  một vòng;
- giải thích **khuếch tán** là "phản xạ mọi biên độ quanh giá trị trung bình"
  (`a → 2·mean − a`), và vì sao nó đẩy biên độ *vào* đúng trạng thái mà oracle
  đã đánh dấu;
- chọn số vòng — vào khoảng `(π/4)·√N` — và giải thích vì sao nhiều vòng hơn
  cuối cùng lại *có hại*.

Bạn cần ba điều từ các chương trước, mỗi điều một dòng: `H` trên mọi qubit tạo
chồng chập đều, biên độ mỗi trạng thái `1/√N`
([Chương 4](ch04-superposition.md)); oracle là một mạch **khả nghịch**, và
**phase kickback** biến câu trả lời của nó thành một dấu
([Chương 9](ch09-deutsch-jozsa.md)); và trạng thái của một chương trình đọc
được sau mỗi bước ([Chương 7](ch07-helloworld-explained.md)) — chính nhờ thế
mà chương này theo dõi từng biên độ di chuyển.

!!! note "Một chút sổ sách: biên độ, dấu, nhãn"
    Chương này in **biên độ**, vốn có thể âm, và **xác suất**, là bình phương
    biên độ — nên `(−1/2)² = 1/4 = (1/2)²`. Nhãn trạng thái cơ sở luôn đọc
    **`q0` trước**, trái sang phải, đúng thứ tự của sách: chỉ số `7` được đánh
    dấu trên sáu qubit nghĩa là `q0 = q1 = q2 = 1` và in ra thành `111000`. Còn
    `N` luôn đếm danh sách: `N = 2^n` mục cho `n` qubit.

## Tìm kiếm không cấu trúc

Ví dụ của sách là một danh bạ nhỏ và một câu hỏi — *ai 29 tuổi và sống ở
Mexico?* Chỗ bực mình không phải câu hỏi mà là danh sách: tuổi chưa sắp xếp,
quốc gia chưa sắp xếp, nên không có khoá để tìm kiếm nhị phân. Một chương trình
cổ điển chỉ có thể nhìn, lần lượt từng mục:

| Mục | Tên | Tuổi | Quốc gia |
|---|---|---|---|
| 0 | Alice | 42 | Nigeria |
| 1 | Bob | 36 | Australia |
| 2 | Eve | 85 | USA |
| 3 | Niels | 18 | Greece |
| **4** | **Albert** | **29** | **Mexico** |
| 5 | Roger | 29 | Belgium |
| 6 | Marie | 15 | Russia |
| 7 | Janice | 52 | China |

Tính tay phép quét: Alice — trượt. Bob — trượt. Eve — trượt. Niels — trượt.
Albert — trúng. Mục khớp nằm ở vị trí 4, nên phép quét mất **5 lần thử**.

Nhưng con 5 là may mắn, không phải chi phí. Xáo trộn danh sách thì mục tiêu rơi
vào mỗi trong 8 vị trí đều nhau, nên cái giá cổ điển trung thực là trung bình
`(1 + 2 + … + 8)/8 = 36/8 = 4.5` lần thử.

![Phép quét cổ điển: mất bao nhiêu lần thử để tìm mục tiêu](../assets/ch10-classical-tries.png){ width="560" }

Biểu đồ phẳng đó *chính là* quy luật tổng quát. Với `N` mục, mục tiêu nằm ở vị
trí `1, 2, …, N` với xác suất bằng nhau `1/N`, nên số lần thử kỳ vọng là

$$(1 + 2 + \dots + N)\,/\,N = (N+1)/2 \;\approx\; N/2,$$

và không mẹo cổ điển nào tốt hơn, vì trên một danh sách không cấu trúc, mỗi phép
thử chỉ loại được đúng một mục. Cái `N/2` đó là mức Grover phải vượt.

??? question "Tự kiểm tra — mục tiêu không bao giờ di chuyển: luôn là Albert ở chỉ số 4. Vậy con 4.5 từ đâu ra?"
    Từ việc *xáo trộn*, không phải từ dữ liệu. Trong một thứ tự cố định bạn luôn
    mất 5 lần thử — nhưng bạn cũng có thể được trao bất kỳ thứ tự nào khác. Trung
    bình trên mọi thứ tự, mục tiêu rơi vào mỗi vị trí đều nhau:
    `(1 + 2 + … + 8)/8 = 4.5`. Con 4.5 là cái giá của việc *không biết phải
    nhìn ở đâu*, đúng là ý nghĩa của "không cấu trúc".

## Oracle: một dấu, và không gì khác

Grover không bao giờ nhìn thấy danh sách. Nó chỉ nhận một **oracle** — hộp đen
khả nghịch của Chương 9 — nhận ra đáp án, và điều duy nhất oracle được phép làm
là đánh dấu nó:

$$U_w : |x\rangle \longrightarrow (-1)^{[x = w]}\,|x\rangle$$

Hãy đọc như một lời hứa với một viên thư ký: *anh không được chỉ tay vào hồ sơ;
anh chỉ được viết lên đó một dấu trừ nhỏ.* Mọi trạng thái giữ nguyên biên độ;
riêng trạng thái được đánh dấu bị lật dấu.

Ví dụ cụ thể: hai qubit, bốn trạng thái, đánh dấu `|11⟩`. Oracle là một ma trận
chéo chỉ có một số `-1`:

| Trạng thái cơ sở | Dấu |
|---|---|
| `00` | +1 |
| `01` | +1 |
| `10` | +1 |
| `11` (đánh dấu) | **−1** |

![Oracle của Grover: một lần lật dấu, không đo được gì](../assets/ch10-oracle-matrix.png){ width="420" }

Áp nó vào trạng thái đều — biên độ `(0.5, 0.5, 0.5, 0.5)` — ta được
`(0.5, .5, 0.5, −0.5)`... 

(Typo alert — fix when writing: `(0.5, 0.5, 0.5, −0.5)`)

Không cái nào đổi độ lớn; đúng một hướng bị đảo ngược. Đó là lý do lật dấu là
một **phản xạ**: nhân một toạ độ với `-1` là lấy đối xứng toạ độ đó qua số
không, giống như tấm gương đảo ngược một bức vẽ — cùng khoảng cách, phía bên
kia.

Và đó chính là chỗ khó: dấu tự nó là vô hình. Xác suất là bình phương biên độ,
mà `(−0.5)² = 0.25 = (0.5)²`, nên đo trước và đo sau oracle cho *cùng một*
biểu đồ. Toàn bộ phần việc còn lại của Grover là biến một dấu ẩn này thành một
xác suất lớn.

Hai nhận xét về cách dựng oracle như vậy trên thực tế:

- Nó phải là **mạch gồm các cổng khả nghịch** — quy tắc của Chương 9; một phép
  tra bảng nuốt đầu vào thì không được phép. Các mẫu ở đây kẹp trạng thái được
  đánh dấu giữa các cổng `X` (đưa nó về trạng thái toàn số 1), lật pha của nó
  bằng một `Z` đa điều khiển, rồi hoàn tác phần kẹp — khả nghịch từ đầu đến
  cuối.
- Đôi khi bạn sẽ gặp một oracle pha có **thêm một qubit**, được chuẩn bị ở
  `|−⟩` để dấu đến bằng phase kickback của Chương 9, dưới dạng `(-1)^f(x)`. Cùng
  một ma trận, cùng một lời hứa; cái `Z` đa điều khiển được kẹp ở đây làm trọn
  việc mà không cần qubit thêm.

??? question "Tự kiểm tra — oracle nhận ra đáp án. Vì sao nó không thể cứ chỉ thẳng trạng thái nào được đánh dấu?"
    Vì "chỉ" nghĩa là đổi biên độ, mà oracle chỉ được đổi dấu. Dấu nằm trong biên
    độ, còn phép đo nào cũng đọc xác suất — bình phương biên độ — nơi
    `(−0.5)² = (0.5)²`: dấu trừ biến mất. Đọc trạng thái sau oracle thì khả
    năng y hệt như trước nó. Dấu là thông tin có thật, nhưng được cất ở dạng mà
    không một phép đo đơn lẻ nào thấy được; mẹo của Grover là làm các trạng thái
    *khác* giao thoa với nó cho tới khi nó nổi lên.

## Khuếch tán: phản xạ quanh giá trị trung bình

Dấu trừ của oracle sẽ nằm ẩn mãi nếu Grover không thêm bước thứ hai: toán tử
**khuếch tán**, ý tưởng của nó đơn giản hơn công thức của nó. Hãy nghĩ về một
lớp học mà điểm trung bình là 7:

- bạn được **5** — thấp hơn trung bình hai điểm;
    phản xạ điểm của bạn quanh trung bình cho `2·7 − 5 = 9` — cao hơn trung
    bình hai điểm.

Quy tắc đó, `a → 2·mean − a`, áp lên *mọi* biên độ cùng lúc, chính là khuếch
tán: tính trung bình của tất cả các biên độ, rồi chuyển mỗi biên độ sang điểm
cách trung bình đúng chừng đó ở *phía bên kia*. Cái nào nằm dưới trung bình
thì được đẩy lên; cái nào nằm trên thì bị kéo xuống.

$$D = H^{\otimes n}\bigl(2|0\rangle\langle 0| - I\bigr)H^{\otimes n} = 2|s\rangle\langle s| - I$$

(Công thức nói cùng một điều bằng bộ áo fancier — h reflecting around chồng
chập đều `|s⟩`, mà với biên độ thì chính là "phản xạ quanh trung bình".)

Hãy xem nó làm việc trên đầu ra của oracle. Sau oracle, bốn biên độ là
`(0.5, 0.5, 0.5, −0.5)` và trung bình là
`(0.5 + 0.5 + 0.5 − 0.5)/4 = 0.25`:

| Biên độ | Phản xạ: `2·mean − a` | Kết quả |
|---|---|---|
| không đánh dấu `+0.5` | `2(0.25) − 0.5` | `0.0` |
| không đánh dấu `+0.5` | `2(0.25) − 0.5` | `0.0` |
| không đánh dấu `+0.5` | `2(0.25) − 0.5` | `0.0` |
| đánh dấu `−0.5` | `2(0.25) − (−0.5)` | `1.0` |

Vì sao nó hoạt động: phép phản xạ đẩy biên độ **vào** đúng những trạng thái
nằm *dưới* trung bình. Sau oracle chỉ có một trạng thái như vậy — trạng thái
được đánh dấu — nên chỉ nó được nâng lên, và nó vượt lên trên tất cả các trạng
thái khác. Các trạng thái không đánh dấu, đều nằm *trên* trung bình, chìm xuống
cùng nhau.

Hai bước này là một cặp, và không bước nào tự làm trọn việc — xem câu hỏi tự
kiểm tra dưới đây.

??? question "Tự kiểm tra — khuếch tán sẽ làm gì nếu bạn chạy nó *trước*, trước cả oracle, trên trạng thái đều mới khởi tạo?"
    Không gì cả. Bốn biên độ là `(0.5, 0.5, 0.5, 0.5)` và trung bình là `0.5`,
    nên mỗi phép phản xạ cho `2(0.5) − 0.5 = 0.5`: trạng thái đều là điểm bất
    động của khuếch tán. Phép phản xạ chỉ khuếch đại một trạng thái nằm *lệch
    khỏi* trung bình — và chính oracle là thứ đặt trạng thái đánh dấu xuống
    dưới nó. Không bước nào một mình tìm được gì; điệu nhảy cần cả hai bước.

## Từng bước trên hai qubit

Hai qubit cho bốn trạng thái — đủ ít để in mọi biên độ sau mỗi bước, nên ta
làm trọn thuật toán bằng tay, với số cụ thể. Đánh dấu `|11⟩` và bắt đầu đều.

**Bước 0 — chuẩn bị.** `H` lên cả hai qubit:

$$|s\rangle = \tfrac{1}{2}\bigl(|00\rangle + |01\rangle + |10\rangle + |11\rangle\bigr)$$

Biên độ `(0.5, 0.5, 0.5, 0.5)`, trung bình `0.5`, và `P(11) = 0.25` — cùng
xác suất như đoán mò.

**Bước 1 — oracle lật một dấu.**

$$(0.5,\; 0.5,\; 0.5,\; 0.5) \;\longrightarrow\; (0.5,\; 0.5,\; 0.5,\; -0.5)$$

Vẫn chưa đo được gì — nhưng trung bình đã lặng lẽ rơi xuống
`(0.5 + 0.5 + 0.5 − 0.5)/4 = 0.25`, và biên độ đánh dấu giờ nằm *dưới* nó.

**Bước 2 — khuếch tán phản xạ quanh trung bình đó**, `a → 2(0.25) − a`:

- không đánh dấu: `2(0.25) − 0.5 = 0`;
- đánh dấu: `2(0.25) − (−0.5) = 1.0`.

Trạng thái bây giờ là đúng `|11⟩` — xác suất `1.00`, đo là trúng chắc chắn.
Một vòng điệu nhảy — một oracle, một khuếch tán — đã biến cú đoán 1-trong-4
thành điều chắc chắn:

| Vòng | `00` | `01` | `10` | `11` đánh dấu |
|---|---|---|---|---|
| sau 0 vòng | +0.50 | +0.50 | +0.50 | +0.50 |
| sau 1 vòng | 0.00 | 0.00 | 0.00 | **+1.00** |
| sau 2 vòng | −0.50 | −0.50 | −0.50 | +0.50 |

![Grover trên 2 qubit: trạng thái đánh dấu lấy hết xác suất](../assets/ch10-step-by-step.png){ width="620" }

**Vì sao một vòng là đủ ở đây.** Mỗi vòng là một phép xoay nhỏ của cả vector
biên độ một góc cố định `2θ`, với `sin θ = 1/√N` (ở đây `sin θ = 1/2`, nên
`θ = 30°` và mỗi vòng xoay `60°`). Xác suất của đáp án sau `k` vòng là
`sin²((2k+1)θ)`, và với `N = 4`, phép cộng rơi đúng vào `sin²(90°) = 1` sau
một vòng — một cú landed hoàn hảo mà chỉ trường hợp nhỏ nhất mới cho phép.

(Landed → "tiếp đất hoàn hảo" — dùng từ tự nhiên)

**Còn vòng thứ hai thì vọt quá.** Chạy lại điệu nhảy đó từ `(0, 0, 0, 1)`:

1. **Oracle:** biên độ đánh dấu bị lật, `1.0 → −1.0`, vector thành
   `(0, 0, 0, −1)` và trung bình rơi xuống `(0 + 0 + 0 − 1)/4 = −0.25`.
2. **Khuếch tán:** không đánh dấu `2(−0.25) − 0 = −0.5`; đánh dấu
   `2(−0.25) − (−1.0) = +0.5`.

Xác suất của trạng thái đánh dấu rơi từ `1` xuống `0.25`. Phép xoay chẳng bao
giờ biết mình đã đến nơi — nó cứ tiếp tục quay, thẳng qua đáp án. Chạy Grover
quá lâu làm kết quả tệ đi.

??? question "Tự kiểm tra — một vòng cho xác suất 1.00, đáp án chắc chắn. Vì sao lặp lại *cùng* vòng đó lại làm tệ đi?"
    Vì một vòng là phép xoay cố định, không phải tên lửa tự tìm mục tiêu. Nó
    xoay vector biên độ cùng một góc `60°` mỗi lần, và không có gì bảo nó dừng
    khi vector đã chỉ vào đáp án. Vòng thứ hai xoay *qua* đáp án, và phép tính
    cho thấy nó đáp xuống đâu: `(−0.5, −0.5, −0.5, +0.5)`, xác suất `0.25`.
    Thêm vòng không phải thêm công sức tìm — mà là thêm xoay, theo hướng giờ đã
    chỉ ra ngoài.

## Grover trên 64 mục

Giờ là thí nghiệm thật của chương: sáu qubit, `N = 64` trạng thái, và trạng
thái `chỉ số 7` — nhãn `111000`, vì `q0 = q1 = q2 = 1` — được oracle đánh dấu.

Điệu nhảy y như cũ nhưng góc nhỏ hơn: `sin θ = 1/√64 = 1/8` cho `θ ≈ 7.18°`,
nên mỗi vòng xoay vector biên độ khoảng `2θ ≈ 14.36°`. Để chỉ vào đáp án,
vector phải xoay khoảng một phần tư vòng — chừng `90° − θ ≈ 82.8°` — mà
`82.8 / 14.36 ≈ 5.8`, nên số vòng tốt nhất là

$$\left\lfloor \tfrac{\pi}{4}\sqrt{N} \right\rfloor
= \left\lfloor \tfrac{\pi}{4}\sqrt{64} \right\rfloor = 6 \text{ vòng}.$$

Simulator xác nhận từng xác suất (đáp án tuân theo `sin²((2k+1)θ)`):

| Vòng | 0 | 1 | 2 | 3 | 4 | 5 | **6** | 7 | 8 | 9 |
|---|---|---|---|---|---|---|---|---|---|---|
| P(đáp án) | 0.02 | 0.13 | 0.34 | 0.59 | 0.82 | 0.96 | **1.00** | 0.91 | 0.72 | 0.47 |

![Grover trên 64 mục: xác suất tăng rồi vọt quá](../assets/ch10-grover-curve.png){ width="620" }

Hai con số cần mang ra khỏi thí nghiệm:

- sau **6 vòng**, `P(đáp án) = 0.997` — tìm kiếm coi như xong, so với trung
  bình **32** lần kiểm tra cổ điển cho cùng danh sách;
- chạy quá lâu thì nó *chưa* xong trở lại: 7 vòng đã rơi xuống `0.907`, 9 vòng
  xuống `0.475`. Phép xoay vọt quá, nên thêm vòng không phải vòng tốt hơn.

Đo 2000 lần sau 6 vòng, đáp án trở về áp đảo — `1995` trên `2000` lần đo trả về
`111000`:

![64 kết quả sau 6 vòng: đáp án chiếm ưu thế](../assets/ch10-grover-outcomes.png){ width="620" }

![Một mạch Grover nhỏ](../assets/ch10-grover-circuit.png){ width="620" }

Mạch là cả vòng lặp hiện hình: `H` lên mọi qubit một lần, rồi mỗi vòng một cặp
**oracle / khuếch tán**. Khối `H, X, MCZ, X, H` ở mỗi vòng là phép phản xạ
quanh giá trị trung bình — cùng một phép phản xạ, viết bằng các cổng khả
nghịch; còn phép lật pha đơn lẻ bên trong là oracle.

## Tăng tốc lớn đến đâu?

| Số mục `N` | Cổ điển (trung bình) | Số vòng Grover |
|---|---|---|
| 8 | 4.5 | 2 |
| 64 | 32 | 6 |
| 1 000 000 | 500 000 | 785 |

Quy luật là `N/2` so với `(π/4)·√N`: **bậc hai**, không phải hàm mũ. Gấp đôi danh
sách thì công việc cổ điển nhân bốn nhưng công việc lượng tử chỉ nhân khoảng
`√2`. Đó là kích thước trung thực của món quà Grover — có thật, hữu ích, và khiêm
tốn — và nó được chứng minh là mức tốt nhất có thể cho một danh sách không có cấu
trúc để khai thác.

!!! note "Tăng tốc đến từ đâu"
    Grover không thử các mục song song rồi đọc hết câu trả lời ra — một phép đo
    chỉ trả về một trạng thái cơ sở. Nó chạy oracle **một lần mỗi vòng** trên cả
    chồng chập và để *giao thoa* dồn xác suất lại. Độ lợi là căn bậc hai vì mỗi
    vòng là thêm một phép xoay của vector biên độ, và vector ấy chỉ cần xoay một
    phần tư vòng để chỉ vào đáp án.

## Các sơ đồ {#cac-so-do}

### Mốc cổ điển

![Phép quét cổ điển: mất bao nhiêu lần thử để tìm mục tiêu](../assets/ch10-classical-tries.png){ width="560" }

### Oracle

![Oracle của Grover: một lần lật dấu, không đo được gì](../assets/ch10-oracle-matrix.png){ width="420" }

### Từng bước

![Grover trên 2 qubit: trạng thái đánh dấu lấy hết xác suất](../assets/ch10-step-by-step.png){ width="620" }

### Grover trên 64 mục

![Một mạch Grover nhỏ](../assets/ch10-grover-circuit.png){ width="620" }

![Grover trên 64 mục: xác suất tăng rồi vọt quá](../assets/ch10-grover-curve.png){ width="620" }

![64 kết quả sau 6 vòng: đáp án chiếm ưu thế](../assets/ch10-grover-outcomes.png){ width="620" }

## Những điều cần nhớ

- **Tìm kiếm không cấu trúc** không có khoá đã sắp xếp để khai thác: cổ điển tốn
  `(N+1)/2 ≈ N/2` phép thử trung bình, và không có cách cổ điển nào tốt hơn.
- **Oracle** đánh dấu đáp án bằng một **lần lật pha** — `(-1)^[x = w]` — và không
  làm gì khác. Lật dấu là một phản xạ, và tự thân nó vô hình vì xác suất bình
  phương làm dấu biến mất.
- **Khuếch tán** (`2|s⟩⟨s| − I`) phản xạ mọi biên độ quanh giá trị trung bình,
  `a → 2·mean − a`. Nó đẩy biên độ vào các trạng thái dưới trung bình — và sau
  oracle, trạng thái đánh dấu là trạng thái duy nhất ở đó.
- Mỗi vòng **oracle + khuếch tán** là một phép xoay cố định `2θ` của vector biên
  độ (`sin θ = 1/√N`); xác suất của đáp án tuân theo `sin²((2k+1)θ)`. Trên bốn
  trạng thái, `0.5 → 1.0` chỉ sau một vòng.
- **Số vòng rất quan trọng**: quá ít vòng thì xác suất còn nhỏ, quá nhiều vòng thì
  xoay vượt qua đáp án — trên 64 mục, 6 vòng cho `0.997` nhưng 9 vòng chỉ còn
  `0.475`. Mức tối ưu vào khoảng `(π/4)·√N`.
- Tăng tốc là **bậc hai** — `(π/4)·√N` so với `N/2`, tức khoảng `785` vòng cho
  một triệu mục so với `500 000` lần kiểm tra — và không thuật toán lượng tử nào
  vượt được nó cho một danh sách không sắp xếp.

## Mã nguồn của chương này

Bốn mẫu, từ mốc cổ điển tới thuật toán đầy đủ:

- [`ch10/search.py`](https://github.com/phonhay103/quantum-computing-in-action/blob/main/src/quantum_computing_in_action/ch10/search.py)
  — hai mẫu ``classicsearch`` và ``quantumsearch``: danh bạ, phép quét tuyến tính,
  và một tìm kiếm Grover trên chính các mục đó.
- [`ch10/oracle.py`](https://github.com/phonhay103/quantum-computing-in-action/blob/main/src/quantum_computing_in_action/ch10/oracle.py)
  — mẫu ``groveroracle``: oracle pha, dựng từ một cổng `Z` đa điều khiển tường
  minh, và ma trận của nó.
- [`ch10/step_by_step.py`](https://github.com/phonhay103/quantum-computing-in-action/blob/main/src/quantum_computing_in_action/ch10/step_by_step.py)
  — mẫu ``stepbystepgrover``: hai qubit, biên độ sau mỗi vòng.
- [`ch10/grover.py`](https://github.com/phonhay103/quantum-computing-in-action/blob/main/src/quantum_computing_in_action/ch10/grover.py)
  — mẫu ``grover``: toán tử khuếch tán, số vòng, đường cong thành công, và các kết
  quả đo được.

Chạy toàn bộ bằng `make ch10`, hoặc từng mẫu một:

```bash
uv run python -m quantum_computing_in_action.ch10.grover
```
