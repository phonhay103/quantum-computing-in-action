# Chương 9 — Deutsch và Deutsch–Jozsa

!!! abstract "Trong một câu"
    Nếu một hàm được hứa là **hằng số** hoặc **cân bằng**, một mạch lượng tử chỉ cần
    **một** lời gọi oracle là quyết định được — trong khi phép kiểm tra cổ điển
    muốn chắc chắn có thể cần tới `2^(n-1) + 1` lời gọi.

## Câu hỏi chương này trả lời

Hãy tưởng tượng một hộp đen tính hàm `f`, được trao kèm một điều kiện duy nhất
rất gắt: hộp không được phép mở ra hay kiểm tra dưới bất kỳ hình thức nào. Dạng
tương tác duy nhất được phép là đưa đầu vào vào và đọc đầu ra mà hộp trả về.
Chương này hỏi — và trả lời — ba câu hỏi về hộp đen đó:

1. **Mạch lượng tử "gọi" một hàm được kiểu gì?** Quy tắc được thiết lập ở Chương 7
   nói rằng mọi cổng lượng tử đều khả nghịch và không được làm mất thông tin —
   vậy mà một hàm như `AND` lại xoá đầu vào của nó, vì nhiều cặp đầu vào khác
   nhau rơi về cùng một đầu ra. Lời giải là **oracle**: một mạch khả nghịch *giữ
   nguyên* đầu vào và ghi câu trả lời lên một qubit dự phòng.
2. **Cần bao nhiêu lời gọi để biết một tính chất *toàn cục* của `f`?** Nếu `f`
   được hứa là **hằng số** (cùng một câu trả lời mọi nơi) hoặc **cân bằng** (hai
   câu trả lời khác nhau, mỗi cái một nửa), phép kiểm tra cổ điển có thể cần
   `2^(n-1) + 1` lời gọi mới *chắc chắn* về phán quyết. Nói cách khác, chi phí
   cổ điển tăng theo độ rộng của đầu vào. Mạch lượng tử của chương này chỉ cần
   **một** lời gọi, dù đầu vào rộng bao nhiêu.
3. **Lời gọi lượng tử duy nhất đó thực sự mang lại gì — và không mang lại gì?**
   Không phải `2^n` câu trả lời: một phép đo chỉ trả về đúng một kết quả. Nó cho
   một bit thông tin toàn cục về `f`, và **giao thoa** là cơ chế chưng cất bit đó
   ra khỏi chồng chập.

Làm qua chương này sẽ hình thành bốn năng lực:

- đọc quy tắc oracle `U_f : |x⟩|y⟩ → |x⟩|y ⊕ f(x)⟩` và giải thích `⊕` là *"hai bit
  có khác nhau không?"*;
- lần theo toàn bộ mạch Deutsch **bằng biên độ**, cho một hàm cân bằng và một hàm
  hằng số, và thấy mỗi dấu đến từ đâu;
- giải thích **phase kickback**: vì sao qubit dự phòng phải bắt đầu ở `|−⟩`, và
  giá trị `f(x)` di chuyển vào *dấu* của từng nhánh như thế nào;
- phát biểu phán quyết của Deutsch–Jozsa — toàn số không nghĩa là hằng số — và
  giới hạn cổ điển `2^(n-1) + 1` mà nó vượt qua.

Ba kết quả từ các chương trước được dùng xuyên suốt, và mỗi kết quả có thể phát
biểu trong một dòng: `H` đưa một qubit vào chồng chập đều 50/50
([Chương 4](ch04-superposition.md)); `CNOT` lật qubit đích khi điều khiển mang
giá trị `1` ([Chương 5](ch05-entanglement.md)); và mọi cổng lượng tử đều khả
nghịch, với **Toffoli** đóng vai trò bản `AND` khả nghịch
([Chương 7](ch07-helloworld-explained.md)).

!!! note "Một chút sổ sách: ký hiệu và thứ tự bit"
    Một nhãn như `01` luôn đọc **`q0` trước**, trái sang phải — thứ tự của sách,
    như ở [Chương 7](ch07-helloworld-explained.md). Vì mọi mạch dưới đây được đọc
    theo đúng quy ước này, đáng chốt nó ngay từ đầu, trước khi dây nào được xem
    xét. Ba ký hiệu dùng suốt chương:

    - `⊕` là **XOR**: *hai bit có khác nhau không?* `0⊕0 = 0`, `0⊕1 = 1`,
      `1⊕0 = 1`, `1⊕1 = 0` — phép cộng modulo 2.
    - `|−⟩ = (|0⟩ − |1⟩)/√2` là chồng chập *dấu trừ*: xác suất vẫn 50/50 như
      `|+⟩ = (|0⟩ + |1⟩)/√2`, nhưng hai nhánh mang **dấu** ngược nhau.
    - `(-1)^f(x)` là `+1` khi `f(x) = 0` và `-1` khi `f(x) = 1` — một dấu mà
      từng nhánh của chồng chập có thể mang.

## Mọi cổng đều khả nghịch

