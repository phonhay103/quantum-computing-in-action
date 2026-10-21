# Thuật ngữ

Bảng dưới đây tập hợp mọi thuật ngữ mà các chương sử dụng, nhóm theo chủ đề và
sắp xếp theo thứ tự khái niệm xuất hiện. Bản tiếng Anh có đúng những hàng này
theo cùng thứ tự, nên việc đổi ngôn ngữ (bộ chọn ngôn ngữ nằm ở thanh trên cùng)
không làm thay đổi vị trí đang đọc.

Những thuật ngữ được chương đánh dấu **lần đầu** cũng được giải thích ngắn gọn
ngay tại chỗ xuất hiện. Vì vậy, trang này là tài liệu tham khảo hợp nhất để quay
lại mỗi khi một định nghĩa đã mờ đi.

## Các khối xây dựng

Các thuật ngữ dưới đây mô tả một qubit duy nhất: đối tượng mà mọi phần sau đó
đều được xây dựng từ nó.

| Thuật ngữ | Nghĩa là gì |
|---|---|
| **bit** | Một đơn vị thông tin cổ điển chỉ nhận một trong hai giá trị, `0` hoặc `1`. Bit giữ đúng một giá trị tại một thời điểm, và việc đọc nó không làm thay đổi giá trị đó — chính sự bền vững khi đọc lại nhiều lần là điểm phân biệt thông tin cổ điển với thông tin lượng tử. |
| **qubit** | Phiên bản lượng tử hoá của bit. Một qubit có thể ở `\|0⟩` hoặc `\|1⟩`, nhưng — khác với bit — nó còn có thể ở *tổ hợp có trọng số* của cả hai cùng lúc, một khả năng mà các hệ quả của nó chi phối phần còn lại của bảng thuật ngữ này. |
| **trạng thái cơ sở** | Một trong các trạng thái được đặt tên mà hệ thống được mô tả dựa trên đó; với một qubit, đó là `\|0⟩` và `\|1⟩`. Mọi trạng thái khác của hệ thống đều được biểu diễn dưới dạng tổng có trọng số của các trạng thái cơ sở, và vì vậy cơ sở được chọn một lần rồi giữ nguyên. |
| **ket** | Ký hiệu `\|ψ⟩` dùng để gọi tên một trạng thái. Bản thân ket không chứa thông tin và chỉ là một nhãn; nội dung vật lý của trạng thái nằm ở các con số đứng trước nhãn đó. |
| **biên độ** | Con số nhân với một trạng thái cơ sở trong tổng có trọng số nói trên. Biên độ không phải là xác suất: nó có thể âm, thậm chí là số phức, và chỉ nhận ý nghĩa xác suất thông qua quy tắc Born bên dưới. |
| **quy tắc Born** | Quy tắc biến biên độ thành xác suất: xác suất của một kết quả đo được cho bởi bình phương độ lớn của biên độ tương ứng. Đây là cầu nối giữa các biên độ mang dấu, số phức và các xác suất không âm thực sự đo được. |
| **chuẩn hoá** | Điều kiện yêu cầu các bình phương biên độ của một trạng thái cộng lại đúng bằng 1, để quy tắc Born cho ra một phân phối xác suất hợp lệ trên mọi kết quả có thể. |
| **chồng chập** (superposition) | Trạng thái đồng thời là tổ hợp có trọng số của các trạng thái cơ sở; nó không phải là trạng thái cơ sở này hay trạng thái cơ sở kia, mà là sự pha trộn nhất quán của cả hai, với trọng số chính là các biên độ đã định nghĩa ở trên. |
| **pha** | Góc đi kèm với một biên độ. Pha của một biên độ đơn lẻ không quan sát được; chỉ *pha tương đối* giữa hai phần của cùng một trạng thái mới cho ra hệ quả đo được, và vì vậy chính pha tương đối đó là thứ các phần sau theo dõi. |
| **giao thoa** | Hiệu ứng xảy ra khi hai phần của một trạng thái được kết hợp: tuỳ theo pha tương đối mà chúng cường hoá lẫn nhau hay triệt tiêu nhau. Giao thoa là cơ chế mà các thuật toán lượng tử dùng để trích ra một câu trả lời dùng được từ một chồng chập. |

