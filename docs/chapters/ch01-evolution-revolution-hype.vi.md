# Chương 1 — Tiến hoá, cách mạng, hay cường điệu?

!!! abstract "Trong một câu"
    Điện toán lượng tử đáng giá vì một lý do: **thuật toán Shor phân tích thừa
    số trong thời gian đa thức**, còn phương pháp cổ điển tốt nhất cần thời
    gian *dưới hàm mũ* — và mã hoá hiện đại dựa vào việc bài toán đó là khó.
    Nói cách khác, tính bảo mật của các hệ mật mã đang triển khai rộng rãi
    hiện nay phụ thuộc vào một giả định về độ khó tính toán, và một thuật toán
    lượng tử — ít nhất xét trên nguyên tắc — đã làm lung lay chính giả định đó.

## Tiến hoá của máy tính

Máy tính cổ điển đã tiến bộ trong suốt nhiều thập kỷ theo đúng một chiến lược
chủ đạo: thu nhỏ transistor. Transistor nhỏ hơn đồng nghĩa với nhiều công tắc
hơn trên một con chip, xung nhịp nhanh hơn và chi phí tính toán thấp hơn cho
mỗi phép toán; chính sự kết hợp đó tạo nên đà tăng hiệu năng ổn định quen
thuộc trong lịch sử của lĩnh vực. Tuy vậy, đà này đang chậm lại. Transistor
ngày nay chỉ còn rộng khoảng vài nguyên tử, và việc thu nhỏ thêm sẽ vấp phải
hai trở ngại cùng lúc: nhiệt lượng sinh ra trên mỗi đơn vị diện tích trở nên
khó giải toả, còn ở thang nguyên tử, các hiệu ứng lượng tử bắt đầu can thiệp
vào hoạt động tin cậy của một công tắc vốn được thiết kế để hoạt động thuần
cổ điển.

Điện toán lượng tử là bước kế tiếp trong tiến hoá đó, nhưng nó thay đổi *loại*
máy được chế tạo chứ không đơn thuần thay đổi kích thước. Thay vì bổ sung thêm
nhiều công tắc cổ điển, nó dùng **qubit** cùng với các quy luật cơ học lượng
tử — chồng chập, giao thoa và rối lượng tử — để tính toán theo những cách mà
máy cổ điển không thể bắt chước một cách hiệu quả. Cần lưu ý rằng ba khái
niệm đó không phải là chi tiết trang trí: mỗi khái niệm đều là một nguồn tài
nguyên tính toán, và mỗi khái niệm lần lượt được mở ra kỹ lưỡng ở một chương
riêng, cụ thể là Chương 2, 4 và 5.

## Cách mạng hay cường điệu?

Người ta dùng cả hai từ này một cách thoải mái trong các thảo luận công khai
về lĩnh vực, nên cần tách bạch hai khái niệm trước khi sử dụng. Bảng dưới đây
trình bày mỗi nhận định theo hình thức thường được nghe thấy, kèm phần phán
quyết thu được khi xem xét công bằng các bằng chứng hiện có:

| Nhận định | Kết luận |
|-----------|----------|
| "Máy lượng tử nhanh hơn ở mọi việc" | **Cường điệu** — với hầu hết tác vụ thường ngày, máy lượng tử không mang lại lợi thế |
| "Một số bài toán cụ thể được tăng tốc vượt bậc" | **Cách mạng** — phân tích thừa số, tìm kiếm và mô phỏng thực sự được tăng tốc |
| "Hôm nay đã dùng được trong sản xuất" | **Cường điệu** — máy hiện tại còn nhỏ, nhiều nhiễu và chưa phù hợp với khối lượng sản xuất |
| "Nền tảng lý thuyết vững và tiến bộ nhanh" | **Cách mạng** — các thuật toán chặt chẽ về mặt toán học và đã được thiết lập rõ |

Tóm lại một cách trung thực: đây là một **cuộc cách mạng cho một nhóm bài toán
hẹp**, không phải sự tăng tốc phổ quát cho tính toán nói chung. Xác định
chính xác *bài toán nào* thuộc nhóm hẹp đó, xét cho cùng, chính là mục đích
trung tâm của cuốn sách này.

## Máy lượng tử giúp được ở đâu

Các ứng dụng vốn thúc đẩy lĩnh vực này chia thành một số nhóm nhỏ, mỗi nhóm
được neo bởi một kết quả thuật toán cụ thể:

- **Mật mã** — thuật toán Shor phá được mã hoá công khai kiểu RSA khi một máy
  lượng tử đủ lớn trở nên khả dụng; phân phối khoá lượng tử và mật mã hậu
  lượng tử là hai hướng phản ứng chính được phát triển để đối phó với mối đe
  doạ đó.
