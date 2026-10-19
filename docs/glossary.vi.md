# Thuật ngữ

Mọi thuật ngữ các chương dùng, gom trong một bảng. Bản tiếng Anh có đúng những
hàng này theo cùng thứ tự, nên bạn đổi ngôn ngữ mà không mất dấu (dùng bộ chọn
ngôn ngữ ở thanh trên cùng).

Những thuật ngữ được chương đánh dấu **lần đầu** cũng được giải thích ngay tại
chỗ. Trang này là chỗ quay lại khi một định nghĩa đã mờ đi.

## Các khối xây dựng

| Thuật ngữ | Nghĩa là gì |
|---|---|
| **bit** | Một `0` hoặc `1` cổ điển. Chỉ giữ một giá trị tại một thời điểm, và đọc nó không làm thay đổi nó. |
| **qubit** | Phiên bản lượng tử của bit. Không chỉ `\|0⟩` và `\|1⟩`, nó còn có thể ở *tổ hợp* của cả hai. |
| **trạng thái cơ sở** | Một trong các trạng thái được đặt tên mà hệ thống có thể ở, ở đây là `\|0⟩` và `\|1⟩`. Mọi thứ khác là tổng có trọng số của chúng. |
| **ket** | Ký hiệu `\|ψ⟩` để gọi tên một trạng thái. Bản thân ket chỉ là nhãn; thông tin nằm ở các con số đứng trước nó. |
| **biên độ** | Con số nhân với một trạng thái cơ sở. Không phải xác suất: có thể âm, thậm chí là số phức. |
| **quy tắc Born** | Quy tắc biến biên độ thành xác suất: bình phương độ lớn của chúng. |
| **chuẩn hoá** | Điều kiện bình phương các biên độ cộng lại bằng 1, để chúng là một phân phối xác suất hợp lệ. |
| **chồng chập** (superposition) | Trạng thái đồng thời là tổ hợp có trọng số của các trạng thái cơ sở. |
| **pha** | Góc đi kèm với một biên độ. Pha của một biên độ đơn lẻ không quan sát được; chỉ **pha tương đối** giữa hai phần của cùng một trạng thái mới quan trọng. |
| **giao thoa** | Hiệu ứng khi hai phần của một trạng thái cộng vào hoặc triệt tiêu nhau, do pha tương đối quyết định. |

## Cổng và mạch

| Thuật ngữ | Nghĩa là gì |
|---|---|
| **cổng** (gate) | Phép toán khả nghịch tác động lên một hay nhiều qubit. Được viết dưới dạng ma trận. |
| **khả nghịch** | Đặc tính định hình của cổng lượng tử: luôn có thể hoàn tác, nên không thông tin nào bị vứt bỏ. |
| **unita** (unitary) | Ma trận thỏa mãn `U^† U = I`. Tính unita là *lý do* cổng khả nghịch và giữ được chuẩn hoá. |
| **Pauli-X** | Cổng `X` — là `NOT` lượng tử. Lật `\|0⟩ ↔ \|1⟩`, còn trạng thái khác thì để yên. |
| **Hadamard** | Cổng `H` — cách chuẩn nhất để tạo chồng chập đều. Nó là nghịch đảo của chính nó, nên áp hai lần là hoàn tác. |
| **Pauli-Z** | Cổng `Z`. Lật **pha** của `\|1⟩` mà không đổi giá trị bit của nó. |
| **CNOT** | Cổng hai qubit gồm qubit **điều khiển** và qubit **đích**. Nó lật qubit đích đúng khi qubit điều khiển bằng `1`. |
| **CZ** | Controlled-Z. Giống `CNOT`, nhưng lật *pha* của qubit đích thay vì bit của nó. |
| **Toffoli** | Cổng ba qubit (`CCNOT`), lật qubit đích chỉ khi **cả hai** qubit điều khiển bằng `1`. Một phép `AND` khả nghịch. |
| **đơn vị** | `I`, ma trận không làm gì cả. Hai cổng `X` liên tiếp cho ra `I`, hai cổng `H` cũng vậy. |
| **mạch** | Sơ đồ đọc từ trái sang phải: mỗi dây là một qubit, mỗi ô là một cổng, mỗi đồng hồ ở cuối là một phép đo. |
| **lần chạy** (shots) | Chạy lại mạch nhiều lần để đếm các kết quả đo được. |

## Nhiều qubit

| Thuật ngữ | Nghĩa là gì |
|---|---|
| **tích tensor** | `⊗`, cách ghép hai qubit thành một trạng thái chung. Không phải nối chuỗi đơn giản. |
| **trạng thái tích** | Trạng thái chung viết được thành trạng thái của qubit này nhân với trạng thái của qubit kia. Hai qubit độc lập. |
| **rối** | Trạng thái chung *không* viết được như vậy. Không qubit nào có trạng thái riêng của riêng nó. |
| **trạng thái Bell** | Cặp rối cực đại, ví dụ `(\|00⟩ + \|11⟩)/√2`. Còn gọi là cặp EPR. |
| **quy ước CNOT** | Quy ước dùng ở đây viết **điều khiển trước**, nên `CNOT(c, t)`. |
| **hạng Schmidt** | Xếp các biên độ thành ma trận 2×2. Hạng 1 là trạng thái tích; hạng 2 là rối. |

