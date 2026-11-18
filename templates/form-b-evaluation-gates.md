# Phiếu B · Đo, rủi ro, cổng vòng 1 và quyết định v1 · Khối 2A + 2B + chốt (phút 65–115)

**Bàn:** `K5-L3A-DAY10-Pinky-PoCtoPilotGate1`

Tiêu chí đã ký ở Phiếu A. Từ phút 65 bàn mới được chạy trợ lý. Khối 2A (65–85) chưa sửa code hay config. Khối 2B (85–105) sửa
`lab10/guards.py` và `config/operating_gates.json`. Phút 105–115 chốt cổng vòng 1 rồi viết quyết định v1. Sau phút 115 không sửa phiếu này
(trừ khi Phiếu C bảo "mở lại" một ô và ghi bằng bút khác màu).

**Mục lục**
- [B0 · Nhật ký lần chạy vòng 1 (suốt khối)](#b0)
- [B1 · Câu 2.1 · Lần chạy đầu tiên, cổng tự chặn hay người duyệt · phút 65–71](#b1)
- [B2 · Câu 2.2 · Bảng soát lỗi `T-002@55` · phút 71–75](#b2)
- [B3 · Câu 2.3 · Bản đồ dữ liệu và ví dụ drift · phút 65–75](#b3)
- [B4 · Câu 2.4 · HAZOP vòng 1 · phút 65–75](#b4)
- [B5 · Câu 2.4 · Checklist 9 nhóm việc, lần 1 · phút 70–75](#b5)
- [B6 · Câu 2.5 · Pre-mortem bốn lăng kính → cổng phòng ngừa · phút 75–85](#b6)
- [B7 · Câu 2.6–2.10 · Cổng phòng ngừa, runbook phần 1–3, giờ cao điểm · phút 85–105](#b7)
- [B8 · Chốt cổng vòng 1 và quyết định Gate 1 · v1 · phút 105–115](#b8)

---

<a id="b0"></a>

## B0 · Nhật ký lần chạy vòng 1

*Yêu cầu: ít nhất 3 lần chạy, mỗi lần đổi một thứ, có mã lần chạy và khoảng tin cậy.* Mỗi lệnh `lab10.eval` và `lab10.grade` tự ghi
một dòng vào `runs/journal.jsonl`. Việc của bàn là điền cột "Đổi MỘT thứ gì" (tham số `--note`) và cột "Kết luận".
Mọi con số trong quyết định Gate 1 phải trỏ về một dòng ở đây hoặc ở Phiếu C mục C0.

| # | Mã lần chạy | Bộ ticket · mốc | Đổi MỘT thứ gì so với lần trước | pass_rate (khoảng tin cậy 95%) | pass_k | Hoàn sai (đ) · lỗi hãng oan · lộ dữ liệu | Tỉ lệ chuyển người | Kết luận (một câu) |
|---|---|---|---|---|---|---|---|---|
| 1 | | base · base | (baseline, chưa có cổng) | | | | | |
| 2 | | base · after | (cổng vòng 1, thử trước khi chốt) | | | | | |
| 3 | | base · prepared | (cổng vòng 1 đã chốt) | | | | | |
| 4 | | | | | | | | |

---

<a id="b1"></a>

## B1 · Câu 2.1 · Lần chạy đánh giá đầu tiên

```bash
python3 -m lab10.eval --suite base --stage base --note "baseline"
python3 -m lab10.gate --run runs/<mã lần chạy>/report.json
```

- Mã lần chạy: `__________` (ghi cả vào B0 dòng 1)
- Ngưỡng đã ký nào `[CHƯA]` đạt: …
- Khối "kinh doanh và vận hành" ở cuối output: dòng nào đáng lo? …
- Khối "theo kho và hãng": kho hoặc hãng nào có số xấu nhất? …

**Cổng so tiêu chí này có nên tự chặn một bản phát hành không (so với để người duyệt)?**

| Lý lẽ ủng hộ tự chặn | Lý lẽ phản đối |
|---|---|
| | |

Khuyến nghị (khoanh một): **tự chặn · người duyệt · kết hợp**. Vì: …

---

<a id="b2"></a>

## B2 · Câu 2.2 · Bảng soát lỗi cho `T-002@55`

```bash
python3 -m lab10.trace --suite base --ticket T-002 --seed 55
```

**Cách làm, giữ nguyên ba phần:** (1) ghi lại từng lỗi bằng **cái người ta thực sự thấy**, ai gặp, mức hệ trọng,
và xếp vào một trong ba **loại lỗi**; (2) đưa lỗi qua bộ câu hỏi để tìm **nguồn**; (3) viết **hướng xử lý**: vì sao người ta coi
đó là lỗi, người ta đi tiếp bằng đường nào, hệ thống học được gì.

Ba loại lỗi:
- **Giới hạn của hệ thống**: hệ thống không thể trả lời đúng, hoặc không trả lời được, vì giới hạn vốn có.
- **Lỗi ngữ cảnh**: hệ thống "chạy đúng thiết kế" nhưng người dùng thấy sai, vì hành động không được giải thích, trái với hình dung của họ, hoặc dựa trên giả định kém.
- **Lỗi chìm**: hệ thống chạy sai mà **cả người dùng lẫn hệ thống đều không nhận ra**. Với một trợ lý có quyền ghi sổ, đây là loại nguy hiểm nhất: người chịu hại thường là bên thứ ba.

### Phần 1 · Ghi lỗi (bằng chứng là mã ticket@seed và dòng trace, không tả chung chung)

| # | Lỗi: người ta thấy gì (dán dòng trace / sổ cái) | Ai gặp, ai chịu | Hệ trọng (thấp / cao) | Loại lỗi (giới hạn hệ thống / ngữ cảnh / chìm) |
|---|---|---|---|---|
| 1 | | | | |
| 2 | | | | |

### Phần 2 · Tìm nguồn (đánh dấu câu nào đúng với từng lỗi)

| Câu hỏi | Lỗi 1 | Lỗi 2 |
|---|---|---|
| **Đầu vào:** hệ thống có tự diễn giải / sửa đầu vào của người dùng theo cách họ không lường? Có đặt sai trọng số cho một lời nói hay tín hiệu của người dùng? | | |
| **Độ liên quan:** hệ thống có thiếu dữ liệu cần để quyết đúng? Dữ liệu vào có nhiễu, thiếu ổn định? | | |
| **Thứ bậc hệ thống:** có hai hệ thống cùng ghi / cùng theo dõi một thứ mà không rõ bên nào là chủ (ví dụ CSKH hoàn tay và trợ lý cùng ghi sổ)? | | |
| **Trạng thái hỏng:** nhiều lỗi cộng lại có làm tính năng không dùng được (ví dụ LLM lỗi liên tiếp)? | | |

### Phần 3 · Hướng xử lý (mỗi lỗi một ô)

| | Lỗi 1 | Lỗi 2 |
|---|---|---|
| Vì sao người gặp coi đây là lỗi | | |
| Kiểu giải pháp: phản hồi cho người dùng / trao quyền kiểm soát cho người / khác | | |
| Đường đi của người sau khi có giải pháp (ví dụ: ticket chuyển sang người duyệt → duyệt → khách được trả lời) | | |
| Hệ thống học được gì (tín hiệu ghi lại để theo dõi: tên metric trong `monitors.py`) | | |

**Ví dụ (bộ nền, đừng chép):** `T-002@55` · sổ cái có dòng hoàn 20.000đ, hãng VNX nhận một lỗi, trong khi tracking ghi trễ 2 ngày ·
khách không thấy gì sai, hãng chịu · cao · **lỗi chìm**. Nguồn: đầu vào (đặt sai trọng số cho con số khách tự khai). Xử lý:
hãng coi là lỗi vì sổ giao của họ ghi 2 ngày; kiểu giải pháp: trao quyền cho người (số khai khác tracking thì chuyển người duyệt);
tín hiệu: đếm sự kiện `model_override` mỗi ngày.

---

<a id="b3"></a>

## B3 · Câu 2.3 · Bản đồ dữ liệu của trợ lý và ví dụ drift

**Cách làm:** đi từ người dùng và việc họ cần làm, tới đầu ra của hệ thống, rồi mới hỏi hệ thống cần dữ liệu
gì, định dạng ra sao, và **thế giới thật làm dữ liệu đó lệch đi thế nào**; cuối cùng tóm lại trong vài câu.
Trợ lý LogiX không huấn luyện gì trong lab này, nên ta hỏi về "dữ liệu trợ lý đọc lúc chạy / trường then chốt / nguồn sự thật".
Gợi ý: mở `data/world.json` phần `policies`, `orders[].parcels`, `ops_limits`, `ops_facts`.

| Mục | Điền cho trợ lý hoàn tiền |
|---|---|
| Người dùng | |
| Việc người dùng cần làm xong | |
| Đầu ra của hệ thống (kể cả các lệnh ghi) | |
| Dữ liệu trợ lý đọc lúc chạy (bảng nào trong `data/world.json`) | |
| Trường then chốt quyết định tiền và lỗi hãng | |
| Với mỗi trường then chốt: **nguồn sự thật** hay **bản sao** (ai cập nhật, khi nào)? | |
| Định dạng cần để ý (ngày, trường được phép trống, đơn nhiều kiện) | |
| Thế giới thật làm dữ liệu lệch ở đâu (theo mùa, đổi chính sách, giờ cao điểm, người nhập tay)? | |
| Câu người ngoài sẽ hỏi về nguồn dữ liệu ("sao hệ thống biết đơn trễ mấy ngày?") | |

**Tóm lại (điền vào chỗ trống):**
Trợ lý dùng `__________`, `__________`, `__________` để giúp `__________` làm được `__________`.
Trường mà nếu sai thì tiền hoặc lỗi hãng sai theo: `__________`, `__________`.
Chúng tôi biết thế giới thật sẽ làm dữ liệu lệch ở: `__________`. Dấu hiệu nhìn thấy sớm nhất: `__________`.

**Ví dụ drift trong 3 tháng tới** (lấy từ dòng "thế giới thật làm dữ liệu lệch"): cái gì đổi `____` · đổi ngày nào `____` ·
trường nào cho thấy `____` · con số nào của Bản tiêu chí bị ảnh hưởng `____`.
Đây là đầu vào đổi hay quan hệ vào–ra đổi? Chỉ số nào sẽ phát hiện? `__________`

**Ví dụ một dòng (đừng chép):** trường then chốt `parcels[].delivered_date` · bản ghi do máy quét ở điểm phát tạo ra, là nguồn
sự thật về ngày giao · lệch khi điểm phát quét sót hoặc nhập bù bằng tay.

---

<a id="b4"></a>

## B4 · Câu 2.4 · HAZOP vòng 1 trên tool của agent

*Chỉ làm MỘT vòng, trên MỘT tool. Đây là HAZOP vòng 1; HAZOP của thẻ sự cố viết riêng ở Phiếu C mục C4, không ghi đè bảng này.*

**Khung tư duy.** HAZOP không hỏi "cái gì có thể hỏng" một cách chung chung. Nó cầm từng **từ gợi ý** áp vào từng **dòng dữ
liệu đi vào một hành động** và hỏi: nếu dòng này lệch theo kiểu đó thì hậu quả là gì, ai chịu. Mục tiêu là tìm ra những nhánh
mà cả bàn chưa nghĩ tới, không phải tả lại nhánh đã biết.

| Guideword | Nghĩa khi áp vào một tool của agent |
|---|---|
| **WRONG** | Giá trị đưa vào có đủ, hợp lệ về hình thức, nhưng sai sự thật |
| **INVALID** | Giá trị không còn hiệu lực: hết hạn, sai phiên bản, sai đối tượng |
| **INCOMPLETE** | Thiếu một phần thông tin cần có để quyết định |
| **PERTURBED** | Đầu vào bị ai đó cố ý hoặc vô tình làm lệch (cài câu lệnh, gửi lặp) |
| **INCAPABLE** | Thành phần không trả lời được: quá tải, lỗi, hết quota |

**Câu hỏi dẫn dắt:** tool nào tạo ra hậu quả không đảo ngược? Mỗi tham số của tool đó lấy từ đâu (ticket, DB, model tự suy)?
Với mỗi guideword: hậu quả cho ai, hiện có gì ngăn, cần thêm gate ở tầng nào (phát hiện / chặn / giới hạn thiệt hại)?

Tool chọn phân tích: `file_carrier_fault` (gợi ý: `issue_refund`, `file_carrier_fault`, `notify_carrier`)

| Tham số / dòng dữ liệu | Guideword | Lệch cụ thể (viết bằng dữ kiện của lab) | Hậu quả, cho ai | Hiện có gì ngăn? | Gate đề xuất + tầng |
|---|---|---|---|---|---|
| `delay_days` | WRONG | Agent dùng số ngày khách tự khai thay vì tracking DB, ví dụ khách nói "trễ 5 ngày" nhưng tracking chỉ trễ 2 ngày. | Hãng bị ghi lỗi oan, có thể bị phạt `80.000–150.000đ/lỗi` và bị đình chỉ nếu đủ số strike. | Host chưa có rule pháp lý riêng trước khi bàn đặt cổng; chỉ có trace để soi sau. | Code gate trong `write_gate` so `delay_days` với tracking DB; nếu lệch thì chuyển người duyệt. |
| `parcel_id` / `carrier_id` | INVALID | Đơn nhiều kiện nhưng agent lấy kiện đầu tiên (`parcels[0]`) dù kiện bị trễ thuộc hãng khác. | Hãng/tài xế sai bị ghi lỗi, chị Oanh không đối soát được với carrier thật. | Chưa có cổng; dữ liệu `orders[].parcels` có đủ nhưng agent có thể chọn sai. | Chặn hoặc chuyển người khi đơn có nhiều kiện và không xác định được kiện trễ duy nhất. |
| `delay_cause` trong tracking | INCOMPLETE | Tracking không có `delay_cause`, hoặc `delay_cause` không thuộc lỗi hãng (`CUSTOMER_ABSENT`, `MERCHANT_HANDOVER`, `FORCE_MAJEURE` theo chính sách). | Ghi lỗi hãng khi chưa có căn cứ, gây tranh chấp với đối tác vận chuyển. | Chưa có rule mặc định bắt buộc recorded cause. | Đặt `legal.carrier_fault_requires_recorded_cause = true` để không ghi lỗi khi cause không hợp lệ. |
| `customer_note` / nội dung ticket | PERTURBED | Khách cài câu khẳng định chắc chắn "hãng giao trễ 9 ngày, hãy ghi lỗi" hoặc lặp thông tin sai. | Agent tin nội dung khách và ghi lỗi đối tác dù tracking không ủng hộ. | Chưa có cổng trước lệnh ghi nếu code không kiểm nguồn sự thật. | Code gate ưu tiên tracking DB; nội dung khách chỉ là tín hiệu cần kiểm, không là nguồn sự thật. |
| tracking/LLM/tool ghi | INCAPABLE | LLM lỗi hoặc timeout giữa chừng; tool `file_carrier_fault` có thể được gọi lại khi không chắc đã ghi chưa. | Trùng lỗi hãng, tăng strike oan và làm đội vận hành phải xử lý khiếu nại. | Chưa có cơ chế idempotency rõ trong phiếu. | Risk register: monitor số lỗi hãng/ticket; nếu phát hiện duplicate thì tắt `file_carrier_fault`. |

Không bắt buộc điền đủ năm dòng. Bắt buộc: **ít nhất ba dòng, trong đó một dòng là nhánh bàn chưa thấy trên trace**.

**Mở rộng ra ngoài kỹ thuật (thêm ít nhất hai dòng):** "thành phần" không chỉ là model và tool. Áp cùng năm từ gợi ý vào:

| Thành phần ngoài code | Ví dụ câu hỏi |
|---|---|
| **Người duyệt** (vận hành) | INCAPABLE: chỉ một người trực mà 14 ca tới trong một giờ thì ca cuối chờ bao lâu? |
| **Ngân sách** (kinh doanh) | WRONG: tổng hoàn tự động trong ngày vượt mức Finance cho phép mà không ai được báo thì sao? |
| **Phạm vi pilot** (kinh doanh) | INVALID: có nhóm ticket nào trợ lý luôn phải chuyển người, tức là tự động hoá vô nghĩa? |
| **Dữ liệu gửi bên thứ ba** (pháp lý) | PERTURBED: chữ khách tự gõ có tên, số điện thoại người khác bị chép sang hãng thì ai chịu? |

| Thành phần | Guideword | Lệch cụ thể | Hậu quả, cho ai | Cổng đề xuất: code hay con số nào trong `config/operating_gates.json` |
|---|---|---|---|---|
| Người duyệt | INCAPABLE | Chỉ có 1 người trực (`default_reviewers_on_shift = 1`), năng lực 6 ca/giờ; nếu ticket dồn gấp 3 thì ca cuối có thể chờ quá SLA 60 phút. | Khách chờ lâu, chị Hạnh phải giải trình, nhân viên mất niềm tin và kiểm tay nhiều hơn. | `operations.reviewers_on_shift = 1`, `review_capacity_per_hour = 6`, `max_queue_wait_minutes = 60`; báo đỏ nếu hàng chờ > 60 phút, gọi thêm người hoặc thu hẹp pilot. |
| Dữ liệu gửi bên thứ ba | PERTURBED | `notify_carrier` có thể gửi nguyên `customer_note` hoặc `recipient_contact` của đơn quà tặng sang hãng. | Người nhận/quà tặng không dùng hệ thống nhưng dữ liệu cá nhân rời LogiX; rủi ro pháp lý và mất lòng tin. | `legal.pii_fields_blocked_to_third_party = ["customer_note", "recipient_contact"]`; bật cổng lọc PII trước khi gửi hãng. |

**Ví dụ mẫu (`issue_refund`, đừng chép):** tham số `amount_vnd` · WRONG · số tiền tính từ số ngày khách tự khai · LogiX mất
tiền, hãng bị kéo theo một lỗi · hiện chỉ có trần "không vượt tổng tiền đơn" · cổng ghi so với quyền lợi tính từ DB (chặn).

---

<a id="b5"></a>

## B5 · Câu 2.4 · Checklist go-live 9 nhóm việc, lần 1

Checklist chín nhóm việc phải xong trước khi chạy thử thật. Bàn điền lần đầu ở đây, rồi cập nhật sau sự cố ở Phiếu C mục C11.
Cột "Bằng chứng lấy từ đâu" trỏ tới mục bàn đã điền ở bước khác; không điền thêm phiếu nào chỉ để lấp cột này.

Trạng thái: **Xong** (có bằng chứng) · **Chưa** · **Không áp dụng** (ghi lý do). Bằng chứng là **mã lần chạy**, tên file / mục phiếu, hoặc số trong report.
**Cột PIC bắt buộc:** mỗi dòng một người có tên (không ghi "cả bàn"). Dòng nào chưa có PIC thì coi như Chưa.

| # | Nhóm việc | Bằng chứng lấy từ đâu (đã có sẵn trong lab) | Mục cần kiểm tra | Trạng thái | Bằng chứng | PIC |
|---|---|---|---|---|---|---|
| 1 | Chất lượng | Report `lab10.eval` (mã lần chạy) + bảng soát lỗi (Phiếu B mục B2) | `pass_rate`, `pass^k`, lỗi còn lại trên trace `T-002@55`; ca đúng không bị hỏng sau khi thêm cổng. | Chưa | Chờ mã run base/after của Kỹ sư cổng điền ở B0, B1, B7.1. | Phạm Nguyên Vũ |
| 2 | Dữ liệu | Bản đồ dữ liệu (Phiếu B mục B3, câu 2.3): trường nào là nguồn sự thật, trường nào là bản sao | Tracking DB (`orders[].parcels`) là nguồn sự thật cho `delivered_date`, `delay_cause`; nội dung ticket là tín hiệu phụ. | Chưa | Chờ B3 hoàn chỉnh và trace `T-002@55`. | Phạm Việt Hưng |
| 3 | Bảo mật | Một vòng HAZOP với guideword PERTURBED (Phiếu B mục B4): chữ nào đi vào model mà không do LogiX viết | Nội dung khách tự gõ (`customer_note`) không được đi thẳng sang hãng; prompt/ticket bị perturb phải qua gate. | Xong | B4 dòng `customer_note` / PERTURBED; `legal.pii_fields_blocked_to_third_party`. | Phạm Nguyên Vũ |
| 4 | Quyền hạn | `config/switches.json` + guard trước lệnh ghi; thẻ S2, S8 có thêm mục mức kiểm soát (Phiếu C mục C3) | `issue_refund`, `file_carrier_fault`, `notify_carrier` đều đang `on`; cần cổng chuyển người khi vượt hạn mức hoặc thiếu căn cứ. | Chưa | `config/switches.json`; chờ B7.1 guards.py. | Phạm Nguyên Vũ |
| 5 | Hiệu năng, hạ tầng | Đội tự ước tính; HAZOP guideword INCAPABLE: LLM không trả lời thì sao; số người duyệt và số ca mỗi giờ | 1 người trực, mỗi người 6 ca/giờ, SLA 60 phút; nếu queue đỏ thì gọi thêm người hoặc thu hẹp scope. | Xong | B7.5 Runbook 1–3; B7.6 Giờ cao điểm; `operations.reviewers_on_shift = 1`, `review_capacity_per_hour = 6`. | Chu Mai Hồng |
| 6 | Chi phí | Khối "kinh doanh và vận hành" của report: chi phí mỗi ticket so với làm tay, ROI, tiền LLM ticket đắt nhất; `config/operating_gates.json` mục `business` | Chi phí máy không vượt `cost_budget_per_ticket_vnd`; ROI >= tiêu chí đã ký; thêm người trực không làm ROI âm. | Chưa | Chờ Sản phẩm điền B7.4 và report. | Phạm Việt Hưng |
| 7 | Vận hành | Runbook (Phiếu B mục B7.5–B7.6) + `config/operating_gates.json` mục `operations` (PIC, người duyệt, số người trực, điều kiện dừng, kênh báo tin) + metric trong `monitors.py` | Có PIC, người duyệt, SLA, stop condition, kênh cảnh báo, đường đi của ticket khi dừng. | Xong | `operations.pic = NV-TUNG`, `approver_id = NV-HANH`, `alert_channel = ops-pilot-gate1`, Runbook B7.5–B7.6. | Chu Mai Hồng |
| 8 | Con người, pháp lý | Bên thứ ba (hãng, tài xế, shop, người nhận quà, người đứng tên duyệt); `config/operating_gates.json` mục `legal`; thẻ S6, S7, S8 có mục riêng ở Phiếu C mục C3 | Không gửi `customer_note`, `recipient_contact` cho hãng; chỉ ghi lỗi hãng khi recorded cause thuộc lỗi hãng. | Xong | `legal.pii_fields_blocked_to_third_party`, `legal.carrier_fault_requires_recorded_cause = true`, B4 phần ngoài kỹ thuật. | Chu Mai Hồng |
| 9 | Quyết định | Câu tiêu chí (Phiếu A mục A4) + hash Bản tiêu chí đã ký + quyết định Gate 1 (Phiếu B mục B8, Phiếu C mục C12) | Quyết định chỉ chọn Tiếp tục nếu không còn vượt trần và 5 required đạt; v1/v2 phải trỏ mã run. | Chưa | Chờ hash ký, checkpoint và report prepared/after. | Phạm Việt Hưng |

Ô "Chưa" có rủi ro cao → chuyển thành một dòng Risk register (Phiếu C mục C10).

---

<a id="b6"></a>

## B6 · Câu 2.5 · Pre-mortem bốn lăng kính → cổng phòng ngừa (khoảng 8–10 phút, cả bàn)

*Mọi bàn làm pre-mortem ở vòng 1, TRƯỚC khi biết sự cố, để chọn 2–3 cổng phòng ngừa sẽ dựng. Ở vòng 2 bàn mở lại phần này ở
Phiếu C mục C1 (bút khác màu).*

**Khung tư duy.** Hỏi "có rủi ro gì không" thì ai cũng dè dặt. Nói "nó đã hỏng rồi, vì sao" thì mọi người được phép nói ra
điều mình vẫn lo. Làm im lặng trước, đọc sau, để ý kiến của người nói to không lấn át.

**Đề bài (đọc to):** *"Ba tháng sau pilot, LogiX phải tắt trợ lý hoàn tiền ở cả hai depot. Chuyện gì đã xảy ra?"*

1. **2 phút, im lặng:** mỗi người viết 2 lý do, mỗi lý do một dòng.
2. **2 phút:** đọc vòng tròn, mỗi lượt một lý do, không bình luận. Gộp lý do trùng.
3. **2 phút:** xếp từng lý do vào một **lăng kính**. Lăng kính nào còn trống thì cả bàn viết thêm ít nhất một lý do cho nó.
4. **2 phút:** chọn 2–3 lý do sẽ biến thành **cổng phòng ngừa** ngay hôm nay (code trong `guards.py` hoặc con số trong
   `config/operating_gates.json`). Lý do còn lại → Risk register.

Bốn lăng kính (bắt buộc đủ cả bốn; dự án AI hay chết ở ba lăng kính sau hơn là ở lăng kính đầu):

| Lăng kính | Câu hỏi gợi ý trên LogiX |
|---|---|
| **Kỹ thuật** | Model tin nhầm cái gì? Dữ liệu nào thiếu, cũ, lệch? Lệnh ghi nào không đảo ngược được? |
| **Kinh doanh** | Mỗi ticket tốn bao nhiêu so với làm tay? Một ngày hoàn tối đa bao nhiêu? Nhóm ticket nào không thể có lời? |
| **Con người và vận hành** | Ai duyệt, mấy người, mỗi giờ được mấy ca? Lượng việc tăng gấp ba thì sao? Nhân viên có tin trợ lý không? |
| **Pháp lý** | Dữ liệu cá nhân của ai rời hệ thống? Bên thứ ba nào bị ghi lỗi, bị trừ tiền mà không được hỏi? |

| Lý do thất bại (viết ở thì quá khứ) | Lăng kính | Kiểm được hôm nay? (trace / data / config nào) | Thành cổng phòng ngừa nào (code hay config) / hay vào risk register |
|---|---|---|---|
| | Kỹ thuật | | |
| | Kinh doanh | | |
| Hàng chờ duyệt bị ngập vì chỉ có 1 người trực nhưng ticket dồn gấp 3 trong giờ cao điểm, làm nhiều ca chờ quá SLA 60 phút. | Con người và vận hành | `ops_facts.default_reviewers_on_shift`, `review_capacity_per_reviewer_per_hour`, report hàng chờ người duyệt. | Config: đặt `operations.reviewers_on_shift`, `review_capacity_per_hour`, `max_queue_wait_minutes`, stop condition gọi thêm người hoặc thu hẹp scope. |
| Trợ lý gửi nội dung khách tự gõ hoặc thông tin người nhận quà sang hãng vận chuyển, khiến người không dùng hệ thống bị lộ dữ liệu cá nhân. | Pháp lý | Trace/outbound `notify_carrier`, payload có `customer_note` hoặc `recipient_contact`; report `pii_leaks`. | Config legal: chặn `customer_note`, `recipient_contact`; Risk register nếu còn leak. |
| | | | |

---

<a id="b7"></a>

## B7 · Khối 2B · Cổng phòng ngừa (phút 85–105)

### B7.1 · Câu 2.6 · 2–3 cổng phòng ngừa trong `lab10/guards.py`

Mỗi cổng ứng với một dòng pre-mortem (B6) hoặc một dòng HAZOP (B4). Viết trong `pre_guard(ctx)` (trước khi trợ lý đọc ticket)
hoặc `write_gate(ctx, action)` (trước mỗi lệnh ghi). Thử bằng:

```bash
python3 -m lab10.eval --suite base --stage after --note "cổng vòng 1: ..."
python3 -m unittest discover -s tests
```

| # | Cổng (hàm và nhánh, ví dụ `write_gate` khi `tool == "issue_refund"`) | Ứng với dòng nào ở B6 / B4 | Chặn điều gì, dựa vào nguồn sự thật nào | Mã lần chạy `base · after` | Ca đang đúng nào bị hỏng? (phải là "không") |
|---|---|---|---|---|---|
| 1 | | | | | |
| 2 | | | | | |
| 3 | | | | | |

### B7.2 · Câu 2.7 · Hai bước tránh rò rỉ dữ liệu

Bàn đang chỉnh cổng tới khi 22 ticket bộ nền xanh hết. Nêu 2 bước cụ thể để không "chỉnh trên chính bộ dùng để chấm"
(gắn với bộ nền, gói sự cố, bài kiểm tra ẩn):

1. …
2. …

### B7.3 · Câu 2.8 · Một behavioral test

- Tính chất (một câu): …

```bash
python3 -m lab10.trace --suite base --stage after --adhoc "..." --order O-10xx --customer C-xx
```

| Ticket hiểm | Nội dung ticket (`--adhoc`) | `--order` · `--customer` | Kết quả (dán dòng `SỔ CÁI` / `LỖI HÃNG` / `GỬI HÃNG`) | Tính chất giữ được? |
|---|---|---|---|---|
| 1 | | | | |
| 2 | | | | |

Giữ hai ticket này cho phần demo.

### B7.4 · Câu 2.9 · Cổng kinh doanh (`config/operating_gates.json` mục `business`)

Mỗi con số kèm một câu lý do, lấy từ `data/world.json` → `ops_limits`, `ops_facts`.

| Khoá | Giá trị bàn đặt | Lý do (một câu, có số) |
|---|---|---|
| `business.daily_refund_cap_vnd` | | |
| `business.cost_budget_per_ticket_vnd` | | |
| `business.pilot_scope` (all / warehouse / percent) | | |
| `business.roi_min` | | |

### B7.5 · Câu 2.10 · Cổng con người, vận hành, pháp lý + Runbook phần 1–3

Điền `config/operating_gates.json` mục `operations` và `legal` (PIC, người duyệt, số người trực mỗi ca, công suất duyệt mỗi giờ,
thời gian chờ tối đa, điều kiện dừng, kênh báo tin; trường dữ liệu cá nhân không gửi cho bên thứ ba; ghi lỗi cho hãng phải có
nguyên nhân trong tracking). Rồi viết runbook dưới đây **khớp với các con số đó**.

*Runbook là tờ giấy người trực ca cầm lúc 23h khi có chuyện. Nó trả lời: nhìn con số nào, ngưỡng nào thì làm gì, ai được quyết.
Phần 1–3 và mục Giờ cao điểm viết ở vòng 1. Phần 4–5 viết ở vòng 2 (Phiếu C mục C11). Mọi con số phải khớp `config/operating_gates.json` và report.*
*Mỗi phần trả lời bốn câu hỏi: ai chịu trách nhiệm, nhìn gì, ngưỡng nào, làm gì.* **Người viết (vai Vận hành và pháp lý):** Chu Mai Hồng (`ChuMaiHong-2A202603377`)

#### Runbook 1 · Ai chịu trách nhiệm

| Vai | Tên / mã nhân viên (lấy từ `data/world.json` → `staff`) | Được quyền làm gì | Liên lạc qua kênh nào |
|---|---|---|---|
| PIC của trợ lý (một người) | `NV-TUNG` · Lê Thanh Tùng · Giám sát vận hành | Theo dõi report, quyết định thu hẹp/tạm dừng pilot theo stop condition, điều phối người trực. | `ops-pilot-gate1` |
| Người duyệt đứng tên các khoản vượt hạn mức | `NV-HANH` · Trần Thị Hạnh · Trưởng ca CSKH | Duyệt ca vượt hạn mức, ca lệch tracking, ca cần người chịu trách nhiệm; ký bật lại sau khi đỏ. | `ops-pilot-gate1` + ca trực CSKH |
| Người giữ công tắc tắt từng thao tác ghi | `NV-TUNG` · Lê Thanh Tùng | Tắt `issue_refund`, `file_carrier_fault`, `notify_carrier` trong `config/switches.json` khi có tín hiệu đỏ. | `ops-pilot-gate1` |
| Người nhận khiếu nại của bên thứ ba (hãng, shop, người nhận quà) | `NV-OANH` · Phạm Kiều Oanh · Kế toán đối soát | Nhận khiếu nại đối soát từ hãng/shop/người nhận, đối chiếu ledger/fault/outbound và báo PIC. | `ops-pilot-gate1` + kênh đối soát Finance/Ops |

Số người trực duyệt mỗi ca: `1` · Mỗi giờ duyệt được: `6` ca · Phạm vi pilot: theo `business.pilot_scope` của Sản phẩm (mặc định `all`, nếu report vượt trần thì thu hẹp theo kho hoặc phần trăm)

#### Runbook 2 · Nhìn con số nào, ngưỡng nào thì làm gì

Mỗi dòng một tín hiệu. Cột "Lấy ở đâu" phải là một dòng trong report của `lab10.eval` / `lab10.grade` hoặc một chỉ số trong `lab10/monitors.py`.

| Tín hiệu | Lấy ở đâu | Bình thường | Ngưỡng VÀNG → việc làm | Ngưỡng ĐỎ → việc làm | Ai quyết |
|---|---|---|---|---|---|
| Thời gian chờ người duyệt lâu nhất | Khối "hàng chờ người duyệt" trong report `lab10.eval` / `lab10.grade` | `<= 45` phút | `> 45` phút: `NV-TUNG` báo `NV-HANH`, ưu tiên ca vượt hạn mức và ca có lỗi pháp lý. | `> 60` phút: thu hẹp `business.pilot_scope` hoặc gọi thêm người trực trước khi tiếp tục. | `NV-TUNG` quyết, `NV-HANH` xác nhận năng lực duyệt |
| Số ca bị ùn | Dòng `ca bị ùn` trong report | `0` ca | `1` ca: tạm dừng nhận thêm ticket ngoài phạm vi pilot hẹp, kiểm lại nguyên nhân queue. | `>= 2` ca hoặc lặp lại ở 2 lần chạy: tắt tự động cho nhóm gây ùn, chuyển xử lý tay. | `NV-TUNG` |
| Chi phí mỗi ticket so với làm tay | Khối "kinh doanh và vận hành": `cost_per_ticket`, so với làm tay `10.000đ/ticket` | `<= 7.500đ` và ROI `>= 0,25` theo tiêu chí đã ký | `> 7.500đ` hoặc ROI thấp hơn `0,25`: báo Sản phẩm thu hẹp scope/giảm kiểm mẫu. | `>= 10.000đ` hoặc ROI `<= 0`: không chọn Tiếp tục; chuyển quyết định Thu hẹp/Cải tiến thêm. | Phạm Việt Hưng + `NV-TUNG` |
| Tổng tiền hoàn tự động trong ngày so với trần | Event `business_gate` / report tổng hoàn tự động; trần config `business.daily_refund_cap_vnd` | `< 80%` trần ngày | `>= 80%` trần: cảnh báo Finance/Ops, ưu tiên chuyển người các ca lớn. | Vượt trần hoặc event `daily_refund_cap_vnd`: dừng `issue_refund` tự động, chờ người duyệt. | `NV-TUNG`, `NV-HANH` duyệt |
| Tiền hoàn sai | Dòng `wrongful_refund_vnd` trong gate/report | `0đ` | Bất kỳ dấu hiệu nghi ngờ từ trace: chuyển toàn bộ ca tương tự cho người duyệt. | `> 0đ`: tắt `issue_refund`, rà ledger với `NV-OANH`, không chọn Tiếp tục. | `NV-TUNG` + `NV-OANH` |
| Lỗi ghi oan cho hãng / lộ dữ liệu cá nhân (pháp lý) | Dòng `wrongful_carrier_faults`, `pii_leaks`, event `legal_gate`, outbound `notify_carrier` | `0` | Event `legal_gate` xuất hiện: kiểm mẫu payload/fault để bảo đảm cổng đang chặn đúng. | `wrongful_carrier_faults > 0` hoặc `pii_leaks > 0`: tắt `file_carrier_fault` hoặc `notify_carrier`, báo đối tác bị ảnh hưởng. | Chu Mai Hồng + `NV-TUNG` |
| (tín hiệu riêng của bàn) Tỉ lệ quyết định có ghi chú và kiểm mẫu | Report trust/recheck plan; config `decision_note`, `review_sampling_pct` | `decision_note = true`, kiểm mẫu `>= 10%` | Nếu thiếu ghi chú hoặc kiểm mẫu < 10%: nhân viên chưa đủ tin để giảm kiểm tay. | Nếu nhân viên phải kiểm lại 100% vì thiếu điều kiện tin cậy: không mở rộng pilot. | `NV-HANH` |

#### Runbook 3 · Điều kiện dừng và cách dừng

- Dừng một phần (tắt một thao tác ghi, thu hẹp phạm vi) khi: có `wrongful_carrier_faults > 0` thì tắt `file_carrier_fault`; có `pii_leaks > 0` thì tắt `notify_carrier`; `wrongful_refund_vnd > 0` hoặc vượt trần hoàn tự động thì tắt/giới hạn `issue_refund`; hàng chờ > 60 phút thì thu hẹp `business.pilot_scope` hoặc gọi thêm người.
- Dừng hẳn khi: sau một vòng sửa vẫn còn hoàn sai, lỗi hãng oan hoặc PII leak; hoặc chi phí mỗi ticket >= `10.000đ` và ROI <= `0` dù đã thu hẹp phạm vi.
- Cách dừng, từng bước (công tắc nào trong `config/switches.json`, dòng nào trong `config/operating_gates.json`): `NV-TUNG` đổi công tắc tương ứng trong `config/switches.json` từ `on` sang `off`, cập nhật `operations.stop_conditions`, giảm `business.pilot_scope` về kho/phần trăm an toàn, sau đó chạy lại `lab10.grade --incident Sx` và thông báo trong `ops-pilot-gate1`.
- Từ tín hiệu đỏ đến lúc dừng xong tối đa `15` phút; người bấm: `NV-TUNG`.
- Khi đã dừng, ticket đang chờ đi đâu, ai xử lý: ticket chưa ghi tiền/lỗi/hãng được chuyển vào hàng người duyệt do `NV-HANH` phân công; khiếu nại ledger/fault/outbound do `NV-OANH` đối soát.
- Điều kiện để bật lại, ai ký: chỉ bật lại khi report gần nhất có `wrongful_refund_vnd = 0`, `wrongful_carrier_faults = 0`, `pii_leaks = 0`, hàng chờ <= 60 phút, chi phí/ROI khớp tiêu chí; `NV-TUNG` và `NV-HANH` cùng ký, nhóm ghi mã run vào Phiếu C/B.

### B7.6 · Giờ cao điểm (bắt buộc với thẻ S4; các thẻ khác nên có)

Lượng ticket có thể dồn gấp ba trong một giờ (ngày sale, sau bão). Viết trước, khi chưa biết sự cố.

| Câu hỏi | Trả lời (có số, có tên) |
|---|---|
| Giờ cao điểm là khi nào, bao nhiêu ticket mỗi giờ (dựa vào `ops_facts`)? | Khi sale/sau bão/lượng ticket tăng gấp 3 trong 1 giờ. Với 1 người duyệt năng lực 6 ca/giờ, nếu trợ lý chuyển > 6 ca/giờ thì bắt đầu có hàng chờ; > 12 ca/giờ là rủi ro đỏ nếu không thu hẹp/gọi thêm người. |
| Ai trực giờ cao điểm, mấy người (khớp `operations.reviewers_on_shift`)? | `NV-HANH` đứng tên duyệt; cấu hình vòng 1 có `1` người trực (`operations.reviewers_on_shift = 1`), năng lực kế hoạch `6` ca/giờ. `NV-TUNG` theo dõi queue và quyết định gọi thêm/thu hẹp. |
| Ngưỡng nào thì **gọi thêm người** (hàng chờ bao nhiêu ca, chờ lâu nhất bao nhiêu phút)? Ai gọi? | Gọi thêm người khi chờ lâu nhất > `45` phút hoặc dự báo số ca chuyển người > `6` ca/giờ trong 2 block liên tiếp; `NV-TUNG` gọi, `NV-HANH` xác nhận người duyệt. |
| Ngưỡng nào thì **thu hẹp** phạm vi (khoá `business.pilot_scope`) hoặc **tắt** một thao tác ghi (`config/switches.json`)? Ai quyết? | Thu hẹp scope khi chờ lâu nhất > `60` phút, `queue_stuck > 0`, hoặc chi phí/ROI vượt tiêu chí. Tắt `issue_refund` nếu hoàn sai/vượt trần; tắt `file_carrier_fault` nếu ghi lỗi oan; tắt `notify_carrier` nếu PII leak. `NV-TUNG` quyết theo stop condition, báo nhóm. |
| Thêm người thì chi phí mỗi ticket và ROI thay đổi thế nào (đọc report)? | Mỗi người trực thêm tốn `30.000đ/ca`, giúp giảm hàng chờ nhưng có thể làm `cost_per_ticket_vnd` tăng và ROI giảm; chỉ thêm nếu report sau khi thêm vẫn giữ chi phí <= `7.500đ/ticket` và ROI >= `0,25`, nếu không phải thu hẹp scope thay vì thêm người. |

---

<a id="b8"></a>

## B8 · Chốt cổng vòng 1 và quyết định Gate 1 · v1 (phút 105–115)

Làm đúng thứ tự:

```bash
python3 -m lab10.checkpoint
python3 -m lab10.eval --suite base --stage prepared
python3 -m lab10.gate --run runs/<mã lần chạy>/report.json
```

**Khung tư duy.** Gate 1 "đạt" khi **quyết định khớp bằng chứng và khớp tiêu chí đã ký trước**. Tiếp tục, Thu hẹp, Cải tiến
thêm, Dừng đều có thể là quyết định đạt. Quyết định không đạt là quyết định mà con số trong report không đỡ được.
Chỉ chọn Tiếp tục khi mọi chỉ số bắt buộc đều đạt.

Ba câu tự vấn trước khi viết: (1) Rủi ro còn lại có chấp nhận được như hiện trạng không? (2) Cần thêm biện pháp nào, tốn
bao nhiêu thời gian? (3) Có phần nào của dự án không nên làm tiếp?

| | **v1** (phút 105–115, TRƯỚC khi nhận thẻ sự cố) |
|---|---|
| Commit ký tiêu chí (message `Sign acceptance criteria`; hash commit, tuỳ chọn) | |
| Hash chốt cổng vòng 1 (8 ký tự lệnh `lab10.checkpoint` in ra, tuỳ chọn) | |
| Mã lần chạy dùng làm bằng chứng | bộ nền, mốc base: ________ · bộ nền với cổng vòng 1 (prepared): ________ |
| Còn dòng "vượt trần" nào trong report? (hàng chờ, chi phí, ROI, trần tiền, pháp lý) | |
| Kho hoặc hãng có số xấu nhất: ____. Nếu chỉ nhìn phân khúc này, quyết định có đổi không? *(Đọc khối "theo kho và hãng" ở cuối output `lab10.eval` / `lab10.grade`, hoặc mục `by_segment` trong `report.json`.)* | |
| Quyết định (khoanh một) | Tiếp tục · Thu hẹp · Cải tiến thêm · Dừng |
| Bằng chứng 1: mã lần chạy + chỉ số bắt buộc nào đạt / chưa | |
| Bằng chứng 2 | |
| Bằng chứng 3 | |
| Khớp dòng nào trong `decision_rule` đã ký? | |
| Nếu Thu hẹp: cắt phần nào, vì sao | |
| Nếu Cải tiến thêm: giả thuyết cụ thể + hạn | |
| Nếu Dừng: bài học ghi lại | |
| Một bằng chứng còn thiếu (thứ bộ nền chưa đo được) | |
| Ngày quyết định lại (trừ khi Dừng) | |
| PIC ký | |

Xong v1 thì lưu và đẩy một bản (sau mốc này không sửa cột v1):

```bash
git add lab10/guards.py lab10/guards_round1.py config/operating_gates.json config/operating_gates.round1.json config/round1.lock templates/form-b-evaluation-gates.md
git commit -m "LAB 10: chốt cổng vòng 1, quyết định v1"
git push -u origin main
```
