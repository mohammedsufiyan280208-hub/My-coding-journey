
import random
import streamlit as st

# ---------- PAGE CONFIGURATION ----------
st.set_page_config(
    page_title="Rock Paper Scissors",
    page_icon="🎮",
    layout="centered"
)

# ---------- GAME DATA ----------
choices = ["rock", "paper", "scissors"]

emoji = {
    "rock": "🪨",
    "paper": "📄",
    "scissors": "✂️"
}

# ---------- SESSION STATE ----------
if "player_score" not in st.session_state:
    st.session_state.player_score = 0
    st.session_state.computer_score = 0
    st.session_state.round_number = 1
    st.session_state.history = []
    st.session_state.winner = None


# ---------- GAME LOGIC ----------
def play_round(player):
    if st.session_state.winner is not None:
        return

    computer = random.choice(choices)

    if player == computer:
        result = "Draw!"
        outcome = "draw"

    elif (
        (player == "rock" and computer == "scissors")
        or (player == "paper" and computer == "rock")
        or (player == "scissors" and computer == "paper")
    ):
        result = "You win this round!"
        outcome = "win"
        st.session_state.player_score += 1

    else:
        result = "Computer wins this round!"
        outcome = "loss"
        st.session_state.computer_score += 1

    st.session_state.history.append({
        "round": st.session_state.round_number,
        "player": player,
        "computer": computer,
        "result": result,
        "outcome": outcome
    })

    st.session_state.round_number += 1

    if st.session_state.player_score == 3:
        st.session_state.winner = "player"
    elif st.session_state.computer_score == 3:
        st.session_state.winner = "computer"


def reset_game():
    st.session_state.player_score = 0
    st.session_state.computer_score = 0
    st.session_state.round_number = 1
    st.session_state.history = []
    st.session_state.winner = None


# ---------- CUSTOM UI ----------
st.markdown("""
<style>
.stApp {
    background: #f5f7fb;
}
.block-container {
    max-width: 700px;
    padding-top: 2rem;
}
h1, h2, h3, p {
    color: #182230;
}
div.stButton > button {
    width: 100%;
    min-height: 55px;
    border-radius: 12px;
    border: 1px solid #d9e0eb;
    background: white;
    color: #182230;
    font-weight: 600;
}
div.stButton > button:hover {
    border-color: #5267e8;
    color: #5267e8;
}
</style>
""", unsafe_allow_html=True)


# ---------- HEADER ----------
st.title("🎮 Rock Paper Scissors")
st.caption("BEST OF 5  •  First to 3 wins")

st.divider()

# ---------- SCOREBOARD ----------
col1, col2 = st.columns(2)

with col1:
    st.metric(
        label="👤 YOUR SCORE",
        value=st.session_state.player_score
    )

with col2:
    st.metric(
        label="🤖 COMPUTER SCORE",
        value=st.session_state.computer_score
    )

st.progress(
    max(
        st.session_state.player_score,
        st.session_state.computer_score
    ) / 3
)

st.divider()

# ---------- CHOICE BUTTONS ----------
st.subheader("Make your move")

st.write("Choose one of the three options below.")

col1, col2, col3 = st.columns(3)

with col1:
    st.button(
        "🪨 Rock",
        key="rock",
        on_click=play_round,
        args=("rock",),
        disabled=st.session_state.winner is not None
    )

with col2:
    st.button(
        "📄 Paper",
        key="paper",
        on_click=play_round,
        args=("paper",),
        disabled=st.session_state.winner is not None
    )

with col3:
    st.button(
        "✂️ Scissors",
        key="scissors",
        on_click=play_round,
        args=("scissors",),
        disabled=st.session_state.winner is not None
    )

# ---------- LATEST ROUND ----------
if st.session_state.history:
    last = st.session_state.history[-1]

    st.divider()
    st.subheader(f"Round {last['round']} result")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("**👤 Your move**")
        st.title(
            f"{emoji[last['player']]} "
            f"{last['player'].title()}"
        )

    with col2:
        st.markdown("**🤖 Computer's move**")
        st.title(
            f"{emoji[last['computer']]} "
            f"{last['computer'].title()}"
        )

    if last["outcome"] == "win":
        st.success("🏆 You won this round!")
    elif last["outcome"] == "loss":
        st.error("💻 Computer won this round!")
    else:
        st.info("🤝 It's a draw!")

# ---------- MATCH RESULT ----------
if st.session_state.winner is not None:
    st.divider()

    if st.session_state.winner == "player":
        st.balloons()
        st.success("🏆 YOU WON THE MATCH!")
    else:
        st.error("💻 COMPUTER WON THE MATCH!")

    st.write(
        f"Final score: **{st.session_state.player_score}**"
        f" – **{st.session_state.computer_score}**"
    )

    st.button(
        "🔄 Play Again",
        on_click=reset_game,
        type="primary"
    )

# ---------- MATCH HISTORY ----------
if st.session_state.history:
    st.divider()
    st.subheader("📋 Match History")

    for item in reversed(st.session_state.history):
        st.write(
            f"**Round {item['round']}** · "
            f"{emoji[item['player']]} {item['player'].title()} "
            f"vs "
            f"{emoji[item['computer']]} "
            f"{item['computer'].title()} "
            f"— {item['result']}"
        )

# ---------- FOOTER ----------
st.divider()
st.caption("Built with Python and Streamlit")
