import json
from pathlib import Path
import streamlit as st

st.set_page_config(page_title="AIONOS Customer Resolution Agent", page_icon="✈️", layout="wide")

DATA_PATH = Path(__file__).parent / "data" / "policy_and_scenarios.json"
with open(DATA_PATH, "r", encoding="utf-8") as f:
    data = json.load(f)

profiles = {x["name"]: x for x in data["customer_profiles"]}
bookings = {x["pnr"]: x for x in data["booking_data"]}
rules = data["service_rules"]

st.title("✈️ AIONOS Customer Resolution Agent")
st.caption("Assignment 3 • Customer-facing airline disruption resolution prototype")

with st.sidebar:
    st.header("Customer")
    customer_name = st.selectbox("Select a supplied scenario", list(profiles.keys()))
    profile = profiles[customer_name]
    booking = bookings[profile["pnr"]]
    st.write(f"**Tier:** {profile['tier']}")
    st.write(f"**PNR:** {profile['pnr']}")
    st.write(f"**Flight:** {booking['flight_number']}")
    st.write(f"**Route:** {booking['route']}")
    st.divider()
    st.info("Prototype uses only the supplied assignment data and policy rules.")

if "messages" not in st.session_state:
    st.session_state.messages = []

# Scenario-specific context
scenario = next(s for s in data["scenarios"] if s["customer"] == customer_name)

st.subheader("1. Customer conversation")
for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        st.markdown(m["content"])

prompt = st.chat_input("Example: I want a refund / I need a hotel / Can I take the higher-fare flight?")
if prompt:
    st.session_state.messages.append({"role":"user", "content":prompt})
    p = prompt.lower()

    # Deterministic policy reasoning over supplied facts.
    if "refund" in p or "cash" in p:
        if booking["disruption_type"] == "cancelled":
            response = (
                f"I understand the frustration. Your flight {booking['flight_number']} was cancelled. "
                "Under the supplied policy, you can choose a full refund to the original payment method "
                "within 7 business days, or free rebooking on the next available flight within 24 hours."
            )
            action = "Initiate full refund to original payment method"
            status = "Allowed"
        else:
            response = (
                "The supplied policy gives full refunds specifically for airline-caused cancellations. "
                "For this delayed booking, I would not promise a refund under the supplied rules."
            )
            action = "Escalate / do not promise refund"
            status = "Needs review"

    elif "hotel" in p or "stay" in p:
        hours = booking.get("delay_hours", 0)
        if hours > 5:
            response = (
                f"Your flight is delayed by {hours} hours. The supplied policy provides meal voucher, "
                "lounge access, and hotel accommodation covering only the delayed hours—not the full night."
            )
            action = "Arrange delayed-hours hotel + meal voucher + lounge access"
            status = "Allowed"
        elif hours > 3:
            response = "For a delay over 3 hours, the supplied policy provides a meal voucher and lounge access. Hotel accommodation is not listed for this delay."
            action = "Issue meal voucher + lounge access"
            status = "Allowed"
        else:
            response = "For a delay under 3 hours, the supplied policy provides a ₹500 meal voucher."
            action = "Issue ₹500 meal voucher"
            status = "Allowed"

    elif "business" in p or "upgrade" in p or "higher" in p or "2000" in p:
        response = (
            "A higher-fare rebooking requires the customer to pay the fare difference. "
            "The agent cannot waive a fare difference above ₹1,500 without supervisor approval."
        )
        action = "Escalate for supervisor approval if waiver above ₹1,500 is requested"
        status = "Escalation required"

    elif "rebook" in p or "next flight" in p:
        if booking["disruption_type"] == "cancelled":
            response = "You can be rebooked free of charge on the next available flight within 24 hours. Gold and Platinum customers receive priority rebooking."
        else:
            response = "The supplied data confirms your current delayed flight status. I can provide the permitted delay support, but I will not invent an alternative flight."
        action = "Rebook next available within 24h" if booking["disruption_type"] == "cancelled" else "Provide delay support"
        status = "Allowed"

    elif any(x in p for x in ["lawyer", "legal", "sue", "complaint", "threat"]):
        response = "I can record the issue, but the supplied policy says threats, legal/formal complaints should be escalated immediately."
        action = "Escalate immediately"
        status = "Escalation required"

    else:
        response = (
            f"I can help with the disruption on {booking['flight_number']}. "
            f"Your current supplied status is: {booking['status']}. "
            "Please tell me whether you need rebooking, refund information, or disruption support."
        )
        action = "Clarify customer intent"
        status = "Information / clarification"

    st.session_state.messages.append({"role":"assistant", "content":response})
    st.session_state.last_action = action
    st.session_state.last_status = status
    st.rerun()

st.divider()
st.subheader("2. Agent decision & action record")

col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Disruption", booking["status"])
with col2:
    st.metric("Customer Tier", profile["tier"])
with col3:
    st.metric("Policy Guardrail", "Active")

action = st.session_state.get("last_action", "No action selected yet")
status = st.session_state.get("last_status", "Waiting")

st.write(f"**Recommended action:** {action}")
if status == "Allowed":
    st.success(status)
elif status == "Escalation required":
    st.warning(status)
else:
    st.info(status)

with st.expander("Supplied policy rules used by the agent"):
    for k, v in rules.items():
        st.write(f"**{k}:** {v}")

with st.expander("Current customer + booking record"):
    st.json({"customer": profile, "booking": booking})

if st.button("Clear conversation"):
    st.session_state.messages = []
    st.session_state.pop("last_action", None)
    st.session_state.pop("last_status", None)
    st.rerun()