Một mạch lượng tử được dựng từ các cổng **khả nghịch**: một khi cổng đã được áp,
nó luôn có thể chạy ngược, và trạng thái gốc được lấy lại trọn vẹn. Ở đây tính
khả nghịch không phải là một sở thích trình bày mà là một tính chất cơ học — một
cổng khả nghịch chuyển toàn bộ thông tin đầu vào tới đầu ra, nên đầu vào luôn
có thể được dựng lại từ một mình đầu ra. Ràng buộc này đã nêu ở Chương 7; ở đây
nó trở thành quy tắc thiết kế của cả chương, nên đáng xem lại một lần với số
cụ thể.

Phép khả nghịch đơn giản nhất là cổng `X` áp hai lần:

![Hai cổng X](../assets/ch09-reversible-circuit.png){ width="360" }

$$|0\rangle \xrightarrow{\;X\;} |1\rangle \xrightarrow{\;X\;} |0\rangle$$

Một lần lật, rồi một lần lật nữa để hoàn tác. Hai phép toán triệt tiêu nhau
chính xác vì `X` không xoá gì: biết qubit đang mang `1` là biết chính xác nó
từng mang gì trước đó, cụ thể là `0`. Chạy mạch rồi đo: kết quả là `0` một cách
chắc chắn, ở mọi lần lặp. Kết quả không phụ thuộc vào số lần cặp cổng được áp
— hai cổng triệt tiêu nhau như một khối — và chính khả năng hoàn tác một phép
toán là điều mà mọi oracle về sau trong chương buộc phải đảm bảo.

Logic cổ điển thì không cẩn thận như vậy. Cổng `AND` nhận hai bit vào, trả một
bit ra:

| a | b | a AND b | |
|---|---|---|---|
| 0 | 0 | 0 | |
| 0 | 1 | 0 | ba đầu vào, một đầu ra |
| 1 | 0 | 0 | |
| 1 | 1 | 1 | |

Đọc ba dòng đầu cho thấy khó khăn: ba đầu vào *khác nhau* chia sẻ cùng đầu ra
`0`. Sau khi cổng chạy, đầu ra không còn chỉ ra đầu vào nào đã đi vào — thông
tin đã mất, và không mạch nào lấy lại được. Do đó `AND` không chạy ngược được,
và vì vậy mạch lượng tử không thể dùng nó. Nguyên nhân là sự xoá thông tin,
chứ không phải một bảng chân lý cụ thể: bất kỳ phép toán nào mà đầu ra không
còn xác định được đầu vào đều vứt bỏ thông tin theo cùng một cách.

??? question "Tự kiểm tra — `AND` bị cấm, vậy mà Chương 7 vẫn tính `a AND b` bằng cổng Toffoli. Vì sao lại được?"
    Việc này được cho phép vì Toffoli không vứt bỏ gì. Nó ghi `a AND b` lên qubit
    *thứ ba* và để `a` với `b` nguyên vị trí: `Toffoli(a, b, 0)` cho
    `(a, b, a AND b)`. Nhìn vào đầu ra có thể đọc ngay được đầu vào, nên phép
    toán chạy ngược được. Quy tắc không phải "cấm `AND` hoàn toàn" — mà là "cấm
    *xoá thông tin*". Trả thêm một qubit, giữ hết mọi thứ, và ngay cả `AND` cũng
    thành cổng lượng tử hợp lệ.

## Oracle: hộp đen khả nghịch

Một thuật toán lượng tử không bao giờ nhìn thấy hàm nó làm việc — nó nhìn thấy
một **oracle**: mạch khả nghịch đánh giá hàm đó. Oracle là giao diện giữa một hàm
thường và thế giới khả nghịch của các cổng lượng tử: bên trong, hàm được tính
như thường; ở biên giới, mọi dấu vết của phép tính đều được bảo toàn. Một hàm
*gọi được* trông ra sao khi buộc phải theo quy tắc "không được xoá gì"? Câu trả
lời được làm rõ ngay tại đây, trên hàm duy nhất có oracle chỉ gồm một cổng.

Lấy `f(x) = x` (một trong hai hàm cân bằng một bit). Oracle của nó là một
`CNOT`, với đầu vào `x` trên `q0` và thanh ghi dự phòng `y` trên `q1`:

![Một oracle cân bằng: một cổng CNOT](../assets/ch09-oracle-circuit.png){ width="420" }

Chạy nó trên cả bốn cặp đầu vào và theo dõi thanh dự phòng: bản ghi thu được
chính là bảng dưới đây. Quy tắc là `y ⊕ f(x)`, còn `⊕` trả lời một câu rất đời:
*hai bit có khác nhau không?*

| x | y | y ⊕ f(x) | chuyện gì xảy ra |
|---|---|---|---|
| 0 | 0 | 0 | `f(0) = 0`: thanh dự phòng đứng im |
| 0 | 1 | 1 | `f(0) = 0`: thanh dự phòng đứng im |
| 1 | 0 | 1 | `f(1) = 1`: thanh dự phòng bị lật |
| 1 | 1 | 0 | `f(1) = 1`: lật trở lại 0 |

