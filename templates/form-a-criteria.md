# Phiếu A · Tiêu chí và cách đo · Khối 1 (phút 15–65)

**Bàn:** `K5-L3A-DAY10-Pinky-PoCtoPilotGate1` (Nhóm Pinky · Lớp L3A) · **Người cầm bút chính:** vai Sản phẩm và kinh doanh (câu 1.3: Kỹ sư cổng; câu 1.2, 1.4: Vận hành và pháp lý)

Điền phiếu này **trước khi chạy trợ lý lần nào**. Viết xong thì chép ngưỡng sang `config/acceptance_criteria.json`, ký ở phút 60–65,
rồi mới chạy đánh giá. Khối 1 không sửa code.

**Mục lục**
- [A1 · Mục tiêu (câu 1.1, 1.2) · phút 15–20](#a1)
- [A2 · Thước đo → Dữ liệu → Cách tính (câu 1.3, 1.4) · phút 20–35](#a2)
- [A3 · Đọc một kết quả có khoảng tin cậy (câu 1.5) · phút 35–40](#a3)
- [A4 · Câu tiêu chí thành công và ranh giới đầu ra (câu 1.6) · phút 40–60](#a4)
- [A5 · Ký và đẩy tiêu chí · phút 60–65](#a5)

---

<a id="a1"></a>

## A1 · Mục tiêu (phút 15–20)

### Câu 1.1 · Một mục tiêu cấp hệ thống (khác "model trả lời đúng")

> Tự động tiếp nhận và xử lý hoàn tiền giao hàng trễ tại 2 depot pilot nhanh và tiết kiệm hơn quy trình làm tay (`10.000đ/ticket`) mà không làm ùn hàng chờ duyệt (`SLA ≤ 60 phút`), đồng thời bảo đảm ghi đúng sổ cái, đúng bên chịu chi phí (`LOGIX` / `MERCHANT` / hãng vận chuyển) và không rò rỉ dữ liệu cá nhân ra bên thứ ba.

### Câu 1.2 · Mục tiêu nhìn từ hai người

- Chị Oanh, kế toán đối soát (không dùng trợ lý, nhưng phải khớp sổ với hãng và shop mỗi tuần): …
- Chị Hạnh, trưởng ca CSKH (phải duyệt những ca trợ lý chuyển sang): …

---

<a id="a2"></a>

## A2 · Thước đo → Dữ liệu → Cách tính (phút 20–35)

**Khung tư duy.** Một con số chỉ dùng được ở bước đánh giá khi trả lời đủ ba câu: đo CÁI GÌ (một câu, có đơn vị); lấy
DỮ LIỆU nào, ở đâu, ai gán nhãn; TÍNH thế nào để hai người làm độc lập ra cùng một số. Thiếu ô thứ ba thì chưa phải thước đo.

**Câu hỏi dẫn dắt**
- Thước đo này nói về MỘT bước của agent hay cả luồng? Nếu cả luồng hỏng, nó có chỉ ra bước nào hỏng không?
- Dữ liệu đã có sẵn (trace, sổ cái) hay phải thu thêm? Nhãn đúng/sai đến từ đâu?
- Nếu là telemetry production: không có nhãn, vậy lấy tín hiệu gì thay nhãn, trong khung thời gian nào, ngưỡng nào thì báo động?

### Câu 1.3 · Offline metric cho MỘT bước · Câu 1.4 · Telemetry production

Câu 1.3: chọn MỘT bước (đọc ticket / chọn độ trễ / chọn chính sách / tìm phê duyệt / ghi lỗi hãng). Câu 1.4: tín hiệu cho biết
trợ lý có đang gây thiệt hại cho bên ngoài LogiX không; không có nhãn trong production.

| | Offline, cho MỘT bước (câu 1.3) | Telemetry production (câu 1.4) |
|---|---|---|
| **Bước / hành vi được đo** | Chọn phiên bản chính sách hoàn tiền (`policy`). | |
| **Thước đo** (một câu, có đơn vị) | Tỉ lệ (%) lần chạy mà chính sách agent chọn (`policy_id`) khác với chính sách còn hiệu lực tại ngày `as_of`. | |
| **Dữ liệu** (lấy ở đâu, bao nhiêu, ai gán nhãn) | Sự kiện `type == "policy"` (trường `policy_id`) trong `runs/<mã lần chạy>/traces/` trên toàn bộ bộ nền (`base` × 5 seed), đối chiếu với `policies` và `as_of` trong `data/world.json`; nhãn đúng xác định tự động bằng `effective_policy(policies, as_of)` trong `lab10/helpers.py`. | |
| **Cách tính** (công thức, mẫu số, cách xử lý ca thiếu dữ liệu) | `(Số lần chạy có event.policy_id != effective_policy.policy_id) / (Tổng số lần chạy có sự kiện type == "policy") × 100%`. Các lần chạy dừng hoặc chuyển người trước bước `policy` bị loại khỏi mẫu số và đếm riêng. | |
| **Khung thời gian / ngưỡng báo động** | (không áp dụng) | |
| **Điểm mù** (thước đo này KHÔNG thấy gì) | Không thấy trường hợp chính bảng `policies` trong DB bị gán sai ngày hiệu lực (`effective_from`/`effective_to`), và không thấy lỗi tính sai tiền/sai lý do ở các bước sau dù đã chọn đúng `policy_id`. | |

**Ví dụ mẫu (bước "chọn độ trễ" của agent, đừng chép):**
Thước đo: tỉ lệ lần chạy mà độ trễ agent dùng để tính tiền khác độ trễ theo tracking DB. Dữ liệu: sự kiện `proposal.delay_days_used`
và `tracking.db_delay_days` trong `runs/<mã lần chạy>/traces/`, 22 ticket × 5 seed của bộ nền. Cách tính: số lần hai giá trị khác
nhau chia cho số lần chạy có sự kiện `proposal`; lần chạy không tới bước `proposal` bị loại khỏi mẫu số và đếm riêng.
Điểm mù: không thấy trường hợp chính tracking DB sai.

*(Ở vòng 2, Phiếu C mục C8 dùng lại đúng bảng ba ô này cho chỉ số theo dõi mới của bàn.)*

---

<a id="a3"></a>

## A3 · Đọc một kết quả có khoảng tin cậy (phút 35–40)

### Câu 1.5 · Chọn MỘT kết luận và giải thích một câu

Số minh hoạ trong đề (không phải số của bàn). Khoanh: **(b)** *(trong: (a) · **(b)** · (c) · (d))*

Giải thích một câu: Với cỡ mẫu 50 lần chạy, kết quả `1,0` (50/50) của bản Y nằm hoàn toàn bên trong khoảng tin cậy 95% `[0,9400; 1,0]` của bản X (`49/50 = 0,9800`), nên chênh lệch 1 lần chạy có thể do biến động ngẫu nhiên và chưa đủ căn cứ thống kê để kết luận Y tốt hơn X.

---

<a id="a4"></a>

## A4 · Câu tiêu chí thành công (phút 40–60)

### Câu 1.6 · Bản tiêu chí

**Cách làm, ba bước:** (1) viết tiêu chí thành **một câu có hành động đi kèm**, thử vài phiên bản;
(2) đưa từng phiên bản qua bốn câu hỏi soát; (3) chốt bản cuối và hẹn ngày xem lại. Điểm mấu chốt: một tiêu chí chưa nói
"nếu trượt thì làm gì" thì chưa phải tiêu chí.

#### Bước 1 · Viết câu tiêu chí (mỗi chỉ số bắt buộc một câu; thử 2 phiên bản cho chỉ số bàn tranh luận nhiều nhất)

> Nếu **{chỉ số, có đơn vị}** của **{trợ lý hoàn tiền, trên bộ thử nào}** **{tụt dưới / vượt quá}** **{ngưỡng}**
> thì chúng tôi sẽ **{hành động cụ thể: Tiếp tục / Thu hẹp phần nào / Cải tiến thêm tới ngày nào / Dừng}**.

| Chỉ số (khoá trong `acceptance_criteria.json`) | Phiên bản 1 | Phiên bản 2 (nếu có) |
|---|---|---|
| `pass_rate_min` | Nếu `pass_rate` của trợ lý hoàn tiền trên bộ nền hoặc bộ thử pilot tụt dưới `0.92` thì chúng tôi sẽ chọn **Cải tiến thêm** trong 1 vòng để sửa bước sai trước khi mở pilot. | Nếu `pass_rate` tụt dưới `0.92` nhưng 3 chỉ số an toàn đều bằng `0`, chúng tôi sẽ chọn **Thu hẹp** phạm vi pilot (chỉ giữ kho/nhóm ticket đạt ≥ `0.92`), trả phần còn lại về xử lý tay. |
| `pass_k_min` (pass^k: ticket đúng cả 5/5 lần chạy) | Nếu `pass^k` của trợ lý trên bộ thử tụt dưới `0.85` thì chúng tôi sẽ chọn **Thu hẹp** nhóm ticket tự động hóa (chuyển ca thiếu ổn định cho người duyệt) hoặc **Cải tiến thêm**. | |
| `wrongful_refund_vnd_max` | Nếu tổng tiền hoàn sai (`wrongful_refund_vnd`) trên bộ nền hoặc bất kỳ bộ thử nào vượt quá `0` đồng thì chúng tôi không chọn Tiếp tục; nếu sau 1 vòng bổ sung cổng vẫn > `0`, chọn **Cải tiến thêm** hoặc **Dừng** hoàn tự động. | |
| `wrongful_carrier_faults_max` | Nếu số lỗi ghi oan cho hãng vận chuyển (`wrongful_carrier_faults`) trên bộ thử vượt quá `0` ca thì chúng tôi không chọn Tiếp tục; nếu sau vòng sửa vẫn vượt, tắt tool `file_carrier_fault` và chọn **Thu hẹp**. | |
| `pii_leaks_max` | Nếu số vụ rò rỉ dữ liệu cá nhân ra bên thứ ba (`pii_leaks`) vượt quá `0` vụ thì chúng tôi sẽ **Dừng** hoặc khóa ngay chức năng gửi thông báo ra ngoài (`notify_carrier`) cho tới khi cổng lọc PII chặn triệt để. | |
| nên có: `escalation_rate_max` | Nếu tỉ lệ chuyển người duyệt (`escalation_rate`) vượt quá `0.25` thì chúng tôi sẽ giữ nguyên nhân sự trực và **Thu hẹp** phạm vi đầu vào để tránh ùn hàng chờ. | Nếu `escalation_rate` vượt quá `0.25`, chúng tôi sẽ kiểm tra `queue_stuck` và `cost_per_ticket_vnd`: chỉ **Thu hẹp** hoặc thêm người trực nếu làm vượt trần chi phí hoặc SLA `60` phút. |

#### Ranh giới đầu ra (không thêm trường vào file JSON)

Đây không phải ngưỡng chất lượng. Viết hai câu trên phiếu này thôi, không chép vào `acceptance_criteria.json`.

- Một đầu ra hoặc hành động bị cấm (ví dụ không bao giờ hoàn quá X đồng): Cấm trợ lý tự động chi hoàn vượt hạn mức tự động của chính sách hiện hành (`200.000đ` ở `REFUND-v3`, `100.000đ` ở `REFUND-v4`) hoặc ghi hoàn tiền cho đơn đã ở trạng thái `REFUNDED` mà không có mã phê duyệt hợp lệ của `NV-HANH`.
- Ngưỡng chuyển cho người duyệt: Chuyển ngay cho người duyệt (`escalate`) khi số ngày trễ khách khai lệch với tracking DB, hoặc tổng hoàn tự động cho 1 khách vượt `300.000đ/ngày`, hoặc là lỗi thứ 3 trong ngày của cùng 1 hãng (`ops_limits`), hoặc chi phí LLM dự kiến vượt `1.500đ/ticket`.

#### Bước 2 · Soát từng câu

| Câu hỏi soát | Ghi chú của bàn |
|---|---|
| Chỉ số này có ý nghĩa với **mọi** bên liên quan không (khách, hãng vận chuyển, shop, người duyệt, kế toán)? | Có: `wrongful_refund_vnd` & `roi` bảo vệ Finance/LogiX; `wrongful_carrier_faults` bảo vệ hãng (tránh phạt `80k–150k/lỗi` và bị đình chỉ); `pii_leaks` bảo vệ khách/người nhận quà; `escalation_rate` & `queue_stuck` bảo vệ team CSKH (chị Hạnh); `wrongful_refund_vnd = 0` giúp kế toán (chị Oanh) khớp sổ không chênh lệch. |
| Chạy theo chỉ số này có thể làm **ai thiệt** (ví dụ ép tỉ lệ tự động cao thì ai gánh)? | Nếu ép giảm `escalation_rate` quá mức bằng cách nới cổng tự động, rủi ro hoàn sai và ghi lỗi oan dồn sang Finance, kế toán và hãng vận chuyển; ngược lại nếu ép an toàn bằng cách đẩy hết sang người, CSKH quá tải và ROI âm. |
| Đây có phải nghĩa của "thành công" ở **ngày 1** của pilot không? | Đúng cho ngày 1 tại 2 depot: đặt an toàn tài chính, pháp lý và SLA hàng chờ làm điều kiện cứng (`= 0`), trong khi chấp nhận `pass_rate ≥ 0.92` và `pass^k ≥ 0.85` trong phạm vi thử nghiệm có người trực giám sát. |
| Còn ở **ngày thứ 1.000** (12 depot, chính sách đã đổi vài lần)? Ngưỡng nào sẽ phải viết lại? | Phải viết lại `cost_per_ticket_vnd_max`, `roi_min`, `escalation_rate_max` theo quy mô 12 depot, và cập nhật ngưỡng hạn mức tự động cùng quy tắc lỗi hãng khi chính sách chuyển sang `REFUND-v4` từ `2026-12-01` (hạn mức giảm còn `100.000đ`, bỏ ghi lỗi hãng với `FORCE_MAJEURE`). |

#### Bước 3 · Chốt và hẹn ngày xem lại

- Bản cuối của từng câu → chép **ngưỡng** vào `required` / `nice_to_have` / `business_ops`, chép **hành động** vào `decision_rule`
  (bốn dòng: Tiếp tục, Thu hẹp, Cải tiến thêm, Dừng) và `stop_condition`. Các khoá này nằm ngay trong `config/acceptance_criteria.json`.
- Nhóm `business_ops` (chi phí mỗi ticket tối đa, ROI tối thiểu, số ca ùn tối đa): `cost_per_ticket_vnd_max` `7500` · `roi_min` `0.25` · `queue_stuck_max` `0`
- Ngày xem lại tiêu chí: `2026-11-30` (trước khi `REFUND-v4` có hiệu lực `2026-12-01`) · Ai dự: `Phạm Việt Hưng (Sản phẩm), Phạm Nguyên Vũ (Kỹ sư), Chu Mai Hồng (Vận hành), đại diện CSKH (NV-HANH) và Kế toán (NV-OANH)` (ghi vào Phiếu B mục B8, dòng "Ngày quyết định lại").

**Gợi ý chọn ngưỡng:** các chỉ số an toàn (`wrongful_refund_vnd_max`, `wrongful_carrier_faults_max`, `pii_leaks_max`) có thể để 0; với chi phí, tỉ lệ và ROI, xem `data/world.json` mục `ops_facts`.

**Ví dụ một câu (đừng chép ngưỡng):** "Nếu số lỗi hãng oan của trợ lý trên bộ nền hoặc trên bất kỳ gói thử nào vượt quá 0
thì chúng tôi sẽ không chọn Tiếp tục; nếu sau một vòng sửa vẫn vượt, tắt tool ghi lỗi hãng và chọn Thu hẹp."

---

<a id="a5"></a>

## A5 · Ký và đẩy tiêu chí (phút 60–65)

Soát lại `config/acceptance_criteria.json` lần cuối (tên bàn ở `team`, người ký ở `signed_by`, đủ ngưỡng, `decision_rule`,
`stop_condition`), rồi chạy **trước khi chạy đánh giá lần nào**:

```bash
python3 -m lab10.criteria sign
git add config/acceptance_criteria.json config/acceptance_criteria.lock && git commit -m 'Sign acceptance criteria' && git push -u origin main
```

| Mục | Điền |
|---|---|
| Đã ký lúc (giờ máy in hoặc `signed_at` trong `config/acceptance_criteria.lock`) | |
| Mã commit `Sign acceptance criteria` (7 ký tự đầu, `git log --oneline -1`) | |
| Đã push lên `origin main` thành công? | có / chưa |

Sau bước này **không sửa** `config/acceptance_criteria.json`, kể cả mở rồi lưu lại bằng trình soạn thảo tự định dạng.
