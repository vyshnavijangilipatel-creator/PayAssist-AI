import streamlit as st
import pandas as pd
import os
from dotenv import load_dotenv
from google import genai
load_dotenv()
# Initialize Gemini Client
client = genai.Client(api_key=os.environ["GOOGLE_API_KEY"])

# PAGE CONFIGURATION
st.set_page_config(
    page_title="PayAssist AI",
    page_icon="💳",
    layout="wide"
)
# SIDEBAR
with st.sidebar:

    st.title("💳 PayAssist AI")
    st.caption("Payment Support Copilot")

    st.divider()

    st.write("### What PayAssist AI does")

    st.write(
        "Helps support teams investigate payment issues, "
        "understand customer impact, prioritize cases, "
        "and generate customer-ready responses."
    )

    st.divider()

    st.write("### 🛡️ Safety")

    st.write("AI recommends actions.")
    st.write("Humans verify sensitive financial actions.")

# MAIN TITLE
st.title("💳 PayAssist AI")

st.subheader(
    "Intelligent Payment Support & Resolution Assistant"
)

st.write(
    "An AI-powered copilot for payment support teams to investigate "
    "transaction issues, understand customer impact, prioritize cases, "
    "and generate clear customer responses."
)

st.info(
    "👩‍💼 Support Copilot — AI assists the support agent; "
    "sensitive financial actions remain under human verification."
)

st.caption(
    "🟢 Prototype: Ready | 🤖 AI: Gemini | "
    "📊 Data: Synthetic Transactions"
)
# LOAD TRANSACTION DATA
df = pd.read_csv("transactions.csv")

# DASHBOARD METRICS
total_transactions = len(df)

successful_transactions = len(
    df[df["status"] == "SUCCESS"]
)

failed_transactions = len(
    df[df["status"] == "FAILED"]
)

pending_refund_df = df[
    df["refund_status"] == "PENDING"
]

pending_refund_amount = pending_refund_df["amount"].sum()


col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Total Transactions",
        total_transactions
    )

with col2:
    st.metric(
        "Successful Payments",
        successful_transactions
    )

with col3:
    st.metric(
        "Failed Payments",
        failed_transactions
    )

with col4:
    st.metric(
        "Pending Refund Amount",
        f"₹{pending_refund_amount:,.0f}"
    )

# TRANSACTION TABLE
st.divider()

st.subheader("📋 Transaction Records")

st.dataframe(
    df,
    use_container_width=True,
    hide_index=True
)

# TRANSACTION INVESTIGATION
st.divider()

st.subheader("🔍 Transaction Investigation")

transaction_id = st.text_input(
    "Enter Transaction ID",
    placeholder="Example: TXN1002"
)