Đầu vào `x` trở về nguyên vẹn ở mọi dòng; câu trả lời được gấp vào thanh dự
phòng. Chỉ *sau đó* quy tắc tổng quát mới được phát biểu:

$$U_f : |x\rangle\,|y\rangle \longrightarrow |x\rangle\,|y \oplus f(x)\rangle$$

Đặt `y = 0` thì thanh dự phòng giữ `f(x)`; đặt `y = 1` thì nó giữ `NOT f(x)`.
Trong cả hai cấu hình, không có gì bị xoá — hàm đã được đánh giá, và đồng thời
mọi đầu vào cũng được giữ lại, chính là sổ sách kép mà quy tắc lượng tử đòi hỏi.

Vì sao phép này khả nghịch? Vì XOR tự hoàn tác: `y ⊕ f(x) ⊕ f(x) = y`. Chạy cùng
oracle hai lần, thanh dự phòng về đúng giá trị ban đầu — oracle là nghịch đảo
của chính nó. Đó chính xác là điều quy tắc khả nghịch đòi hỏi, và là lý do `U_f`
là cổng lượng tử hợp lệ. Tính tự-đảo-nghịch này không phải ngẫu nhiên của hàm
được chọn ở đây: nó do chính cấu trúc XOR suy ra, và mọi oracle dựng trên cùng
quy tắc đều kế thừa nó.

## Bốn hàm một bit

Chỉ có bốn hàm một bit — hai câu trả lời qua hai đầu vào — và chúng chia thành
hai họ. Việc liệt kê gọn trong một bảng, và đáng làm, vì mọi lập luận trong
phần còn lại của chương dựa trên đúng danh sách này:

| Hàm | f(0) | f(1) | Loại | Mạch oracle |
|---|---|---|---|---|
| hằng 0 | 0 | 0 | hằng số | không làm gì |
| hằng 1 | 1 | 1 | hằng số | `X` lên `y` |
| cân bằng: `f(x) = x` | 0 | 1 | cân bằng | `CNOT(x, y)` |
| cân bằng: `f(x) = NOT x` | 1 | 0 | cân bằng | `X` lên `y`, rồi `CNOT(x, y)` |

![Bốn ma trận oracle](../assets/ch09-oracle-matrices.png){ width="620" }

Mỗi ma trận là một **ma trận hoán vị**: đúng một số `1` trên mỗi hàng và mỗi
cột, mọi ô khác `0`. Tính khả nghịch trông ra vậy dưới dạng ma trận — một cuộc
sắp xếp lại các trạng thái cơ sở mà không mất gì, nên luôn sắp lại được như cũ.

Hai họ khác nhau đúng một điểm: đầu vào có làm thay đổi câu trả lời không? Hàm
**hằng số** phớt lờ `x` hoàn toàn (`f(0) = f(1)`); hàm **cân bằng** trả lời khác
nhau trên `0` và trên `1` (`f(0) ≠ f(1)`). Câu hỏi đó — *"đầu vào có quan trọng
không?"* — đáng giữ trong đầu suốt chương, vì đó là toàn bộ điều mà các thuật
toán phía dưới thành công hỏi chỉ bằng một truy vấn. Đó là một câu hỏi *toàn cục* rõ rệt: nó
không hỏi giá trị của `f` tại đầu vào nào, chỉ hỏi hai giá trị có chuyển động
dồng loạt cùng nhau hay không.

## Chiêu thuật: phase kickback

Oracle ghi câu trả lời lên thanh dự phòng — nhưng cần lưu ý một điểm: nếu thanh
dự phòng ở `|0⟩` hay `|1⟩` thường trong khi đầu vào đang chồng chập, thì *đo*
thanh dự phòng để đọc câu trả lời sẽ phá vỡ chồng chập. Mạch Deutsch cần câu
trả lời hiện lên ở một nơi không làm sụp các nhánh. Chiêu là chuẩn bị qubit dự
phòng ở `|−⟩`, để cú lật của oracle biến thành một *dấu*.

Bắt đầu với sự thật nhỏ nhất, được kiểm chứng bằng phép nhân trực tiếp. `X`
hoán đổi `|0⟩` và `|1⟩`, nên áp lên `|−⟩`:

$$X\,|-\rangle = X\,\frac{|0\rangle - |1\rangle}{\sqrt{2}}
= \frac{|1\rangle - |0\rangle}{\sqrt{2}} = -\,\frac{|0\rangle - |1\rangle}{\sqrt{2}} = -\,|-\rangle$$

Lật cả hai nhánh của `|−⟩` thì kết quả vẫn là `|−⟩`, **nhân với trừ một**. Không
gì nhìn thấy được thay đổi — xác suất 50/50 vẫn thế — nhưng trạng thái nhận thêm
một dấu. Nói cách khác, cú lật không rời khỏi hệ lượng tử; nó được ghi lại ở
nơi duy nhất mà phép đo không thể huỷ hoại: pha tương đối.

Giờ oracle được áp lên `|x⟩|−⟩` với một `x` xác định. Oracle lật thanh dự phòng
đúng khi `f(x) = 1`, và một cú lật trên `|−⟩` là một phép nhân với `-1`:

