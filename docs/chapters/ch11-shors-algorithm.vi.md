# Chương 11 — Thuật toán Shor

!!! abstract "Trong một câu"
    Phân tích thừa số chỉ khó vì **tìm bậc** khó; một chồng chập tuần hoàn cộng
    với **biến đổi Fourier lượng tử** tìm ra bậc trong thời gian đa thức, rồi vài phép
    `gcd` biến bậc đó thành các thừa số.

## Câu hỏi chương này trả lời

Nhân hai số nguyên tố là việc tức thì: `3 × 5 = 15`, xong. Đi ngược lại — cho
`15`, tìm lại `3` và `5` — được tin là vô vọng với các số lớn, và mật mã khoá
công khai kiểu RSA dựa chính vào khoảng trống đó. Thuật toán Shor là vết nứt
lượng tử nổi tiếng ở nơi đó, và chương này đặt ra ba câu cần được trả lời để
hiểu nó một cách trung thực. Mỗi câu xây trên câu trước: câu đầu xác định chỗ
khó cổ điển nằm ở đâu, câu hai biến khó đó thành một bài toán khác khả thi
hơn, và câu ba chỉ ra chính xác nơi máy lượng tử tham gia.

1. **Vì sao phân tích thừa số là bài toán mọi người quan tâm, và điều gì làm
   nó khó?** Mốc trung thực là phép chia thử học ở trường — thử `2`, rồi
   `3`, rồi `5`, … Nó chạy được, và nó chết vì căn bậc hai: công việc tăng theo
   `√N`, nên một số dài gấp đôi tốn chi phí khổng lồ gấp nhiều lần. Nói cách
   khác, khó khăn không nằm ở khái niệm mà ở mặt tính toán: đáp án được định
   nghĩa rõ ràng và dễ kiểm tra, thế mà chưa có thủ tục cổ điển hiệu quả nào
   sinh ra được nó.
2. **Phân tích thừa số có liên quan gì tới chu kỳ?** Phép quy giản của Shor:
   đừng đi tìm ước số trực tiếp. Hãy tìm chu kỳ `r` của dãy `a^x mod N`, rồi
   các thừa số rơi ra từ hai phép `gcd`. Chương này tính trọn vẹn cho
   `N = 15`, rồi tới ví dụ lớn hơn của sách, `N = 493`, vì phép quy giản chỉ
   thuyết phục khi mọi con số trên đường đi đều được sinh ra tường minh.
3. **Máy lượng tử tìm chu kỳ bằng cách nào?** Một chồng chập tính `a^x mod N`
   cho *mọi* `x` cùng lúc, và biến đổi Fourier lượng tử là mảnh ghép biến
   nhịp lặp ẩn đó thành vài đỉnh nhọn, đo được. Đọc một đỉnh là khôi phục
   được `r` — và `r` bẻ gãy `N`. Cần lưu ý rằng máy lượng tử ở đây chỉ giải
   một bước nhỏ được định nghĩa gọn; mọi thứ bao quanh bước đó vẫn giữ nguyên
   tính cổ điển.

Sau chương này, các năng lực sau đây sẵn sàng:

- phân tích `15` bằng chia thử và nói chính xác *khi nào* phương pháp đó chết;
- biến một chu kỳ thành các thừa số bằng hai phép `gcd`, và giải thích vì sao
  chu kỳ lẻ nghĩa là "không may, chọn `a` khác";
- giải thích QFT như là "đếm một mẫu lặp lại bao lâu một lần", với các con số
  cụ thể cho thấy các đỉnh rơi ở đâu;
- đi trọn thuật toán cho `N = 15`, nói rõ bước nào cổ điển và bước nào thật sự
  lượng tử.

Bốn thành phần từ các chương trước là cần thiết, mỗi điều một dòng: `H` đưa
một thanh ghi vào chồng chập đều của mọi giá trị của nó cùng lúc, và phép đo
chọn một kết quả với xác suất = biên độ²
([Chương 4](ch04-superposition.md)); một cổng có điều khiển chỉ tác động lên
đích khi điều khiển của nó là `1` ([Chương 3](ch03-qubits-and-gates.md)); một
mạch là một chương trình — một danh sách bước có thứ tự, đọc được từng cổng
một ([Chương 7](ch07-helloworld-explained.md)); và một oracle tính `f` trên
mọi đầu vào cùng lúc trong một chồng chập
([Chương 9](ch09-deutsch-jozsa.md)).

!!! note "Một chút sổ sách: từ ngữ và ký hiệu"
    - `x mod N` là *số dư* khi chia `x` cho `N`: `16 mod 15 = 1`. "Nhân mod N"
      đơn giản nghĩa là "chỉ giữ số dư". Hiểu như vậy, số học modulo `N`
      không bao giờ rời khoảng `0 … N − 1` dù nhân bao nhiêu lần đi nữa.
    - `gcd(u, v)` là số lớn nhất chia hết cả hai: `gcd(12, 15) = 3`. Nếu
      `gcd(a, N) = 1` thì `a` và `N` **nguyên tố cùng nhau** — không chia sẻ
      ước số nào. Chính tính nguyên tố cùng nhau là điều kiện khiến cơ chế
      chu kỳ của chương này được định nghĩa rõ ràng.
    - **Chu kỳ** của `a` modulo `N` — còn gọi là **bậc** — là số `r ≥ 1` nhỏ
      nhất với `a^r mod N = 1`. Cả chương này săn đúng một con số ấy; phần
      còn lại của thuật toán hoặc giúp tìm nó, hoặc biến nó thành các thừa số
      về sau.
    - Hai thanh ghi xuyên suốt: thanh ghi **đếm** giữ số mũ `x`; thanh ghi
      **công việc** giữ giá trị `a^x mod N`. Một kết quả đo `s` của thanh ghi
      đếm luôn được đọc là phân số `s / 2^m ≈ k / r`.

