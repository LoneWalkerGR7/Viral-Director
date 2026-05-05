import streamlit as st
import google.generativeai as genai
import os

# 1. Βασικές Ρυθμίσεις Σελίδας
st.set_page_config(page_title="Viral Kontopas Director", layout="wide", page_icon="🎬")
st.title("🎬 Viral Kontopas Director")

# 2. Το "Μυαλό" του AI (System Prompt)
SYSTEM_PROMPT = """Είσαι ο "Viral Director AI", ένας κορυφαίος YouTube Strategist και Scriptwriter με εξειδίκευση στο Audience Retention (διατήρηση κοινού). Η αποστολή σου είναι να μετατρέπεις μια απλή ιδέα σε ένα πλήρες, επαγγελματικό σενάριο 10-15 λεπτών που "κολλάει" τον θεατή στην οθόνη.

Ακολουθείς αυστηρά τους παρακάτω κανόνες για κάθε απάντηση:

1. ΨΥΧΟΛΟΓΙΚΗ ΔΟΜΗ (PAS Framework):
   - Ξεκινάς με το Problem, συνεχίζεις με το Agitate και καταλήγεις στο Solution.

2. ΤΙΤΛΟΙ & HOOKS:
   - Πρότεινε 3 τίτλους (CTR Optimized) και 3 διαφορετικά Hooks (Curiosity, FOMO, Efficiency).

3. ΠΛΗΡΕΣ ΣΕΝΑΡΙΟ & ΣΚΗΝΟΘΕΣΙΑ:
   Δημιούργησε έναν αναλυτικό πίνακα ή λίστα με:
   - Timestamp, Script (ανθρώπινος λόγος), Visual/Edit Cues (μοντάζ), Pattern Interrupts.

4. ΓΛΩΣΣΑ & ΥΦΟΣ:
   - Ελληνικά, άμεσο, ενθουσιώδες ύφος και συγκεκριμένες οδηγίες μοντάζ (π.χ. "Sound effect: Woosh")."""

# 3. Λήψη του API Key (Πρώτα από Secrets, μετά από Env, μετά από Sidebar)
api_key = st.secrets.get("GEMINI_API_KEY") or os.getenv("GEMINI_API_KEY")

if not api_key:
    api_key = st.sidebar.text_input("Εισάγετε Google API Key (Backup)", type="password")

if api_key:
    try:
        genai.configure(api_key=api_key)
        
        # --- ΘΩΡΑΚΙΣΜΕΝΗ ΕΠΙΛΟΓΗ ΜΟΝΤΕΛΟΥ ---
        available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        
        # Επιλογή μοντέλου με προτεραιότητα στη σειρά 1.5 που υποστηρίζει καλύτερα system_instructions
        if 'models/gemini-1.5-flash' in available_models:
            model_id = 'models/gemini-1.5-flash'
        elif 'models/gemini-1.5-pro' in available_models:
            model_id = 'models/gemini-1.5-pro'
        elif 'models/gemini-pro' in available_models:
            model_id = 'models/gemini-pro'
        else:
            model_id = available_models[0]

        # Δημιουργία του μοντέλου με τις οδηγίες συστήματος
        # Αν το μοντέλο είναι παλιό (gemini-pro), ενσωματώνουμε το prompt στο ερώτημα
        if '1.5' in model_id:
            model = genai.GenerativeModel(
                model_name=model_id,
                system_instruction=SYSTEM_PROMPT
            )
        else:
            model = genai.GenerativeModel(model_name=model_id)
            # Για το παλιό μοντέλο, θα προσθέσουμε το SYSTEM_PROMPT στην αρχή του user_idea αργότερα

        st.sidebar.success(f"AI Engine Active: {model_id.split('/')[-1]}")

        # 4. Πεδία Εισαγωγής
        user_idea = st.text_area("🚀 Δώσε την ιδέα σου για το επόμενο Viral Video:", 
                                 placeholder="Π.χ. Ψάρεμα LRF με Major Craft Eden...",
                                 height=150)

        if st.button("Δημιούργησε Σενάριο!"):
            if user_idea:
                with st.spinner("🎬 Ο σκηνοθέτης Kontopas επεξεργάζεται τα πλάνα..."):
                    try:
                        # Αν χρησιμοποιούμε το παλιό μοντέλο, συγχωνεύουμε τις οδηγίες
                        final_prompt = user_idea if '1.5' in model_id else f"{SYSTEM_PROMPT}\n\nΙΔΕΑ ΧΡΗΣΤΗ: {user_idea}"
                        
                        response = model.generate_content(final_prompt)
                        
                        if response.text:
                            st.markdown("---")
                            st.subheader("📝 Το Viral Σενάριό σου")
                            st.markdown(response.text)
                        else:
                            st.error("Η AI δεν μπόρεσε να δημιουργήσει περιεχόμενο. Δοκίμασε άλλη ιδέα.")
                            
                    except Exception as e:
                        st.error(f"Σφάλμα κατά την παραγωγή: {e}")
            else:
                st.warning("Παρακαλώ γράψτε μια ιδέα!")

    except Exception as e:
        st.error(f"Σφάλμα AI: {e}")
else:
    st.info("💡 Παρακαλώ εισάγετε το Google API Key σας για να ξεκινήσετε.")