- `f(x) = 0`: không lật, `|x⟩|−⟩ → |x⟩|−⟩` — dấu `(-1)^0 = +1`;
- `f(x) = 1`: một cú lật, `|x⟩|−⟩ → |x⟩·(-|−⟩) = -|x⟩|−⟩` — dấu `(-1)^1 = -1`.

$$U_f\,|x\rangle|-\rangle = (-1)^{f(x)}\,|x\rangle|-\rangle$$

Làm trên oracle cân bằng `f(x) = x` với đầu vào `1`: `CNOT` thấy `x = 1`, lật
thanh dự phòng, và `|1⟩|−⟩` ra thành `-|1⟩|−⟩`. Giá trị `f(1) = 1` không còn là
một bit nằm trên dây — nó đã *chuyển vào dấu* của nhánh. Đó là **phase
kickback**: câu trả lời bật ngược lên pha của thanh ghi đầu vào, nơi chồng chập
vẫn còn sống. Thông tin được di chuyển chứ không bị phá huỷ — được đặt ngay ở
nơi Hadamard cuối vẫn có thể chuyển thành một bit đọc được.

??? question "Tự kiểm tra — vì sao qubit dự phòng phải bắt đầu ở `|−⟩` mà không phải `|+⟩`?"
    Vì `X` làm hai việc khác nhau trên hai trạng thái đó. Trên `|−⟩`, một cú lật
    hiện lên thành dấu: `X|−⟩ = -|−⟩`, nên `f(x) = 1` để lại `(-1)^f(x)` nhìn
    thấy được trên nhánh. Trên `|+⟩`, cú lật tàng hình: `X|+⟩ = |+⟩` — hoán đổi
    `|0⟩` và `|1⟩` trong `(|0⟩ + |1⟩)/√2` thì nhận lại đúng trạng thái cũ, chẳng
    thêm gì. Với thanh dự phòng ở `|+⟩`, oracle tác động `|x⟩|+⟩ → |x⟩|+⟩` bất
    kể `f(x)` là `0` hay `1`, và không cổng nào về sau phân biệt nổi hai trường
    hợp. Cả thuật toán sống trong một dấu trừ ấy, và `|−⟩` là trạng thái duy
    nhất mang được nó.

## Thuật toán Deutsch

Bài toán Deutsch có dạng như sau: một trong bốn oracle trên được trao, niêm
phong, và câu hỏi duy nhất được đặt ra là *nó thuộc họ nào* — **hằng số** hay
**cân bằng**. Bản thân các giá trị `f(0)` và `f(1)` không bị yêu cầu; chỉ việc
chúng có bằng nhau hay không mới là điều quan trọng. Chỉ có họ — một tính chất
toàn cục của hàm — được đặt ra, và chính sự giới hạn này khiến một truy vấn
trở nên hữu nghĩa: câu hỏi đã được cắt gọn về đúng kích thước một bit. Chỉ phần bên trong của
oracle thay đổi giữa các bài toán; các phép toán bao quanh — chuẩn bị, chồng
chập, giao thoa, đo — giữ nguyên.

Về cổ điển, cả hai đầu vào buộc phải được xem xét: truy vấn `f(0)`, truy vấn
`f(1)`, rồi so sánh — hai lần tra cứu, không lối nào vòng qua được, vì một lời
gọi cổ điển chẳng tiết lộ gì về đầu vào còn lại. Về lượng tử, **một** truy vấn
là đủ, và phần lớn chương này dành để giải thích vì sao: cơ chế là giao thoa,
được chuyển qua một Hadamard cuối duy nhất.

![Mạch Deutsch](../assets/ch09-deutsch-circuit.png){ width="460" }

Mạch, từng cổng một, với `q0` là thanh ghi đầu vào và `q1` là thanh dự phòng:

1. `X(1)` — thanh dự phòng được đưa thành `|1⟩`;
2. `H(0), H(1)` — cả hai thanh ghi vào chồng chập, `q1` hạ xuống `|−⟩`;
3. oracle — **một** lần đánh giá `f`, trên cả hai đầu vào cùng lúc;
4. `H(0)` — hai nhánh được cho giao thoa với nhau;
5. đo `q0`.

### Trường hợp cân bằng, `f(x) = x`, bằng biên độ

Mọi thanh ghi bắt đầu ở `|0⟩`, nên trạng thái hai qubit là `|00⟩`. Từng bước
giờ được lần theo chi tiết — đây là chính xác các biên độ mà simulator báo cáo:

**Bước 1 — `X(1)`.** Thanh dự phòng lật: `q1 = 1`, đầu vào không bị chạm tới.

$$|00\rangle \;\xrightarrow{\;X(1)\;}\; |0\rangle|1\rangle$$

**Bước 2 — `H(0), H(1)`.** `q0` thành `|+⟩`, còn `q1` — một `|1⟩` qua Hadamard —
thành `|−⟩`:

$$|0\rangle|1\rangle \;\xrightarrow{\;H,H\;}\;
\frac{|0\rangle + |1\rangle}{\sqrt{2}} \otimes \frac{|0\rangle - |1\rangle}{\sqrt{2}}
\;=\; \tfrac{1}{2}\left(|00\rangle - |01\rangle + |10\rangle - |11\rangle\right)$$

