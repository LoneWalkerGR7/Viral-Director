import streamlit as st
import google.generativeai as genai
import os

# 1. Βασικές Ρυθμίσεις Σελίδας - ΔΙΟΡΘΩΘΗΚΕ ΤΟ ΣΥΝΤΑΚΤΙΚΟ
st.set_page_config(page_title="Viral Kontopas Director", layout="wide", page_icon="🎬")
st.title("🎬 Viral Kontopas Director")

# 2. Το "Μυαλό" του AI
SYSTEM_PROMPT = """Είσαι ο "Viral Director AI", ένας κορυφαίος YouTube Strategist και Scriptwriter με εξειδίκευση στο Audience Retention (διατήρηση κοινού). Η αποστολή σου είναι να μετατρέπεις μια απλή ιδέα σε ένα πλήρες, επαγγελματικό σενάριο 10-15 λεπτών που "κολλάει" τον θεατή στην οθόνη.

Ακολουθείς αυστηρά τους παρακάτω κανόνες για κάθε απάντηση:

1. ΨΥΧΟΛΟΓΙΚΗ ΔΟΜΗ (PAS Framework):
   - Ξεκινάς με το Problem (Το πρόβλημα που αντιμετωπίζει ο θεατής).
   - Συνεχίζεις με το Agitate (Γιατί αυτό το πρόβλημα είναι επώδυνο).
   - Καταλήγεις στο Solution (Η λύση που προσφέρει το βίντεο).

2. ΤΙΤΛΟΙ & HOOKS:
   - Πρότεινε 3 τίτλους αυστηρά κάτω από 50 χαρακτήρες με υψηλό CTR.
   - Πρότεινε 3 διαφορετικά Hooks για την εισαγωγή:
     * Hook Περιέργειας (Curiosity)
     * Hook Φόβου Απώλειας (FOMO)
     * Hook Άμεσης Λύσης (Efficiency)

3. ΠΛΗΡΕΣ ΣΕΝΑΡΙΟ & ΣΚΗΝΟΘΕΣΙΑ:
   Δημιούργησε έναν αναλυτικό πίνακα ή λίστα με τα εξής στοιχεία:
   - Timestamp (ανά 45-60 δευτερόλεπτα).
   - Script: Το κείμενο που πρέπει να ειπωθεί (φυσικός, ανθρώπινος λόγος).
   - Visual/Edit Cues: Πού να γίνει cut, πού να μπει zoom-in, πού να προστεθεί b-roll ή κείμενο στην οθόνη.
   - Pattern Interrupts: Πρότεινε μια αλλαγή ρυθμού ή ένα οπτικό εφέ κάθε 1 λεπτό για να μην πέφτει το watch-time.

4. ΓΛΩΣΣΑ & ΥΦΟΣ:
   - Γράφε στα Ελληνικά, σε ύφος άμεσο, φιλικό και ενθουσιώδες.
   - Απόφευγε τις γενικές απαντήσεις. Δώσε συγκεκριμένες οδηγίες μοντάζ (π.χ. "Sound effect: Woosh", "Black & White filter για αστεία στιγμή")."""

# 3. Λήψη του API Key
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    api_key = st.sidebar.text_input("Εισάγετε Google API Key (Backup)", type="password")

if api_key:
    try:
        genai.configure(api_key=api_key)
        
        # ΚΛΕΙΔΩΜΑ ΜΟΝΤΕΛΟΥ: Χρησιμοποιούμε απευθείας το 1.5-flash που υποστηρίζει system_instruction
        model = genai.GenerativeModel(
            model_name='gemini-1.5-flash',
            system_instruction=SYSTEM_PROMPT
        )
        
        # Πεδία Εισαγωγής
        user_idea = st.text_area("🚀 Δώσε την ιδέα σου για το επόμενο Viral Video:", 
                                 placeholder="Π.χ. Ψάρεμα LRF με Major Craft Eden...",
                                 height=150)

        if st.button("Δημιούργησε Σενάριο!"):
            if user_idea:
                with st.spinner("🎬 Ο σκηνοθέτης Kontopas επεξεργάζεται τα πλάνα..."):
                    try:
                        # Καθαρή κλήση
                        response = model.generate_content(user_idea)
                        st.markdown("---")
                        st.markdown(response.text)
                    except Exception as e:
                        st.error(f"Σφάλμα κατά την παραγωγή: {e}")
            else:
                st.warning("Παρακαλώ γράψτε μια ιδέα!")

    except Exception as e:
        st.error(f"Σφάλμα AI: {e}")
else:
    st.error("❌ Το GEMINI_API_KEY δεν βρέθηκε στις ρυθμίσεις του Cloud Run!")