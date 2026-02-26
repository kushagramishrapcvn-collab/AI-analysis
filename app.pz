import streamlit as st
from google import genai
import fitz  # PyMuPDF
import os
import uuid

# --- 1. CONFIGURATION ---
st.set_page_config(page_title="Logic-Aware Symmetry Editor", layout="wide")

# Check for the API Key in the Cloud Secrets
if "GEMINI_API_KEY" not in st.secrets:
    st.error("Missing GEMINI_API_KEY! Add it to 'Secrets' in the Streamlit Dashboard.")
    st.stop()

client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])

st.title("🎯 New Logic-Aware PDF Editor")

# --- 2. UI ---
uploaded_file = st.file_uploader("Upload Math/Marksheet PDF", type="pdf")

col1, col2 = st.columns(2)
with col1:
    target_text = st.text_input("Find text (e.g., 66)", placeholder="Old value")
with col2:
    new_instruction = st.text_input("New value/logic (e.g., 76)", placeholder="New value")

mode = st.radio(
    "Processing Mode",
    ["Surgical Edit (Single)", "Smart Logic (Recalculate Totals/Math)"],
    horizontal=True
)

if st.button("Apply & Preserves Symmetry"):
    if uploaded_file and target_text:
        with st.spinner("Analyzing document layers..."):
            # Multiuser ID to prevent path collisions
            run_id = str(uuid.uuid4())[:6]
            in_file = f"input_{run_id}.pdf"
            out_file = f"output_{run_id}.pdf"

            with open(in_file, "wb") as f:
                f.write(uploaded_file.getbuffer())

            doc = fitz.open(in_file)
            
            # --- LOGIC ENGINE ---
            if "Smart" in mode:
                full_context = "\n".join([p.get_text() for p in doc])
                prompt = f"""
                Context: {full_context}
                Task: Change '{target_text}' to '{new_instruction}'.
                Update all related math (Totals, %, derivatives).
                Return ONLY pairs: {target_text} -> {new_instruction} | OldVal -> NewVal
                """
            else:
                prompt = f"Change '{target_text}' to '{new_instruction}'. Return ONLY result."

            try:
                response = client.models.generate_content(model='gemini-2.0-flash', contents=prompt)
                ai_data = response.text.strip()

                # Parse changes
                updates = []
                if "Smart" in mode and "->" in ai_data:
                    for item in ai_data.split("|"):
                        if "->" in item:
                            o, n = item.split("->")
                            updates.append((o.strip(), n.strip()))
                else:
                    updates.append((target_text, ai_data))

                # --- APPLY SURGERY ---
                found_count = 0
                for old_val, new_val in updates:
                    for page in doc:
                        instances = page.search_for(old_val)
                        for inst in instances:
                            # 1. Whitening (surgical)
                            page.add_redact_annot(inst, fill=(1, 1, 1))
                            page.apply_redactions()
                            
                            # 2. Symmetry Insertion (Baseline -2)
                            # inst.y1 is the bottom edge of the original text box
                            page.insert_text(
                                fitz.Point(inst.x0, inst.y1 - 2), 
                                new_val, 
                                fontsize=10, 
                                fontname="helv", 
                                color=(0, 0, 0)
                            )
                            found_count += 1

                if found_count > 0:
                    doc.save(out_file)
                    with open(out_file, "rb") as f:
                        st.success(f"Updated {len(updates)} logical fields!")
                        st.download_button("Download Edited PDF", f, file_name="edited_logic.pdf")
                else:
                    st.error(f"Target text '{target_text}' not found.")

            except Exception as e:
                st.error(f"Error: {e}")

            # Cleanup
            doc.close()
            if os.path.exists(in_file): os.remove(in_file)
            if os.path.exists(out_file): os.remove(out_file)
    else:
        st.warning("Please upload a file and fill in all text fields.")