- **Mô phỏng** — phân tử và vật liệu vốn tự chúng là hệ lượng tử, do đó máy
  lượng tử có thể mô hình hoá chúng một cách tự nhiên (phạm vi này bao gồm
  hoá học, phát triển thuốc và khoa học vật liệu). Một hệ lượng tử có `n`
  qubit "sống" trong không gian `2^n` biên độ, và chính không gian trạng thái
  theo cấp số nhân này khiến việc mô phỏng cổ điển chính xác trở nên quá đắt.
- **Tìm kiếm và tối ưu** — thuật toán Grover tăng tốc tìm kiếm không cấu
  trúc, cùng với nhiều bài toán tối ưu có liên quan.
- **Lấy mẫu và học máy** — nhóm này còn ở giai đoạn sớm, nhưng vẫn là một
  hướng nghiên cứu tích cực.

Ba nhóm đầu thể hiện lợi thế thuật toán rõ ràng nhất, và chúng tương ứng
chính xác với những thuật toán mà cuốn sách này phát triển và lần lượt đi qua
chi tiết.

Một ý niệm liên quan mà sách sử dụng xuyên suốt là **điện toán lai**: thiết
bị lượng tử nhỏ chỉ đảm nhận phần tính toán mà quy tắc lượng tử tạo ra lợi
thế, trong khi máy cổ điển điều khiển phần còn lại của quy trình — thường là
tiền xử lý, điều khiển và hậu xử lý.

Hơn nữa, các mức tăng tốc không đồng đều về độ lớn. Lợi thế của Shor là
**hàm mũ**. Trái lại, Grover chỉ mang lại lợi thế **bậc hai** — nó cắt một
bài tìm kiếm `N` bước xuống còn khoảng `√N` bước, tức là một cải thiện cỡ căn
bậc hai chứ không phải loại hàm mũ. Vì lý do đó, mỗi phát biểu rằng máy
lượng tử "nhanh hơn" đều cần được bổ sung định lượng: nhanh hơn bao nhiêu,
và cho bài toán nào.

## Vì sao phân tích thừa số là "mồi nhử"

Phần lớn tính bảo mật của Internet, trong đó có **RSA**, dựa trên một sự bất
đối xứng đơn giản: nhân hai số nguyên tố lớn thì dễ, nhưng *hoàn tác* phép
nhân đó — phân tích tích số trở lại thành các thừa số nguyên tố — được cho là
rất khó. "Khó" ở đây cần được hiểu theo một nghĩa cụ thể: nó được đo bằng
**thời gian**, tức là bằng cách thức khối lượng công việc tăng lên khi số cần
phân tích lớn dần.

!!! note "RSA dựa vào điều gì"
    Trong RSA, khoá công khai chứa một số `N = p · q` là tích của hai số
    nguyên tố lớn. Bất kỳ ai cũng có thể mã hoá một thông điệp bằng `N`, nhưng
    để giải mã thì cần `p` và `q` — tức là giải mã đòi hỏi các thừa số của
    `N`. Chừng nào việc phân tích `N` còn khó, khoá còn an toàn. Thuật toán
    Shor đe doạ đúng giả định này.

Nếu việc phân tích thừa số bỗng trở nên nhanh, kết quả là rất nhiều hệ mã hoá
đang triển khai sẽ trở nên dễ bị phá. Đây là hiện thân kịch tính nhất của câu
hỏi tiến hoá/cách mạng, do đó chương được mở đầu từ đây.

## Đo độ khó: chi phí tăng theo kích thước thế nào

Gọi `b` là số bit của số cần phân tích. Khi `b` lớn dần, số giây chính xác ít
quan trọng hơn **hình dạng** của sự tăng trưởng (xem
[tốc độ tăng trưởng và Big-O](../foundations.md) trong phần kiến thức nền,
nơi các khái niệm này được định nghĩa chính thức hơn):

| Tăng trưởng | Tên | Trực giác |
|-------------|-----|-----------|
| tăng như `b`, `b²`, `b³` … | **đa thức** | Gấp đôi `b` chỉ nhân tổng khối lượng công việc lên một hằng số nhỏ — mức tăng trưởng vẫn trong tầm kiểm soát |
| tăng như `2^b`, `e^b` … | **hàm mũ** | Thêm *một* bit có thể xấp xỉ gấp đôi công việc — độ khó nhanh chóng trở nên vô vọng |
| nằm giữa hai loại trên | **dưới hàm mũ** | Nhanh hơn mọi đa thức, song chậm hơn một hàm mũ đầy đủ |

Toàn bộ lời hứa của điện toán lượng tử, theo cách trình bày của chương này,
là bước nhảy từ các hàng dưới của bảng lên đúng hàng trên cùng.

## Chi phí cổ điển

Phương pháp cổ điển tốt nhất đã biết để phân tích thừa số là **sàng trường số
tổng quát (GNFS)**. Thời gian chạy của nó xấp xỉ

$$e^{\left(\tfrac{64}{9}\,b\,(\ln b)^2\right)^{1/3}}$$

