# Chương 3 — Cổng Pauli-X

!!! abstract "Trong một câu"
    Cổng **Pauli-X** lật một qubit — `|0⟩` thành `|1⟩` và ngược lại — nên đo sau
    khi áp dụng `X` luôn cho cùng một kết quả. Ở đây không có ngẫu nhiên.

## Từ chồng chập trở về sự chắc chắn

Chương 2 dùng cổng Hadamard để tạo chồng chập 50/50. Chương này dùng một cổng làm
điều ngược lại: nó chuyển một qubit **gọn gàng từ trạng thái cơ sở này sang trạng
thái cơ sở kia**, không liên quan gì tới chồng chập.

## Một cổng NOT cho qubit

Cổng **Pauli-X** là tương tự lượng tử của cổng `NOT` cổ điển:

$$X\,|0\rangle = |1\rangle, \qquad X\,|1\rangle = |0\rangle$$

Nó hoán đổi vai trò của hai trạng thái cơ sở trong khi giữ mọi thứ khác nhất quán.
Bắt đầu ở `|0⟩`, áp dụng `X`, qubit giờ chắc chắn là `|1⟩`. Đo nó, bạn nhận `1` —
mọi lần.

!!! note "Các cổng có tính thuận nghịch"
    Khác với một số phép toán cổ điển, cổng lượng tử có tính **thuận nghịch**: áp
    dụng `X` hai lần đưa qubit trở về chỗ cũ (`X·X = I`, toán tử đơn vị). Tính
    thuận nghịch này là một tính chất sâu sắc của tiến hoá lượng tử, không phải
    ngẫu nhiên của riêng cổng này.

## Vì sao kết quả là tất định

So sánh trực tiếp hai chương:

| | Chương 2 (Hadamard) | Chương 3 (Pauli-X) |
|---|---|---|
| Trạng thái sau cổng | `(|0⟩ + |1⟩)/√2` | `\|1⟩` |
| Xác suất ra `0` | 50 % | 0 % |
| Xác suất ra `1` | 50 % | 100 % |
| Đo lặp nhiều lần | lẫn lộn `0` và `1` | luôn là `1` |

Khác biệt nằm ở trạng thái, không phải ở thiết bị đo. Trạng thái xác định thì đo ra
xác định; chồng chập đều thì đo ra ngẫu nhiên.

## Các sơ đồ

### Mạch

![Mạch Pauli-X](../assets/ch03-pauli-x.png){ width="420" }

Từ trái sang phải: qubit `q` bắt đầu ở `|0⟩`, ô `X` lật nó, và phép đo `M` ghi kết
quả vào bit cổ điển `c`. Sơ đồ nhỏ này là toàn bộ câu chuyện của chương.

### Trước và sau, trên mặt cầu Bloch

![Qubit trước và sau cổng X](../assets/ch03-pauli-x-bloch.png){ width="520" }

**Mặt cầu Bloch** giúp việc lật trở nên trực quan:

- **Trước** — mũi tên chỉ lên cực bắc, `|0⟩`.
- **Sau** — mũi tên chỉ xuống cực nam, `|1⟩`.

Về mặt hình học, `X` là một **phép quay 180° quanh trục X** của mặt cầu. Vì trạng
thái đi từ cực này sang cực kia và không hề chạm đường xích đạo, nên không có chồng
chập và do đó không có ngẫu nhiên trong kết quả.

## Ghi nhớ chính

- Cổng Pauli-X tương đương `NOT` đối với qubit.
- `X|0⟩ = |1⟩` và `X|1⟩ = |0⟩`; hai cổng `X` triệt tiêu nhau.
- Áp dụng `X` lên `|0⟩` rồi đo luôn trả về `1` — tất định, không ngẫu nhiên.
- Trên mặt cầu Bloch, `X` là phép quay 180° quanh trục X.

## Mã nguồn của chương này

Ví dụ vẽ mạch và hai mặt cầu Bloch trước/sau nằm trong
[`src/quantum_computing_in_action/ch03/pauli_x.py`](https://github.com/phonhay103/quantum-computing-in-action/blob/main/src/quantum_computing_in_action/ch03/pauli_x.py).
Chạy bằng `make ch03`.
