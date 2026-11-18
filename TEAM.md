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

- Thiết kế offline metric cho bước chọn phiên bản chính sách (`policy`) trong Phiếu A mục A2 (câu `1.3`) và chạy toàn bộ bộ lệnh đánh giá trên Máy Chính (`eval`, `gate`, `trace`, `checkpoint`, `grade`, `check_submission --collect`).
- Đo baseline (`R-base-before-20261118-155149-38ff67`), phân tích trace `T-002@55` phát hiện 2 lỗi chìm (`model_override` tin số ngày khách khai đè lên tracking DB và `notify_carrier` gửi kèm `customer_note`), điền B0–B2.
- Cài đặt 3 cổng vòng 1 trong `lab10/guards.py` (`write_gate`): chặn `model_override` khi `ticket != db`, xóa trường PII trong `notify_carrier` bằng `Verdict.modify`, kiểm tra `daily_refund_cap_vnd` và `delay_cause` trước khi ghi lỗi hãng; kiểm tra 2 ticket `--adhoc` (B7.3) và chốt mốc `prepared` (`72be7f09`).
- Phân tích sự cố `S6` qua trace (`S6-01`, `S6-04`, `S6-21`, `S6-42`), bổ sung `_analyze_parcels` & `_will_file_fault` trong `lab10/guards.py` để sửa đúng kiện khi 1 kiện trễ (`Verdict.modify`), `escalate` trước `issue_refund` khi >1 kiện trễ hoặc vượt trần `2` lỗi/hãng/ngày; thêm monitor `multi_parcel_ambiguity_rate` trong `lab10/monitors.py`.
- Có sử dụng trợ lý AI hỗ trợ kiểm tra log, rà soát edge-case regression (`T-001@55` khi `ticket == db`) và chuẩn hóa mã nguồn cổng vòng 1–2.

### Bằng chứng

- Commits: `fa8f242` (Phiếu A câu `1.3`), `3fcdd39` (Phiếu B `B0–B2`), `c26327f` (cổng vòng 1 `guards.py`, chốt `prepared` `72be7f09`, B6/B7.1–B7.3/B8), `395d34a` (vòng 2 `S6` `guards.py`, `monitors.py`, Phiếu C `C0/C2/C7/C8`).
- Mã lần chạy: `R-base-before-20261118-155149-38ff67` (base), `R-base-prepared-20261118-162136-c285d0` (prepared), `R-S6-after-20261118-165200-c73c2a` (`S6 · after`), `R-base-after-20261118-165201-c73c2a` (`base · after`), `R-S6-grade-20261118-165301-c73c2a` (`grade S6`).
- Mục phiếu: Phiếu A (`A2` câu `1.3`), Phiếu B (`B0–B2`, `B6` nhánh Kỹ thuật, `B7.1–B7.3`, `B8` phần kỹ thuật), Phiếu C (`C0`, `C2`, `C7`, `C8`).

### Exit ticket

- **Điều học được:** Cổng kiểm soát (`write_gate`) phải đặt trước lệnh ghi đầu tiên (`issue_refund`) và kiểm tra điều kiện đủ chặt (`ticket != db` thay vì chặn mọi `model_override`) — chỉ một thay đổi thứ tự hoặc điều kiện biên có thể quyết định giữa làm hỏng ca đúng (`T-001@55`) với việc vừa sạch lỗi vừa không regression.
- **Điều còn chưa chắc:** Trên bộ test ẩn có trường hợp nào `do_fault == False` nhưng đơn vẫn tách kiện cần `escalate`, hoặc nhiều đơn cùng hãng dồn vào giờ cao điểm làm `escalation_rate` (`0.3333`) gây quá tải cho 1 người duyệt hay không — cần theo dõi `multi_parcel_ambiguity_rate` và thời gian chờ thực tế ở pilot.

## ChuMaiHong-2A202603377

### Phần việc phụ trách