## Phân tích thừa số, và vì sao nó khó

Mọi số là tích của các số nguyên tố. Với số nhỏ, các thừa số hiện ra ngay;
với một số 600 chữ số, không ai biết cách tìm chúng. Phương pháp cổ điển
tốt nhất — **sàng trường số tổng quát** — vẫn *dưới hàm mũ*: chi phí tăng gần
như `2^số bit`. Thuật toán Shor là *đa thức*, và đó là toàn bộ danh tiếng của
điện toán lượng tử gói trong một câu. Do đó, khác biệt ở đây không phải là
một cải thiện cỡ bội số: hai tốc độ tăng trưởng thuộc về hai thế giới, và với
đầu vào cỡ mật mã, khoảng cách đó thành vực thẳm.

Nhưng trước khi ngắm câu trả lời lượng tử, câu trả lời cổ điển phải được
dựng lên và nhìn thấy gục ngã. Đó là những gì chương này (và mô-đun
`ch11.classical`) làm trước tiên — vì thuật toán Shor *chính là* phương pháp
cổ điển với một bước được thay ra, và không ai thấy được bước nào cho tới khi
phương pháp cổ điển nằm gọn trong tay. Có mốc cơ sở, từng thành phần cổ điển
trong bản lượng tử mới có thể lần về nó từng cái một.

## Chia thử: mốc cổ điển trung thực

Phương pháp ngây thơ dễ tin vì mỗi bước đều có thể kiểm bằng tay. Để phân
tích `N`: thử `2`, rồi mọi số lẻ `3, 5, 7, …`, dừng ở số đầu tiên chia hết
`N`. Không có gì tinh vi hơn — phương pháp chỉ là một tìm kiếm mệt mỏi mà có
thứ tự, và chính sự minh bạch đó khiến nó trở thành mốc đối chiếu để đo tốc
độ nhanh hơn của bản lượng tử.

**Tính trọn: `N = 15`.**

- thử `2`: `15 = 2 × 7 + 1` — số dư `1`, không phải ước;
- thử `3`: `15 = 3 × 5` — số dư `0`. Tìm được thừa số: `3`, còn số ghép của nó
  là `15 / 3 = 5`.

Hai phép chia, đáp án `15 = 3 × 5`. Mô-đun báo cáo đúng như vậy:
`trial_division(15) = 3` sau `steps_to_factor(15) = 2` phép chia.

**Tính trọn: `N = 91`.**

- `2`: `91 = 2 × 45 + 1` — không;
- `3`: `91 = 3 × 30 + 1` — không;
- `5`: `91 = 5 × 18 + 1` — không;
- `7`: `91 = 7 × 13` — đúng.

Bốn phép chia, đáp án `91 = 7 × 13`. Hai ví dụ cũng chỉ ra quy luật đáng chú
ý: số phép chia do *khoảng cách của thừa số đầu tiên tới 0* quyết định, chứ
không chỉ do kích thước của `N`. Số nguyên tố là trường hợp xấu nhất, vì lần
tìm chỉ dừng ở `√N` mà chưa có gì chia được `N`.

![Chia thử cổ điển: công việc tăng như sqrt(n)](../assets/ch11-classical-factor.png){ width="620" }

**Quy tắc chung, và vì sao nó chết.** Chỉ cần thử các ước tới `√N`, vì ước
số đi theo cặp: nếu `d` chia hết `N` thì `N / d` cũng vậy, và số nhỏ hơn
trong cặp không bao giờ vượt `√N`. (Với `91`: `√91 ≈ 9,5`, và ước nhỏ nhất
`7` nằm dưới ngưỡng đó; nếu không gì chia được `91` trước ngưỡng, `91` là số
nguyên tố.) Đó là tin tốt — và cũng là bản án chết, vì vòng lặp vẫn chạy
khoảng `√N` lần:

| `N` | chữ số | phép chia thử (`steps_to_factor`) |
|---|---|---|
| `15` | 2 | 2 |
| `91` | 2 | 4 |
| `999983` (nguyên tố) | 6 | 500 |
| `999999999989` (nguyên tố) | 12 | 500 000 |

Gấp đôi số chữ số là nhân công việc lên khoảng `1000` lần, vì `√10^6 ≈ 10^3`
trở thành `√10^12 = 10^6`. Trường hợp xấu nhất dưới `200` trong
`steps_curve` của mô-đun là `N = 169 = 13²` với 7 phép chia — đường cong gần
như phẳng ở quy mô này, còn một mô-đun RSA 600 chữ số sẽ cần cỡ `10^300`
phép. Chia thử không phải phương pháp cổ điển tốt nhất, nhưng *mọi* phương
pháp cổ điển đã biết đều bùng nổ kiểu này; chỉ khác về số mũ. Vì vậy, điểm
yếu nằm ở quy luật tăng trưởng chứ không phải một lần cài đặt cụ thể nào.

