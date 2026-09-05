 # PayAssist AI

## AI-Powered Payment Support & Resolution Assistant

PayAssist AI is an AI-powered support copilot that helps support teams investigate customer payment issues, understand the likely cause, assess customer impact, prioritize cases, and generate clear customer-ready responses.

> **Prototype:** This project uses synthetic transaction data and simulates payment-system integration. It does not connect to a live bank or payment gateway and does not perform real financial transactions.

## Problem

Payment-related customer complaints can be difficult for support teams to investigate quickly.

For example:

> "₹2,000 was deducted, but my order failed."

A support agent may need to check transaction details, understand the failure reason, determine whether a refund is pending, assess the urgency, and explain the situation to the customer.

PayAssist AI brings these steps together in one support workflow.

## Solution

The support agent enters a transaction ID. PayAssist AI retrieves the available transaction information and provides:

- Transaction details
- Likely issue explanation
- Customer impact
- Recommended next action
- Risk level
- Support priority
- Customer-ready response

The AI assists the support agent rather than making autonomous financial decisions.

## Key Features

### Transaction Investigation

Search transactions using a transaction ID and view relevant payment information.

### AI Investigation

Gemini analyzes the available transaction information and explains:

- Likely issue
- Customer impact
- Recommended action
- Risk level

### Customer Response Generator

Generates a concise and professional response that the support agent can review before sending.

### Support Priority

Cases are categorized into priority levels based on transaction conditions such as pending refunds, failure reasons, and transaction amount.

### Support Analytics

Provides an overview of:

- Total transactions
- Successful payments
- Failed payments
- Failed payment amounts
- Pending refund amounts
- Failure reasons

### Human Verification

PayAssist AI is a support copilot. Sensitive financial actions remain under human verification.

## How It Works

```text
Customer Complaint
       ↓
Support Agent
       ↓
PayAssist AI
       ↓
Transaction Data
       ↓
AI Investigation
       ↓
Issue + Customer Impact
       ↓
Recommended Action + Risk
       ↓
Customer Response
       ↓
Support Agent Review
       ↓
Customer
```

## Architecture

```text
Customer
   ↓
Support Agent
   ↓
PayAssist AI (Streamlit)
   ↓
Transaction Data (CSV + Pandas)
   ↓
Transaction Investigation
   ↓
Gemini AI
   ↓
AI Insights + Customer Response
   ↓
Human Verification
```

## Technology Stack

- Python
- Streamlit
- Pandas
- Google Gemini API
- python-dotenv
- CSV-based synthetic transaction data

## Example Scenarios

| Transaction | Amount | Payment Method | Issue | Priority |
|---|---:|---|---|---|
| TXN1012 | ₹6,999 | UPI | Bank Timeout | High |
| TXN1017 | ₹2,199 | UPI | Network Error | Medium |
| TXN1014 | ₹2,999 | Card | Payment Declined | Low |

## Safety & Responsible AI

PayAssist AI is designed as a support copilot, not an autonomous financial decision-maker.

The prototype:

- Uses synthetic transaction data
- Does not connect to real bank accounts
- Does not initiate refunds
- Does not perform financial transactions
- Uses only the transaction information provided to the AI
- Avoids unsupported financial assumptions
- Keeps sensitive financial actions under human verification

In a production system, transaction information could be supplied through secure payment gateway APIs, webhooks, and internal support systems.

## Installation

### 1. Clone or download the repository

Download the project and open the project folder in your development environment.

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure the Gemini API key

Create a `.env` file in the project root:

```text
GOOGLE_API_KEY=your_api_key_here
```

Do not upload `.env` to GitHub.

### 4. Run the application

```bash
streamlit run app.py
```

The application will open in your browser.

## Demo

Try these transaction IDs:

```text
TXN1012
TXN1017
TXN1014
```

### TXN1012 — High Priority

- Amount: ₹6,999
- Payment Method: UPI
- Status: Failed
- Failure Reason: Bank Timeout
- Refund Status: Pending

This demonstrates how PayAssist AI investigates a payment failure, assesses customer impact, recommends a next step, and generates a customer-ready response.

### TXN1017 — Medium Priority

Demonstrates a network-related payment failure with a pending refund status.

### TXN1014 — Low Priority

Demonstrates a payment declined scenario where the transaction did not proceed.

## Future Scope

- Integration with real payment gateway APIs
- Webhook-based transaction updates
- Secure database integration
- Automated support ticket creation
- Advanced payment failure analysis
- Support-team analytics
- Role-based access control
- Audit logs for AI recommendations and human actions

## Project Status

**Prototype — Built for the Razorpay AI Builder Buildathon 2026**
