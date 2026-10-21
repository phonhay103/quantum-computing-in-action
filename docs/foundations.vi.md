# Kiến thức nền

Ghi chú này chỉ giả định người đọc đã nắm được một chút đại số tuyến tính và
không đòi hỏi kiến thức nào trước đó về cơ học lượng tử. Trang này tập hợp số
nhỏ các ý tưởng nền tảng mà mọi chương đều dựa vào: bit và qubit, biên độ và xác
suất, pha số phức, vector và cổng unita, mô hình mạch, các cơ sở đo, và phần số
học đằng sau hàm tuần hoàn. Nên đọc trang này lướt một lần khi bắt đầu, rồi quay
lại tra cứu mỗi khi một chương dùng tới một thuật ngữ mà người đọc chưa nhận ra
ngay.

Mọi thuật ngữ được nêu ở đây đều có mục riêng trong bảng
**[Thuật ngữ](glossary.md)**, kèm tiếng Anh tương ứng; nhờ vậy bảng này vừa là
tài liệu tra cứu nhanh, vừa là chỉ mục song ngữ cho vốn từ được sử dụng xuyên
suốt cuốn sách.

## Bit, qubit và ký hiệu Dirac

**Bit** cổ điển là một đại lượng luôn có giá trị `0` hoặc `1`; tại mọi thời
điểm, bit chỉ giữ đúng một trong hai giá trị này chứ không gì ở giữa. Bit lượng
tử — **qubit** — khác biệt ở đúng điểm đó: nó có thể được chuẩn bị, hoặc tiến
hóa thành, *tổ hợp* của cả hai giá trị cổ điển cùng một lúc. Trạng thái của nó
được viết là

$$|\psi\rangle = \alpha\,|0\rangle + \beta\,|1\rangle$$

Các ký hiệu `|0⟩` và `|1⟩` là hai **trạng thái cơ sở**, đọc là "ket không" và
"ket một". Một ket như `|ψ⟩` chỉ là nhãn gắn cho một trạng thái; thông tin nằm ở
các con số đặt trước các trạng thái cơ sở. Nói cách khác, mọi ket chỉ là tên
gọi, còn các hệ số mới là thứ phân biệt trạng thái này với trạng thái khác.

## Biên độ, xác suất và quy tắc Born

Các số `α` và `β` là **biên độ**, không phải xác suất. Sự phân biệt này quan
trọng: biên độ có thể âm và thậm chí là số phức, trong khi xác suất luôn là một
số thực không âm. Để biến biên độ thành xác suất, người ta bình phương độ lớn
của chúng — **quy tắc Born**:

$$P(0) = |\alpha|^2, \qquad P(1) = |\beta|^2$$

Vì hai kết quả là đầy đủ — một phép đo chắc chắn cho ra một trong hai — tổng hai
xác suất phải bằng một, do đó các biên độ thoả mãn

$$|\alpha|^2 + |\beta|^2 = 1$$

Đây là điều kiện **chuẩn hoá**: nó phát biểu rằng trạng thái có "tổng trọng
số" bằng 1, nghĩa là xác suất được phân bổ trọn vẹn giữa hai kết quả có thể và
không bị mất đi phần nào.

## Số phức và pha

Biên độ là số phức, nên mỗi biên độ mang một **độ lớn** và một **pha**. Pha của
một biên độ riêng lẻ, xét độc lập, không quan sát được — nhân cả trạng thái với
`e^{iθ}` không thay đổi thống kê đo nào, nên vật lý mô tả vẫn là một. Thứ
*quan sát được* là **pha tương đối**: sự chênh lệch pha giữa hai phần của cùng
một trạng thái. Pha tương đối quyết định các biên độ cộng vào hay triệt tiêu
nhau như thế nào khi chúng được kết hợp — hiệu ứng gọi là **giao thoa**. Điều
này có nghĩa là giao thoa, chứ không phải pha tuyệt đối, mới là thứ mang hậu quả
đo được.

## Vector, ma trận và cổng unita