## Phép quy giản: phân tích thừa số trở thành tìm bậc

Ý tưởng của Shor là ước số không nên đi tìm trực tiếp. Thay vào đó, một nhịp
ẩn trong một dãy số được săn lùng — và các thừa số rơi ra từ nhịp ấy như sản
phẩm phụ, gần như không tốn thêm công.

Chọn `a` nguyên tố cùng nhau với `N` — chẳng hạn `a = 2`, `N = 15` — và nhìn
vào dãy

$$f(x) = a^x \bmod N = 2^x \bmod 15$$

Tính từng bước một (mỗi phần tử bằng phần tử trước nhân `2`, giữ số dư):

| `x` | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 |
|---|---|---|---|---|---|---|---|---|---|
| `2^x mod 15` | 1 | 2 | 4 | 8 | 1 | 2 | 4 | 8 | 1 |

`1, 2, 4, 8`, rồi lại `1`. Dãy **tuần hoàn** với chu kỳ `r = 4`: số `r` nhỏ
nhất với `2^r mod 15 = 1` (thật vậy `2^4 = 16 = 1 × 15 + 1`).

![Chu kỳ của 2^x mod 15 là 4](../assets/ch11-period-function.png){ width="620" }

**Vì sao chu kỳ cho ra thừa số — tính trọn.** Chỉ cần đúng một hằng đẳng
thức: hiệu hai bình phương.

$$a^r - 1 = \left(a^{r/2} - 1\right)\left(a^{r/2} + 1\right)$$

Vì `a^r mod N = 1`, số `N` chia hết `a^r − 1`, nên `N` chia hết tích của hai
ngoặc. Với `a = 2`, `r = 4`, `N = 15`:

- `a^(r/2) = 2^(4/2) = 2^2 = 4`;
- `a^r − 1 = 16 − 1 = 15 = (4 − 1)(4 + 1) = 3 × 5` — hai ngoặc *chính là*
  các thừa số ở đây;
- `gcd(4 − 1, 15) = gcd(3, 15) = 3` và `gcd(4 + 1, 15) = gcd(5, 15) = 5`.

**Quy tắc chung.** Biết chu kỳ `r` của `a` mod `N`:

1. nếu `r` lẻ, hoặc `a^(r/2) ≡ −1 (mod N)`, thì `a` này không may — chọn `a`
   khác và thử lại;
2. ngược lại hai thừa số của `N` là `gcd(a^(r/2) − 1, N)` và
   `gcd(a^(r/2) + 1, N)`.

Hai điều kiện loại đều tồn tại vì `N` phải *xẻ đôi* giữa hai ngoặc. Nếu `N`
chia hết trọn một ngoặc, ngoặc đó `≡ 0` hoặc `≡ −1` và `gcd` của nó cho đáp
án tầm thường (`1` hoặc `N`) — không mang thông tin. Các trường hợp không may
là thật: với `a = 2`, `N = 7` dãy là `2, 4, 1` với `r = 3` (lẻ — `a^(r/2)`
thậm chí không phải luỹ thừa nguyên); còn với `a = 2`, `N = 5` chu kỳ
`r = 4` chẵn nhưng `2^2 = 4 ≡ −1 (mod 5)`, nên `gcd(3, 5) = 1` và
`gcd(5, 5) = 5` — không học được gì. Chọn `a` khác. Vì hầu hết các lựa chọn
`a` đều không rơi vào nhóm không may, một lựa chọn ngẫu nhiên cùng số lần
thử lại có hạn làm cho toàn bộ thủ tục vẫn giữ hiệu quả.

**Ví dụ lớn hơn của sách, tính trọn.** `a = 6`, `N = 493` (đúng các con số
hai snippet `jshell` của sách kiểm tra; `reduction_steps(6, 493)` tái tạo
chúng):

- chu kỳ của `6 mod 493` là `r = 112`;
- `6^(r/2) = 6^56 mod 493 = 407`;
- `gcd(407 − 1, 493) = gcd(406, 493) = 29`;
- `gcd(407 + 1, 493) = gcd(408, 493) = 17`;
- và đúng là `493 = 17 × 29`.

**Vấn đề.** Tìm `r` bằng vét cạn — nhân `a` với chính nó cho tới khi số dư
trở về `1` — tốn tới `r` phép nhân, mà `r` có thể lớn bằng `N`. Nó *khó như
phân tích thừa số*, nên phép quy giản tự nó không đem lại gì. Thứ nó làm là
cô lập bước duy nhất máy lượng tử làm tốt: **tìm bậc**. Mọi thứ khác trong
thuật toán Shor là phép số học cổ điển vừa được đọc ở trên, và sự phân công
ấy — lớp giàn giáo cổ điển ôm lấy một bước lượng tử duy nhất — là nét đặc
trưng của phần lớn thuật toán lượng tử có ý nghĩa thực dụng.

