# Chương 3 — Qubit và cổng lượng tử

!!! abstract "Trong một câu"
    **Qubit** là đơn vị cơ bản của thông tin lượng tử, còn **cổng** là một phép
    toán khả nghịch tác động lên nó; cổng đầu tiên cần gặp là **Pauli-X**, lật
    `|0⟩` thành `|1⟩` một cách tất định — nói cách khác, chính là `NOT` lượng tử.

## Những đơn vị cơ bản

Chương trình lượng tử được dựng từ hai mảnh rất nhỏ:

- một **qubit** — vật mang thông tin lượng tử, được trang bị hai trạng thái cơ
  sở `|0⟩` và `|1⟩`;
- một **cổng** — phép toán áp lên một hay nhiều qubit.

Mọi thứ xuất hiện về sau trong cuốn sách — chồng chập, rối lượng tử cũng như các
thuật toán hoàn chỉnh — đều được lắp từ riêng hai ý tưởng này. Do đó chương này
chính là chương "đơn vị cơ bản": trước khi có thể thực hiện bất kỳ phép xây
dựng nào tinh vi hơn, cần xác định rõ qubit là gì và cổng tác động lên nó ra
sao.

## Qubit

Bit cổ điển chỉ nhận đúng một trong hai giá trị: `0` hoặc `1`. Qubit có thể ở
một trong hai trạng thái đó, nhưng cũng có thể được đặt vào trạng thái **chồng
chập** — tổ hợp có trọng số của cả hai trạng thái cơ sở cùng một lúc. Chương 2
đã tận dụng tính chất này để tạo bit ngẫu nhiên. Chương hiện tại tập trung vào
phép toán đơn giản nhất mà một cổng có thể thực hiện: chuyển qubit gọn gàng
giữa hai trạng thái cơ sở.

Cần ghi nhớ một con số về quy mô để dùng về sau: `n` qubit được mô tả bởi `2^n`
biên độ, nên số biên độ nhân đôi với mỗi qubit thêm vào. Sự tăng trưởng theo cấp
số nhân đó chính là nguyên liệu thô của Chương 4 và các chương kế tiếp.

## Cổng có tính khả nghịch

Một thuộc tính định hình của cổng lượng tử là chúng **khả nghịch**: thông tin
không bao giờ bị ném đi. Mỗi cổng đều có nghịch đảo khôi phục lại trạng thái
trước đó. Điều này tương phản rõ rệt với các cổng cổ điển quen thuộc — `AND`
nhận hai đầu vào nhưng chỉ trả một đầu ra, nên không thể khôi phục đầu vào tính
từ đầu ra. Về mặt toán học, tính khả nghịch tương đương với yêu cầu cổng phải
được biểu diễn bằng một ma trận **unita**
(xem [vector, ma trận và cổng unita](../foundations.md)), điều Chương 4 sẽ trình
bày đầy đủ.

- Nghịch đảo của `X` chính là `X`: `X·X = I`.
- Nghịch đảo của `H` cũng chính là `H` (Chương 4).

Ở đây `I` ký hiệu phép **đơn vị** — "không làm gì". Tính khả nghịch này không
phải là một chi tiết vụn; chính nó cho phép các mạch lượng tử được dựng lên và,
khi cần, được hoàn tác.

!!! note "Phép đo là ngoại lệ"
    Cổng thì khả nghịch, nhưng **phép đo** thì không: phép đo làm sụp trạng thái
    và chỉ để lại một kết quả cổ điển duy nhất. Chính sự bất đối xứng đó khiến
    một thuật toán lượng tử được viết dưới dạng mạch khả nghịch, rồi ở bước cuối
    cùng mới thực hiện phép đo.

## Một cổng NOT cho qubit

Cổng **Pauli-X** là tương tự lượng tử của `NOT` cổ điển:

$$X\,|0\rangle = |1\rangle, \qquad X\,|1\rangle = |0\rangle$$

Cổng này hoán đổi vai trò của hai trạng thái cơ sở mà vẫn giữ mọi thứ khác về
qubit ở trạng thái nhất quán. Nếu phép tính bắt đầu ở `|0⟩` rồi `X` được áp vào,
qubit từ đó chắc chắn ở `|1⟩`; kết quả là phép đo luôn trả về `1` — trong mọi
lần lặp lại của thí nghiệm.

## Các cổng bạn sẽ gặp

`X` là cổng đầu tiên được gặp, nhưng chỉ là một thành viên trong một họ nhỏ. `H`
(đã giới thiệu ở Chương 2) tạo chồng chập, còn cổng **hai qubit** như `CNOT`
xuất hiện cùng rối lượng tử ở Chương 5. Mỗi cổng như vậy sẽ được giới thiệu
chính xác tại điểm mà nó trở nên cần thiết, nên ở giai đoạn này không yêu cầu
sự quen thuộc trước với chúng. Xét theo góc độ này, điểm mấu chốt lúc
này là mọi cổng trong họ đều tuân theo cùng hai quy tắc: nó khả nghịch, và nó
đưa qubit tới một điểm xác định trên mặt cầu Bloch.

## Vì sao kết quả là tất định

Vì sao cùng một kiểu thí nghiệm — một cổng rồi phép đo — lại cho kết quả ngẫu
nhiên ở chương này nhưng tất định ở chương kia? Hai chương có thể được đối sánh
trực tiếp, mỗi hàng một đặc điểm:

