# Chương 1 — Tiến hoá, cách mạng, hay cường điệu?

!!! abstract "Trong một câu"
    Điện toán lượng tử là một **bước tiến hoá** thực sự của máy tính, nhưng không
    phải bản nâng cấp thay thế tất cả: nó quan trọng vì **thuật toán Shor phân
    tích thừa số trong thời gian đa thức**, còn phương pháp cổ điển tốt nhất cần
    thời gian *siêu đa thức* (dưới hàm mũ) — và mã hoá hiện đại dựa vào việc bài
    toán đó là khó.

## Tiến hoá của máy tính

Máy tính cổ điển phát triển suốt nhiều thập kỷ nhờ thu nhỏ transistor: nhiều
công tắc hơn, xung nhịp nhanh hơn, chi phí rẻ hơn. Đà đó đang chậm lại.
Transistor giờ chỉ còn vài nguyên tử, và thu nhỏ thêm sẽ vấp phải nhiệt lượng
cùng các hiệu ứng lượng tử.

Điện toán lượng tử là bước kế tiếp trong tiến hoá đó, nhưng nó thay đổi *loại*
máy mà ta chế tạo. Thay vì thêm nhiều công tắc cổ điển, nó dùng **qubit** và các
quy luật cơ học lượng tử — chồng chập, giao thoa và rối lượng tử — để tính theo
cách mà máy cổ điển không thể bắt chước một cách hiệu quả.

## Cách mạng hay cường điệu?

Người ta dùng cả hai từ, nên cần tách bạch:

| Nhận định | Kết luận |
|-----------|----------|
| "Máy lượng tử nhanh hơn ở mọi việc" | **Cường điệu** — với hầu hết tác vụ thường ngày thì không |
| "Một số bài toán cụ thể được tăng tốc vượt bậc" | **Cách mạng** — phân tích thừa số, tìm kiếm, mô phỏng |
| "Hôm nay đã dùng được trong sản xuất" | **Cường điệu** — máy hiện tại còn nhỏ và nhiễu |
| "Nền tảng lý thuyết vững và tiến bộ nhanh" | **Cách mạng** — các thuật toán là thật |

Tóm lại cho trung thực: một **cuộc cách mạng cho một nhóm bài toán hẹp**, không
phải tăng tốc phổ quát. Biết *bài toán nào* chính là mục đích của cuốn sách này.

## Máy lượng tử giúp được ở đâu

Các ứng dụng thúc đẩy lĩnh vực này gom thành vài nhóm:

- **Mật mã** — thuật toán Shor phá được mã hoá công khai kiểu RSA; phân phối khoá
  lượng tử và mật mã hậu lượng tử là phản ứng trước mối đe doạ đó.
- **Mô phỏng** — phân tử và vật liệu vốn là hệ lượng tử; máy lượng tử mô hình hoá
  chúng một cách tự nhiên (hoá học, phát triển thuốc, vật liệu). Một hệ lượng tử
  có `n` qubit sống trong không gian `2^n` biên độ, chính điều đó khiến việc mô
  phỏng cổ điển chính xác trở nên quá đắt.
- **Tìm kiếm và tối ưu** — thuật toán Grover tăng tốc tìm kiếm không cấu trúc và
  nhiều bài toán tối ưu.
- **Lấy mẫu và học máy** — còn sớm, nhưng đang được nghiên cứu tích cực.

Ba nhóm đầu có lợi thế thuật toán rõ ràng nhất, và đúng là những thuật toán mà
cuốn sách này lần lượt đi qua.

Một ý liên quan mà sách dùng là **điện toán lai**: thiết bị lượng tử nhỏ đảm nhận
phần mà quy tắc lượng tử thắng thế, còn máy cổ điển điều khiển phần còn lại. Các
mức tăng tốc cũng không như nhau — Shor là **hàm mũ**, còn tìm kiếm Grover chỉ là
**bậc hai** — nên "nhanh hơn" luôn cần thêm vế định tính.

## Vì sao phân tích thừa số là "mồi nhử"

Phần lớn bảo mật Internet, gồm **RSA**, dựa trên một sự bất đối xứng đơn giản:
nhân hai số nguyên tố lớn thì dễ, nhưng *hoàn tác* phép nhân đó — phân tích tích
số trở lại thành các thừa số nguyên tố — được cho là rất khó. "Khó" ở đây được đo
bằng **thời gian**: công việc tăng lên thế nào khi con số lớn dần.

!!! note "RSA dựa vào điều gì"
    Trong RSA, khoá công khai chứa một số `N = p · q` là tích của hai số nguyên tố
    lớn. Ai cũng có thể mã hoá bằng `N`, nhưng giải mã cần `p` và `q` — tức là cần
    các thừa số của `N`. Chừng nào phân tích `N` còn khó, khoá còn an toàn. Thuật
    toán Shor đe doạ đúng giả định này.

Nếu phân tích thừa số bỗng trở nên nhanh, rất nhiều mã hoá sẽ bị phá nhanh. Đây là
ví dụ kịch tính nhất cho câu hỏi tiến hoá/cách mạng, nên chương bắt đầu từ đây.