??? question "Tự kiểm tra — vì sao `a` phải nguyên tố cùng nhau với `N`?"
    Nếu `gcd(a, N) = d > 1` thì `d` **đã là một thừa số** — chẳng hạn `a = 5`,
    `N = 15`: `gcd(5, 15) = 5`, xong, không cần máy lượng tử. Tệ hơn, dãy
    `a^x mod N` sẽ không bao giờ trở về `1` (mọi luỹ thừa của `a` vẫn chia
    hết cho `d`), nên sẽ không có chu kỳ để tìm. Vì thế bước đầu tiên của Shor
    tính `gcd(a, N)`: nó hoặc kết thúc công việc tức thì, hoặc chứng minh `a`
    dùng được.

??? question "Tự kiểm tra — chu kỳ của `4 mod 21` là `r = 3`, lẻ. Vì sao đó là 'không may', và Shor làm gì?"
    Toàn bộ mẹo quy giản `a^r − 1` thành hai ngoặc `a^(r/2) ± 1`, mà với
    `r = 3` thì số mũ `r/2 = 1,5` không nguyên — hai ngoặc không tồn tại. Shor
    đơn giản chọn `a` khác. Với `N = 21`, thử lại với `a = 2` cho chu kỳ chẵn
    `r = 6`, `2^3 mod 21 = 8`, và `gcd(7, 21) = 7`, `gcd(9, 21) = 3` — vậy
    `21 = 3 × 7`. (Kiểm tra trường hợp không may bằng tay: `4, 16, 64 = 3 ×
    21 + 1` — ba bước trở về `1`.)

## Biến đổi Fourier lượng tử

Mục tiêu bằng lời nói của mục này: **đếm một mẫu lặp lại bao lâu một lần**.
Biến đổi Fourier — cùng nền toán học cho thấy một dây đàn ghi-ta
rung 440 lần một giây — lấy một tín hiệu và trả lời "cái này lặp lại bao lâu
một lần?". **Biến đổi Fourier lượng tử** (QFT) là biến đổi Fourier rời rạc
viết dưới dạng mạch, để một thanh ghi lượng tử tự hỏi câu đó về biên độ của
chính nó. Nên nhấn mạnh rằng ở đây không có toán học mới nào tham gia; cái
mới nằm hoàn toàn ở chỗ biến đổi đã quen thuộc được áp lên biên độ lượng tử
thay vì dữ liệu cổ điển.

![Mạch QFT ba qubit](../assets/ch11-qft-circuit.png){ width="620" }

**Tính trọn: một danh sách lặp mỗi 4 bước.** Lấy `m = 4` qubit, tức danh sách
`2^4 = 16` biên độ. Đặt biên độ `1/2` tại các vị trí `0, 4, 8, 12` và `0`
khắp nơi khác — một mẫu lặp mỗi `r = 4` vị trí. (Đúng hình dạng thanh ghi
đếm sẽ có ở mục sau.) Áp dụng `qft_matrix(4)` và nhìn xác suất của 16 kết quả:

| kết quả `s` | 0 | 4 | 8 | 12 | mọi `s` khác |
|---|---|---|---|---|---|
| xác suất | 0.25 | 0.25 | 0.25 | 0.25 | 0 |

Toàn bộ trọng số đổ vào **bốn đỉnh nhọn**, và vị trí của chúng đọc là phân số
của cả dải:

$$\frac{0}{16} = 0,\qquad \frac{4}{16} = \frac{1}{4},\qquad
\frac{8}{16} = \frac{1}{2},\qquad \frac{12}{16} = \frac{3}{4}$$

Các bội của `1/4` — mà `4` chính là chu kỳ. Đó là toàn bộ mẹo: **chu kỳ di
chuyển từ *khoảng cách* của mẫu sang *vị trí* của các đỉnh**, còn vị trí đỉnh
là thứ đo được. Kết quả là, biến đổi chuyển một *tính chất thống kê* (biên độ
trải ra sao) thành một *tính chất vị trí* (các kết quả dồn về đâu), và chỉ
thứ hai mới là thứ tiếp cận được sau phép đo.

**Vì sao nó hoạt động.** Mỗi biên độ đầu ra là tổng của các bản sao
pha-tăng-dần của đầu vào, mỗi phần tử khác 0 một bản sao. Tại đầu ra `s`, hai
bản sao liên tiếp (cách nhau 4 vị trí) lệch nhau một bước pha
`e^{2πi·4·s/16} = e^{πis/2}`. Khi `s` là bội của `16/4 = 4` — tại
`s = 0, 4, 8, 12` — bước đó là số nguyên vòng quay, mọi bản sao chỉ cùng hướng
và cộng nhau. Tại mọi `s` khác, các bản sao xoay vòng quanh hình tròn và triệt
tiêu: chẳng hạn tại `s = 1` bốn bản sao chỉ về `0°, 90°, 180°, 270°` — đủ bốn
hướng la bàn, tổng bằng không. Các đỉnh là giao thoa cộng; sự im lặng ở nơi
khác là giao thoa triệt tiêu. Suy ra rằng QFT không tính thứ gì máy cổ điển
không tính được; điều đáng ghi nhận là phép tính được thực hiện trên mọi biên
độ của một chồng chập trong một lượt duy nhất.

![QFT|1>: độ lớn đều, dốc pha tuyến tính](../assets/ch11-qft-phase.png){ width="620" }

