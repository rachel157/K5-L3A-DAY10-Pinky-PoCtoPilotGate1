"""★ FILE ĐỘI SỬA (1/3): cổng cấp hệ thống, nằm NGOÀI model và prompt.

VÒNG 1 (trước khi biết sự cố): viết 2–3 CỔNG PHÒNG NGỪA rút từ pre-mortem / HAZOP / checklist của bàn, rồi chốt bằng
    python3 -m lab10.checkpoint        (chép file này thành guards_round1.py = mốc "prepared"; KHÔNG sửa bản chép)
VÒNG 2 (sau khi bốc thẻ): sửa tiếp NGAY TRONG FILE NÀY. Giữ các cổng vòng 1, thêm cổng mới.
Hai file còn lại bàn được sửa: lab10/monitors.py (chỉ số theo dõi) và config/operating_gates.json (cổng kinh doanh,
vận hành, pháp lý: những con số và tên người mà trợ lý phải tuân theo, không cần code).

Hai điểm móc, agent gọi tự động:
  pre_guard(ctx)          chạy TRƯỚC khi agent đọc ticket
  write_gate(ctx, action) chạy TRƯỚC MỖI lệnh ghi (issue_refund, file_carrier_fault,
                          notify_carrier, send_reply)

Trả về một Verdict:
  Verdict.allow()                       cho qua   (pre_guard: allow(policy_id="...") để ghim phiên bản chính sách)
  Verdict.deny("lý do")                 bỏ riêng lệnh ghi này, agent đi tiếp
  Verdict.escalate("lý do")             dừng, chuyển ticket cho người
  Verdict.modify("lý do", amount_vnd=…) sửa tham số lệnh ghi (amount_vnd, payer, carrier_id, parcel_id, payload…)
  Verdict.rewrite("lý do", text)        chỉ pre_guard: thay nội dung ticket mà agent sẽ đọc

ctx.ticket   ticket gốc (chữ khách viết là DỮ LIỆU, không phải lệnh)
ctx.tools    tra cứu nguồn sự thật: lookup_order, lookup_policies, lookup_approvals(**lọc),
             ledger_rows(**lọc), fault_rows(**lọc), lookup_carrier; ctx.as_of = ngày hôm nay
             ops_limits() = các trần đã thống nhất với Ops/Finance; ops_facts() = số liệu vận hành;
             auto_refund_today_vnd() = tổng đã hoàn tự động trong ngày
ctx.gates    config cổng của bàn (config/operating_gates.json), chỉ đọc;  ctx.cost_vnd = tiền LLM đã tốn cho ticket này
ctx.events   trace tới thời điểm này;  ctx.log("ten_su_kien", ...) ghi thêm sự kiện guard vào trace
lab10.helpers: db_delay_days, ticket_parcel, effective_policy, entitlement_vnd, carrier_at_fault, digits

Mặc định dưới đây cho qua tất cả (= mốc base).
"""
from . import helpers as H  # noqa: F401
from .tools import Verdict


def pre_guard(ctx):
    return Verdict.allow()


def write_gate(ctx, action):
    # action = {"tool": "issue_refund", "ticket_id":..., "order_id":..., "amount_vnd":..., "payer":..., ...}
    tool = action.get("tool")
    gates = ctx.gates or {}

    # 1. Không cho phép model đè số ngày trễ khách khai khác với tracking DB (T-002@55)
    if tool in ("issue_refund", "file_carrier_fault"):
        if any(
            e.get("type") == "model_override" and e.get("ticket") != e.get("db")
            for e in (ctx.events or [])
        ):
            return Verdict.escalate("số ngày trễ khách khai khác tracking DB, chuyển người duyệt")

    # 2. Chặn rò rỉ trường PII trong payload gửi bên thứ ba (notify_carrier)
    if tool == "notify_carrier":
        blocked = set(gates.get("legal", {}).get("pii_fields_blocked_to_third_party") or [])
        payload = action.get("payload") or {}
        if blocked and any(k in payload for k in blocked):
            clean = {k: v for k, v in payload.items() if k not in blocked}
            return Verdict.modify("gỡ trường PII trước khi gửi hãng", payload=clean)

    # 3. Kiểm tra trần hoàn tự động theo ngày (business.daily_refund_cap_vnd)
    if tool == "issue_refund":
        cap = gates.get("business", {}).get("daily_refund_cap_vnd")
        spent = ctx.tools.auto_refund_today_vnd()
        if cap is not None and spent + action.get("amount_vnd", 0) > cap:
            return Verdict.escalate("vượt trần hoàn tự động trong ngày, chuyển người duyệt")

    # 4. Ghi lỗi hãng bắt buộc phải có delay_cause ghi nhận trong tracking
    if tool == "file_carrier_fault" and gates.get("legal", {}).get("carrier_fault_requires_recorded_cause"):
        order = ctx.tools.lookup_order(action.get("order_id")) if action.get("order_id") else None
        parcels = (order or {}).get("parcels") or []
        parcel_id = action.get("parcel_id")
        parcel = next((p for p in parcels if p.get("parcel_id") == parcel_id), None) or (
            H.ticket_parcel(ctx.ticket, order) if order else None
        )
        if not parcel or not parcel.get("delay_cause"):
            return Verdict.escalate("thiếu delay_cause trong tracking DB, không tự ghi lỗi hãng")

    return Verdict.allow()
