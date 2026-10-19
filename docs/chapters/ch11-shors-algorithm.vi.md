# Chương 11 — Thuật toán Shor

!!! abstract "Trong một câu"
    Phân tích thừa số chỉ khó vì **tìm bậc** khó; một chồng chập tuần hoàn cộng với
    **biến đổi Fourier lượng tử** tìm ra bậc trong thời gian đa thức, rồi vài phép
    `gcd` biến bậc đó thành các thừa số.

## Phân tích thừa số, và vì sao nó khó

Phân tích thừa số một số lớn là bài toán làm nên tên tuổi của điện toán lượng tử.
Các phương pháp cổ điển tốt nhất — **sàng trường số tổng quát** — là *dưới hàm mũ*;
thuật toán Shor là *đa thức*. Cả chương chỉ nói về một phép quy giản và một mạch
lượng tử.

## Chia thử: mốc cổ điển trung thực

Sách bắt đầu bằng phương pháp ngây thơ, vì nó dễ tin: thử 2, rồi mọi số lẻ cho tới
`√N`, dừng ở ước số đầu tiên.

![Chia thử cổ điển: công việc tăng như sqrt(n)](../assets/ch11-classical-factor.png){ width="620" }

Nó đúng, và nó vô vọng: vòng lặp chạy khoảng `√N` lần, nên một số vài trăm chữ số
đã ngoài tầm với. Giá trị của nó ở đây là cột mốc cần vượt qua.

## Phép quy giản: phân tích thừa số trở thành tìm bậc

Ý tưởng của Shor là bạn không đi tìm ước số trực tiếp. Chọn `a` nguyên tố cùng nhau
với `N` và nhìn vào dãy

$$f(x) = a^x \bmod N$$

Dãy này **tuần hoàn**. Gọi chu kỳ của nó là `r`. Với `N = 15` và `a = 2`, các giá
trị chạy `1, 2, 4, 8, 1, 2, 4, 8, …` — chu kỳ bằng 4.

![Chu kỳ của 2^x mod 15 là 4](../assets/ch11-period-function.png){ width="620" }

Khi đã biết `r`, việc phân tích chỉ còn vài phép `gcd`:

1. nếu `r` lẻ, hoặc `a^(r/2) ≡ −1 (mod N)`, thì `a` này không may — chọn `a` khác
   và thử lại;
2. ngược lại hai thừa số là `gcd(a^(r/2) − 1, N)` và `gcd(a^(r/2) + 1, N)`.

Với `a = 2`, `r = 4`: `a^(r/2) = 4`, `gcd(4 − 1, 15) = 3`, và `15/3 = 5`. Xong.

Sách kiểm lại phép tính đó trên một ví dụ lớn hơn, tính tay:

$$a = 6,\quad N = 493,\quad r = 112,\quad 6^{56} \bmod 493 = 407$$

nên `gcd(407 − 1, 493) = 29` và `gcd(407 + 1, 493) = 17` — và đúng là
`493 = 17 × 29`. Hai snippet `jshell` trong thư mục chương 11 của sách chính là hai
phép kiểm đó; `ch11.classical.reduction_steps(6, 493)` tái tạo chúng trong một lần gọi.

Vấn đề là: tìm `r` bằng cổ điển cũng khó như phân tích thừa số, nên phép quy giản
này *tự nó* không đem lại gì. Thứ nó làm là cô lập bước duy nhất mà máy lượng tử làm
tốt — **tìm bậc** — và đó là phần còn lại của chương.

## Biến đổi Fourier lượng tử

Công cụ tìm chu kỳ là **biến đổi Fourier lượng tử** (QFT): biến đổi Fourier rời rạc
viết dưới dạng mạch. Trên một trạng thái cơ sở, nó trải một dốc pha:

$$\mathrm{QFT}\,|k\rangle = \frac{1}{\sqrt{N}}\sum_j e^{2\pi i j k / N} |j\rangle$$