**Trên một trạng thái cơ sở, cùng mạch đó làm điều có thể viết vào bảng.**
QFT của `|k⟩` trải một **dốc pha** trên mọi đầu ra:

$$\mathrm{QFT}\,|k\rangle = \frac{1}{\sqrt{N}}\sum_j e^{2\pi i j k / N} |j\rangle$$

Nạp `|1⟩` cho mạch ba qubit (`k = 1`, `N = 8`) thì mọi đầu ra có cùng độ lớn
`1/√8 ≈ 0,354`, còn pha leo `2π/8 = π/4` mỗi bước — đo bởi `phase_ramp(3)`:

| `j` | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 |
|---|---|---|---|---|---|---|---|---|
| pha (đơn vị π) | 0 | 0.25 | 0.50 | 0.75 | 1.00 | −0.75 | −0.50 | −0.25 |

Ba phần tử cuối đã vượt `π` và được in gập vào khoảng `(−π, π]`: pha `−0.75π`
là đúng điểm `1.25π` trên hình tròn. Dốc pha leo đều; chỉ nhãn bị gập. Độ
lớn thì trái lại không đổi: một trạng thái cơ sở duy nhất đặt hết biên độ
lên các đầu ra cùng kích thước, nên toàn bộ thông tin Fourier nằm trong pha.

Ma trận đứng sau tất cả là ma trận Fourier quen thuộc
`F[j, k] = e^(2πi j k / N)/√N` — đối xứng, **unita**, và khả nghịch bằng cách
chạy cùng mạch đó ngược lại (`qft_circuit(n, inverse=True)`). Tính unita không
phải trang trí: đó là lý do QFT (nghịch đảo) đứng được trong một thuật toán
lượng tử, và QFT *nghịch đảo* chính là thứ Shor áp dụng — một thanh ghi
*tuần hoàn* là thứ nó biến thành các đỉnh nhọn phía trên. Một biến đổi không
unita sẽ làm mất chuẩn biên độ và không thể xuất hiện trong một mạch lượng tử
khả nghịch.

## Tìm bậc: chu kỳ thành các đỉnh

Giờ bộ tìm chu kỳ được ghép lại. Mạch dùng **hai thanh ghi**, mỗi thanh một
việc gọi tên được bằng lời:

- thanh ghi **đếm** — `m` qubit — *đếm* `x = 0, 1, 2, …`. Hadamard đưa nó vào
  chồng chập đều của **mọi số mũ cùng lúc** (`2^m` giá trị);
- thanh ghi **công việc** — đủ qubit để giữ `N` — *giữ giá trị*
  `f(x) = a^x mod N`. Nó khởi đầu ở `|1⟩`, và các phép nhân modular có điều
  khiển `|y⟩ → |a^(2^j)·y mod N⟩` ghi `f` vào đó: qubit đếm `j` nhân thanh
  ghi công việc với `a^(2^j)` khi nó là `1`.

Đây lại là khuôn mẫu Deutsch–Jozsa ([Chương 9](ch09-deutsch-jozsa.md), giới
thiệu việc tính hàm bên trong một chồng chập): một mạch tính `f` trên mọi đầu
vào cùng lúc. Với `a = 2`, `N = 15`, `m = 8`: thanh ghi đếm giữ cả `256` số
mũ, còn thanh ghi công việc giữ `2^x mod 15` cạnh mỗi số mũ — dãy tuần hoàn
`1, 2, 4, 8, 1, 2, 4, 8, …` trải trên một chồng chập. Hiệu quả là cặp thanh
ghi ghép mỗi số mũ với giá trị mà nó sinh ra, và cấu trúc tuần hoàn của
dãy giờ nằm trong *tương quan giữa hai thanh ghi* chứ không trong một giá trị
được lưu nào.

![Một mạch tìm bậc gọn](../assets/ch11-order-circuit.png){ width="620" }

Đo thanh ghi công việc sẽ sập nó về một giá trị — vô dụng, vì một giá trị đơn
lẻ của `f(x)` không mang vết tích nào về tính tuần hoàn mà phần còn lại của
thuật toán cần. Thay vào đó, mạch áp dụng **QFT nghịch đảo** lên thanh ghi
đếm, và chu kỳ ẩn trong nó thành các đỉnh đọc được:

![QFT nghịch đảo của thanh ghi tuần hoàn: bốn đỉnh](../assets/ch11-order-peaks.png){ width="620" }

`order_distribution(2, 15)` cho đúng các con số. Thanh ghi đếm (`m = 8`, tức
`2^m = 256` kết quả) cho **bốn đỉnh**, mỗi đỉnh xác suất `0.25`, tại

$$0,\quad 64,\quad 128,\quad 192 \qquad\text{— cách nhau } \frac{2^m}{r} = \frac{256}{4} = 64.$$

Đọc một đỉnh là phân số `k/r = outcome / 2^m` rồi đưa qua khai triển **phân
số liên tục** (thuật toán Euclid trên `outcome` và `2^m`; mỗi thương bóc ra
một chữ số của phân số):