## Cổng và mạch

Các thuật ngữ dưới đây nói về cách qubit bị tác động: bản thân các cổng, tính
khả nghịch làm nền cho chúng, và các sơ đồ mà phép tác động được vẽ trong đó.

| Thuật ngữ | Nghĩa là gì |
|---|---|
| **cổng** (gate) | Phép toán khả nghịch tác động lên một hay nhiều qubit. Mỗi cổng trong các chương này được viết dưới dạng ma trận, và việc áp dụng cổng lên một trạng thái tương ứng với nhân ma trận đó vào vector biên độ của trạng thái. |
| **khả nghịch** | Đặc tính định hình của cổng lượng tử: luôn có một cổng khác hoàn tác được nó. Tính khả nghịch có nghĩa là không thông tin nào bị vứt bỏ ở bất kỳ đâu trong mạch; chỉ có phép đo (bên dưới) phá vỡ quy tắc này. |
| **unita** (unitary) | Ma trận thỏa mãn `U^† U = I`. Tính unita là *lý do* cổng khả nghịch và giữ được chuẩn hoá: phép biến đổi bảo toàn tổng bình phương biên độ, nên kết quả thu được vẫn là một trạng thái hợp lệ. |
| **Pauli-X** | Cổng `X` — là phép `NOT` lượng tử. Nó lật `\|0⟩ ↔ \|1⟩`, tức hoán đổi hai biên độ với nhau, và ngoài phần hoán đổi đó không thay đổi gì thêm ở trạng thái. |
| **Hadamard** | Cổng `H` — cách chuẩn để tạo một chồng chập đều, và cũng là cách chuẩn để biến chồng chập như vậy trở lại thành một trạng thái cơ sở. Cổng này là nghịch đảo của chính nó, nên áp dụng hai lần là hoàn tác, yếu tố được các mạch ở chương sau dùng đi dùng lại. |
| **Pauli-Z** | Cổng `Z`. Nó lật **pha** của `\|1⟩` mà không chạm vào giá trị bit, và vì vậy được đối chiếu xuyên suốt với `X` — cổng lật giá trị bit nhưng không lật pha. |
| **CNOT** | Cổng hai qubit gồm một qubit **điều khiển** và một qubit **đích**. Qubit đích bị lật đúng khi qubit điều khiển bằng `1`, và được giữ nguyên trong trường hợp ngược lại; chính hành vi có điều kiện đó cho phép trạng thái của một qubit phụ thuộc vào qubit kia. |
| **CZ** | Controlled-Z. Nó được bố trí giống `CNOT`, cùng gồm điều khiển và đích, nhưng lật *pha* của qubit đích thay vì bit của nó; hệ quả của một phép lật pha như vậy chỉ hiện ra sau khi đổi cơ sở. |
| **Toffoli** | Cổng ba qubit (`CCNOT`), lật qubit đích chỉ khi **cả hai** qubit điều khiển bằng `1`. Nó thực hiện phép `AND` khả nghịch, và nhờ đó nối các cổng khả nghịch ở phần này với các mạch số học bên dưới. |
| **đơn vị** | `I`, ma trận không làm gì cả với bất kỳ trạng thái nào. Hai cổng `X` liên tiếp hợp thành `I`, hai cổng `H` cũng vậy; những đồng nhất thức kiểu này là cách mạch được kiểm tra và rút gọn. |
| **mạch** | Sơ đồ được đọc từ trái sang phải: mỗi dây là một qubit, mỗi ô là một cổng tác động tại thời điểm đó, và mỗi đồng hồ ở mép phải là một phép đo kết thúc đầu ra cổ điển. |
| **lần chạy** (shots) | Chạy lại cùng một mạch nhiều lần để đếm các kết quả, nhờ đó xác suất được ước lượng từ tần suất quan sát được thay vì đọc trực tiếp. |

## Nhiều qubit

Các thuật ngữ dưới đây mô tả điều gì xảy ra khi hai qubit được xét cùng nhau
thay vì từng qubit một.

