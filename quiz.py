import streamlit as st
import random
import pandas as pd
import os





# Store MCQs
mcq_data = [
    {"question": "What was the first-ever online display ad?", 
     "options": ["A dancing baby GIF", "An AT&T banner ad on HotWired", "A flashing pop-up from Yahoo!", "A “Click Here to Win a Free iPod” ad"], 
     "answer": "An AT&T banner ad on HotWired"},

    {"question": "Which of these is NOT a major component of the AdTech ecosystem?", 
     "options": ["Demand-Side Platforms (DSPs)", "Supply-Side Platforms (SSPs)", "Walled Gardens", "The Dark Web"], 
     "answer": "The Dark Web"},

    {"question": "What does ‘CPM’ stand for in advertising?", 
     "options": ["Clicks Per Month", "Cost Per Mille", "Cost Per Marketer", "Conversion Profit Margin"], 
     "answer": "Cost Per Mille"},

    {"question": "Which company acquired DoubleClick in 2007, making it a dominant force in digital advertising?", 
     "options": ["Facebook", "Microsoft", "Google", "Amazon"], 
     "answer": "Google"},

    {"question": "What is ‘Real-Time Bidding’ (RTB)?", 
     "options": ["A live auction where advertisers yell out bids for ad space", "A process where ads are bought and sold in milliseconds via automated bidding", "A stock market for memes", "A tool for tracking ad clicks in real-time"], 
     "answer": "A process where ads are bought and sold in milliseconds via automated bidding"},

    {"question": "What is the primary role of a Supply-Side Platform (SSP)?", 
     "options": ["Helping publishers sell their ad inventory", "Managing influencer sponsorships", "Preventing ad fraud", "Optimizing search engine rankings"], 
     "answer": "Helping publishers sell their ad inventory"},

    {"question": "Which of these is a common type of ad fraud?", 
     "options": ["Cookie Stuffing", "Click Farming", "Impression Laundering", "All of the above"], 
     "answer": "All of the above"},

    {"question": "What is a “walled garden” in AdTech?", 
     "options": ["A garden where only VIP marketers can enter", "A platform that controls access to its data and users (e.g., Google, Facebook)", "A secret society of advertisers", "A hidden section of the internet where ads are auctioned"], 
     "answer": "A platform that controls access to its data and users (e.g., Google, Facebook)"},

    {"question": "What does ‘DMP’ stand for?", 
     "options": ["Digital Marketing Platform", "Data Management Platform", "Demand Market Predictor", "Dynamic Media Program"], 
     "answer": "Data Management Platform"},

    {"question": "What major change is disrupting online tracking in 2024-2025?", 
     "options": ["Google banning third-party cookies", "TikTok launching its own ad network", "AI taking over marketing jobs", "Twitter becoming the new Facebook"], 
     "answer": "Google banning third-party cookies"},
]

LEADERBOARD_FILE = "leaderboard.csv"

def init_leaderboard():
    if not os.path.exists(LEADERBOARD_FILE):
        df = pd.DataFrame(columns=["Name", "Score"])
        df.to_csv(LEADERBOARD_FILE, index=False)

init_leaderboard() 


# Function to remove 2 wrong options (50-50 Lifeline)
def fifty_fifty(options, correct_answer):
    wrong_options = [opt for opt in options if opt != correct_answer]
    removed = random.sample(wrong_options, 2)  # Remove 2 incorrect answers
    return [opt for opt in options if opt not in removed]

# Initialize session state variables
if "user_name" not in st.session_state:
    st.session_state.user_name = ""
if "quiz_started" not in st.session_state:
    st.session_state.quiz_started = False
if "current_question" not in st.session_state:
    st.session_state.current_question = 0
if "score" not in st.session_state:
    st.session_state.score = 0
if "quiz_over" not in st.session_state:
    st.session_state.quiz_over = False
if "fifty_fifty_used" not in st.session_state:
    st.session_state.fifty_fifty_used = False  # Track if lifeline was used once
if "reduced_options" not in st.session_state:
    st.session_state.reduced_options = {}  # Store reduced options per question
if "show_popup" not in st.session_state:
    st.session_state.show_popup = False  # Track if confirmation popup is needed

# Function to start the quiz
def start_quiz():
    st.session_state.quiz_started = True
    st.session_state.current_question = 0
    st.session_state.score = 0
    st.session_state.quiz_over = False
    st.session_state.fifty_fifty_used = False  # Reset lifeline usage for new quiz
    st.session_state.reduced_options = {}  # Reset stored options