| Đo được | `k/r = outcome / 2^m` | Giản phân | Chu kỳ tìm được |
|---|---|---|---|
| 0 | 0 | `0/1` | — (`k = 0`, không có thông tin) |
| 64 | `64/256 = 1/4` | `0/1 → 1/4` | **4** |
| 128 | `128/256 = 1/2` | `0/1 → 1/2` | — (`2^2 = 4 ≠ 1`, phép kiểm thất bại) |
| 192 | `192/256 = 3/4` | `0/1 → 1/1 → 3/4` | **4** |

Tính trọn cho `outcome = 64`: `64/256 = 0,25`, và Euclid trên `(64, 256)` cho
`256 = 4 × 64`, nên `64/256 = 1/4` — mẫu số `4`. Phép kiểm `2^4 mod 15 = 16
mod 15 = 1` xác nhận: `r = 4`. Hai đỉnh có tử số `k` chia sẻ ước với `r`
(`k = 0` và `k = 2`) cho một *ước* của `r` hoặc chẳng có gì, và phép kiểm
`a^r ≡ 1` bác bỏ chúng. Vì lẽ đó, phép kiểm cổ điển không phải một chi tiết
trang trí mà là bộ phận cấu thành của quy trình tìm chu kỳ.

**Mỗi lần chạy cho một đỉnh.** Phép đo trả về *một* kết quả duy nhất, lấy
mẫu từ bốn đỉnh xác suất `0.25` mỗi đỉnh. Một lần chạy có thể được `64` —
xong ngay trong một lượt. Có thể được `128`, ứng viên `r = 2` của nó thất
bại phép kiểm, hoặc `0`, chẳng nói gì. Đó là lý do Shor lặp phần lượng tử
vài lần: mỗi lần đo là một vé số trúng đỉnh, và chỉ những đỉnh với `k`
nguyên tố cùng nhau với `r` mới trả chu kỳ. Số lần chạy kỳ vọng là nhỏ và
không đổi; sự lặp lại ấy thuộc về thiết kế của thuật toán, không phải dấu
hiệu của sự thiếu tin cậy.

??? question "Tự kiểm tra — các đỉnh QFT *chứa* chu kỳ, vậy vì sao một phép đo không đưa thẳng nó ra?"
    Vì phép đo không cho thấy phân phối — nó lấy mẫu phân phối. Cả bốn đỉnh
    cùng nằm trong thanh ghi với xác suất `0.25` mỗi đỉnh, và đo sập thanh ghi
    về **một** trong số đó, ngẫu nhiên. Đọc `outcome/2^m` chỉ giúp khi kết quả
    rơi vào đỉnh có `k` nguyên tố cùng nhau với `r` (`64` hoặc `192` ở đây).
    Các kết quả khác cho chẳng có gì (`0`) hoặc một ước không qua được phép
    kiểm `a^r ≡ 1` (`128`). Lặp lại lần chạy và kết hợp với phép kiểm cổ
    điển, chu kỳ lộ ra sau vài lần.

## Ghép Shor lại

Từ đầu tới cuối cho mục tiêu demo `N = 15` — đúng những gì mô-đun `ch11.shor`
chạy, và mọi con số đều là những con số đã gặp ở trên. Đọc các bước nối tiếp
cho thấy phần nào của tiến trình là lượng tử: trong bảy giai đoạn dưới đây,
chỉ hai giai đoạn chạm vào qubit, và cả hai đều xoay quanh thanh ghi tuần
hoàn mà mạch tìm bậc sản sinh.

1. **Kiểm chẵn (cổ điển).** `15` lẻ, nên lối tắt không áp dụng — số `N` chẵn
   bị phân tích ngay tại chỗ: `shor(14) → 2 × 7`.
2. **Tiền xử lý (cổ điển).** Chọn `a = 2`; `gcd(2, 15) = 1` — không có thừa
   số miễn phí, và `2` dùng được.
3. **Dựng mạch tìm bậc (lượng tử).** Thanh ghi đếm `m = counting_width(15) = 8`
   qubit, thanh ghi công việc `4` qubit. Hadamard trải cả `256` số mũ; thanh
   ghi công việc khởi đầu ở `|1⟩`; các phép nhân có điều khiển với
   `2^(2^j) mod 15` ghi `f(x)` vào — chỉ có `j = 0` (× 2) và `j = 1` (× 4),
   vì `2^(2^2) = 16 ≡ 1` khiến phần còn lại là đồng nhất. Sự dừng này xảy ra
   vì nhân với `16` modulo `15` không thay đổi gì, nên mọi qubit điều khiển
   tiếp theo sẽ thực hiện phép tính để thanh ghi công việc bất động.
4. **QFT nghịch đảo (lượng tử).** Thanh ghi đếm tuần hoàn sập về bốn đỉnh
   `0, 64, 128, 192`.
5. **Đo và đọc chu kỳ (lượng tử + cổ điển).** Một kết quả, ví dụ `64`. Phân số
   liên tục: `64/256 = 1/4`, kiểm `2^4 mod 15 = 1` — chu kỳ `r = 4`. (Đo được
   `0` hoặc `128`? Đo lại.)
6. **Điều kiện loại (cổ điển).** `r = 4` chẵn, và `2^(r/2) mod 15 = 4`, không
   `≡ −1 = 14` — `a` này dùng được.