![Mạch QFT ba qubit](../assets/ch11-qft-circuit.png){ width="620" }

Cho nó `|1⟩` và mọi đầu ra có cùng độ lớn, với pha quét tuyến tính từ 0 đến `2π`:

![QFT|1>: độ lớn đều, dốc pha tuyến tính](../assets/ch11-qft-phase.png){ width="620" }

Ma trận là ma trận Fourier quen thuộc `F[j, k] = e^(2πi j k / N)/√N` — đối xứng,
**unita**, và khả nghịch bằng cách chạy cùng mạch đó ngược lại. Tính khả nghịch đó
mới là điểm mấu chốt: đầu vào *tuần hoàn* chính là thứ mà QFT (nghịch đảo) biến
thành các đỉnh nhọn.

## Tìm bậc: chu kỳ thành các đỉnh

Ghép các mảnh lại. Hai thanh ghi:

- một thanh ghi **đếm** gồm `m` qubit, được đưa vào chồng chập đều bằng Hadamard —
  mọi số mũ `x` cùng lúc;
- một thanh ghi **công việc**, khởi tạo ở `|1⟩`, ghi lại `a^x mod N` nhờ các phép
  nhân modular được điều khiển `|y⟩ → |a^(2^j)·y mod N⟩`.

Lúc này thanh ghi đếm giữ một chồng chập **tuần hoàn**, và QFT nghịch đảo biến chu
kỳ đó thành một nhúm đỉnh đo được:

![Một mạch tìm bậc gọn](../assets/ch11-order-circuit.png){ width="620" }

![QFT nghịch đảo của thanh ghi tuần hoàn: bốn đỉnh](../assets/ch11-order-peaks.png){ width="620" }

Với `N = 15`, `a = 2`, các đỉnh nằm ở `0, 64, 128, 192` — cách nhau `2^m / r =
256/4 = 64`. Đọc một đỉnh là `k/r = outcome / 2^m` rồi đưa qua khai triển **phân số
liên tục**:

| Đo được | k/r = outcome / 2^m | Giản phân | Chu kỳ tìm được |
|---|---|---|---|
| 0 | 0 | `0/1` | — (k = 0) |
| 64 | 1/4 | `0/1 → 1/4` | **4** |
| 128 | 1/2 | `0/1 → 1/2` | — (k không nguyên tố cùng nhau với r) |
| 192 | 3/4 | `0/1 → 1/1 → 3/4` | **4** |

Hai đỉnh cho đáp án trực tiếp. Hai đỉnh còn lại có tử số chia sẻ ước với `r`, nên
giản phân cho một *ước* của `r` — và phép kiểm `a^r ≡ 1 (mod N)` bác bỏ nó. Shor chỉ
việc nhìn đỉnh khác. Đó là lý do thuật toán lặp lại một hai lần đo.

## Ghép Shor lại

| Bước | Làm gì | Cổ điển hay lượng tử |
|---|---|---|
| Tiền xử lý | chọn `a`; `gcd(a, N) > 1` thì đã có thừa số | cổ điển |
| Hadamard | mọi số mũ cùng lúc | lượng tử |
| Nhân modular có điều khiển | ghi `a^x mod N` vào thanh ghi công việc | lượng tử |
| QFT nghịch đảo | biến chu kỳ thành các đỉnh | lượng tử |
| Đo | đọc một đỉnh | lượng tử |
| Phân số liên tục | khôi phục `r` từ đỉnh | cổ điển |
| Guard và `gcd` | biến `r` thành các thừa số | cổ điển |

Phần lượng tử chỉ nằm ở giữa. Mọi thứ trước và sau là số học mà một máy tính xách
tay làm tức thì — đó là lý do chương này dành cả một mô-đun cho phép quy giản cổ
điển trước.