| Thuật ngữ | Nghĩa là gì |
|---|---|
| **tích tensor** | `⊗`, phép toán kết hợp hai trạng thái một qubit thành một trạng thái chung duy nhất. Việc kết hợp không phải là nối chuỗi nhãn đơn giản: các biên độ nhân theo từng cặp, và trạng thái chung thu được mang một biên độ cho mỗi cặp kết quả cổ điển. |
| **trạng thái tích** | Trạng thái chung *viết được* thành trạng thái của qubit này nhân với trạng thái của qubit kia. Khi đó hai qubit hoàn toàn độc lập: việc đo một qubit không cho biết điều gì về qubit còn lại. |
| **rối** | Trạng thái chung *không* viết được ở dạng tích như vậy. Khi đó không qubit nào có trạng thái riêng của chính nó; phần mô tả nằm trọn trong các biên độ chung, và các kết quả đo của hai qubit trở nên tương quan. |
| **trạng thái Bell** | Cặp rối cực đại, ví dụ `(\|00⟩ + \|11⟩)/√2`. Còn gọi là cặp EPR, và các cặp như vậy là tài nguyên bị tiêu hao trong truyền tải lượng tử (xem phần Mạng). |
| **quy ước CNOT** | Quy ước dùng ở đây viết **điều khiển trước**, nên `CNOT(c, t)`: vị trí thứ nhất chứa qubit có giá trị được đọc, vị trí thứ hai chứa qubit có giá trị bị lật. |
| **hạng Schmidt** | Xếp các biên độ chung thành ma trận 2×2 rồi tính hạng của nó. Hạng 1 cho biết trạng thái tích; hạng 2 cho biết trạng thái rối, nhờ đó sự phân biệt nói trên trở thành một bài toán đại số tuyến tính thay vì trực giác. |

## Phép đo

Các thuật ngữ dưới đây nói về bước kết thúc một chồng chập và cho ra một câu
trả lời cổ điển.

| Thuật ngữ | Nghĩa là gì |
|---|---|
| **phép đo** | Hành động làm trạng thái sụp về một trạng thái cơ sở — được chọn theo các xác suất của quy tắc Born — và cho ra một bit cổ điển. Đây là bước duy nhất trong phép tính không khả nghịch, và vì vậy đánh dấu ranh giới giữa phần lượng tử và phần cổ điển của mạch. |
| **cơ sở** | Cặp trạng thái mà phép đo được thực hiện đối chiếu; mặc định là `{\|0⟩, \|1⟩}` trừ khi nói khác. Cùng một qubit được đo trong một cơ sở khác sẽ cho các kết quả khác, và chính phụ thuộc đó là điều phần Mật mã khai thác. |
| **tính toàn vẹn** (coherence) | Khoảng thời gian mà một chồng chập cùng các quan hệ pha bên trong nó còn tồn tại trước khi nhiễu làm hỗn loạn chúng. Khi tính toàn vẹn mất đi, chồng chập giảm thành hỗn hợp cổ điển, và giao thoa không thể được khai thác nữa. |
| **suy hao** | Tình huống trạng thái không bao giờ tới nơi, vì đã bị hấp thụ hoặc tán xạ dọc đường đi. Suy hao biểu hiện là sự vắng mặt của tín hiệu đo, và khác với việc mất tính toàn vẹn được mô tả ở dòng trên. |

## Số học

Những thuật ngữ này cho thấy các cổng khả nghịch được giới thiệu ở trên được
lắp ráp thành phép cộng kiểu cổ điển như thế nào.

| Thuật ngữ | Nghĩa là gì |
|---|---|
| **bộ bán cộng** (half-adder) | Mạch cộng hai bit **modulo 2** — giá trị `a XOR b`, được tính bằng một cổng `CNOT` duy nhất — trong khi không giữ số nhớ. Kết quả là `1 + 1` đọc ra `0`: mạch hoàn chỉnh về phép cộng nhưng chưa hoàn chỉnh về hành vi số học. |
| **bộ cộng đầy đủ** (full adder) | Bộ bán cộng được mở rộng thêm một cổng `Toffoli` tính **số nhớ** ra một đầu ra riêng, nên `1 + 1` cho đúng kết quả `2` thay vì quấn về `0`. Nói cách khác, tổng và số nhớ được trả về cùng lúc. |
| **số nhớ** (carry) | Bit bằng `1` đúng khi một tổng tràn khỏi một bit duy nhất: phép `AND` logic của hai đầu vào, được ghi lên một qubit dự phòng. Đây là lý do một cổng `AND` khả nghịch — `Toffoli` nói ở trên — là đủ để tính số nhớ. |