7. **Trích xuất (cổ điển).** `gcd(4 − 1, 15) = 3`, `gcd(4 + 1, 15) = 5`.
   Thừa số: **3 và 5**.

| Bước | Làm gì | Cổ điển hay lượng tử |
|---|---|---|
| Tiền xử lý | chọn `a`; `gcd(a, N) > 1` thì đã có thừa số | cổ điển |
| Hadamard | mọi số mũ cùng lúc | lượng tử |
| Nhân modular có điều khiển | ghi `a^x mod N` vào thanh ghi công việc | lượng tử |
| QFT nghịch đảo | biến chu kỳ thành các đỉnh | lượng tử |
| Đo | đọc một đỉnh | lượng tử |
| Phân số liên tục | khôi phục `r` từ đỉnh | cổ điển |
| Điều kiện loại và `gcd` | biến `r` thành các thừa số | cổ điển |

Cùng mã đó rồi phân tích `21`: `a = 2` có chu kỳ `r = 6`, `2^3 mod 21 = 8`, và
`gcd(7, 21) = 7`, `gcd(9, 21) = 3` → `21 = 3 × 7`. Một nếp nhăn trung thực
xuất hiện ở đó: `2^m / r = 1024/6 ≈ 170,7` không nguyên, nên các đỉnh loang
sang các kết quả lân cận (`171`, `341`, `683`, `853` thay vì các bội đúng) —
vẫn đủ gần để phân số liên tục khôi phục `1/6`, vậy là `r = 6`. Sự suýt soát
này mang tính minh hoạ: nó cho thấy quy trình chịu đựng được các đỉnh không
tròn trịa, miễn là phép khai triển phân số liên tục vẫn nhận ra phân số đã
định.

!!! warning "Nói thẳng về chi phí"
    Demo dừng ở `15` và `21`, và đó là giới hạn của *mô phỏng này*, không phải
    của thuật toán. Mỗi bit thêm vào `N` làm rộng cả hai thanh ghi, và ma trận
    phép nhân modular mô phỏng có `(2^width)²` phần tử: `15` tức thì, `21` mất
    vài giây, và `N` 30 bit đã ngoài tầm. Trên phần cứng thật, Shor là **đa
    thức** theo số bit, nhưng hằng số khổng lồ: một số 2048 bit cần hàng nghìn
    qubit *logic* và hàng triệu cổng, và mỗi qubit logic cần sửa lỗi (hàng
    nghìn qubit vật lý). Thuật toán phá mật mã khoá công khai hiện nay *về
    nguyên tắc*; chế tạo cỗ máy mới là phần khó, và các trang này không hứa
    quá mức.

??? question "Tự kiểm tra — mẫu semiclassic phân tích 15 và 21 không cần mạch lượng tử nào. Có phải chơi gian không?"
    Không — đó chính là điểm mấu chốt. Thuật toán Shor *hầu như cổ điển*:
    phép quy giản, các điều kiện loại, các phép `gcd`, kể cả phân số liên tục
    đều là số học thường. Bước lượng tử duy nhất là phép **tìm** chu kỳ.
    `semiclassic_factor` làm mọi thứ bằng cổ điển và ra cùng các thừa số —
    chỉ khác là nó thay bộ tìm chu kỳ lượng tử bằng vét cạn, và vì thế trên
    `N` lớn nó sẽ mất cả đời. Cặp demo (`semiclassic_factor` và `shor`) tồn tại
    chính để cho thấy máy lượng tử thay thế bước nào, và không bước nào khác.

## Các sơ đồ {#cac-so-do}

### Mốc cổ điển

![Chia thử cổ điển: công việc tăng như sqrt(n)](../assets/ch11-classical-factor.png){ width="620" }

Số phép chia thử theo `n` tới 120 — đường `steps_curve` của mô-đun. Gần như
phẳng ở đây; ở 600 chữ số, cùng đường cong đó cần cỡ `10^300` phép chia. Điểm
trực quan chính là sự tương phản về độ dốc: độ phẳng ở số `n` nhỏ khiến cú
bùng nổ về sau dễ bị đánh giá thấp, và đó chính là lý do khó khăn cổ điển
dễ bị bỏ qua.

![Chu kỳ của 2^x mod 15 là 4](../assets/ch11-period-function.png){ width="620" }

`2^x mod 15` với `x = 0 … 15`: nhịp bốn bước `1, 2, 4, 8` — con số mà toàn bộ
thuật toán được dựng để tìm. Mỗi lần giá trị `1` lặp lại đánh dấu một chu kỳ
hoàn tất, vì vậy nhìn thấy nhịp bằng mắt tương đương với việc tự tính chu kỳ.

### Biến đổi Fourier lượng tử

![Mạch QFT ba qubit](../assets/ch11-qft-circuit.png){ width="620" }

Một Hadamard mỗi qubit cộng một cổng pha có điều khiển cho mỗi cặp — mạch nhỏ
so với lượng toán học nó chở. Sự ngắn gọn đáng chú ý: toàn bộ cơ chế Fourier
quy về giao thoa có điều khiển giữa các cặp dây.

![QFT|1>: độ lớn đều, dốc pha tuyến tính](../assets/ch11-qft-phase.png){ width="620" }