Bốn trạng thái cơ sở, biên độ mỗi cái `±1/2`, xác suất mỗi cái `1/4`. Hai nhánh
của `q0` là cặp `|0…⟩` và cặp `|1…⟩`. Ở thời điểm này oracle chưa tác động: cả
hai giá trị đầu vào cùng lúc hiện diện, chờ bước 3 đánh dấu chúng.

**Bước 3 — oracle (ở đây là một `CNOT`).** Nó tác động lên từng nhánh một, XOR
`f(x)` vào thanh dự phòng: `|00⟩→|00⟩`, `|01⟩→|01⟩`, `|10⟩→|11⟩`,
`|11⟩→|10⟩`:

$$\tfrac{1}{2}\left(|00\rangle - |01\rangle + |10\rangle - |11\rangle\right)
\;\xrightarrow{\;U_f\;}\;
\tfrac{1}{2}\left(|00\rangle - |01\rangle - |10\rangle + |11\rangle\right)$$

Gom các số hạng lại thì kickback hiện rõ: trạng thái giờ là

$$\frac{|0\rangle - |1\rangle}{\sqrt{2}} \otimes |-\rangle$$

Thanh ghi `q0` — vốn là `|+⟩` — giờ là `|−⟩`. Nhánh `x = 0` mang
`(-1)^f(0) = +1` và nhánh `x = 1` mang `(-1)^f(1) = -1`; *dấu* của thanh ghi đầu
vào giờ chính là câu trả lời của hàm.

**Bước 4 — `H(0)`.** Hadamard biến khác biệt dấu thành khác biệt bit:
`H|+⟩ = |0⟩` và `H|−⟩ = |1⟩`:

$$\frac{|0\rangle - |1\rangle}{\sqrt{2}} \otimes |-\rangle
\;\xrightarrow{\;H(0)\;}\; |1\rangle \otimes |-\rangle$$

**Bước 5 — đo `q0`:** nó đọc `1` với xác suất 1.00. Phán quyết: **cân bằng**,
sau một truy vấn.

### Trường hợp hằng 0, bằng biên độ

Cùng khởi đầu, hai bước đầu y hệt — trạng thái sau bước 2 không đổi. Nhưng
oracle hằng 0 là mạch rỗng, nên bước 3 không thay đổi gì:

$$\tfrac{1}{2}\left(|00\rangle - |01\rangle + |10\rangle - |11\rangle\right)
\;\xrightarrow{\;U_f\;}\;
\tfrac{1}{2}\left(|00\rangle - |01\rangle + |10\rangle - |11\rangle\right)$$

Hai nhánh của `q0` vẫn mang `+1 = (-1)^f(0) = (-1)^f(1)` — hai dấu khớp nhau.
Bước 4 cho `H|+⟩ = |0⟩`, nên trạng thái thành `|0⟩ ⊗ |−⟩`, và phép đo đọc `0`
với xác suất 1.00. Phán quyết: **hằng số**. Chuẩn bị là như hệt nhau trong hai
lượt chạy, nên thứ tách hai họ phải đến từ phần đóng góp của oracle ở bước 3 —
mà với hằng 0 phần đóng góp đó là không gì cả.

Hai hàm còn lại hành xử y như họ của chúng:

- **hằng 1** — oracle là một `X` trên thanh dự phòng, biến `|−⟩` thành `-|−⟩`.
  Mọi nhánh lật dấu, nên cả trạng thái được nhân với `-1`. Đó là pha *toàn cục*
  — vô hình với mọi phép đo — và sau `H(0)` cuối, qubit vẫn đọc `0`.
- **`f(x) = NOT x`** — nhánh `x = 0` lật dấu (vì `f(0) = 1`), nhánh `x = 1`
  thì không. Trạng thái sau oracle là `-|−⟩ ⊗ |−⟩` — giống hệt trường hợp cân
  bằng trừ một dấu toàn cục tàng hình — và phép đo đọc `1`.

| Hàm | f(0) | f(1) | Dấu hai nhánh | q0 đo được | Kết luận |
|---|---|---|---|---|---|
| hằng 0 | 0 | 0 | `+1, +1` | 0 | hằng số |
| hằng 1 | 1 | 1 | `-1, -1` | 0 | hằng số |
| f(x) = x | 0 | 1 | `+1, -1` | 1 | cân bằng |
| f(x) = NOT x | 1 | 0 | `-1, +1` | 1 | cân bằng |

![Một truy vấn: hằng số đo 0, cân bằng đo 1](../assets/ch09-deutsch-outcomes.png){ width="620" }