## Mạng

Những thuật ngữ này nói về những gì định lý không nhân bản hàm ý cho việc gửi
các trạng thái lượng tử giữa các nút.

| Thuật ngữ | Nghĩa là gì |
|---|---|
| **định lý không nhân bản** (no-cloning) | Phát biểu rằng không máy nào sao chép được một trạng thái lượng tử chưa biết tùy ý. Chính sự không thể đó khiến mạng lượng tử không thể chuyển tiếp gói tin theo cách cổ điển, vì một bản sao của nội dung gói tin không thể được tạo ra giữa đường truyền. |
| **truyền tải lượng tử** (teleportation) | Chuyển một trạng thái bằng cách hủy bản gốc rồi dựng lại nó ở điểm đến từ cặp rối dùng chung cộng hai bit cổ điển. Thông tin là thứ được chuyển, không phải vật chất: bản thân trạng thái không bao giờ nằm trên đường truyền giữa hai nút. |
| **trạm lặp** (repeater) | Nút nối các liên kết truyền tải kế tiếp nhau lại với nhau để một trạng thái vượt được tổng khoảng cách dài hơn. Điểm mấu chốt là nó *dựng lại*, không khuếch đại; việc khuếch đại một trạng thái đang di chuyển sẽ đồng nghĩa với bản sao bị cấm. |
| **liên kết** (link) | Một kết nối giữa hai nút kề nhau. Một lần truyền tải đi qua đúng một liên kết; trạm lặp là thiết bị nối nhiều liên kết thành một đường đi dài hơn. |
| **độ trung thực** (fidelity) | Số nằm giữa 0 và 1 đo hai trạng thái giống nhau đến đâu. Giá trị 1.0 nghĩa là "giống hệt"; đại lượng này xuất hiện chính thức dưới dạng `\|⟨a\|b⟩\|²` trong bảng ký hiệu bên dưới. |

## Mật mã

Các thuật ngữ dưới đây mô tả giao thức phân phối khoá lượng tử đầu tiên và cách
lập luận bảo mật của nó.

| Thuật ngữ | Nghĩa là gì |
|---|---|
| **cơ sở** (base) | Cặp trạng thái mà một qubit được viết trong đó và được đọc đối chiếu với đó. Cơ sở **Z** là `{\|0⟩, \|1⟩}`; cơ sở **X** là `{\|+⟩, \|−⟩}`. Một qubit chỉ mang bit tương đối với một cơ sở, và nếu cùng qubit đó được đọc trong cơ sở kia thì kết quả thu được trông ngẫu nhiên. |
| **BB84** | Giao thức phân phối khoá lượng tử đầu tiên. Alice và Bob mỗi người chọn ngẫu nhiên một cơ sở cho từng qubit; sau đó họ **sàng lọc** — chỉ giữ những qubit mà cơ sở trùng nhau — và các bit từ nhóm qubit đó hợp thành khoá chung bí mật. |
| **sàng lọc** (sifting) | Bước công bố *cơ sở* (không bao giờ công bố giá trị bit) và loại bỏ mọi qubit được đo trong cơ sở khác. Khoảng một nửa số qubit truyền đi sống sót, và chính nhóm sống sót đó hợp thành khoá chung thô. |
| **kẻ nghe lén** | Bất kỳ ai đọc các qubit trong lúc chúng nằm trên đường truyền. Vì sao chép là không thể, hành vi đó buộc phải đo rồi gửi lại, gây ra tỉ lệ lỗi khoảng **25%** trên khoá đã sàng lọc; chính tỉ lệ lỗi cao đột ngột này là tín hiệu phát hiện. |

## Thuật toán

Các thuật ngữ này bao gồm những khối xây dựng thuật toán được Deutsch–Jozsa,
Grover và Shor sử dụng.