def save_score(name, score):
    df = pd.read_csv(LEADERBOARD_FILE)
    new_entry = pd.DataFrame({"Name": [name], "Score": [score]})
    df = pd.concat([df, new_entry], ignore_index=True)
    df.to_csv(LEADERBOARD_FILE, index=False)


# Function to move to the next question
def next_question(user_choice):
    correct_answer = mcq_data[st.session_state.current_question]["answer"]
    
    if user_choice == correct_answer:
        st.session_state.score += 1  # Increase score if correct

    st.session_state.current_question += 1  # Move to the next question

    if st.session_state.current_question >= len(mcq_data):
        st.session_state.quiz_over = True  # End quiz if no more questions
    if st.session_state.current_question >= len(mcq_data):
        st.session_state.quiz_over = True  # End quiz
        save_score(st.session_state.user_name, st.session_state.score)  # Save result


# **Step 1: User enters name**
if not st.session_state.user_name:
    st.title("Welcome to the ADTECH Quiz! ")
    st.session_state.user_name = st.text_input("Enter your name:")
    if st.button("Enter"):
        start_quiz()
    st.stop()

# **Step 2: Welcome screen before quiz starts**
if not st.session_state.quiz_started:
    st.title(f"Welcome, {st.session_state.user_name}! 🎉")
    st.write("🎯 **Quiz Instructions:**")  
    st.markdown("""
        ✅ **Answer multiple-choice questions on AdTech.**  
        ✅ **Click 'Save & Next' to move to the next question.**  
        ✅ **You can use the '🔀 50-50 Lifeline' ONCE to remove 2 wrong options.**  
        ✅ **Your final score will be shown at the end!**  
        ✅ **Have fun and test your knowledge! 🚀**  
    """)
    if st.button("Enter"):
        start_quiz()
    st.stop()

# **Step 3: Show quiz questions**
if st.session_state.quiz_started and not st.session_state.quiz_over:
    st.title(f"🎯 Question {st.session_state.current_question + 1} of {len(mcq_data)}")
    question_data = mcq_data[st.session_state.current_question]
    st.write(f"📝 {question_data['question']}")

    # **Handle 50-50 Lifeline Logic**  
    question_index = st.session_state.current_question
    
    if st.session_state.fifty_fifty_used:
        options = st.session_state.reduced_options.get(question_index, question_data["options"])
    else:
        options = question_data["options"]

    user_choice = st.radio("Select your answer:", options, index=None)

    # **50-50 Lifeline Button (Only usable once per quiz)**
    if not st.session_state.fifty_fifty_used and st.button("🔀 Use 50-50 Lifeline"):
        st.session_state.show_popup = True  # Trigger confirmation popup

    # **Confirmation Popup for Lifeline**
    if st.session_state.show_popup:
        st.warning("⚠️ You can use this lifeline only once! Are you sure?")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("✅ Yes, Use Lifeline"):
                st.session_state.reduced_options[question_index] = fifty_fifty(question_data["options"], question_data["answer"])
                st.session_state.fifty_fifty_used = True  # Mark as used
                st.session_state.show_popup = False  # Close popup
                st.rerun()
        with col2:
            if st.button("❌ No, Cancel"):
                st.session_state.show_popup = False  # Close popup
                st.rerun()

    # **Submit Answer and Move to Next**
    if st.button("✅ Save & Next"):
        if user_choice:
            next_question(user_choice)
            st.rerun()
        else:
            st.warning("Please select an answer before moving to the next question.")

if st.session_state.quiz_over:
    st.title("🎉 Quiz Completed!")
    
    # Custom messages based on score
    if st.session_state.score == 10:
        st.success(f"🏆 Perfect Score, {st.session_state.user_name}! 🎯 You got **10/10**! Amazing work!")
        st.balloons()
    elif st.session_state.score >= 7:
        st.success(f"👏 Well done, {st.session_state.user_name}! You scored **{st.session_state.score}/10**! Great job! 🚀")
        st.balloons()
    elif st.session_state.score >= 4:
        st.warning(f"😊 Nice effort, {st.session_state.user_name}! You scored **{st.session_state.score}/10**. Keep practicing!")
    else:
        st.error(f"😬 Better luck next time, {st.session_state.user_name}! You scored **{st.session_state.score}/10**. Try again!")

    df = pd.read_csv(LEADERBOARD_FILE).sort_values(by="Score", ascending=False).reset_index(drop=True)
    st.subheader("🏅 **Leaderboard - Top 5 Players** 🏅")
    st.dataframe(df.head(5))  # Show top 5 scores


    # Restart button
    st.button("🔄 Restart Quiz", on_click=start_quiz)
