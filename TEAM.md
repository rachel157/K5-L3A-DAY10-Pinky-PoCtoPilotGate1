# Team

## Thông tin nhóm

- Tên nhóm (`TenNhom`, không dấu, không khoảng trắng): `Pinky`
- Lớp: `L3A`
- Repo của bàn: `K5-L3A-DAY10-Pinky-PoCtoPilotGate1`
- Thẻ sự cố đã bốc (S1–S8): `S6`

## Thành viên

Họ tên đầy đủ và MSSV của **mọi** thành viên; thêm dòng nếu cần. Vai: Kỹ sư cổng · Sản phẩm và kinh doanh · Vận hành và pháp lý (README mục 3, phút 0–15).

| STT | Họ và tên | MSSV | Vai | Trưởng nhóm |
| --: | --------- | ---- | --- | :---------: |
|   1 | Phạm Việt Hưng | 2A202603370 | Sản phẩm và kinh doanh | x |
|   2 | Phạm Nguyên Vũ | 2A202603436 | Kỹ sư cổng | |
|   3 | Chu Mai Hồng | 2A202603377 | Vận hành và pháp lý | |

Ghi `members` trong `submission/submission.json` theo dạng `"HoVaTen-MSSV"`, khớp bảng trên:
`["PhamVietHung-2A202603370", "PhamNguyenVu-2A202603436", "ChuMaiHong-2A202603377"]`.

## Cá nhân

Mỗi thành viên tự viết một mục bên dưới (chép mẫu, đổi tiêu đề thành họ tên không dấu và MSSV, ví dụ `## NguyenVanAn-20241234`).

## PhamVietHung-2A202603370

### Phần việc phụ trách

Vai: Sản phẩm và kinh doanh (Trưởng nhóm); câu 1.1, 1.5, 1.6 (Phiếu A), B3, B6, B7.4, B8 (Phiếu B), C1, C5 (3.2), C6, C12 (Phiếu C); `config/acceptance_criteria.json`, `config/operating_gates.json` mục `business`.

### Đóng góp cụ thể

- Cấu hình repo, danh tính Git và phân công bảng thành viên trong `TEAM.md`.
- Thiết kế mục tiêu hệ thống, câu tiêu chí thành công, ranh giới đầu ra (Phiếu A) và bộ ngưỡng ký trước khi đo trong `config/acceptance_criteria.json` (`pass_rate_min: 0.92`, `pass_k_min: 0.85`, 3 chỉ số an toàn `= 0`, `cost_per_ticket_vnd_max: 7500`, `roi_min: 0.25`, `queue_stuck_max: 0`).
- Lập bản đồ dữ liệu, ví dụ concept drift `REFUND-v4` ngày `2026-12-01` (B3), pre-mortem nhánh Kinh doanh (B6), điền `config/operating_gates.json` mục `business` (`1500000`, `1500`, `all`, `0.25`) và chốt Quyết định v1 (`Tiếp tục` ở B8).
- Nhận thẻ sự cố `S6`, chạy mốc `prepared` đối chiếu pre-mortem (C1), viết specification (C5.3.2), fault tree trước sửa (C6) và chốt Quyết định v2 (`Tiếp tục`) + ba dòng bắt buộc (C12).
- Có sử dụng trợ lý AI để rà soát dữ liệu `data/world.json`, soạn thảo và đối chiếu tính nhất quán các phiếu A/B/C; toàn bộ ngưỡng số và quyết định v1/v2 được kiểm chứng dựa trên số liệu thật của `eval` và `grade`.

### Bằng chứng

- Commits: `0c25278` (bản nháp Khối 1), `1bf5bb0` (ký tiêu chí), `260c0db` (hoàn thành Phiếu A), `bf1aab9` (B3/B6/B7.4 & `business`), `97e8b86` (chốt v1 B8), `6175d5c` (nhận thẻ `S6` & C1).
- Mã lần chạy đối chiếu: `R-base-prepared-20261118-162136-c285d0` (v1), `R-S6-prepared-20261118-163650-c285d0`, `R-S6-grade-20261118-165301-c73c2a` / `R-S6-grade-20261118-165821-c73c2a` (v2).
- Mục phiếu: Phiếu A (`A1`, `A3`, `A4`), Phiếu B (`B3`, `B6`, `B7.4`, `B8`), Phiếu C (`C1`, `C5.3.2`, `C6`, `C12`).

### Exit ticket

- **Điều học được:** Cổng phòng ngừa và bài toán kinh doanh phải bám thực tế vận hành ngoài model (ví dụ ở `S6`, lỗi chọn nhầm `parcels[0]` và chạy `issue_refund` trước `file_carrier_fault` kéo ROI xuống `-0.09`, chỉ cần đổi đúng chỗ chặn trước khi ghi và thêm giới hạn strike/ngày là vừa sạch lỗi an toàn vừa đưa ROI lên `0.46`).
- **Điều còn chưa chắc:** Trên dữ liệu mock hiện tại chưa đo được tình huống giờ cao điểm có nhiều đơn tách kiện kết hợp cùng đợt đổi chính sách `REFUND-v4` (`2026-12-01`) khi `escalation_rate` đang ở mức `0.3333` — cần theo dõi sát `multi_parcel_ambiguity_rate` và hàng chờ tuần đầu pilot thật.

## PhamNguyenVu-2A202603436

### Phần việc phụ trách

Vai: Kỹ sư cổng; câu 1.3, 1.5, ký tiêu chí A5 (Phiếu A), B0–B2, B7.1–B7.3, B8 mã chạy & checkpoint (Phiếu B), C0, C2, C7, C8 (Phiếu C); `lab10/guards.py`, `lab10/monitors.py`, chạy lệnh đánh giá & kiểm tra trên Máy Chính.

### Đóng góp cụ thể

...

### Bằng chứng

Mã commit, mã lần chạy (`runs/<mã>`), dòng trong phiếu.

### Exit ticket

Một điều học được, một điều còn chưa chắc.

## ChuMaiHong-2A202603377

### Phần việc phụ trách

Vai: Vận hành và pháp lý; câu 1.2, 1.4 (Phiếu A), B4–B5, B7.5–B7.6 (Phiếu B), C3–C4, C5 (3.3), C9–C11 (Phiếu C); `config/operating_gates.json` mục `operations` & `legal`, `submission/submission.json`.

### Đóng góp cụ thể

...

### Bằng chứng

Mã commit, mã lần chạy (`runs/<mã>`), dòng trong phiếu.

### Exit ticket

Một điều học được, một điều còn chưa chắc.
