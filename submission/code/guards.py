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


def _analyze_parcels(ctx, order):
    """Identify which parcel(s) in `order` are actually late under the effective policy."""
    parcels = (order or {}).get("parcels") or []
    policies = ctx.tools.lookup_policies()
    pol = H.effective_policy(policies, ctx.as_of) or next((p for p in policies if p.get("index_active")), None)
    min_days = (pol or {}).get("late", {}).get("min_days_fee", 1)
    late_parcels = [p for p in parcels if H.db_delay_days(p, ctx.as_of) >= min_days]
    explicit_id = (ctx.ticket or {}).get("parcel_id")
    if explicit_id:
        match = next((p for p in parcels if p.get("parcel_id") == explicit_id), None)
        return ([match] if match else []), pol
    return late_parcels, pol


def _will_file_fault(ctx):
    """Check if the current proposal intends to file a carrier fault."""
    prop = next((e for e in reversed(ctx.events or []) if e.get("type") == "proposal"), None)
    return bool(prop and prop.get("do_fault"))


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

    # 3. Kiểm tra trước khi ghi (issue_refund & file_carrier_fault): tách kiện & trần lỗi/hãng/ngày (S6)
    if tool in ("issue_refund", "file_carrier_fault") and action.get("order_id"):
        order = ctx.tools.lookup_order(action["order_id"])
        if order and (tool == "file_carrier_fault" or _will_file_fault(ctx)):
            late_parcels, _ = _analyze_parcels(ctx, order)
            if len(late_parcels) > 1:
                return Verdict.escalate("đơn nhiều kiện cùng trễ chưa rõ kiện nào, chuyển người duyệt")
            if len(late_parcels) == 1:
                target = late_parcels[0]
                if gates.get("legal", {}).get("carrier_fault_requires_recorded_cause") and not target.get("delay_cause"):
                    return Verdict.escalate("kiện trễ thiếu delay_cause trong tracking DB, chuyển người duyệt")
                max_strikes = (ctx.tools.ops_limits() or {}).get("max_auto_strikes_per_carrier_per_day")
                if max_strikes is not None:
                    today_faults = ctx.tools.fault_rows(carrier_id=target.get("carrier_id"))
                    if len(today_faults) >= max_strikes:
                        return Verdict.escalate("vượt ngưỡng lỗi tự động/hãng/ngày, chuyển người duyệt")
                if tool == "file_carrier_fault" and action.get("parcel_id") != target.get("parcel_id"):
                    return Verdict.modify(
                        "chọn đúng kiện trễ trong đơn tách kiện",
                        parcel_id=target.get("parcel_id"),
                        carrier_id=target.get("carrier_id"),
                        driver_id=target.get("driver_id"),
                        delay_days=H.db_delay_days(target, ctx.as_of),
                    )

    # 4. Kiểm tra trần hoàn tự động theo ngày (business.daily_refund_cap_vnd)
    if tool == "issue_refund":
        cap = gates.get("business", {}).get("daily_refund_cap_vnd")
        spent = ctx.tools.auto_refund_today_vnd()
        if cap is not None and spent + action.get("amount_vnd", 0) > cap:
            return Verdict.escalate("vượt trần hoàn tự động trong ngày, chuyển người duyệt")

    return Verdict.allow()