| | Chương 2 (Hadamard) | Chương 3 (Pauli-X) |
|---|---|---|
| Trạng thái sau cổng | (\|0⟩ + \|1⟩)/√2 | \|1⟩ |
| Xác suất ra `0` | 50 % | 0 % |
| Xác suất ra `1` | 50 % | 100 % |
| Đo lặp nhiều lần | lẫn lộn `0` và `1` | luôn là `1` |

Khác biệt nằm ở chính trạng thái, không phải ở thiết bị đo. Trạng thái xác định
cho kết quả xác định; chồng chập đều cho kết quả ngẫu nhiên. Nói cách khác, phân
bổ thống kê được quyết định hoàn toàn bởi trạng thái tại thời điểm thực hiện
phép đo.

!!! info "Cơ sở đo là gì"
    Xuyên suốt ghi chú, "đo" luôn có nghĩa là đo trong cơ sở tính toán
    `{|0⟩, |1⟩}` — chính trục Z mà hai cực của mặt cầu Bloch biểu diễn. Chọn cơ
    sở khác sẽ cho ra kết quả khác; Chương 6 gặp một trường hợp mà dấu của trạng
    thái thay đổi nhưng mọi xác suất đo vẫn giữ nguyên.

??? question "Tự kiểm tra — cổng `H` của Chương 2 cũng khả nghịch. Vậy tính ngẫu nhiên của nó có thể bị hoàn tác không?"
    Có — nhưng chỉ khi qubit chưa bị đo. Áp `H` thứ hai trước khi đo, qubit quay
    về `|0⟩`; đo khi đó luôn ra `0` (Chương 4 lấy điều này làm kết quả tiêu
    đề). Tính ngẫu nhiên chỉ trở nên vĩnh viễn tại chính phép đo — đúng là ngoại
    lệ mà ghi chú phía trên mô tả.

## Các sơ đồ {#cac-so-do}

### Mạch

![Mạch Pauli-X](../assets/ch03-pauli-x.png){ width="420" }

Đọc từ trái sang phải: qubit `q` bắt đầu ở `|0⟩`, ô `X` lật nó, và phép đo `M`
ghi kết quả vào bit cổ điển `c`. Sơ đồ nhỏ này gói trọn toàn bộ câu chuyện của
chương.

### Hai cổng `X` triệt tiêu nhau

![Hai cổng Pauli-X](../assets/ch03-pauli-x2-circuit.png){ width="420" }

Vì `X·X = I`, cổng `X` thứ hai hoàn tác cổng thứ nhất. Một mạch không gì hơn là
các cổng xếp theo thứ tự, và chuỗi `X, X` tương đương với không làm gì cả.

### Trước, sau một `X`, sau hai `X`

![Qubit trước, sau X, và sau X·X](../assets/ch03-pauli-x-bloch.png){ width="720" }

**Mặt cầu Bloch** làm phép lật trở nên trực quan:

- **Trước** — mũi tên trạng thái chỉ cực bắc, `|0⟩`.
- **Sau một `X`** — mũi tên chỉ cực nam, `|1⟩`.
- **Sau hai `X`** — mũi tên đã trở lại cực bắc, `|0⟩`.

Về hình học, `X` là một **phép quay 180° quanh trục X** của mặt cầu. Vì trạng
thái đi từ cực này sang cực kia và không bao giờ chạm đường xích đạo, nên không
có chồng chập được tạo ra và, kết quả là, không có ngẫu nhiên nào xuất hiện
trong kết quả đo.

### Kết quả đo được

![1000 lần chạy X](../assets/ch03-pauli-x-counts.png){ width="420" }
![1000 lần chạy X·X](../assets/ch03-pauli-x2-counts.png){ width="420" }

Sau một `X`, cả 1000 kết quả đều là `1`; sau hai `X`, cả 1000 kết quả đều là
`0`. Kết quả tất định trong cả hai trường hợp — nguồn ngẫu nhiên duy nhất trong
các chương này đến từ cổng Hadamard. Cần lưu ý rằng một mẫu gồm 1000 lần lặp
là đủ lớn để ngay cả một xác suất dư nhỏ cũng đã hiện ra trong số đếm; sự vắng
mặt hoàn toàn của sai lệch vì vậy là bằng chứng có ý nghĩa rằng kết quả là chắc
chắn chứ không chỉ là khả dĩ.

## Những điều cần nhớ

- Qubit và cổng là hai **đơn vị cơ bản** của chương trình lượng tử.
- Cổng lượng tử **khả nghịch**; mỗi cổng đều có nghịch đảo.
- Cổng Pauli-X là tương tự lượng tử của `NOT`.
- `X|0⟩ = |1⟩` và `X|1⟩ = |0⟩`; hai cổng `X` triệt tiêu nhau (`X·X = I`).
- Áp `X` lên `|0⟩` rồi đo luôn trả về `1` — tất định, không ngẫu nhiên.
- Trên mặt cầu Bloch, `X` là phép quay 180° quanh trục X.

## Mã nguồn của chương này

Ví dụ vẽ mạch, mặt cầu Bloch trước/sau và biểu đồ số lần đo nằm trong
[`src/quantum_computing_in_action/ch03/pauli_x.py`](https://github.com/phonhay103/quantum-computing-in-action/blob/main/src/quantum_computing_in_action/ch03/pauli_x.py).
Chạy bằng `make ch03`.
