import streamlit as st
import google.generativeai as genai
import os

# 1. Βασικές Ρυθμίσεις Σελίδας
st.set_page_config(page_title="Viral Kontopas Director", layout="wide", page_icon="🎬")
st.title("🎬 Viral Kontopas Director")

# 2. Το "Μυαλό" του AI (System Prompt)
SYSTEM_PROMPT = """Είσαι ο "Viral Director AI", ένας κορυφαίος YouTube Strategist. 
Αποστολή σου: Μετάτρεψε την ιδέα σε επαγγελματικό σενάριο 10-15 λεπτών.

ΔΟΜΗ ΑΠΑΝΤΗΣΗΣ:
1. 3 Τίτλοι με υψηλό CTR.
2. 3 Hooks (Curiosity, FOMO, Efficiency).
3. Αναλυτικό Σενάριο με Timestamps, Script και οδηγίες μοντάζ (Visual Cues).
4. Pattern Interrupts κάθε 1 λεπτό.

Γλώσσα: Ελληνικά. Ύφος: Ενθουσιώδες και άμεσο."""

# 3. Λήψη του API Key
api_key = st.secrets.get("GEMINI_API_KEY") or os.getenv("GEMINI_API_KEY")

if not api_key:
    api_key = st.sidebar.text_input("Εισάγετε Google API Key", type="password")

if api_key:
    try:
        genai.configure(api_key=api_key)
        
        # Χρήση του gemini-pro που είναι το πιο σταθερό παγκοσμίως
        # Προσοχή: Το gemini-pro δεν δέχεται system_instruction στην κατασκευή, 
        # οπότε θα το προσθέσουμε στο κείμενο παρακάτω.
        model = genai.GenerativeModel('gemini-pro')
        
        st.sidebar.success("AI Engine: Stable Gemini Pro")

        # 4. Πεδία Εισαγωγής
        user_idea = st.text_area("🚀 Δώσε την ιδέα σου για το επόμενο Viral Video:", 
                                 placeholder="Π.χ. Ψάρεμα LRF με Major Craft Eden...",
                                 height=150)

        if st.button("Δημιούργησε Σενάριο!"):
            if user_idea:
                with st.spinner("🎬 Ο σκηνοθέτης Kontopas γράφει το σενάριο..."):
                    try:
                        # Συνενώνουμε τις οδηγίες με την ιδέα του χρήστη
                        full_query = f"{SYSTEM_PROMPT}\n\nΙΔΕΑ ΧΡΗΣΤΗ: {user_idea}"
                        
                        response = model.generate_content(full_query)
                        
                        if response.text:
                            st.markdown("---")
                            st.subheader("📝 Το Viral Σενάριό σου")
                            st.markdown(response.text)
                        else:
                            st.error("Η AI δεν επέστρεψε κείμενο. Δοκίμασε να αλλάξεις λίγο την περιγραφή.")
                            
                    except Exception as e:
                        st.error(f"Σφάλμα κατά την παραγωγή: {e}")
            else:
                st.warning("Παρακαλώ γράψτε μια ιδέα!")

    except Exception as e:
        st.error(f"Σφάλμα AI: {e}")
else:
    st.info("💡 Παρακαλώ εισάγετε το Google API Key σας για να ξεκινήσετε.")
