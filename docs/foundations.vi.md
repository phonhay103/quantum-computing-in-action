# Kiến thức nền

Ghi chú này giả định bạn đọc được một chút đại số tuyến tính và còn mới với cơ
học lượng tử. Trang này gom các ý tưởng nền nhỏ mà mọi chương đều dựa vào. Đọc
lướt một lần, rồi quay lại mỗi khi một chương dùng thuật ngữ bạn chưa nhận ra.

Mọi thuật ngữ ở đây đều có mục trong bảng **[Thuật ngữ](glossary.md)**, kèm
tiếng Anh tương ứng.

## Bit, qubit và ký hiệu Dirac

**Bit** cổ điển là `0` hoặc `1`. Bit lượng tử — **qubit** — còn có thể là *tổ hợp*
của cả hai. Ta viết trạng thái của nó là

$$|\psi\rangle = \alpha\,|0\rangle + \beta\,|1\rangle$$

Ký hiệu `|0⟩` và `|1⟩` là hai **trạng thái cơ sở**, đọc là "ket không" và "ket
một". Một ket như `|ψ⟩` chỉ là nhãn của một trạng thái; thông tin nằm ở các con số
đặt trước các trạng thái cơ sở.

## Biên độ, xác suất và quy tắc Born

Các số `α` và `β` là **biên độ**, không phải xác suất. Chúng có thể âm và thậm chí
là số phức. Để biến chúng thành xác suất, bạn bình phương độ lớn của chúng — **quy
tắc Born**:

$$P(0) = |\alpha|^2, \qquad P(1) = |\beta|^2$$

Vì hai kết quả là đầy đủ, các biên độ thoả mãn

$$|\alpha|^2 + |\beta|^2 = 1$$

Đây là điều kiện **chuẩn hoá**: nói rằng trạng thái có "tổng trọng số" bằng 1.

## Số phức và pha

Biên độ là số phức, nên mỗi biên độ mang một **độ lớn** và một **pha**. Pha của
một biên độ riêng lẻ không quan sát được — nhân cả trạng thái với `e^{iθ}` vẫn mô
tả cùng một vật lý. Thứ *quan sát được* là **pha tương đối**: sự chênh lệch pha
giữa hai phần của cùng một trạng thái. Pha tương đối là thứ khiến các biên độ
cộng vào hoặc triệt tiêu nhau — hiệu ứng gọi là **giao thoa**.

## Vector, ma trận và cổng unita

Trạng thái một qubit là một **vector cột** hai phần tử:

$$|\psi\rangle = \begin{bmatrix}\alpha\\ \beta\end{bmatrix}$$

Một **cổng** là một ma trận nhân vào trạng thái:

$$|\psi'\rangle = U\,|\psi\rangle$$

Cổng lượng tử là **unita** (unitary): `U^† U = I`. Tính chất unita là lý do toán học
khiến một cổng khả nghịch và bảo toàn chuẩn hoá của trạng thái.

## Nhiều qubit và tích tensor

Hai qubit không phải hai vector tách rời dán lại — trạng thái chung của chúng là
**tích tensor** của các trạng thái riêng, viết `|a⟩ ⊗ |b⟩` (hay `|a⟩|b⟩`). Tích
tensor của hai trạng thái hai chiều có bốn trạng thái cơ sở:

$$|00\rangle,\ |01\rangle,\ |10\rangle,\ |11\rangle$$

Nhãn đọc từ trái sang phải: `|01⟩` nghĩa là ký tự thứ nhất là `0`, ký tự thứ hai
là `1`. Như với một qubit, trạng thái là tổng có trọng số của bốn biên độ này, và
xác suất đo là bình phương độ lớn của chúng.

Trạng thái *có thể* viết thành tích tensor gọi là **trạng thái tích**; trạng thái
không thể viết được gọi là **rối** (Chương 5).

## Mô hình mạch

Mạch lượng tử được đọc **từ trái sang phải**. Mỗi **dây** ngang là một qubit, mỗi
**ô** trên dây là một cổng, và **đồng hồ đo** ở cuối là phép đo tạo ra một bit cổ
điển. Chạy mạch nhiều lần gọi là lấy **shots**; các lần đếm kết quả chính là thứ
biểu đồ số lần đo thể hiện.