Trong cách nhìn vector của cơ học lượng tử, trạng thái một qubit là một
**vector cột** hai phần tử:

$$|\psi\rangle = \begin{bmatrix}\alpha\\ \beta\end{bmatrix}$$

Một **cổng** được biểu diễn bằng một ma trận nhân vào trạng thái; phép nhân này
biến trạng thái ban đầu thành trạng thái mới

$$|\psi'\rangle = U\,|\psi\rangle$$

Cổng lượng tử là **unita** (unitary): `U^† U = I`. Tính unita là lý do toán học
khiến một cổng khả nghịch — áp dụng cổng nghịch đảo sẽ xoá bỏ đúng hiệu ứng của
cổng ban đầu — và cũng bảo đảm cổng bảo toàn chuẩn hoá của trạng thái, nên kết
quả thu được vẫn là một phân phối xác suất hợp lệ.

## Nhiều qubit và tích tensor

Hai qubit không phải hai vector tách rời dán lại — trạng thái chung của chúng là
**tích tensor** của các trạng thái riêng, viết `|a⟩ ⊗ |b⟩` (hay `|a⟩|b⟩`). Vì
mỗi thành phần góp vào hai trạng thái cơ sở, tích tensor của hai trạng thái hai
chiều có tổng cộng bốn trạng thái cơ sở:

$$|00\rangle,\ |01\rangle,\ |10\rangle,\ |11\rangle$$

Nhãn đọc từ trái sang phải: `|01⟩` nghĩa là ký tự thứ nhất là `0`, ký tự thứ hai
là `1`. Giống như với một qubit, trạng thái chung là tổng có trọng số của bốn
trạng thái cơ sở này, và xác suất đo của mỗi kết quả là bình phương độ lớn của
biên độ tương ứng.

Trạng thái *có thể* viết thành tích tensor gọi là **trạng thái tích**; những
trạng thái loại này có thể được suy xét từng qubit một. Trạng thái không thể
viết theo cách đó gọi là **rối** (Chương 5), và sự rối tạo ra hành vi mà không
trạng thái tích nào tái hiện được.

## Mô hình mạch

Mạch lượng tử được đọc **từ trái sang phải**, cùng chiều với dòng chảy thời gian
của phép tính. Mỗi **dây** ngang là một qubit, mỗi **ô** trên dây là một cổng áp
dụng lên qubit đó, và **đồng hồ đo** ở cuối là phép đo tạo ra một bit cổ điển
làm kết quả. Chạy cùng một mạch nhiều lần gọi là lấy **shots**; các lần đếm số
kết quả thu được chính là thứ biểu đồ số lần đo thể hiện.

## Mặt cầu Bloch

**Mặt cầu Bloch** là hình học mô tả một qubit: mọi trạng thái có thể của một
qubit ứng với một điểm trên bề mặt mặt cầu. **Cực bắc** là `|0⟩` và **cực nam**
là `|1⟩`. **Đường xích đạo** chứa các trạng thái hỗn hợp đều 50/50. Mọi trạng
thái một qubit là một điểm trên mặt cầu, mô tả bởi hai góc `θ` và `φ`. Cần lưu
ý rằng mặt cầu chỉ dùng được cho một qubit — nó không mở rộng sang các trạng
thái rối, vốn không thể được đặt vào vị trí nào trên mặt cầu.

## Cơ sở đo

Một phép đo luôn được thực hiện **trong một cơ sở**, và một qubit chỉ mang một
bit xác định sau khi cơ sở được chốt; hỏi qubit có bit là gì mà không nêu cơ sở
là một câu hỏi không xác định. Mặc định là **cơ sở Z**, với các trạng thái `|0⟩`
và `|1⟩` — bit thông thường. Xoay cả hai trạng thái bằng một cổng Hadamard cho
**cơ sở X**, gồm `|+⟩ = (|0⟩ + |1⟩)/√2` và `|−⟩ = (|0⟩ − |1⟩)/√2`.

