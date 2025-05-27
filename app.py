import streamlit as st
import pandas as pd

st.set_page_config(page_title="Text Labeling Gamified", layout="wide")
st.title("🎮 Quick Text Labeling App")

uploaded_file = st.sidebar.file_uploader("Upload a CSV file", type="csv")
if not uploaded_file:
    st.sidebar.info("Please upload a CSV to get started.")
    st.stop()

df = pd.read_csv(uploaded_file)

st.session_state.setdefault("idx", 0)
st.session_state.setdefault("labels", {})

cols = st.sidebar.multiselect(
    "Columns to display",
    options=df.columns.tolist(),
    default=df.columns.tolist()[:1]
)

label_input = st.sidebar.text_input(
    "Enter labels (comma-separated)",
    value="Positive,Negative,Neutral"
)
base_labels = [l.strip() for l in label_input.split(",") if l.strip()]

label_options = ["Select…"] + base_labels


c1, _, c3 = st.sidebar.columns([1,2,1])
with c1:
    if st.button("◀️ Prev") and st.session_state.idx > 0:
        st.session_state.idx -= 1
with c3:
    if st.button("Next ▶️") and st.session_state.idx < len(df)-1:
        st.session_state.idx += 1

st.sidebar.markdown(f"**{st.session_state.idx+1} / {len(df)}**")

row = df.iloc[st.session_state.idx]
st.markdown("---")
st.subheader("Record to label:")
for c in cols:
    st.markdown(f"**{c}**: {row[c]}")

key = f"label_radio_{st.session_state.idx}"

if st.session_state.idx in st.session_state.labels:
    default_i = base_labels.index(st.session_state.labels[st.session_state.idx]) + 1
else:
    default_i = 0

choice = st.radio(
    "Assign a label:",
    options=label_options,
    index=default_i,
    key=key
)

if choice != "Select…":
    st.session_state.labels[st.session_state.idx] = choice
elif st.session_state.idx in st.session_state.labels:
    del st.session_state.labels[st.session_state.idx]

if st.sidebar.button("📥 Download Labeled CSV"):
    out = df.copy()
    out["label"] = ""
    for idx, lbl in st.session_state.labels.items():
        out.at[idx, "label"] = lbl
    csv = out.to_csv(index=False).encode("utf-8")
    st.sidebar.download_button(
        "Download annotated CSV",
        data=csv,
        file_name="labeled_data.csv",
        mime="text/csv"
    )