## Mặt cầu Bloch

**Mặt cầu Bloch** là hình học mô tả một qubit. **Cực bắc** là `|0⟩` và **cực nam**
là `|1⟩`. **Đường xích đạo** chứa các trạng thái hỗn hợp đều 50/50. Mọi trạng thái
một qubit là một điểm trên mặt cầu, mô tả bởi hai góc `θ` và `φ`. Mặt cầu chỉ dùng
được cho một qubit — không mở rộng sang các trạng thái rối.

## Cơ sở đo

Một phép đo luôn được thực hiện **trong một cơ sở**, và một qubit chỉ mang một bit
xác định sau khi cơ sở được chốt. Mặc định là **cơ sở Z**, với các trạng thái `|0⟩`
và `|1⟩` — bit thông thường. Xoay cả hai trạng thái bằng một cổng Hadamard cho **cơ
sở X**, gồm `|+⟩ = (|0⟩ + |1⟩)/√2` và `|−⟩ = (|0⟩ − |1⟩)/√2`.

Quy tắc khiến cơ sở trở nên quan trọng rất ngắn: **đo trong đúng cơ sở mà trạng thái
được chuẩn bị thì được câu trả lời chắc chắn; đo trong cơ sở kia thì được một đồng
xu công bằng.** Về hình thức, `|⟨+|0⟩|² = ½` — hai cơ sở cách nhau 45° trên mặt cầu
Bloch, nên mỗi trạng thái của cơ sở này là hỗn hợp đều của các trạng thái cơ sở kia.
Đây chính là sự thật đứng sau [Chương 8](chapters/ch08-secure-communication.md): một
cơ sở là thứ bạn có thể nấp một bit phía sau, và kẻ nghe lén đoán sai cơ sở sẽ làm
nhiễu trạng thái.

## Hàm tuần hoàn và số học modular

`a mod N` là **số dư** khi chia `a` cho `N`: `17 mod 15 = 2`, và `a mod N` luôn nằm
giữa `0` và `N − 1`. Hai số **nguyên tố cùng nhau** khi ước chung duy nhất của chúng
là 1, và `gcd(a, N)` — ước chung lớn nhất — được tính bằng thuật toán Euclid trong
thời gian `O(log N)`.

**Dãy** `f(x) = a^x mod N` chính là thứ [Chương 11](chapters/ch11-shors-algorithm.md)
đi tìm. Nó luôn **tuần hoàn** khi `a` và `N` nguyên tố cùng nhau: sau một số bước `r`
các giá trị lặp lại y hệt (`a^(x+r) = a^x mod N`), và `r` nhỏ nhất như vậy là **bậc**
của `a` modulo `N`. Với `a = 2`, `N = 15`, dãy chạy `1, 2, 4, 8, 1, 2, 4, 8, …`, nên
bậc là 4.

Tìm `r` đó là *tìm bậc*, và nó khó ngang với việc phân tích thừa số nếu làm cổ điển.
Mẹo khiến nó dễ trên máy lượng tử là **biến đổi Fourier**: một danh sách giá trị tuần
hoàn biến thành vài **đỉnh** nhọn khi lấy biến đổi, và các đỉnh nằm tại các bội của
`1/r`. Đọc một đỉnh ngược lại thành phân số sẽ khôi phục `r`, và `r` biến thành các
thừa số của `N` chỉ với hai phép `gcd`.

## Tốc độ tăng trưởng và Big-O

Ta mô tả mức độ tăng của một phép tính bằng **ký hiệu Big-O**: `O(f)` nghĩa là
"tăng không nhanh hơn `f`, bỏ qua hằng số". Tăng trưởng được gọi là

- **đa thức** khi tăng như `b`, `b²`, `b³`, … — gấp đôi `b` chỉ nhân công việc với
  một hằng số nhỏ;
- **hàm mũ** khi tăng như `2^b`, `e^b`, … — thêm một bit có thể gấp đôi công việc;
- **dưới hàm mũ** khi nằm giữa hai loại trên: nhanh hơn mọi đa thức nhưng chậm hơn
  một hàm mũ đầy đủ.
