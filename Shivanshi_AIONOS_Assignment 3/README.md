# AIONOS Assignment 3 — Customer Resolution Agent

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

Then open the local Streamlit URL shown in the terminal.

## Demo scenarios
1. Priya Nair — cancellation, refund/rebooking, business-class request.
2. Arvind Kulkarni — 4-hour delay and hotel request.
3. Meher Kaur — 6-hour delay, full-night hotel request and ₹2,000 fare difference.

## Important
The assignment data pack says to use only the supplied material. This prototype therefore avoids inventing flight options, compensation, customer information or policies.

## Submission
The assignment brief requires:
- working/clickable prototype;
- architecture/process flow;
- inputs, sources and assumptions;
- AI tools used and how they were used;
- 15-minute demo/defence;
- open-access Drive demo video;
- GitHub link;
- 10-slide PPT.

The brief does not state the actual submission portal URL. Upload/submit through the portal provided by AIONOS/university/recruiter, if separately communicated.

## Suggested GitHub repository
`aionos-assignment-3-customer-resolution-agent`