| Thuật ngữ | Nghĩa là gì |
|---|---|
| **hàm hằng số** | Hàm cho cùng một câu trả lời trên mọi đầu vào, nên mọi giá trị ra đều trùng nhau. Đây là một trong hai loại hàm được thuật toán oracle đầu tiên phân biệt. |
| **hàm cân bằng** | Hàm cho `0` trên đúng một nửa số đầu vào và `1` trên nửa còn lại. Cùng với các hàm hằng số, nó tạo thành loại thứ hai để oracle được thử nghiệm. |
| **phase kickback** | Mẹo biến giá trị của một hàm thành một *dấu*: khi thanh ghi dự phòng ở `\|−⟩`, oracle nhân mỗi nhánh của chồng chập với `(-1)^f(x)`. Các cổng Hadamard áp dụng sau đó biến bức tranh dấu đó thành một bit đọc được. |
| **song song lượng tử** | Đánh giá một hàm trên cả `2^n` đầu vào chỉ trong một lượt, bằng cách chạy oracle trên một chồng chập đều của các đầu vào. Các câu trả lời song song không thể được đọc hết cùng lúc; chính giao thoa mới trích ra từ chúng một bit dùng được. |
| **khuếch đại biên độ** | Mẹo chung đứng sau Grover: trạng thái được phản xạ lặp đi lặp lại để biên độ của các phần tử mong muốn lớn lên, trong khi mọi biên độ khác nhỏ đi. Vòng lặp Grover bên dưới là hiện thực cụ thể của mẹo này. |
| **khuếch tán** (diffusion) | Bước thứ hai của Grover, toán tử `2\|s⟩⟨s\| − I`: phản xạ mọi biên độ quanh giá trị trung bình, trong đó biên độ được đánh dấu được nâng lên trên mức trung bình, còn mọi biên độ khác bị đẩy xuống dưới. |
| **vòng lặp Grover** | Một lần áp dụng oracle cộng một bước khuếch tán. Khoảng `(π/4)·√N` vòng như vậy là đủ để tìm ra đáp án trong một danh sách `N` phần tử không cấu trúc. |
| **tìm kiếm không cấu trúc** | Tìm kiếm trong một danh sách không có thứ tự để khai thác. Theo phương pháp cổ điển cần trung bình `N/2` lần kiểm, trong khi Grover cần `(π/4)·√N` vòng — một tăng tốc **bậc hai**, chứ không phải hàm mũ. |
| **tìm bậc** (order finding) | Tìm `r` nhỏ nhất thỏa mãn `a^r = 1 (mod N)` — tức chu kỳ của `a^x mod N`. Đây là bước duy nhất của thuật toán Shor đòi hỏi thực sự máy tính lượng tử. |
| **chu kỳ** (period) | Giá trị `r` trong quan hệ `a^(x+r) = a^x (mod N)`: khoảng cách mà sau đó dãy lũy thừa của `a` lặp lại chính nó. |
| **biến đổi Fourier lượng tử** | Biến đổi Fourier rời rạc được hiện thực thành một mạch. Biến đổi này chuyển một chồng chập tuần hoàn thành vài **đỉnh** nhọn đặt tại các bội của `N/r`, và chu kỳ được đọc ra từ các đỉnh đó. |
| **phân số liên tục** | Cách cổ điển để đọc một phân số ra từ một đỉnh đo được: mẫu số của giản phân tốt nhất là chu kỳ `r`. Bước hậu xử lý này hoàn tất thuật toán Shor. |
| **chia thử** (trial division) | Phương pháp cổ điển ngây thơ nhất để phân tích thừa số: thử mọi ước số tới `√N`. Phương pháp này đúng, nhưng vô vọng với `N` lớn, vì thời gian chạy của nó lớn như căn bậc hai của chính `N`. |

## Độ phức tạp và thuật toán

Những thuật ngữ này quy định vốn từ vựng dùng để so sánh thời gian chạy của
các phương pháp cổ điển và lượng tử.

