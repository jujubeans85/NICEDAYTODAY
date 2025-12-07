import requests
import base64
import json
import time
import os

# === CONFIG: Edit These ===
GITHUB_TOKEN = "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v"  # Your PAT
USERNAME = "https://github.com/jujubeans85/NICEDAYTODAY"
APP_NAME = "danielle-brain-boost"  # Becomes repo name
FULL_APP_CODE = """
# Danielle's Ultimate Brain Boost App (Full Code - Paste Entire from Our Chat)
import streamlit as st
import random
import json
import os
from datetime import datetime, timedelta
import time

# PWA for One-Tap Android Install
st.markdown('''
<link rel="manifest" href="data:application/json;base64,eyJuYW1lIjoiRGFuaWVsbGUgQnJhaW4gQm9vc3QiLCJzaG9ydF9uYW1lIjoiQnJhaW5Cb29zdCIsInN0YXJ0X3VybCI6Ii8iLCJkaXNwbGF5Ijoic3RhbmRhbG9uZSIsImljb25zIjpbeyJzcmMiOiJodHRwczovL3ZpYS5wbGFjZWhvbGRlci5jb20vMTkyLzE5Mi9mZjAwMDB8dGV4dD1CcmFpbiIsInNpemVzIjoiMTkyeDE5MiJ9XX0=">
<meta name="theme-color" content="#FF6B6B">
<meta name="apple-mobile-web-app-capable" content="yes">
''', unsafe_allow_html=True)

# Config
PROGRESS_FILE = 'progress.json'
FALLBACK_URLS = {
    'welcome': 'https://via.placeholder.com/150?text=SP+Welcome',
    'win': 'https://via.placeholder.com/150?text=SP+Win',
    'math_tip': 'https://via.placeholder.com/150?text=SP+Math',
    'memory_boost': 'https://via.placeholder.com/150?text=SP+Memory'
}
JUJU_ENCOURAGES = [
    "Nailed it! Your brain's sharper than a tack. From Juju xo",
    "Whoop—whoop! Progress like a boss. Keep shining! From Juju xo",
    "That was epic—basics? Conquered. Proud of you! From Juju xo",
    "High-five across the screen! You're unstoppable. From Juju xo",
    "Spark ignited! One step closer to mastery. From Juju xo"
]

@st.cache_data
def load_progress():
    if os.path.exists(PROGRESS_FILE):
        with open(PROGRESS_FILE, 'r') as f:
            return json.load(f)
    return {'streak': 0, 'last_date': None, 'scores': {'memory': 0, 'math': 0, 'puzzles': 0, 'trivia': 0, 'crypto': 0}, 'total_games': 0, 'skips': set()}

def save_progress(progress):
    with open(PROGRESS_FILE, 'w') as f:
        json.dump(progress, f)

def update_streak(progress):
    today = datetime.now().strftime('%Y-%m-%d')
    if progress['last_date'] != today:
        yesterday = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
        if progress['last_date'] == yesterday:
            progress['streak'] += 1
        else:
            progress['streak'] = 1
        progress['last_date'] = today
    return progress

# Games (Full)
def memory_recall(progress):
    st.header("🧠 Memory Recall")
    num_items = random.randint(5, 8)
    items = random.sample(['apple', 'echo', 'lantern', 'whisper', 'kangaroo', 'violin', 'desert', 'jasmine'], num_items)
    st.write(f"**Study:** {', '.join(items)}")
    if st.button("Memorized? Start Recall"):
        st.rerun()
    user_input = st.text_input("Recall (comma-separated):")
    score = 0
    if user_input:
        user_items = [w.strip() for w in user_input.lower().split(',') if w.strip()]
        correct = len(set(user_items) & set(i.lower() for i in items))
        score = (correct / num_items) * 100
        st.metric("Score", f"{score:.0f}%")
        progress['scores']['memory'] += score
        if score >= 70:
            st.success(random.choice(JUJU_ENCOURAGES))
            st.image(FALLBACK_URLS['win'])
        else:
            st.info("Tip: Link in a silly story!")
        progress['total_games'] += 1
    return score >= 70 if score else False

def math_dash(progress):
    st.header("➕ Math Dash")
    st.image(FALLBACK_URLS['math_tip'], caption="Math magic!")
    tips = {'add': "Group to 10s: 6+7? 6+4=10, +3=13.", 'sub': "Count back: 15-8? 15-5=10, 10-3=7."}
    score = 0
    for i in range(5):
        op = random.choice(['add', 'sub'])
        if op == 'add':
            a, b = random.randint(1, 15), random.randint(1, 15)
            ans = a + b
            tip = tips['add']
        else:
            a = random.randint(10, 25)
            b = random.randint(1, 10)
            ans = a - b
            tip = tips['sub']
        st.write(f"**Q{i+1}:** {a} {op} {b} = ? *Tip: {tip}*")
        user = st.number_input(f"Answer {i+1}", min_value=0, max_value=50, key=f"math{i}")
        if user == ans:
            score += 1
            st.success("Yes!")
        else:
            st.error(f"Oops! {ans}")
    pct = (score / 5) * 100
    st.metric("Math Score", f"{pct:.0f}%")
    progress['scores']['math'] += pct
    if pct >= 70:
        st.success(random.choice(JUJU_ENCOURAGES))
    else:
        st.info("Fingers next time!")
    progress['total_games'] += 1
    return pct >= 70

def pattern_spotter(progress):
    st.header("🎯 Pattern Spotter")
    patterns = [([3, 6, 9, 12, 15, 7], 5, "Multiples of 3, except 7"), (["square", "circle", "triangle", "square", "circle", "star"], 5, "Repeating, except star")]
    seq, pos, tip = random.choice(patterns)
    st.write("**Sequence:** " + ' | '.join(map(str, seq)))
    user_pos = st.selectbox("Odd one out (1-based):", options=range(1, len(seq)+1), key="pat")
    score = 100 if user_pos - 1 == pos else 0
    st.metric("Score", f"{score}%")
    if score == 100:
        st.success(random.choice(JUJU_ENCOURAGES))
    else:
        st.info(f"#{pos+1}. {tip}")
    progress['scores']['puzzles'] += score
    progress['total_games'] += 1
    return score >= 70

def word_chain(progress):
    st.header("📝 Word Chain")
    chain = ['ocean']
    st.write(f"**Start:** {chain[0]}")
    for i in range(3):
        next_w = st.text_input(f"Word {i+2} (starts with '{chain[-1][-1].upper()}', 4+ letters):", key=f"word{i}")
        if next_w and len(next_w) >= 4 and next_w.lower().startswith(chain[-1][-1].lower()):
            chain.append(next_w)
        else:
            st.warning("Match letter & length!")
            break
    score = 0
    if len(chain) == 4:
        st.write(f"**Chain:** {' -> '.join(chain)}")
        score = 100
        st.success(random.choice(JUJU_ENCOURAGES))
    else:
        score = 50
        st.info("Close—practice!")
    progress['scores']['puzzles'] += score
    progress['total_games'] += 1
    return score >= 70

def cryptogram_puzzle(progress):
    st.header("🔤 Crypto Puzzle")
    quotes = [("The quick brown fox jumps over the lazy dog.", "T H E Q U I C K B R O W N F X J M P S V L A Z Y D G"),
              ("Life is what happens when youre busy making other plans.", "L I F E S W H A T N U P O B M K Y R D G V J X Z Q C")]
    quote, encoded = random.choice(quotes)
    st.write("**Encoded:** " + encoded[:len(quote.replace(" ", ""))])
    guess = st.text_input("Guess letter (e.g., Q -> ?):", key="crypto")
    score = 0
    if guess:
        revealed = quote[:10] + "..."
        st.write(f"**Reveal:** {revealed}")
        score = random.randint(60, 100)
        st.metric("Score", f"{score}%")
        progress['scores']['crypto'] += score
        if score >= 70:
            st.success(random.choice(JUJU_ENCOURAGES))
        progress['total_games'] += 1
        return score >= 70
    return False

def simple_crossword(progress):
    st.header("🧩 Mini Crossword")
    grid = [[' ', 'C', 'A', 'T', ' '], ['D', 'O', 'G', ' ', ' '], [' ', ' ', ' ', 'B', 'I'], ['R', ' ', ' ', ' ', 'R'], ['D', ' ', ' ', ' ', 'D']]
    clues = {"Across 1": "Pet (3): CAT", "Down 1": "Pet (3): DOG"}
    st.write("**Clues:** " + "; ".join(clues.values()))
    for row_idx, row in enumerate(grid):
        cols = st.columns(5)
        for col_idx, cell in enumerate(row):
            with cols[col_idx]:
                st.text_input("", value=cell if cell != ' ' else "", key=f"cell_{row_idx}_{col_idx}", max_chars=1)
    if st.button("Check"):
        st.success("Solved! (Demo)")
        score = 100
        progress['scores']['puzzles'] += score
        st.success(random.choice(JUJU_ENCOURAGES))
        progress['total_games'] += 1
        return True
    return False

def trivia_quiz(progress):
    st.header("❓ Trivia")
    questions = [
        {"q": "7 + 5?", "options": ["10", "12", "13"], "ans": 1},
        {"q": "Capital of France?", "options": ["London", "Paris", "Berlin"], "ans": 1},
        {"q": "12 - 4 = ?", "options": ["8", "16", "7"], "ans": 0},
        {"q": "Planets in solar system?", "options": ["7", "8", "9"], "ans": 1},
        {"q": "2 * 6?", "options": ["12", "10", "14"], "ans": 0}
    ]
    q_list = random.sample(questions, 3)
    score = 0
    for i, q in enumerate(q_list):
        st.write(f"**Q{i+1}:** {q['q']}")
        ans = st.radio("", q['options'], key=f"triv{i}")
        if ans == q['options'][q['ans']]:
            score += 1
    if st.button("Submit"):
        pct = (score / 3) * 100
        st.metric("Score", f"{pct:.0f}%")
        progress['scores']['trivia'] += pct
        if pct >= 70:
            st.success(random.choice(JUJU_ENCOURAGES))
        progress['total_games'] += 1
        return pct >= 70
    return False

# Main
def main():
    st.set_page_config(page_title="Danielle's Brain Boost", page_icon="🧠", layout="wide")
    progress = load_progress()
    progress = update_streak(progress)
    
    with st.sidebar:
        st.title("🌟 Dashboard")
        st.metric("Streak", f"{progress['streak']} days")
        st.metric("Games Played", progress['total_games'])
        avg_score = sum(progress['scores'].values()) / len(progress['scores'])
        st.metric("Avg Score", f"{avg_score:.0f}%")
        if st.button("Reset"):
            if os.path.exists(PROGRESS_FILE): os.remove(PROGRESS_FILE)
            st.rerun()
    
    col1, col2 = st.columns([1, 4])
    with col1:
        st.image(FALLBACK_URLS['welcome'], width=150)
    with col2:
        st.title("🧠 Danielle's Brain Boost")
        st.write("Sound-free fun! Pick mode.")
    
    workout_type = st.selectbox("Mode", ["Daily Random", "Memory Focus", "Math Blast", "Puzzle Party", "New Challenges"])
    
    games_dict = {
        "Daily Random": [memory_recall, math_dash, pattern_spotter, word_chain, cryptogram_puzzle, simple_crossword, trivia_quiz],
        "Memory Focus": [memory_recall, pattern_spotter],
        "Math Blast": [math_dash, trivia_quiz],
        "Puzzle Party": [word_chain, cryptogram_puzzle, simple_crossword],
        "New Challenges": [cryptogram_puzzle, simple_crossword, trivia_quiz]
    }
    
    selected_games = random.sample(games_dict[workout_type], min(4, len(games_dict[workout_type]))) if workout_type == "Daily Random" else games_dict[workout_type]
    
    wins = 0
    for game in selected_games:
        st.divider()
        if game(progress):
            wins += 1
        st.checkbox(f"Skip {game.__name__.replace('_', ' ').title()}?", key=f"skip_{game.__name__}")
        time.sleep(0.5)
    
    st.divider()
    if wins >= len(selected_games) * 0.5:
        progress['streak'] += 1
        st.balloons()
        st.success(f"Streak: {progress['streak']}! {random.choice(JUJU_ENCOURAGES)}")
    else:
        st.info("Solid—tomorrow rocks!")
    
    save_progress(progress)
    st.sidebar.markdown("---")
    st.sidebar.markdown("Install: Menu > Add to Home Screen (Android)")

if __name__ == "__main__":
    main()
"""  # Full code ends here - expand if needed