**Vì sao hiệu quả, bằng lời.** Oracle không trao đi các *giá trị* của `f` — nó
trao đi các *dấu* của chúng, mỗi nhánh một dấu, nhờ thanh dự phòng `|−⟩`. Dấu
bằng nhau (hằng số) nghĩa là hai nhánh vẫn giao thoa như `|+⟩` từng giao thoa,
và `q0` trở về `|0⟩`. Dấu ngược nhau (cân bằng) nghĩa là hai nhánh giao thoa
*theo chiều ngược lại*, đúng như `|−⟩` từng giao thoa, và `q0` kết thúc ở
`|1⟩`. Hadamard cuối là người phiên dịch: nó biến khác biệt dấu — thứ không
phép đo nào đọc trực tiếp được — thành khác biệt bit, thứ một phép đo chốt được
chắc chắn.

??? question "Tự kiểm tra — hằng 1 nhân cả trạng thái với `-1`. Vì sao phép đo không nhận ra?"
    Một dấu đứng trước toàn bộ trạng thái là một **pha toàn cục**: mọi kết quả
    đo khả dĩ đều được nhân cùng một `-1`, và xác suất dùng `|biên độ|²`, thứ
    xoá sạch nó. `|-0⟩` và `|0⟩` đo như nhau. Cái phép đo *có thể* nhận ra là
    dấu *tương đối* — một nhánh âm, một nhánh dương — vì khi đó các nhánh triệt
    tiêu hay cộng cường cho nhau khi gặp nhau ở Hadamard cuối. Hàm hằng số chỉ
    tạo ra dấu toàn cục; chỉ hàm cân bằng mới đặt được `+1` lên nhánh này và
    `-1` lên nhánh kia. Đúng là ranh giới mà thuật toán vạch ra.

## Deutsch–Jozsa: một truy vấn cho mọi `n`

Bản tổng quát mở rộng đầu vào: `f : {0,1}^n → {0,1}`, vẫn niêm phong trong
oracle, vẫn kèm lời hứa — **hằng số** (cùng một câu trả lời trên cả `2^n` đầu
vào) hoặc **cân bằng** (`0` trên đúng một nửa, `1` trên nửa còn lại). Mạch là
Lời hứa rộng hơn về scale nhưng không khác về bản chất: hằng số vẫn là một câu
trả lời mọi nơi, cân bằng vẫn là chia 50/50 — giờ trên `2^n` đầu vào thay vì
hai. Mạch là mạch Deutsch với nhiều dây hơn:

![Deutsch–Jozsa cho n = 3](../assets/ch09-dj-circuit.png){ width="620" }

1. `X` lên ancilla (thanh ghi dự phòng, chỉ số `n`); `H` lên cả `n + 1` qubit;
2. oracle được chạy **một lần** — trên cả `2^n` đầu vào cùng lúc;
3. `H` lên `n` qubit đầu vào;
4. đo thanh ghi đầu vào.

### Một trường hợp cụ thể: `n = 2`, hằng số đối cân bằng

Lấy `n = 2`, thanh ghi đầu vào giữ `q0 q1`, ancilla là `q2`. Trường hợp này nhỏ
đủ để lần bằng tay, và phép tính tay khớp chính xác với simulator. Sau bước 1,
thanh ghi đầu vào là chồng chập đều của cả bốn đầu vào và ancilla ở `|−⟩` — tách
thành thừa số, trạng thái là

$$\frac{1}{2}\left(|00\rangle + |01\rangle + |10\rangle + |11\rangle\right) \otimes |-\rangle$$

Mỗi nhánh đầu vào có biên độ `1/2`. Với hàm cân bằng, các dấu đến đều nhau —
đúng nửa `+1`, đúng nửa `-1` — một cách phát biểu lại lời hứa, thứ sẽ quan
trọng trực tiếp khi các dấu được cộng lại. Giờ đến oracle, và câu trả lời hạ
cánh vào dấu của các nhánh `(-1)^f(x)`:

- **hằng 0** — không có gì xảy ra; cả bốn dấu giữ `+1`:

  $$\frac{1}{2}\left(|00\rangle + |01\rangle + |10\rangle + |11\rangle\right) \otimes |-\rangle$$

- **cân bằng, hàm chẵn lẻ** `f(x) = q0 ⊕ q1` — với `f(00) = 0`, `f(01) = 1`,
  `f(10) = 1`, `f(11) = 0`, các dấu thành `+1, -1, -1, +1`:

  $$\frac{1}{2}\left(|00\rangle - |01\rangle - |10\rangle + |11\rangle\right) \otimes |-\rangle$$

Bước 3 áp `H` lên cả hai qubit đầu vào, và mỗi nhánh đóng góp vào mọi kết quả
kèm theo dấu. Biên độ của kết quả toàn số không `|00⟩` là **tổng các dấu của
các nhánh**, có scaling:

$$\text{biên độ của } |00\rangle \;=\; \frac{1}{2^n} \sum_x (-1)^{f(x)}$$

Tính nó bằng các số ở trên:

- **hằng số**: `(1/4)(+1 +1 +1 +1) = 4/4 = 1` → `P(00) = 1`. (Hằng 1 cho
  `(1/4)(-1 -1 -1 -1) = -1` — biên độ `-1`, xác suất vẫn 1.)
- **cân bằng**: `(1/4)(+1 -1 -1 +1) = 0` → `P(00) = 0`.

