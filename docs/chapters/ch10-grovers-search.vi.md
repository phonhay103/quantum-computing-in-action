# Chương 10 — Thuật toán tìm kiếm của Grover

!!! abstract "Trong một câu"
    Với một danh sách không cấu trúc và chỉ có một phép thử nhận ra đáp án, Grover
    tìm ra nó trong khoảng `(π/4)·√N` bước thay vì `N/2` của cổ điển — một tăng tốc
    **bậc hai**, và là mức tốt nhất mà một danh sách không cấu trúc cho phép.

## Tìm kiếm không cấu trúc

Ví dụ của sách là một danh bạ nhỏ và một câu hỏi — *ai 29 tuổi và sống ở Mexico?*
Không có khoá đã sắp xếp để tìm kiếm nhị phân, nên một chương trình cổ điển chỉ có
thể nhìn, lần lượt từng mục:

| Mục | Tên | Tuổi | Quốc gia |
|---|---|---|---|
| 0 | Alice | 42 | Nigeria |
| 1 | Bob | 36 | Australia |
| 2 | Eve | 85 | USA |
| 3 | Niels | 18 | Greece |
| **4** | **Albert** | **29** | **Mexico** |
| 5 | Roger | 29 | Belgium |
| 6 | Marie | 15 | Russia |
| 7 | Janice | 52 | China |

Mục khớp ở vị trí 4, nên phép quét cần 5 lần thử. Xáo trộn danh sách thì mục tiêu
rơi vào mỗi vị trí đều nhau, cho trung bình `(1 + 2 + … + 8)/8 = 4.5` lần thử. Con
số 4.5 đều đặn đó là mức Grover phải vượt.

![Phép quét cổ điển: mất bao nhiêu lần thử để tìm mục tiêu](../assets/ch10-classical-tries.png){ width="560" }

## Oracle: một dấu, và không gì khác

Grover không bao giờ nhìn thấy danh sách. Nó chỉ nhận một **oracle** nhận ra đáp
án, và điều duy nhất oracle được phép làm là *đánh dấu* trạng thái cần tìm bằng
một **lần lật pha**:

$$U_w : |x\rangle \longrightarrow (-1)^{[x = w]}\,|x\rangle$$

Với hai qubit và `|11⟩` được đánh dấu, đó là một ma trận chéo chỉ có một số `-1`:

![Oracle của Grover: một lần lật dấu, không đo được gì](../assets/ch10-oracle-matrix.png){ width="420" }

Một dấu tự nó là vô hình. Pha toàn cục không có ý nghĩa gì, và đo `|x⟩` trước và
sau oracle cho cùng một biểu đồ. Toàn bộ công việc của Grover là biến một dấu ẩn
này thành một xác suất lớn.

## Khuếch tán: phản xạ quanh giá trị trung bình

Bước thứ hai là **khuếch tán**, một phép phản xạ mọi biên độ quanh giá trị trung
bình:

$$D = H^{\otimes n}\bigl(2|0\rangle\langle 0| - I\bigr)H^{\otimes n} = 2|s\rangle\langle s| - I$$

Áp sau oracle, nó đặt mỗi biên độ `a → 2·mean − a`. Trạng thái được đánh dấu, thứ
mà oracle đẩy *xuống dưới* giá trị trung bình, là trạng thái duy nhất lật trở lại
*lên trên* nó; còn các trạng thái khác chìm xuống. Lặp lại cặp bước này và biên độ
của trạng thái đánh dấu lớn dần mỗi vòng.

## Từng bước trên hai qubit

Hai qubit cho bốn trạng thái — đủ ít để in ra mọi biên độ sau mỗi vòng. Đánh dấu
`|11⟩` và bắt đầu đều nhau, mọi biên độ bằng `1/2`:

| Vòng | `00` | `01` | `10` | `11` đánh dấu |
|---|---|---|---|---|
| sau 0 vòng | +0.50 | +0.50 | +0.50 | +0.50 |
| sau 1 vòng | 0.00 | 0.00 | 0.00 | **+1.00** |
| sau 2 vòng | −0.50 | −0.50 | −0.50 | +0.50 |

Đọc theo ba bước:

1. **Oracle** lật dấu của biên độ được đánh dấu: `+0.50 → −0.50`. Trung bình của
   bốn biên độ rơi từ `0.50` xuống `0.25`.
2. **Khuếch tán** phản xạ quanh trung bình đó: `0.50 → 2(0.25) − 0.50 = 0` và
   `−0.50 → 2(0.25) + 0.50 = 1`. Một vòng và trạng thái đánh dấu giữ **toàn bộ**
   xác suất.
3. **Vòng thứ hai** xoay vượt qua đáp án — trở lại `1/4` — đó là hiện tượng vọt
   quá. Chạy Grover quá lâu sẽ làm kết quả tệ đi.

![Grover trên 2 qubit: trạng thái đánh dấu lấy hết xác suất](../assets/ch10-step-by-step.png){ width="620" }

## Grover trên 64 mục

Mở rộng lên sáu qubit (`N = 64`), đánh dấu một trạng thái, và mỗi vòng là một phép
xoay nhỏ của cả vector biên độ. Xác suất của đáp án tuân theo
`sin²((2k+1)θ)` với `sin θ = 1/√N`:

| Vòng | 0 | 1 | 2 | 3 | 4 | 5 | **6** | 7 | 8 | 9 |
|---|---|---|---|---|---|---|---|---|---|---|
| P(đáp án) | 0.02 | 0.13 | 0.34 | 0.59 | 0.82 | 0.96 | **1.00** | 0.91 | 0.72 | 0.47 |

![Grover trên 64 mục: xác suất tăng rồi vọt quá](../assets/ch10-grover-curve.png){ width="620" }