## Phép đo

| Thuật ngữ | Nghĩa là gì |
|---|---|
| **phép đo** | Làm trạng thái sụp về một trạng thái cơ sở và cho ra một bit cổ điển. Đây là bước duy nhất không khả nghịch. |
| **cơ sở** | Cặp trạng thái mà bạn đo đối chiếu. Mặc định là `{\|0⟩, \|1⟩}` trừ khi nói khác. |
| **tính toàn vẹn** (coherence) | Bao lâu chồng chập và mối quan hệ pha của nó còn sống trước khi nhiễu làm hỗn loạn chúng. |
| **suy hao** | Trạng thái không tới nơi vì bị hấp thụ hoặc tán xạ dọc đường đi. Khác với mất tính toàn vẹn ở trên. |

## Số học

| Thuật ngữ | Nghĩa là gì |
|---|---|
| **bộ bán cộng** (half-adder) | Mạch cộng hai bit **modulo 2** (`a XOR b`) và không giữ số nhớ, nên `1 + 1` đọc ra `0`. Một cổng `CNOT`. |
| **bộ cộng đầy đủ** (full adder) | Bộ bán cộng cộng thêm một cổng `Toffoli` tính **số nhớ**, nên `1 + 1 = 2` thay vì quấn về `0`. |
| **số nhớ** (carry) | Bit bằng `1` khi tổng tràn khỏi một bit: phép `AND` logic của hai đầu vào, được ghi lên một qubit dự phòng. |

## Mạng

| Thuật ngữ | Nghĩa là gì |
|---|---|
| **định lý không nhân bản** (no-cloning) | Không máy nào sao chép được một trạng thái lượng tử chưa biết tùy ý. Vì vậy mạng lượng tử không chuyển tiếp gói tin theo cách cổ điển. |
| **truyền tải lượng tử** (teleportation) | Chuyển một trạng thái bằng cách hủy bản gốc rồi dựng lại từ cặp rối dùng chung cộng hai bit cổ điển. Chuyển thông tin, không chuyển vật chất. |
| **trạm lặp** (repeater) | Nút nối các liên kết truyền tải lại với nhau để trạng thái vượt khoảng cách xa hơn. Nó *dựng lại*, không khuếch đại. |
| **liên kết** (link) | Một kết nối giữa hai nút. Truyền tải đi qua một liên kết; trạm lặp nối nhiều liên kết. |
| **độ trung thực** (fidelity) | Số từ 0 đến 1 đo hai trạng thái giống nhau đến đâu. 1.0 nghĩa là "giống hệt". |

## Mật mã

| Thuật ngữ | Nghĩa là gì |
|---|---|
| **cơ sở** (base) | Cặp trạng thái mà một qubit được viết trong đó. Cơ sở **Z** là `{\|0⟩, \|1⟩}`; cơ sở **X** là `{\|+⟩, \|−⟩}`. Một qubit chỉ mang bit tương đối với một cơ sở. |
| **BB84** | Giao thức phân phối khoá lượng tử đầu tiên: Alice và Bob mỗi người chọn một cơ sở ngẫu nhiên cho từng qubit, rồi **sàng lọc** — chỉ giữ những qubit mà cơ sở khớp nhau, và các bit đó là khoá chung. |
| **sàng lọc** (sifting) | Công bố *cơ sở* (không bao giờ công bố bit) và bỏ những qubit đo trong cơ sở khác. Khoảng một nửa sống sót. |
| **kẻ nghe lén** | Bất kỳ ai đọc các qubit trên đường truyền. Vì không thể sao chép, kẻ đó buộc phải đo rồi gửi lại, gây ra tỉ lệ lỗi khoảng **25%** trên khoá đã sàng lọc — đó là cách phát hiện. |

## Thuật toán

