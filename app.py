import streamlit as st
import networkx as nx
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# --- 1. SETUP & CONFIG ---
st.set_page_config(page_title="Contagion Simulator", layout="wide")
st.title("🕸️ Financial Contagion Simulator (High Leverage Edition)")

# --- 2. DATA GENERATION (TUNED FOR CHAOS) ---
def generate_economy(num_banks=8):
    np.random.seed(42) 
    
    bank_names = [f"Bank {chr(65+i)}" for i in range(num_banks)]
    
    # Capital between 10 and 50
    capital_values = np.random.randint(10, 50, size=num_banks)
    
    df_banks = pd.DataFrame({
        'ID': bank_names,
        'Capital': capital_values,
        'Original_Capital': capital_values, # We store this here
        'Status': 'Solvent'
    })
    
    loans = []
    # Create connections
    for _ in range(num_banks * 3): 
        lender = np.random.choice(bank_names)
        borrower = np.random.choice(bank_names)
        amount = np.random.randint(20, 70) 
        
        if lender != borrower:
            if not any(l == lender and b == borrower for l, b, a in loans):
                loans.append((lender, borrower, amount))
            
    return df_banks, loans

# Initialize Session State
if 'df_banks' not in st.session_state:
    st.session_state.df_banks, st.session_state.loans = generate_economy()
    st.session_state.simulation_log = []

def run_simulation(df, loans_list, patient_zero, recovery_rate):
    sim_df = df.copy()
    
    sim_df.set_index('ID', inplace=True)
    
    logs = []
    
    G = nx.DiGraph()
    for l, b, a in loans_list:
        G.add_edge(l, b, weight=a)
        
    # Crash Patient Zero
    sim_df.loc[patient_zero, 'Status'] = 'Bankrupt'
    sim_df.loc[patient_zero, 'Capital'] = 0
    logs.append(f"💥 {patient_zero} defaults! (Patient Zero)")
    
    failed_queue = [patient_zero]
    visited_failures = {patient_zero}
    
    while failed_queue:
        current_failed = failed_queue.pop(0)
        
        lenders = list(G.predecessors(current_failed))
        
        for lender in lenders:
            if lender in visited_failures:
                continue
                
            amount_lent = G[lender][current_failed]['weight']
            loss = amount_lent * (1 - recovery_rate)
            
            old_cap = sim_df.loc[lender, 'Capital']
            sim_df.loc[lender, 'Capital'] -= loss
            new_cap = sim_df.loc[lender, 'Capital']
            
            logs.append(f"{lender} loses ${loss:.1f} from {current_failed}")
            
            if new_cap <= 0:
                sim_df.loc[lender, 'Status'] = 'Bankrupt'
                visited_failures.add(lender)
                failed_queue.append(lender)
                logs.append(f"{lender} INSOLVENT! ({old_cap} -> {new_cap:.1f})")
    
    # 3. RESET INDEX so 'ID' becomes a column again before returning
    return sim_df.reset_index(), visited_failures, logs

# --- 4. UI & VISUALIZATION ---
with st.sidebar:
    st.header("Controls")
    
    bank_options = st.session_state.df_banks['ID'].tolist()
    patient_zero = st.selectbox("Trigger Failure In:", bank_options)
    
    recovery = st.slider("Recovery Rate (0=Total Loss)", 0.0, 1.0, 0.0, 0.1)
    
    if st.button("KILL BANK"):
        st.session_state.run_sim = True
        
    if st.button("New Economy"):
        st.session_state.df_banks, st.session_state.loans = generate_economy()
        st.session_state.run_sim = False
        st.session_state.simulation_log = []

col_graph, col_data = st.columns([2, 1])

# Run Logic
if st.session_state.get('run_sim', False):
    final_df, failed_set, logs = run_simulation(
        st.session_state.df_banks, 
        st.session_state.loans, 
        patient_zero, 
        recovery
    )
    st.session_state.simulation_log = logs
else:
    final_df = st.session_state.df_banks
    failed_set = set()

# Draw Graph
with col_graph:
    st.subheader("Interbank Network")
    fig, ax = plt.subplots(figsize=(10, 7))
    G_viz = nx.DiGraph()
    
    # Add nodes/edges
    for _, row in final_df.iterrows():
        G_viz.add_node(row['ID'])
    for l, b, a in st.session_state.loans:
        G_viz.add_edge(l, b)
        
    # Colors
    node_colors = []
    for node in G_viz.nodes():
        # Safe lookup for status
        status = final_df[final_df['ID'] == node]['Status'].values[0]
        if status == 'Bankrupt':
            node_colors.append('#FF4B4B') 
        else:
            node_colors.append('#00CC96') 
            
    pos = nx.shell_layout(G_viz)
    nx.draw(G_viz, pos, ax=ax, node_color=node_colors, with_labels=True, 
            node_size=2500, edge_color='#cccccc', font_weight='bold', arrowsize=20)
    st.pyplot(fig)

# Show Data
with col_data:
    st.subheader("Balance Sheets")
    
    # CHECK: Does the dataframe actually have the columns we want?
    # This prevents the KeyError by ensuring we only ask for existing columns
    cols_to_show = ['ID', 'Original_Capital', 'Capital', 'Status']
    
    # Just in case of errors, we filter to only available columns
    actual_cols = [c for c in cols_to_show if c in final_df.columns]
    
    st.dataframe(final_df[actual_cols], hide_index=True)
    
    st.subheader("Event Log")
    if st.session_state.simulation_log:
        for log in st.session_state.simulation_log:
            if "INSOLVENT" in log or "defaults" in log:
                st.error(log)
            elif "loses" in log:
                st.warning(log)
            else:
                st.success(log)
    else:
        st.info("System Stable.")