Và simulator đồng ý: oracle hằng số đo `00` với xác suất 1.00, còn oracle chẵn
lẻ đo `11` với xác suất 1.00 và **không bao giờ** `00`. Quy tắc phán quyết, cho
mọi `n`:

> **Toàn số không nghĩa là hằng số; bất kỳ thứ gì khác nghĩa là cân bằng.**

| n | Oracle | P(0…0) | Kết luận | Cổ điển xấu nhất |
|---|---|---|---|---|
| 1 | hằng 0 | 1.00 | hằng số | 2 |
| 1 | hằng 1 | 1.00 | hằng số | 2 |
| 1 | cân bằng | 0.00 | cân bằng | 2 |
| 2 | hằng 0 | 1.00 | hằng số | 3 |
| 2 | hằng 1 | 1.00 | hằng số | 3 |
| 2 | cân bằng | 0.00 | cân bằng | 3 |
| 3 | hằng 0 | 1.00 | hằng số | 5 |
| 3 | hằng 1 | 1.00 | hằng số | 5 |
| 3 | cân bằng | 0.00 | cân bằng | 5 |

![n = 2: oracle hằng số trả về 00, oracle cân bằng thì không bao giờ](../assets/ch09-dj-outcomes.png){ width="620" }

### Chi phí cổ điển, bằng lời

Vì sao phép kiểm tra cổ điển có thể cần `2^(n-1) + 1` lời gọi? Vì hàm cân bằng
được phép đồng ý với hàm hằng số một khoảng *dài*: nó trả `0` trên đúng một nửa
đầu vào, nên có thể nói cùng một chuyện suốt `2^(n-1)` lời gọi liên tiếp mà vẫn
cân bằng. Ngay khi hai câu trả lời *khác nhau* xuất hiện, vấn đề được chốt —
hàm đó cân bằng. Nhưng muốn kết luận **hằng số**, các truy vấn phải tiếp tục cho
đến khi hơn một nửa số đầu vào đã đồng ý: sau `2^(n-1) + 1` câu trả lời giống
nhau, hàm cân bằng hết chỗ nấp, vì nửa đồng ý của nó chỉ gồm `2^(n-1)` đầu vào.
Một nửa, rồi thêm một: hoặc lời gọi thêm đó tìm ra chỗ bất đồng, hoặc nó loại
trừ hẳn trường hợp cân bằng. Nói cách khác, giới hạn cổ điển không phải hình
phạt cho sự bất cẩn; nó là giá chính xác của việc đòi một phán quyết *chắc
chắn* dựa trên lời hứa. Với `n = 1, 2, 3` đó là `2, 3, 5` lời gọi — và với
`n = 10` đã là `513`. Chi phí lượng tử vẫn giữ ở **một** truy vấn, dù đầu vào
rộng đến đâu.

!!! note "Song song lượng tử, và điều nó không phải"
    Oracle thật sự đánh giá `f` trên cả `2^n` đầu vào trong một lượt — đó là
    **song song lượng tử**. Nhưng không thể đọc hết các giá trị đó ra: một phép
    đo chỉ trả về một trạng thái cơ sở. Thứ mạch trích ra không phải các câu
    trả lời riêng lẻ, mà là một bit **toàn cục** về `f` (ở đây là tính hằng số
    của nó). Giao thoa là thứ biến việc đánh giá song song thành bit đó, và đó
    là lý do các tăng tốc lượng tử nói về *câu hỏi*, không phải về việc tính
    mọi thứ cùng lúc.

??? question "Tự kiểm tra — oracle đã đánh giá `f` trên cả `2^n` đầu vào. Vì sao phép đo không trao cho bạn cả `2^n` câu trả lời?"
    Vì một phép đo chỉ trả về **một** trạng thái cơ sở, lấy mẫu theo các xác suất
    — đọc thanh ghi phá vỡ chồng chập, và thông tin của các nhánh còn lại chết
    theo. Thuật toán không bao giờ cố đọc từng câu trả lời. Thay vào đó, các
    Hadamard cuối cho cả `2^n` nhánh *bầu chọn* cùng một kết quả — `|0…0⟩` — và
    tổng số phiếu (`2^n` cho hằng số, `0` cho cân bằng) là một tính chất của `f`
    như một tổng thể. Một truy vấn mua một bit toàn cục, không phải `2^n` bit
    cục bộ; tăng tốc hiệu quả được vì câu hỏi cũng chỉ cần đúng một bit đó.

## Các sơ đồ {#cac-so-do}

### Tính khả nghịch

![Hai cổng X](../assets/ch09-reversible-circuit.png){ width="360" }

`X` hai lần đưa qubit về `|0⟩` một cách chắc chắn: mạch nhỏ nhất tự hoàn tác,
và cũng là quy tắc mà mọi oracle phải tuân theo.

### Oracle

![Một oracle cân bằng: một cổng CNOT](../assets/ch09-oracle-circuit.png){ width="420" }

Oracle cho `f(x) = x`: đầu vào `x` trên `q0`, thanh dự phòng `y` trên `q1`, một
`CNOT`.

![Bốn ma trận oracle](../assets/ch09-oracle-matrices.png){ width="620" }