| Thuật ngữ | Nghĩa là gì |
|---|---|
| **hàm hằng số** | Hàm cho cùng một câu trả lời trên mọi đầu vào. |
| **hàm cân bằng** | Hàm cho `0` trên đúng một nửa số đầu vào và `1` trên nửa còn lại. |
| **phase kickback** | Mẹo biến giá trị của hàm thành một *dấu*: với thanh ghi dự phòng ở `\|−⟩`, oracle nhân mỗi nhánh với `(-1)^f(x)`. Hadamard sau đó biến dấu đó thành một bit. |
| **song song lượng tử** | Đánh giá hàm trên cả `2^n` đầu vào trong một lượt, bằng cách chạy oracle trên một chồng chập. Không thể đọc hết các câu trả lời — giao thoa mới là thứ trích ra một bit dùng được. |
| **khuếch đại biên độ** | Mẹo chung đứng sau Grover: phản xạ trạng thái để biên độ cần tìm lớn lên. |
| **khuếch tán** (diffusion) | Bước thứ hai của Grover, `2\|s⟩⟨s\| − I`: phản xạ mọi biên độ quanh giá trị trung bình, nâng biên độ được đánh dấu lên. |
| **vòng lặp Grover** | Một oracle cộng một khuếch tán. Khoảng `(π/4)·√N` vòng như vậy là tìm ra đáp án trong một danh sách không cấu trúc. |
| **tìm kiếm không cấu trúc** | Tìm trong một danh sách không có thứ tự để khai thác. Cổ điển trung bình `N/2` lần kiểm; Grover cần `(π/4)·√N` — tăng tốc **bậc hai**. |
| **tìm bậc** (order finding) | Tìm `r` nhỏ nhất với `a^r = 1 (mod N)` — chu kỳ của `a^x mod N`. Bước duy nhất Shor lấy được từ máy lượng tử. |
| **chu kỳ** (period) | Số `r` trong `a^(x+r) = a^x (mod N)`. |
| **biến đổi Fourier lượng tử** | Biến đổi Fourier rời rạc dưới dạng mạch. Nó biến một chồng chập tuần hoàn thành vài **đỉnh** nhọn tại các bội của `N/r`. |
| **phân số liên tục** | Cách cổ điển để đọc một phân số từ một đỉnh đo được: mẫu số của giản phân tốt nhất là chu kỳ `r`. |
| **chia thử** (trial division) | Phương pháp phân tích thừa số cổ điển ngây thơ: thử mọi ước số tới `√N`. Đúng, và vô vọng với `N` lớn. |

## Độ phức tạp và thuật toán

| Thuật ngữ | Nghĩa là gì |
|---|---|
| **Big-O** | `O(f)` nghĩa là tăng không nhanh hơn `f`, bỏ qua hằng số. |
| **đa thức** | Tăng như `b`, `b²`, `b³`. Gấp đôi đầu vào chỉ nhân công việc lên một hằng số nhỏ — xử lý được. |
| **hàm mũ** | Tăng như `2^b`. Thêm *một* bit có thể gấp đôi công việc — nhanh chóng vô vọng. |
| **dưới hàm mũ** | Nằm giữa hai loại trên: nhanh hơn mọi đa thức nhưng chậm hơn một hàm mũ đầy đủ. GNFS nằm ở đây. |
| **siêu đa thức** | Nhanh hơn mọi đa thức nhưng *không* nhất thiết là hàm mũ. Đây là một lớp khác với "dưới hàm mũ" — đừng nhầm hai cái. |
| **bậc hai** | Tăng như `b²`. Tăng tốc cỡ căn bậc hai: có thật, nhưng không phải hàm mũ. |
| **GNFS** | Sàng trường số tổng quát — cách *cổ điển* tốt nhất để phân tích thừa số. |
| **NISQ** | Noisy Intermediate-Scale Quantum. Máy thế hệ hiện tại: vài trăm qubit nhiễu, chưa sửa lỗi. |
| **oracle** | Hàm hộp đen được áp bên trong mạch. Dùng trong Deutsch–Jozsa và Grover. |

## Ký hiệu dùng xuyên suốt

| Ký hiệu | Ý nghĩa |
|---|---|
| <code⟩\|0⟩</code⟩, <code⟩\|1⟩</code⟩ | Hai trạng thái cơ sở của qubit |
| <code⟩\|ψ⟩</code⟩ | Một trạng thái một-qubit bất kỳ |
| <code⟩\|+⟩</code⟩, <code⟩\|−⟩</code⟩ | Hai chồng chập đều `(\|0⟩ ± \|1⟩)/√2` |
| <code⟩\|00⟩</code⟩ … <code⟩\|11⟩</code⟩ | Các trạng thái cơ sở hai qubit, đọc từ trái sang phải |
| `α`, `β` | Biên độ — xác suất là bình phương độ lớn của chúng |
| `H`, `X`, `Z`, `I`, `U` | Cổng Hadamard, Pauli-X, Pauli-Z, đơn vị, và cổng tổng quát |
| `CNOT(c,t)`, `CZ` | Cổng hai qubit; ở đây viết qubit điều khiển trước |
| `Toffoli(c,c,t)` | Cổng ba qubit — một phép `AND` khả nghịch; lật đích khi cả hai điều khiển bằng `1` |
| `U_f` | Oracle của một hàm: <code>\|x⟩\|y⟩ → \|x⟩\|y ⊕ f(x)⟩</code> |
| `QFT` | Biến đổi Fourier lượng tử |
| <code>\|s⟩</code> | Chồng chập đều trên mọi trạng thái cơ sở |
| `⊗` | Tích tensor |
| `P(0)`, `P(1)` | Xác suất đo, theo quy tắc Born |
| <code⟩\|⟨a\|b⟩\|²</code⟩ | Độ trung thực giữa hai trạng thái |

Bảng ký hiệu đầy đủ, kèm chương dùng ở đâu, nằm ở trang
[Tham chiếu](reference.vi.md).