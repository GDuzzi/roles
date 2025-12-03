import streamlit as st
import pandas as pd
import os
import pickle

# -------------------------------------
# FUNÇÕES DE SALVAMENTO
# -------------------------------------
SAVE_FILE = "roles.pkl"

def save_roles(data):
    with open(SAVE_FILE, "wb") as f:
        pickle.dump(data, f)

def load_roles():
    if os.path.exists(SAVE_FILE):
        with open(SAVE_FILE, "rb") as f:
            return pickle.load(f)
    return []


# -------------------------------------
# PAGE CONFIG
# -------------------------------------
st.set_page_config(
    page_title="Notas dos Rolês",
    page_icon="💖",
    layout="centered"
)

# -------------------------------------
# CSS DEFINITIVO
# -------------------------------------
st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;800&display=swap');

:root {
    --rose: #e9b8c7;
    --rose-light: #f4dce4;
    --champagne: #f9f5f2;
    --text-dark: #3b2f36;
    --accent: #d26a98;
    --white-glass: rgba(255,255,255,0.45);
}

* { font-family: "Poppins", sans-serif !important; }

div[data-testid="stVerticalBlock"],
div[data-testid="stVerticalBlock"] > div,
div[data-testid="stForm"],
div[data-testid="stAppViewContainer"] > div,
section.main > div,
div.block-container,
div[data-testid="stAppViewBlockContainer"] {
    background: transparent !important;
    border: none !important;
    box-shadow: none !important;
    padding: 0 !important;
    margin: 0 !important;
}

section.main { padding-top: 0 !important; }

html, body, div[data-testid="stAppViewContainer"] {
    background: radial-gradient(circle at top left, #fbe3ef, #f5d6e8, #eed0e0);
}

.header {
    text-align: center;
    margin-top: 40px;
    margin-bottom: 0;
}
.header h1 {
    font-size: 50px;
    font-weight: 800;
    color: var(--text-dark);
    text-shadow: 0 4px 14px rgba(0,0,0,0.12);
}
.header-icon {
    font-size: 40px;
    animation: heartbeat 1.8s infinite ease-in-out;
}
@keyframes heartbeat {
    0% { transform: scale(1); }
    15% { transform: scale(1.18); }
    30% { transform: scale(1); }
    45% { transform: scale(1.18); }
    60% { transform: scale(1); }
}

.spacing { height: 35px; }

.form-card {
    background: var(--white-glass);
    padding: 35px 40px;
    border-radius: 22px;
    backdrop-filter: blur(14px);
    border: 1px solid rgba(255,255,255,0.55);
    box-shadow: 0 10px 35px rgba(0,0,0,0.12);
    max-width: 850px;
    margin: 0 auto;
}

input, textarea {
    border-radius: 12px !important;
    border: 1px solid rgba(210,106,152,0.35) !important;
    background: #fff7fa !important;
}

input:focus, textarea:focus {
    border-color: var(--accent) !important;
    box-shadow: 0 0 8px rgba(210,106,152,0.35);
}

.stSlider > div > div > div {
    background: var(--accent) !important;
}

.stButton > button {
    background: linear-gradient(135deg, var(--rose), var(--accent));
    padding: 14px 32px;
    width: 60%;
    display: block;
    margin: 0 auto;
    color: white !important;
    border-radius: 14px;
    border: none;
    font-weight: 600;
    box-shadow: 0 6px 22px rgba(210,106,152,0.40);
    transition: 0.25s;
}
.stButton > button:hover { transform: scale(1.05); }

.divider {
    margin: 40px auto 20px auto;
    width: 60%;
    height: 3px;
    background: linear-gradient(90deg, transparent, var(--accent), transparent);
}

.section-title {
    font-size: 26px;
    font-weight: 700;
    text-align: center;
    color: var(--text-dark);
    margin-bottom: 15px;
}

</style>
""", unsafe_allow_html=True)


# -------------------------------------
# ESTADO
# -------------------------------------
if "roles" not in st.session_state:
    st.session_state.roles = load_roles()

if "open_cards" not in st.session_state:
    st.session_state.open_cards = {i: False for i in range(len(st.session_state.roles))}


# -------------------------------------
# HEADER
# -------------------------------------
st.markdown("""
<div class="header">
    <div class="header-icon">💞</div>
    <h1>Notas dos Rolês</h1>
</div>
""", unsafe_allow_html=True)

st.markdown("<div class='spacing'></div>", unsafe_allow_html=True)


# -------------------------------------
# FORMULÁRIO
# -------------------------------------
st.markdown("<div class='section-title'>Adicionar novo rolê ❤️</div>", unsafe_allow_html=True)

col1, col2 = st.columns(2)
with col1:
    role = st.text_input("Nome do rolê")
with col2:
    date = st.date_input("Data", format="DD/MM/YYYY")

col3, col4 = st.columns(2)
with col3:
    nota_voce = st.slider("Jovem", 0, 10, 7)
with col4:
    nota_namorada = st.slider("Senhorita", 0, 10, 7)

comentario = st.text_area("Comentário sobre o rolê")

add = st.button("Adicionar")


# -------------------------------------
# SALVAR
# -------------------------------------
if add and role.strip() != "":
    novo = {
        "Rolê": role,
        "Data": date.strftime("%d/%m/%Y"),
        "Sua nota": nota_voce,
        "Nota dela": nota_namorada,
        "Comentário": comentario
    }

    st.session_state.roles.append(novo)
    save_roles(st.session_state.roles)

    st.session_state.open_cards[len(st.session_state.roles) - 1] = False

    st.success("Adicionado com muito amor! 💘")


# -------------------------------------
# HISTÓRICO
# -------------------------------------
st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
st.markdown("<div class='section-title'> Histórico de Rolês</div>", unsafe_allow_html=True)

if len(st.session_state.roles) == 0:
    st.info("Nenhum rolê adicionado ainda! 💗")

else:
    df = pd.DataFrame(st.session_state.roles)
    st.markdown("<div class='spacing'></div>", unsafe_allow_html=True)

    for index, row in df.iterrows():

        media = (row["Sua nota"] + row["Nota dela"]) / 2

        if media >= 7:
            bg = "rgba(180, 255, 200, 0.55)"
            border = "rgba(0, 180, 70, 0.55)"
        else:
            bg = "rgba(255, 170, 170, 0.55)"
            border = "rgba(255, 80, 80, 0.55)"

        btn = st.button(row["Rolê"], key=f"btn_{index}")

        if btn:
            st.session_state.open_cards[index] = not st.session_state.open_cards.get(index, False)

        if st.session_state.open_cards.get(index, False):
            st.markdown(f"""
            <div style="
                background:{bg};
                padding:20px;
                border-radius:15px;
                border:2px solid {border};
                backdrop-filter: blur(10px);
                box-shadow: 0 6px 20px rgba(0,0,0,0.12);
                margin-bottom:15px;
                margin-top:10px;
                color:#3b2f36;
            ">
                <p><strong>📅 Data:</strong> {row['Data']}</p>
                <p><strong>⭐ Nota jovem:</strong> {row['Sua nota']}</p>
                <p><strong>❤️ Nota senhorita:</strong> {row['Nota dela']}</p>
                <p><strong>💬 Comentário:</strong> {row['Comentário'] if row['Comentário'] else "—"}</p>
            </div>
            """, unsafe_allow_html=True)
