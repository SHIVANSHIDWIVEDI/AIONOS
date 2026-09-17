# # AIONOS Assignment 3 — Customer Resolution Agent

## What this is
A working Streamlit prototype for the Customer-Facing Resolution Agent assignment.

The prototype:
- identifies customer intent from the conversation;
- uses the supplied customer, booking and policy data;
- applies explicit policy guardrails;
- recommends an allowed action or escalation;
- keeps a visible action record;
- handles cancellation, delay, hotel, refund, rebooking and escalation requests.

## Run locally
```bash
pip install -r requirements.txt
streamlit run app.py
```


## Demo scenarios
1. Priya Nair — cancellation, refund/rebooking, business-class request.
2. Arvind Kulkarni — 4-hour delay and hotel request.
3. Meher Kaur — 6-hour delay, full-night hotel request and ₹2,000 fare difference.