Bốn ma trận hoán vị — một số `1` mỗi hàng, mỗi cột. Oracle hằng số không sắp
xếp lại gì (hoặc chỉ hoán đổi trong thanh dự phòng); oracle cân bằng hoán đổi
theo giá trị đầu vào.

### Deutsch

![Mạch Deutsch](../assets/ch09-deutsch-circuit.png){ width="460" }

`X(1)` chuẩn bị thanh dự phòng, các Hadamard tạo `|+⟩|−⟩`, oracle đá dấu ngược
lên `q0`, và `H(0)` cuối đọc dấu đó ra.

![Một truy vấn: hằng số đo 0, cân bằng đo 1](../assets/ch09-deutsch-outcomes.png){ width="620" }

P(q0 = 1) của bốn hàm một bit: đúng bằng 0 cho cả hai hàm hằng số, đúng bằng 1
cho cả hai hàm cân bằng.

### Deutsch–Jozsa

![Deutsch–Jozsa cho n = 3](../assets/ch09-dj-circuit.png){ width="620" }

Cùng một mạch, rộng ba dây đầu vào: Hadamard, một lượt oracle, Hadamard lên
thanh ghi đầu vào.

![n = 2: oracle hằng số trả về 00, oracle cân bằng thì không bao giờ](../assets/ch09-dj-outcomes.png){ width="620" }

Phân phối đo với `n = 2`: oracle hằng số trả `00`; oracle chẵn lẻ trả `11` — và
`00` là bất khả thi. Kết quả toàn số không là then chốt của phán quyết, vì
vậy toàn bộ phép thử có thể phát biểu chỉ dựa trên nó.

## Những điều cần nhớ

- Mọi cổng lượng tử đều **khả nghịch**; `AND`, thứ xoá đầu vào, bị cấm. Bản thay
  thế khả nghịch là cổng **Toffoli**: trả thêm một qubit, giữ nguyên đầu vào, và
  phép toán chạy ngược được.
- Một **oracle** đánh giá hàm mà không xoá gì:
  `U_f : |x⟩|y⟩ → |x⟩|y ⊕ f(x)⟩`, với `⊕` nghĩa là *hai bit có khác nhau không?*.
  Nó là nghịch đảo của chính nó, nên là cổng lượng tử hợp lệ.
- Hàm một bit là **hằng số** (`f(0) = f(1)`) hoặc **cân bằng** (`f(0) ≠ f(1)`);
  có bốn hàm như vậy, mỗi hàm một oracle một cổng.
- **Phase kickback**: với thanh dự phòng ở `|−⟩`, cú lật của oracle thành một
  dấu, `U_f|x⟩|−⟩ = (-1)^f(x)|x⟩|−⟩` — giá trị của `f` chuyển vào pha. Với thanh
  dự phòng ở `|+⟩`, cú lật tàng hình, không gì trích ra được.
- **Deutsch** đọc dấu đó bằng một Hadamard cuối: dấu bằng nhau (hằng số) đo `0`,
  dấu ngược nhau (cân bằng) đo `1` — một truy vấn, chắc chắn.
- **Deutsch–Jozsa** mở rộng sang `n` bit: biên độ của `|0…0⟩` là
  `(1/2^n) Σ_x (-1)^f(x)` — `±1` cho hằng số, `0` cho cân bằng — nên *toàn số
  không nghĩa là hằng số*, và một truy vấn chốt được điều mà kiểm tra cổ điển có
  thể cần `2^(n-1) + 1`.
- Thuật toán không đọc `2^n` câu trả lời; nó trích ra một bit **toàn cục** —
  *đầu vào có quan trọng gì không?* — nhờ giao thoa.

## Mã nguồn của chương này

Bốn mẫu, đi từ quy tắc nền tới thuật toán hoàn chỉnh:

- [`ch09/reversible.py`](https://github.com/phonhay103/quantum-computing-in-action/blob/main/src/quantum_computing_in_action/ch09/reversible.py)
  — mẫu ``reversibleX``: `X·X = I`, và vì sao `AND` không thể làm oracle.
- [`ch09/oracles.py`](https://github.com/phonhay103/quantum-computing-in-action/blob/main/src/quantum_computing_in_action/ch09/oracles.py)
  — bốn hàm một bit, mạch oracle và ma trận của chúng, cùng các oracle `n` bit
  cho Deutsch–Jozsa.
- [`ch09/deutsch.py`](https://github.com/phonhay103/quantum-computing-in-action/blob/main/src/quantum_computing_in_action/ch09/deutsch.py)
  — mạch Deutsch, lần theo bằng biên độ, và phép phân loại một truy vấn của nó.
- [`ch09/deutschjozsa.py`](https://github.com/phonhay103/quantum-computing-in-action/blob/main/src/quantum_computing_in_action/ch09/deutschjozsa.py)
  — thuật toán tổng quát, phép thử toàn số không, và so sánh cổ điển.

Chạy toàn bộ bằng `make ch09`, hoặc từng mẫu một:

```bash
uv run python -m quantum_computing_in_action.ch09.deutschjozsa
```