if transaction_id:

    transaction_result = df[
        df["transaction_id"].astype(str).str.upper()
        == transaction_id.strip().upper()
    ]
 
    # CHECK WHETHER TRANSACTION EXISTS
    if not transaction_result.empty:

        transaction = transaction_result.iloc[0]
         
        # TRANSACTION DETAILS
        st.write("### Transaction Details")

        col1, col2, col3 = st.columns(3)

        with col1:

            st.write(
                "**Transaction ID:**",
                transaction["transaction_id"]
            )

            st.write(
                "**Customer ID:**",
                transaction["customer_id"]
            )

            st.write(
                "**Amount:**",
                f"₹{transaction['amount']:,.0f}"
            )


        with col2:

            st.write(
                "**Payment Method:**",
                transaction["payment_method"]
            )

            st.write(
                "**Status:**",
                transaction["status"]
            )

            st.write(
                "**Failure Reason:**",
                transaction["failure_reason"]
            )


        with col3:

            st.write(
                "**Refund Status:**",
                transaction["refund_status"]
            )

            st.write(
                "**Attempt Count:**",
                transaction["attempt_count"]
            )

            st.write(
                "**Timestamp:**",
                transaction["timestamp"]
            )  
        # TRANSACTION INFORMATION FOR AI
        
        transaction_info = f"""
Transaction ID: {transaction['transaction_id']}
Customer ID: {transaction['customer_id']}
Amount: ₹{transaction['amount']}
Payment Method: {transaction['payment_method']}
Status: {transaction['status']}
Failure Reason: {transaction['failure_reason']}
Refund Status: {transaction['refund_status']}
Attempt Count: {transaction['attempt_count']}
Timestamp: {transaction['timestamp']}
"""

        # SUPPORT PRIORITY

        amount = float(transaction["amount"])
        refund_status = transaction["refund_status"]
        failure_reason = transaction["failure_reason"]


        if refund_status == "PENDING" and amount >= 5000:

            priority = "🔴 HIGH"

        elif (
            refund_status == "PENDING"
            or failure_reason == "NETWORK_ERROR"
        ):

            priority = "🟠 MEDIUM"

        else:

            priority = "🟢 LOW"


        st.divider()

        st.subheader("🎯 Support Priority")

        st.info(
            f"Recommended Priority: **{priority}**"
        )

        # AI INVESTIGATION

        st.divider()

        st.subheader("🤖 AI Investigation")

        if st.button("🤖 Investigate with AI"):

            prompt = f"""
You are PayAssist AI, an AI assistant for payment support teams.

Analyze the following transaction information.

{transaction_info}

Provide a concise support investigation with exactly these sections:

1. Issue
2. Customer Impact
3. Recommended Action
4. Risk Level

Important:
- Only use the information provided.
- Do not claim to have contacted the bank.
- Do not claim that money was refunded unless the data says so.
- Do not invent information.
- For sensitive financial actions, recommend human verification.
-Do not assume or speculate whether money was debited, credited, or held.
-Do not provide refund timelines unless a specific timeline is explicitly provided in the transaction data.
"""

            with st.spinner(
                "AI is investigating the transaction..."
            ):

                response = client.models.generate_content(
                    model="gemini-2.5-flash",
                    contents=prompt
                )

            st.write(response.text)

        # CUSTOMER RESPONSE
        st.divider()

        st.subheader("💬 Customer Response")

        if st.button("✉️ Generate Customer Response"):

            response_prompt = f"""
You are a payment support assistant.

Based only on the following transaction information,
write a clear and polite response that a support agent
can send to the customer.

Transaction information:

{transaction_info}

Rules:
- Be polite and empathetic.
- Explain the payment issue simply.
- Do not invent information.
- Do not promise a refund unless the data confirms it.
- Do not provide unsupported refund timelines.
- Do not claim that you contacted the bank or payment gateway.
- If human verification is needed, clearly mention it.
- Keep the response concise and professional.
-Do not assume that a refund has been initiated just because the refund status is PENDING.
-Do not claim that money was debited, credited, or held unless the transaction data explicitly states it.
-Do not provide refund processing timelines or tell the customer to wait for a specific period unless a timeline is explicitly provided in the transaction data.
-Only describe the refund status exactly as provided.
"""

            with st.spinner(
                "Generating customer response..."
            ):

                customer_response = client.models.generate_content(
                    model="gemini-2.5-flash",
                    contents=response_prompt
                )

            st.write(customer_response.text)

    # INVALID TRANSACTION ID

    else:

        st.warning(
            "Transaction ID not found. Please check the ID."
        )
# SUPPORT ANALYTICS

st.divider()

st.subheader("📊 Support Analytics")

failed_df = df[
    df["status"] == "FAILED"
]

total_failed_amount = failed_df["amount"].sum()

pending_refund_amount = df[
    df["refund_status"] == "PENDING"
]["amount"].sum()


col1, col2 = st.columns(2)

with col1:

    st.metric(
        "Failed Payment Amount",
        f"₹{total_failed_amount:,.0f}"
    )

with col2:

    st.metric(
        "Pending Refund Amount",
        f"₹{pending_refund_amount:,.0f}"
    )


st.write("### Failure Reasons")

failure_counts = (
    failed_df["failure_reason"]
    .value_counts()
)

st.bar_chart(failure_counts)

# AI SAFETY & HUMAN VERIFICATION

st.divider()

st.subheader(
    "🛡️ AI Safety & Human Verification"
)

st.write(
    "PayAssist AI provides investigation insights and "
    "recommendations. Sensitive financial actions require "
    "human verification."
)


col1, col2, col3 = st.columns(3)

with col1:

    st.success(
        "✅ AI analyzes available transaction data"
    )

with col2:

    st.warning(
        "⚠️ AI does not initiate refunds"
    )

with col3:

    st.info(
        "👩‍💼 Support agent verifies sensitive actions")