Quy tắc khiến cơ sở trở nên quan trọng rất ngắn: **đo một qubit trong đúng cơ sở
mà nó được chuẩn bị thì cho ra kết quả chắc chắn, còn đo trong cơ sở kia thì cho
ra kết quả như một đồng xu công bằng.** Về hình thức, `|⟨+|0⟩|² = ½` — hai cơ sở
cách nhau 45° trên mặt cầu Bloch, nên mỗi trạng thái của cơ sở này là hỗn hợp
đều của các trạng thái cơ sở kia. Kết quả là, phép đo trong cơ sở "sai" thực sự
không thể dự đoán. Đây chính là sự thật đứng sau
[Chương 8](chapters/ch08-secure-communication.md) về truyền thông an toàn: một
cơ sở là thứ mà một bit có thể nấp phía sau, và kẻ nghe lén đoán sai cơ sở sẽ
làm nhiễu trạng thái, nhờ đó có thể bị phát hiện.

## Hàm tuần hoàn và số học modular

`a mod N` là **số dư** còn lại khi chia `a` cho `N`: chẳng hạn
`17 mod 15 = 2`, và theo định nghĩa `a mod N` luôn nằm giữa `0` và `N − 1`. Hai
số **nguyên tố cùng nhau** khi ước chung duy nhất của chúng là 1, còn
`gcd(a, N)` — ước chung lớn nhất — được tính bằng thuật toán Euclid trong thời
gian `O(log N)`, tức là chỉ tăng theo logarit theo `N`.

**Dãy** `f(x) = a^x mod N` chính là thứ
[Chương 11](chapters/ch11-shors-algorithm.md) về thuật toán Shor đi tìm. Nó luôn
**tuần hoàn** khi `a` và `N` nguyên tố cùng nhau: sau một số bước `r` các giá
trị lặp lại y hệt, theo nghĩa `a^(x+r) = a^x mod N`, và `r` nhỏ nhất như vậy là
**bậc** của `a` modulo `N`. Với `a = 2`, `N = 15`, dãy chạy
`1, 2, 4, 8, 1, 2, 4, 8, …`, nên bậc là 4.

Tìm `r` đó là *tìm bậc*, và nó khó ngang với việc phân tích thừa số nếu làm cổ
điển. Mẹo khiến nó dễ trên máy lượng tử là **biến đổi Fourier**: một danh sách
giá trị tuần hoàn, khi bị biến đổi, biến thành vài **đỉnh** nhọn, và các đỉnh
nằm tại các bội của `1/r`. Đọc một đỉnh ngược lại thành phân số sẽ khôi phục
`r`, và `r` biến thành các thừa số của `N` chỉ với hai phép `gcd`. Nói cách
khác, phần tính toán lượng tử quy bài toán phân tích thừa số về bài toán tìm
chu kỳ, mà biến đổi Fourier giải quyết hiệu quả.

## Tốc độ tăng trưởng và Big-O

Nhịp độ tăng của một phép tính khi kích thước dữ liệu vào tăng lên được mô tả
bằng **ký hiệu Big-O**: `O(f)` nghĩa là "tăng không nhanh hơn `f`, bỏ qua hằng
số". Kiểu tăng trưởng được gọi là

- **đa thức** khi tăng như `b`, `b²`, `b³`, … — gấp đôi `b` chỉ nhân khối lượng
  công việc với một hằng số nhỏ, nên chi phí vẫn trong tầm kiểm soát khi dữ
  liệu vào phình to;
- **hàm mũ** khi tăng như `2^b`, `e^b`, … — thêm một bit có thể gấp đôi khối
  lượng công việc, đó là lý do khiến chi phí hàm mũ nhanh chóng trở nên không
  khả thi;
- **dưới hàm mũ** khi nằm giữa hai loại trên: nhanh hơn mọi đa thức nhưng chậm
  hơn một hàm mũ đầy đủ, tức là cải thiện so với chi phí vét cạn mà vẫn chưa
  đạt hiệu năng bậc đa thức.