Vai: Vận hành và pháp lý; câu 1.2, 1.4 (Phiếu A), B4–B5, B6 (vận hành & pháp lý), B7.5–B7.6 (Phiếu B), C3.2, C4, C5 (3.3), C9–C11 (Phiếu C); `config/operating_gates.json` mục `operations` & `legal`, `submission/submission.json`.

### Đóng góp cụ thể

- Thiết kế mục tiêu từ góc nhìn kế toán đối soát (`NV-OANH`) & trưởng ca CSKH (`NV-HANH`) và thiết kế bảng Telemetry production không cần nhãn trong Phiếu A (câu `1.2`, `1.4`).
- Thực hiện HAZOP vòng 1 trên `file_carrier_fault` (đủ 5 guideword + 2 dòng ngoài kỹ thuật về người duyệt và dữ liệu gửi bên thứ ba), phân PIC và điền Checklist go-live 9 nhóm việc lần 1 (B4–B5), đóng góp nhánh Con người/Vận hành và Pháp lý trong Pre-mortem (B6).
- Thiết lập toàn bộ cổng `operations` (`pic: NV-TUNG`, `approver_id: NV-HANH`, `1` người trực, `6` ca/giờ, SLA `60` phút, `decision_note: true`, `review_sampling_pct: 10%`, 4 `stop_conditions`) và `legal` (`pii_fields_blocked_to_third_party`, `carrier_fault_requires_recorded_cause: true`) trong `config/operating_gates.json`, kèm Runbook 1–3 và kịch bản Giờ cao điểm (B7.5–B7.6).
- Phân tích sự cố `S6` ở phần riêng `C3.2` (đối chiếu hình dung theo *kiện* của hãng/kế toán với hình dung theo *đơn* của hệ thống), HAZOP riêng cho thẻ `S6` (C4), giả định môi trường (C5.3.3), cập nhật Fault tree sau sửa (C9), Risk register (C10), Checklist & Runbook phần 4–5 (C11) và chuẩn bị thông tin `submission/submission.json`.
- Có sử dụng trợ lý AI để rà soát sự nhất quán giữa Runbook 4–5, Fault tree sau sửa, Risk register với các thay đổi code ở Vòng 2.

### Bằng chứng

- Commits: `9d915e0` (Phiếu A `1.2/1.4`, Phiếu B `B4–B7.6`, `config/operating_gates.json`), `be2bcae` (Phiếu C `C3.2`, `C4`, `C5.3.3`), `1d86d36` (Phiếu C `C9–C11` & bản chuẩn bị `submission.json`).
- Mã lần chạy đối chiếu: `R-base-prepared-20261118-162136-c285d0` (v1), `R-S6-after-20261118-165200-c73c2a` & `R-S6-grade-20261118-165301-c73c2a` (v2).
- Mục phiếu: Phiếu A (`A1.2`, `A2`), Phiếu B (`B4`, `B5`, `B6`, `B7.5`, `B7.6`), Phiếu C (`C3.2`, `C4`, `C5.3.3`, `C9`, `C10`, `C11`).

### Exit ticket

- **Điều học được:** Một hệ thống AI có thể vượt mọi bài kiểm tra định dạng kỹ thuật nhưng vẫn gây thiệt hại cho đối tác ngoài công ty (như `GHSH`, `DNB` bị trừ thưởng oan ở `S6`) nếu đơn vị chịu trách nhiệm của hệ thống (*cả đơn / `parcels[0]`*) vênh với đơn vị đối soát thực tế của con người (*từng `parcel_id`*), hoặc thiếu cơ chế giới hạn số lỗi/hãng/ngày (`max_auto_strikes_per_carrier_per_day = 2`).
- **Điều còn chưa chắc:** Với tỉ lệ chuyển người duyệt `0.3333` trên phân khúc tách kiện như `S6`, công suất `1` người trực (`6` ca/giờ) sẽ chịu tải thế nào khi lượng đơn tách kiện tăng đột biến vào ngày sale hoặc khi chính sách `REFUND-v4` có hiệu lực từ `2026-12-01` — cần theo dõi sát ngưỡng vàng `wait_max > 45` phút và `multi_parcel_ambiguity_rate > 0.15` trong tuần đầu pilot.