## Đo độ khó: chi phí tăng theo kích thước thế nào

Gọi `b` là số bit của số ta muốn phân tích. Khi `b` lớn dần, ta ít quan tâm số
giây chính xác mà quan tâm **hình dạng** của sự tăng trưởng (xem
[tốc độ tăng trưởng và Big-O](../foundations.md) trong phần kiến thức nền):

| Tăng trưởng | Tên | Trực giác |
|-------------|-----|-----------|
| tăng như `b`, `b²`, `b³` … | **đa thức** | Gấp đôi `b` chỉ nhân công việc lên một hằng số nhỏ — xử lý được |
| tăng như `2^b`, `e^b` … | **hàm mũ** | Thêm *một* bit có thể gấp đôi công việc — nhanh chóng vô vọng |

Toàn bộ lời hứa của điện toán lượng tử, trong chương này, là bước nhảy từ hàng thứ
hai xuống hàng thứ nhất.

## Chi phí cổ điển

Phương pháp cổ điển tốt nhất đã biết để phân tích thừa số là **sàng trường số
tổng quát (GNFS)**. Thời gian chạy của nó xấp xỉ

$$e^{\left(\tfrac{64}{9}\,b\,(\ln b)^2\right)^{1/3}}$$

Đây là ước lượng rút gọn của sách cho GNFS. Chi tiết then chốt là `(ln b)^2` nằm
trong căn: số mũ tăng theo `b`, khiến cả biểu thức tăng **siêu đa thức**. Thêm bit
không chỉ thêm việc — nó nhân việc lên, hết lần này đến lần khác. Nói chặt chẽ,
GNFS là **dưới hàm mũ** — nhanh hơn một hàm mũ đầy đủ nhưng vẫn vượt xa mọi đa
thức.

Hệ quả thực tế: mỗi vài bit khoá thêm vào khiến việc phân tích cổ điển đắt lên
rất nhiều. Đó là lý do khoá 2048 bit được coi là an toàn ngày nay.

## Chi phí của Shor

Thuật toán Shor phân tích thừa số trong **thời gian đa thức**, khoảng

$$b^3$$

Tăng trưởng bậc ba nhẹ nhàng hơn nhiều khi so sánh. Đi từ số 1024 bit lên số 2048
bit chỉ nhân công việc lên khoảng `2³ = 8`, trong khi phương pháp cổ điển bùng nổ
dữ dội hơn hẳn.

!!! warning "Kiểm chứng thực tế"
    "Đa thức" không đồng nghĩa với "dễ ngay hôm nay". Shor vẫn cần một máy lượng
    tử lớn, đã sửa lỗi. Máy hiện nay là **NISQ** — nhiễu, quy mô trung bình, và
    chưa sửa lỗi — nên phải dùng nhiều qubit *vật lý* để mã hoá một qubit
    **logic** đáng tin. Chương này nói về *lời hứa tiệm cận*, không phải về việc
    phá RSA trên phần cứng hiện tại.

## Các sơ đồ

Sách vẽ **hai** biểu đồ: một so sánh cả hai thuật toán, và một chỉ vẽ đường cổ điển
để hình dạng của nó không bị đường Shor thấp hơn che khuất.

![Độ phức tạp cổ điển so với Shor](../assets/ch01-time-complexity.png){ width="520" }

![Đường cổ điển riêng lẻ](../assets/ch01-time-complexity-classical.png){ width="520" }

- Đường **cổ điển** (vàng) dốc đứng — đó là bức tường siêu đa thức.
- Đường **Shor** (xanh lá) thấp và gần như phẳng khi so sánh — đó là con đường đa
  thức.

Khoảng cách ngày càng rộng giữa hai đường *chính là* sự tăng tốc lượng tử.

## Ví dụ cho thấy điều gì

Khi chạy chương, nó in một bảng ước lượng cho 4, 8, 16, 32 và 64 bit. Đọc theo
cột giúp hai tốc độ tăng trưởng trở nên cụ thể: cột cổ điển phình thành những con
số khổng lồ trong khi cột Shor vẫn tương đối khiêm tốn. Các hình trên kể cùng câu
chuyện đó bằng hình ảnh.

## Ghi nhớ chính

- Điện toán lượng tử là một **bước tiến hoá** với tăng tốc **cách mạng** cho một
  nhóm bài toán hẹp — không phải máy tính nhanh phổ quát.
- Lợi thế rõ nhất là mật mã, mô phỏng lượng tử và tìm kiếm.
- GNFS cổ điển là **siêu đa thức**; Shor là **đa thức** (`b³`).
- Tăng tốc nằm ở *tăng trưởng tiệm cận*, không phải máy móc hiện nay.
- Đây chính là lý do mật mã hậu lượng tử đang được nghiên cứu tích cực.

## Mã nguồn của chương này

Ví dụ tạo bảng và các biểu đồ nằm trong
[`src/quantum_computing_in_action/ch01/time_complexity.py`](https://github.com/phonhay103/quantum-computing-in-action/blob/main/src/quantum_computing_in_action/ch01/time_complexity.py).
Chạy bằng `make ch01`.
