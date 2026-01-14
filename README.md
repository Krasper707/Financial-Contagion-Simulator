
# 🕸️ Financial Contagion Simulator

### A Network Science Approach to Systemic Risk Analysis

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://streamlit.io)
[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://www.python.org/)
[![Graph Theory](https://img.shields.io/badge/NetworkX-Graph%20Theory-red)](https://networkx.org/)

## Overview
This application is a Systemic Risk Engine designed to conduct Stress Testing on an interbank network. While traditional Credit Risk models assess individual borrower default, this engine models Second-Order Effects (Contagion).

Leveraging Graph Theory, it identifies Systemically Important Financial Institutions (SIFIs)—banks that are "Too Big To Fail"—and simulates how an Idiosyncratic Shock (single bank failure) transmits through the Counterparty Exposure Matrix, leading to potential Liquidity Crises.

<img width="1919" height="1037" alt="image" src="https://github.com/user-attachments/assets/61387187-2a25-486b-ae35-d2038e20c4be" />

## Features
*   **Interactive Network Graph:** Visualizes banks (Nodes) and interbank loans (Directed Edges).
*   **"Idiosyncratic Shock Injection" Simulation:** Select any bank to be "Patient Zero" and trigger a bankruptcy.
*   **Recursive Shock Propagation:** Algorithms automatically calculate the chain reaction of losses across the network.
*   **Real-time Balance Sheets:** Watch Capital buffers deplete in real-time.
*   **Adjustable Recovery Rates:** Test scenarios from "Total Loss" (0%) to "Partial Recovery" (e.g., 40%).
*   **Detailed Event Logs:** Track exactly how much money was lost by each institution during the crash.

## Tech Stack
*   **Python:** Core logic and data processing.
*   **NetworkX:** Graph algorithms (Directed Graphs, Predecessor lookup) to model financial connections.
*   **Streamlit:** Interactive web dashboard and UI.
*   **Pandas:** Balance sheet manipulation and state management.
*   **Matplotlib:** Network visualization and rendering.

## The Logic (How it works)
1.  **The Economy:** We generate a synthetic financial system where banks hold Capital (Equity) and owe money to each other (Interbank Loans).
2.  **The Shock:** User selects a bank to fail (Capital = 0).
3.  **The Propagation:**
    *   The algorithm identifies all **Creditors** (banks that lent money *to* the failed bank).
    *   Losses are applied based on the loan amount and the `Recovery Rate`.
    *   `New Capital = Old Capital - (Loan Amount * (1 - Recovery Rate))`
4.  **The Cascade:** If a Creditor's capital falls below 0, they become the new "Failed Bank," and the loop repeats recursively until the system stabilizes.
## Risk Methodology
This simulator applies core **Basel III** and **Risk Management** principles:

1.  **Counterparty Credit Risk:**
    *   The model treats interbank loans as assets subject to default risk.
    *   We calculate the **Exposure at Default (EAD)** for every lender node.

2.  **Solvency Stress Testing:**
    *   The simulation applies a **Scenario Analysis** (a core Goldman Risk function).
    *   **Scenario:** "What if a Top-3 Bank defaults with 60% LGD?"
    *   The model checks if the Lender's **Capital Buffer** is sufficient to absorb the loss.

3.  **Mitigation Analysis:**
    *   By adjusting the connectivity (topology), we can observe how **Diversification** (spreading loans across many banks) mitigates systemic collapse.

## Installation & Usage

1. **Clone the repository**
   ```bash
   git clone https://github.com/Krasper707/financial-contagion-simulator.git
   cd financial-contagion-simulator
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**
   ```bash
   streamlit run app.py
   ```

## Requirements
Create a `requirements.txt` file with the following:
```text
streamlit
pandas
networkx
matplotlib
numpy
```

## Future Improvements
*   Implement **PageRank** to identify "Too Big To Fail" banks automatically.
*   Add **Bailout Mechanisms** (Inject capital to stop the spread).
*   Use **Plotly** for interactive, hover-over graph visualizations.

## License
[MIT](https://choosealicense.com/licenses/mit/)
```


