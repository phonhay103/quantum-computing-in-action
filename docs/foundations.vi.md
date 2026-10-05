# Kiến thức nền

Ghi chú này giả định bạn đọc được một chút đại số tuyến tính và còn mới với cơ
học lượng tử. Trang này gom các ý tưởng nền nhỏ mà mọi chương đều dựa vào. Đọc
lướt một lần, rồi quay lại mỗi khi một chương dùng thuật ngữ bạn chưa nhận ra.

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

## Vector, ma trận và cổng unitary

Trạng thái một qubit là một **vector cột** hai phần tử:

$$|\psi\rangle = \begin{bmatrix}\alpha\\ \beta\end{bmatrix}$$

Một **cổng** là một ma trận nhân vào trạng thái:

$$|\psi'\rangle = U\,|\psi\rangle$$

Cổng lượng tử là **unitary**: `U^† U = I`. Tính unitary là lý do toán học khiến một
cổng khả nghịch và bảo toàn chuẩn hoá của trạng thái.

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

## Tốc độ tăng trưởng và Big-O

Ta mô tả mức độ tăng của một phép tính bằng **ký hiệu Big-O**: `O(f)` nghĩa là
"tăng không nhanh hơn `f`, bỏ qua hằng số". Tăng trưởng được gọi là

- **đa thức** khi tăng như `b`, `b²`, `b³`, … — gấp đôi `b` chỉ nhân công việc với
  một hằng số nhỏ;
- **hàm mũ** khi tăng như `2^b`, `e^b`, … — thêm một bit có thể gấp đôi công việc;
- **dưới hàm mũ** khi nằm giữa hai loại trên: nhanh hơn mọi đa thức nhưng chậm hơn
  một hàm mũ đầy đủ.
