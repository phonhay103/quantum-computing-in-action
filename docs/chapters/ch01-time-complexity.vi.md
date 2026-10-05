# Chương 1 — Độ phức tạp thời gian phân tích thừa số

!!! abstract "Trong một câu"
    Máy tính lượng tử quan trọng vì **thuật toán Shor phân tích thừa số số lớn
    trong thời gian đa thức**, trong khi thuật toán cổ điển tốt nhất cần thời gian
    *hàm mũ* — và mã hoá hiện đại dựa vào việc phân tích thừa số là khó.

## Vì sao phân tích thừa số là điểm mấu chốt

Phần lớn an ninh của internet, trong đó có **RSA**, dựa trên một sự bất đối xứng
đơn giản: nhân hai số nguyên tố lớn thì dễ, nhưng *hoàn tác* phép nhân đó — phân
tích tích số trở lại thành các thừa số nguyên tố — được cho là rất khó. "Khó" ở
đây được đo bằng **thời gian**: công việc tăng lên thế nào khi con số trở nên lớn
hơn.

Nếu phân tích thừa số bỗng trở nên nhanh, rất nhiều hệ mã hoá sẽ bị phá vỡ nhanh
chóng. Chương này nói về việc máy tính lượng tử làm nó nhanh lên *bao nhiêu*.

## Đo độ khó: chi phí tăng thế nào theo kích thước

Gọi `b` là số bit của con số ta muốn phân tích. Khi `b` lớn dần, ta ít quan tâm
đến số giây chính xác mà quan tâm đến **hình dạng** của sự tăng trưởng:

| Tăng trưởng | Tên gọi | Trực giác |
|-------------|---------|-----------|
| tăng như `b`, `b²`, `b³` … | **đa thức** | Gấp đôi `b` chỉ nhân công việc lên một hằng số nhỏ — xử lý được |
| tăng như `2^b`, `e^b` … | **hàm mũ** | Thêm *một* bit có thể gần như gấp đôi công việc — chẳng mấy chốc vô vọng |

Toàn bộ lời hứa của điện toán lượng tử, trong chương này, là bước nhảy từ hàng
thứ hai xuống hàng thứ nhất.

## Chi phí cổ điển

Phương pháp cổ điển tốt nhất để phân tích thừa số là **sàng trường số tổng quát
(GNFS)**. Thời gian chạy của nó xấp xỉ

$$e^{\left(\tfrac{64}{9}\,b\,(\ln b)^2\right)^{1/3}}$$

Chi tiết then chốt là `(ln b)^2` nằm trong căn: số mũ tăng theo `b`, khiến cả
biểu thức tăng **siêu đa thức**. Thêm bit không chỉ cộng thêm việc — mà nhân việc
lên, lặp đi lặp lại.

Hệ quả thực tế: chỉ cần thêm vài bit vào độ dài khoá là việc phân tích thừa số
cổ điển đắt lên chóng mặt. Đó là lý do khoá 2048 bit được coi là an toàn ngày nay.

## Chi phí của Shor

Thuật toán Shor phân tích thừa số trong **thời gian đa thức**, khoảng

$$b^3$$

Tăng trưởng bậc ba khá nhẹ nhàng nếu đem so. Đi từ số 1024 bit lên 2048 bit chỉ
nhân công việc lên khoảng `2³ = 8`, trong khi phương pháp cổ điển bùng nổ dữ dội hơn
nhiều.

!!! warning "Thực tế cần lưu ý"
    "Đa thức" không đồng nghĩa với "dễ ngay hôm nay". Shor vẫn cần một máy tính
    lượng tử lớn, đã sửa lỗi. Chương này nói về *lời hứa tiệm cận*, không phải về
    việc phá RSA trên phần cứng hiện tại.

## Sơ đồ

![Độ phức tạp cổ điển so với Shor](../assets/ch01-time-complexity.png){ width="560" }

Biểu đồ vẽ cả hai ước lượng theo số bit:

- Đường **cổ điển** (màu vàng) dốc lên nhanh — đây là bức tường hàm mũ.
- Đường **Shor** (màu xanh lá) vẫn thấp và gần như phẳng khi so sánh — đây là
  con đường đa thức.

Khoảng cách ngày càng rộng giữa hai đường *chính là* tốc độ tăng mà lượng tử đem lại.

## Ví dụ cho thấy điều gì

Khi chạy chương trình, nó in một bảng ước lượng cho 4, 8, 16, 32 và 64 bit. Đọc
theo cột giúp hai tốc độ tăng trở nên cụ thể: cột cổ điển phình lên thành những
con số khổng lồ, còn cột Shor vẫn tương đối khiêm tốn. Hình trên là câu chuyện đó
được vẽ ra.

## Ghi nhớ chính

- Độ khó phân tích thừa số là nơi danh tiếng của điện toán lượng tử bắt đầu.
- GNFS cổ điển là **siêu đa thức**; Shor là **đa thức** (`b³`).
- Tốc độ tăng nằm ở *độ phức tạp tiệm cận*, không phải máy móc hiện nay.
- Đây chính là lý do lĩnh vực mật mã hậu lượng tử đang rất sôi động.

## Mã nguồn của chương này

Ví dụ tạo ra bảng và hình nằm trong
[`src/quantum_computing_in_action/ch01/time_complexity.py`](https://github.com/phonhay103/quantum-computing-in-action/blob/main/src/quantum_computing_in_action/ch01/time_complexity.py).
Chạy bằng `make ch01`.