Đỉnh nằm ở 6 vòng — `floor((π/4)·√64)` — trong khi phép quét cổ điển cần trung
bình `32` lần thử. Đo 2000 lần, đáp án trở về áp đảo:

![64 kết quả sau 6 vòng: đáp án chiếm ưu thế](../assets/ch10-grover-outcomes.png){ width="620" }

![Một mạch Grover nhỏ](../assets/ch10-grover-circuit.png){ width="620" }

Mạch chính là cả vòng lặp, lặp lại: `H` trên mọi qubit một lần, rồi mỗi vòng một
cặp **oracle / khuếch tán**. Khối `H, X, MCZ, X, H` ở mỗi vòng là phép phản xạ quanh
giá trị trung bình; còn phép lật pha đơn lẻ là oracle.

## Tăng tốc lớn đến đâu?

| Số mục `N` | Cổ điển (trung bình) | Số vòng Grover |
|---|---|---|
| 8 | 4.5 | 2 |
| 64 | 32 | 6 |
| 1 000 000 | 500 000 | 785 |

Quy luật là `N/2` so với `(π/4)·√N`: **bậc hai**, không phải hàm mũ. Gấp đôi danh
sách thì công việc cổ điển nhân bốn nhưng công việc lượng tử chỉ nhân khoảng
`√2`. Đó là kích thước trung thực của món quà Grover — có thật, hữu ích, và khiêm
tốn — và nó được chứng minh là mức tốt nhất có thể cho một danh sách không có cấu
trúc để khai thác.

!!! note "Tăng tốc đến từ đâu"
    Grover không thử các mục song song rồi đọc hết câu trả lời ra — một phép đo
    chỉ trả về một trạng thái cơ sở. Nó chạy oracle **một lần mỗi vòng** trên cả
    chồng chập và để *giao thoa* dồn xác suất lại. Độ lợi là căn bậc hai vì mỗi
    vòng là thêm một phép xoay của vector biên độ, và vector ấy chỉ cần xoay một
    phần tư vòng để chỉ vào đáp án.

## Sơ đồ

### Mốc cổ điển

![Phép quét cổ điển: mất bao nhiêu lần thử để tìm mục tiêu](../assets/ch10-classical-tries.png){ width="560" }

### Oracle

![Oracle của Grover: một lần lật dấu, không đo được gì](../assets/ch10-oracle-matrix.png){ width="420" }

### Từng bước

![Grover trên 2 qubit: trạng thái đánh dấu lấy hết xác suất](../assets/ch10-step-by-step.png){ width="620" }

### Grover trên 64 mục

![Một mạch Grover nhỏ](../assets/ch10-grover-circuit.png){ width="620" }

![Grover trên 64 mục: xác suất tăng rồi vọt quá](../assets/ch10-grover-curve.png){ width="620" }

![64 kết quả sau 6 vòng: đáp án chiếm ưu thế](../assets/ch10-grover-outcomes.png){ width="620" }

## Những điều cần nhớ

- **Tìm kiếm không cấu trúc** không có khoá đã sắp xếp để khai thác: cổ điển tốn
  `N/2` phép thử trung bình, và không có cách cổ điển nào tốt hơn.
- **Oracle** đánh dấu đáp án bằng một **lần lật pha** — `(-1)^[x = w]` — và không
  làm gì khác. Riêng một dấu thì không đo được.
- **Khuếch tán** (`2|s⟩⟨s| − I`) phản xạ mọi biên độ quanh giá trị trung bình. Áp
  sau oracle, nó nâng biên độ được đánh dấu lên trên trung bình và đẩy các biên độ
  khác xuống.
- Mỗi vòng **oracle + khuếch tán** xoay vector biên độ; xác suất của đáp án tuân
  theo `sin²((2k+1)θ)`, `sin θ = 1/√N`.
- **Số vòng rất quan trọng**: quá ít vòng thì xác suất còn nhỏ, quá nhiều vòng thì
  xoay vượt qua đáp án. Mức tối ưu vào khoảng `(π/4)·√N`.
- Tăng tốc là **bậc hai** — `(π/4)·√N` so với `N/2` — và không thuật toán lượng tử
  nào vượt được nó cho một danh sách không cấu trúc.

## Mã nguồn của chương này

Bốn mẫu, từ mốc cổ điển tới thuật toán đầy đủ:

- [`ch10/search.py`](https://github.com/phonhay103/quantum-computing-in-action/blob/main/src/quantum_computing_in_action/ch10/search.py)
  — hai mẫu ``classicsearch`` và ``quantumsearch``: danh bạ, phép quét tuyến tính,
  và một tìm kiếm Grover trên chính các mục đó.
- [`ch10/oracle.py`](https://github.com/phonhay103/quantum-computing-in-action/blob/main/src/quantum_computing_in_action/ch10/oracle.py)
  — mẫu ``groveroracle``: oracle pha, dựng từ một cổng `Z` đa điều khiển tường
  minh, và ma trận của nó.
- [`ch10/step_by_step.py`](https://github.com/phonhay103/quantum-computing-in-action/blob/main/src/quantum_computing_in_action/ch10/step_by_step.py)
  — mẫu ``stepbystepgrover``: hai qubit, biên độ sau mỗi vòng.
- [`ch10/grover.py`](https://github.com/phonhay103/quantum-computing-in-action/blob/main/src/quantum_computing_in_action/ch10/grover.py)
  — mẫu ``grover``: toán tử khuếch tán, số vòng, đường cong thành công, và các kết
  quả đo được.

Chạy toàn bộ bằng `make ch10`, hoặc từng mẫu một:

```bash
uv run python -m quantum_computing_in_action.ch10.grover
```