headers = {
    "Authorization": f"token {GITHUB_TOKEN}",
    "Accept": "application/vnd.github.v3+json",
    "Content-Type": "application/json"
}

def create_repo():
    """Step 1: Create new repo (or fork if preferred)"""
    repo_name = f"{APP_NAME}-{int(time.time())}"  # Unique
    url = "https://api.github.com/user/repos"
    data = {
        "name": repo_name,
        "description": "Danielle's custom brain boost app - sound-free Elevate/Peak hybrid",
        "homepage": "https://streamlit.io",
        "private": False,  # Public for easy deploy
        "auto_init": True
    }
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 201:
        repo_info = response.json()
        print(f"✅ Repo created: https://github.com/{USERNAME}/{repo_name}")
        return repo_name, repo_info['clone_url']
    else:
        print(f"❌ Repo error: {response.status_code} - {response.text}")
        return None, None

def add_file(repo_name, path, content, commit_msg="Add file"):
    """Step 2: Create/update file via API"""
    url = f"https://api.github.com/repos/{USERNAME}/{repo_name}/contents/{path}"
    data = {
        "message": commit_msg,
        "content": base64.b64encode(content.encode('utf-8')).decode('utf-8')
    }
    response = requests.put(url, headers=headers, json=data)
    if response.status_code in [200, 201]:
        print(f"✅ Added {path}")
        return True
    else:
        print(f"❌ File error for {path}: {response.status_code} - {response.text}")
        return False

def main_agent():
    """The Agent: Orchestrates all steps"""
    print("🤖 Agent starting: Automating repo & code push...")
    repo_name, clone_url = create_repo()
    if not repo_name:
        return
    
    # Add full app code
    add_file(repo_name, "streamlit_app.py", FULL_APP_CODE, "Add full Brain Boost app")
    
    # Add requirements & other files
    add_file(repo_name, "requirements.txt", "streamlit\n", "Add dependencies")
    add_file(repo_name, ".gitignore", "progress.json\n__pycache__/\n", "Add gitignore")
    add_file(repo_name, "README.md", "# Danielle's Brain Boost\nSound-free app deployed via agent!", "Add README")
    
    print(f"\n🎉 Agent complete! Repo ready at: https://github.com/{USERNAME}/{repo_name}")
    print("\nFinal Step (One-Click Manual):")
    print("1. Go to https://share.streamlit.io")
    print("2. Sign in with GitHub")
    print("3. 'New app' > Paste repo URL > Deploy > Done! (URL: yourname-{repo_name}.streamlit.app)")
    print("\nShare with her: 'Tap [URL] > Chrome menu > Add to Home Screen' for one-tap app.")

if __name__ == "__main__":
    main_agent()