| Thuật ngữ | Nghĩa là gì |
|---|---|
| **Big-O** | `O(f)` nghĩa là tăng trưởng không nhanh hơn `f`, bỏ qua các hằng số. Đây là ký hiệu dùng trong các chương này để phát biểu chi phí của các phương pháp cổ điển và lượng tử nói ở trên. |
| **đa thức** | Tăng trưởng như `b`, `b²`, `b³`. Gấp đôi đầu vào chỉ nhân lượng công việc với một hằng số nhỏ, và vì vậy dạng tăng trưởng này được coi là xử lý được. |
| **hàm mũ** | Tăng trưởng như `2^b`. Chỉ thêm *một* bit vào đầu vào có thể làm gấp đôi công việc, và do đó chi phí nhanh chóng trở nên vô vọng. |
| **dưới hàm mũ** | Nằm giữa hai loại ngay trước đó: nhanh hơn mọi đa thức nhưng chậm hơn một hàm mũ đầy đủ. Chính trong vùng này mà GNFS bên dưới nằm. |
| **siêu đa thức** | Nhanh hơn mọi đa thức nhưng *không* nhất thiết là hàm mũ. Đây là lớp khác với "dưới hàm mũ", và hai lớp này không được phép nhầm lẫn với nhau. |
| **bậc hai** | Tăng trưởng như `b²`. Một tăng tốc cỡ căn bậc hai là có thật và đáng giá, nhưng nó không vượt qua ranh giới đa thức/hàm mũ. |
| **GNFS** | Sàng trường số tổng quát — cách *cổ điển* được biết đến tốt nhất để phân tích thừa số một số nguyên, và là mốc so sánh với kết quả lượng tử nói ở trên. |
| **NISQ** | Noisy Intermediate-Scale Quantum. Tên gọi dành cho các máy thuộc thời đại hiện tại: vài trăm qubit dễ lỗi, chưa có sự sửa lỗi nào khả dụng. |
| **oracle** | Hàm hộp đen được áp dụng bên trong mạch, dưới dạng unita `U_f`. Đây là cấu trúc truy vấn được dùng trong Deutsch–Jozsa và trong Grover. |

## Ký hiệu dùng xuyên suốt

Các ký hiệu sau lặp lại qua các chương; mỗi ký hiệu được liệt kê cùng với ý
nghĩa đã được thiết lập của nó.

| Ký hiệu | Ý nghĩa |
|---|---|
| <code>\|0⟩</code>, <code>\|1⟩</code> | Hai trạng thái cơ sở của qubit, mà mọi trạng thái một qubit được viết dựa trên đó |
| <code>\|ψ⟩</code> | Một trạng thái một-qubit bất kỳ, được viết dưới dạng một ket |
| <code>\|+⟩</code>, <code>\|−⟩</code> | Hai chồng chập đều `(\|0⟩ ± \|1⟩)/√2`, hợp thành cơ sở X |
| <code>\|00⟩</code> … <code>\|11⟩</code> | Các trạng thái cơ sở hai qubit, đọc từ trái sang phải |
| `α`, `β` | Biên độ; các xác suất tương ứng là bình phương độ lớn của chúng, theo quy tắc Born |
| `H`, `X`, `Z`, `I`, `U` | Các cổng Hadamard, Pauli-X, Pauli-Z, đơn vị, và cổng tổng quát |
| `CNOT(c,t)`, `CZ` | Các cổng hai qubit; ở đây qubit điều khiển được viết trước |
| `Toffoli(c,c,t)` | Cổng ba qubit — một phép `AND` khả nghịch; lật qubit đích khi cả hai qubit điều khiển bằng `1` |
| `U_f` | Oracle của một hàm: <code>\|x⟩\|y⟩ → \|x⟩\|y ⊕ f(x)⟩</code> |
| `QFT` | Biến đổi Fourier lượng tử, trình bày ở phần Thuật toán |
| <code>\|s⟩</code> | Chồng chập đều trên mọi trạng thái cơ sở |
| `⊗` | Tích tensor — phép toán ghép các qubit vào một trạng thái chung |
| `P(0)`, `P(1)` | Các xác suất đo, thu được bằng cách áp dụng quy tắc Born |
| <code>\|⟨a\|b⟩\|²</code> | Độ trung thực giữa hai trạng thái |

Bảng ký hiệu đầy đủ, kèm chương dùng ở đâu, nằm ở trang
[Tham chiếu](reference.vi.md).