`QFT|1⟩` trên ba qubit: mọi đầu ra độ lớn `1/√8`, pha leo `π/4` mỗi bước
(gập lại sau `π`). Độ lớn đứng im làm rõ rằng biến đổi tác động lên pha
tương đối chứ không lên biên độ, khi đầu vào là một trạng thái cơ sở.

### Tìm bậc

![Một mạch tìm bậc gọn](../assets/ch11-order-circuit.png){ width="620" }

Thanh ghi đếm phía trên, thanh ghi công việc phía dưới: Hadamard, hai phép
nhân modular có điều khiển (× 2 và × 4), rồi QFT nghịch đảo. Chỉ hai phép
nhân phụ thuộc vào lựa chọn `N` và `a`; phần còn lại của mạch là chung.

![QFT nghịch đảo của thanh ghi tuần hoàn: bốn đỉnh](../assets/ch11-order-peaks.png){ width="620" }

Thanh ghi đếm sau QFT nghịch đảo: bốn đỉnh tại `0, 64, 128, 192`, mỗi đỉnh
xác suất `0.25` — chu kỳ `4` dưới dạng đỉnh. Đọc bất kỳ đỉnh nào thành phân
số của `256` đều cho ra một phân số mà mẫu số của nó là một ước của
`4`, và đó chính là điểm mà bước phân số liên tục khai thác.

## Những điều cần nhớ

- Phân tích thừa số quan trọng vì mật mã kiểu RSA dựa vào việc nó khó: sinh
  khoá là nhân hai số nguyên tố, phá khoá là phải tìm lại chúng, nên an toàn
  của cả sơ đồ quy về độ khó duy nhất của một bài toán số học. Chia thử tốn
  khoảng `√N`: 500 phép cho số nguyên tố 6 chữ số `999983`, 500 000 phép cho
  số 12 chữ số `999999999989` — gấp đôi chữ số, nghìn lần công việc.
- Phép quy giản của Shor: chu kỳ `r` của `a^x mod N` cho các thừa số qua
  `gcd(a^(r/2) − 1, N)` và `gcd(a^(r/2) + 1, N)`, vì `N` chia hết
  `a^r − 1 = (a^(r/2) − 1)(a^(r/2) + 1)` và xẻ đôi giữa hai ngoặc. Thử lại
  với `a` khác nếu `r` lẻ hoặc `a^(r/2) ≡ −1`, vì trong cả hai trường hợp
  đó, hai ngoặc không đủ sức mang sự xẻ đôi theo.
- **QFT** là "đếm một mẫu lặp lại bao lâu một lần": một thanh ghi tuần hoàn
  với chu kỳ `r` biến thành các **đỉnh** nhọn tại các bội của `2^m / r` —
  giao thoa cộng tại các đỉnh, triệt tiêu ở nơi khác. Biến đổi nhờ đó dời
  chu kỳ từ mẫu biên độ sang các kết quả đo.
- **Tìm bậc** dựng mọi số mũ cùng lúc bằng Hadamard, ghi `a^x mod N` vào
  thanh ghi công việc bằng phép nhân có điều khiển, rồi đọc chu kỳ từ các
  đỉnh của QFT nghịch đảo. Mỗi phép đo cho một đỉnh, nên vài lần lặp là phần
  thiết kế, không phải thất bại.
- Khôi phục `r` từ đỉnh là cổ điển: phân số liên tục của `outcome / 2^m`, kiểm
  bằng `a^r ≡ 1 (mod N)`. Điều kiện loại và `gcd` cũng cổ điển — chỉ riêng
  phép *tìm* chu kỳ là lượng tử, vì vậy các biến thể mô phỏng cổ điển tái tạo
  lại được mọi con số trong chương này.
- Demo dừng ở `15` và `21` vì mô phỏng mạch luỹ thừa modular bùng nổ; Shor
  thật là đa thức nhưng cần phần cứng sửa lỗi đo bằng hàng nghìn qubit logic.

## Mã nguồn của chương này

Ba mẫu, từ mốc cổ điển tới thuật toán — ba mẫu này bao phủ đúng ba lớp của
chương: phép số học cổ điển, biến đổi Fourier, và cả thuật toán hoàn chỉnh:

- [`ch11/classical.py`](https://github.com/phonhay103/quantum-computing-in-action/blob/main/src/quantum_computing_in_action/ch11/classical.py)
  — hai mẫu ``classicfactor`` và ``semiclassicfactor``: chia thử, phép quy giản,
  `gcd(a^(r/2) ± 1, N)`, và phép tìm chu kỳ cổ điển.
- [`ch11/qft.py`](https://github.com/phonhay103/quantum-computing-in-action/blob/main/src/quantum_computing_in_action/ch11/qft.py)
  — biến đổi Fourier lượng tử: mạch, ma trận, và dốc pha mà nó đặt lên `|1⟩`.
- [`ch11/shor.py`](https://github.com/phonhay103/quantum-computing-in-action/blob/main/src/quantum_computing_in_action/ch11/shor.py)
  — mẫu ``quantumfactor``: nhân modular, mạch tìm bậc, QFT nghịch đảo, phân số liên
  tục, và các thừa số của 15 và 21.

Chạy toàn bộ bằng `make ch11`, hoặc từng mẫu một:

```bash
uv run python -m quantum_computing_in_action.ch11.shor
```