!!! warning "Nói thẳng về chi phí"
    Shor là **đa thức** theo số bit, nhưng hằng số và số qubit rất lớn: phân tích
    một số 2048 bit cần hàng nghìn qubit *logic* và hàng triệu cổng, và những qubit
    logic ấy lại cần sửa lỗi (mỗi cái tốn hàng nghìn qubit vật lý). Thuật toán phá
    mật mã khoá công khai hiện nay *về nguyên tắc*; chế tạo cỗ máy mới là phần khó,
    và mô phỏng này chỉ chạm tới `N` vài bit trước khi độ rộng thanh ghi làm nó bất
    khả thi.

## Sơ đồ

### Mốc cổ điển

![Chia thử cổ điển: công việc tăng như sqrt(n)](../assets/ch11-classical-factor.png){ width="620" }

![Chu kỳ của 2^x mod 15 là 4](../assets/ch11-period-function.png){ width="620" }

### Biến đổi Fourier lượng tử

![Mạch QFT ba qubit](../assets/ch11-qft-circuit.png){ width="620" }

![QFT|1>: độ lớn đều, dốc pha tuyến tính](../assets/ch11-qft-phase.png){ width="620" }

### Tìm bậc

![Một mạch tìm bậc gọn](../assets/ch11-order-circuit.png){ width="620" }

![QFT nghịch đảo của thanh ghi tuần hoàn: bốn đỉnh](../assets/ch11-order-peaks.png){ width="620" }

## Những điều cần nhớ

- Phân tích thừa số cổ điển tốn khoảng `√N` bằng chia thử, và dưới hàm mũ bằng sàng
  trường số; thuật toán Shor là **đa thức**.
- Phân tích thừa số quy giản về **tìm bậc**: chu kỳ `r` của `a^x mod N` cho các thừa
  số qua `gcd(a^(r/2) ± 1, N)`, thử lại nếu `r` lẻ hoặc `a^(r/2) ≡ −1`.
- **QFT** là biến đổi Fourier dưới dạng mạch: unita, khả nghịch, và nó biến một
  thanh ghi *tuần hoàn* thành vài **đỉnh** nhọn tại các bội của `2^m / r`.
- **Tìm bậc** dựng một chồng chập tuần hoàn bằng các phép nhân modular có điều khiển
  rồi đọc chu kỳ từ các đỉnh của QFT nghịch đảo.
- Khôi phục `r` là phần cổ điển: **phân số liên tục** của `outcome / 2^m`, kiểm tra
  bằng `a^r ≡ 1 (mod N)`.
- Shor là đa thức, nhưng tài nguyên đòi hỏi khổng lồ; thuật toán quan trọng vì *nó
  làm cho cái gì trở nên rẻ*, và sửa lỗi mới là thứ biến nó thành hiện thực.

## Mã nguồn của chương này

Ba mẫu, từ mốc cổ điển tới thuật toán:

- [`ch11/classical.py`](https://github.com/phonhay103/quantum-computing-in-action/blob/main/src/quantum_computing_in_action/ch11/classical.py)
  — hai mẫu ``classicfactor`` và ``semiclassicfactor``: chia thử, phép quy giản,
  `gcd(a^(r/2) ± 1, N)`, và phép tìm chu kỳ cổ điển.
- [`ch11/qft.py`](https://github.com/phonhay103/quantum-computing-in-action/blob/main/src/quantum_computing_in_action/ch11/qft.py)
  — biến đổi Fourier lượng tử: mạch, ma trận, và dốc pha mà nó đặt lên `|1⟩`.
- [`ch11/shor.py`](https://github.com/phonhay103/quantum-computing-in-action/blob/main/src/quantum_computing_in_action/ch11/shor.py)
  — mẫu ``quantumfactor``: nhân modular, mạch tìm bậc, QFT nghịch đảo, phân số liên
  tục, và các thừa số của 15 và 21.

Chạy toàn bộ bằng `make ch11`, hoặc từng mẫu một:

```bash
uv run python -m quantum_computing_in_action.ch11.shor
```