Đây là ước lượng rút gọn của sách cho GNFS. Chi tiết then chốt là thừa số
`(ln b)^2` nằm trong căn: chính số mũ tăng theo `b`, và chính đặc điểm này
khiến toàn bộ biểu thức tăng **dưới hàm mũ**.

"Dưới hàm mũ" là một thuật ngữ chính xác, và nó *không* đồng nghĩa với "siêu
đa thức". *Siêu đa thức* chỉ phát biểu rằng khối lượng công việc tăng nhanh
hơn mọi đa thức. *Dưới hàm mũ* phát biểu điều đó **và** phát biểu thêm rằng
nó vẫn tăng chậm hơn một hàm mũ thật như `2^b` — tốc độ tăng trưởng nằm giữa
hai chế độ. Cả hai mô tả đều đúng với GNFS, và mô tả thứ hai là nhận định mạnh
hơn (chứa nhiều thông tin hơn), bởi vì nó cung cấp cả cận trên chứ không chỉ
cận dưới. Tác dụng thực tế là thêm bit không đơn thuần thêm việc; nó *nhân*
khối lượng công việc lên — hết lần này đến lần khác.

Hệ quả thực tế là mỗi vài bit chiều dài khoá thêm vào khiến việc phân tích
cổ điển đắt lên đáng kể. Vì lý do đó, khoá 2048 bit được coi là an toàn ngày
nay.

## Chi phí của Shor

Thuật toán Shor phân tích thừa số trong **thời gian đa thức**, khoảng

$$b^3$$

Tăng trưởng bậc ba nhẹ nhàng hơn nhiều khi so sánh. Đi từ một số 1024 bit lên
số 2048 bit chỉ nhân khối lượng công việc lên khoảng `2³ = 8`, trong khi
phương pháp cổ điển bùng nổ dữ dội hơn hẳn trên chính lần gấp đôi đó.

!!! warning "Kiểm chứng thực tế"
    "Đa thức" không đồng nghĩa với "dễ ngay hôm nay". Shor vẫn đòi hỏi một máy
    lượng tử lớn, đã được sửa lỗi. Máy hiện nay thuộc loại **NISQ** — *Noisy
    Intermediate-Scale Quantum*: vài trăm qubit dễ bị nhiễu, hoàn toàn chưa có
    sửa lỗi. Các thiết bị như vậy phải dùng nhiều qubit *vật lý* để mã hoá một
    qubit **logic** đáng tin. Vì vậy, chương này nói về *lời hứa tiệm cận*,
    không phải về việc phá RSA trên phần cứng hiện tại.

## Các sơ đồ {#cac-so-do}

Sách vẽ **hai** biểu đồ: một biểu đồ so sánh cả hai thuật toán trên cùng hệ
trục, và một biểu đồ chỉ vẽ đường cổ điển, để hình dạng của nó không bị đường
Shor thấp hơn nhiều che khuất về mặt trực quan.

![Độ phức tạp cổ điển so với Shor](../assets/ch01-time-complexity.png){ width="520" }

![Đường cổ điển riêng lẻ](../assets/ch01-time-complexity-classical.png){ width="520" }

- Đường **cổ điển** (vàng) dốc đứng — đó chính là bức tường dưới hàm mũ.
- Đường **Shor** (xanh lá) thấp và gần như phẳng khi so sánh — đó là con
  đường đa thức.

Chính khoảng cách ngày càng rộng giữa hai đường *là* biểu hiện trực quan của
sự tăng tốc lượng tử.

## Ví dụ cho thấy điều gì

Khi chương trình của chương được thực thi, nó in một bảng ước lượng cho 4, 8,
16, 32 và 64 bit. Đọc theo từng cột giúp hai tốc độ tăng trưởng trở nên cụ
thể: cột cổ điển phình thành những con số khổng lồ, trong khi cột Shor vẫn
tương đối khiêm tốn. Các hình trên kể lại câu chuyện đó dưới dạng hình ảnh.

## Những điều cần nhớ

- Điện toán lượng tử là một **bước tiến hoá** về phần cứng, kết hợp với mức
  tăng tốc **cách mạng** cho một nhóm bài toán hẹp — nó không phải một máy
  tính nhanh hơn phổ quát.
- Lợi thế rõ ràng nhất nằm ở mật mã, mô phỏng lượng tử và tìm kiếm.
- GNFS cổ điển là **dưới hàm mũ**; thuật toán Shor là **đa thức** (`b³`).
- Mức tăng tốc nói về *tăng trưởng tiệm cận*, không phải về máy móc hiện nay.
- Đây chính là lý do mật mã hậu lượng tử là một lĩnh vực nghiên cứu tích cực.

## Mã nguồn của chương này

Chương trình mẫu tạo ra bảng và các biểu đồ nằm trong
[`src/quantum_computing_in_action/ch01/time_complexity.py`](https://github.com/phonhay103/quantum-computing-in-action/blob/main/src/quantum_computing_in_action/ch01/time_complexity.py).
Nó được chạy bằng `make ch01`.
