import streamlit as st
import pandas as pd
import os
from fpdf import FPDF
from datetime import datetime

# File paths
USER_FILE = "users.csv"
DATA_FILE = "users_edupath.csv"

# -------------------- USER MANAGEMENT --------------------
def load_users():
    if os.path.exists(USER_FILE):
        return pd.read_csv(USER_FILE)
    df = pd.DataFrame(columns=["username", "password"])
    df.to_csv(USER_FILE, index=False)
    return df

def save_user(username, password):
    df = load_users()
    if username in df["username"].values:
        return False
    new_user = pd.DataFrame([[username, password]], columns=["username", "password"])
    df = pd.concat([df, new_user], ignore_index=True)
    df.to_csv(USER_FILE, index=False)
    return True

def check_user(username, password):
    df = load_users()
    return ((df["username"] == username) & (df["password"] == password)).any()

# -------------------- PDF GENERATION --------------------
def generate_pdf(name, academics, interests, career, universities, scholarships):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    pdf.cell(200, 10, txt="EduPath Career Guidance Report", ln=True, align='C')
    pdf.ln(5)

    pdf.cell(200, 10, txt=f"Name: {name}", ln=True)
    pdf.ln(3)

    pdf.cell(200, 10, txt="Subject Combinations:", ln=True)
    for sub in academics:
        pdf.cell(200, 10, txt=f"- {sub}", ln=True)

    pdf.ln(3)
    pdf.cell(200, 10, txt="Interests:", ln=True)
    for i in interests:
        pdf.cell(200, 10, txt=f"- {i}", ln=True)

    pdf.ln(3)
    pdf.cell(200, 10, txt="Suggested Careers:", ln=True)
    for c in career:
        pdf.cell(200, 10, txt=f"- {c}", ln=True)

    pdf.ln(3)
    pdf.cell(200, 10, txt="Suggested Universities:", ln=True)
    for u in universities:
        pdf.cell(200, 10, txt=f"- {u}", ln=True)

    pdf.ln(3)
    pdf.cell(200, 10, txt="Scholarship Alerts:", ln=True)
    for s in scholarships:
        pdf.cell(200, 10, txt=f"- {s}", ln=True)
    pdf.ln(7)
    pdf.set_font("Arial", size=10)
    pdf.cell(200, 10, txt=f"Developed by Beloved Team © 2025 | Contact:09018181284 | Email:gbadebogideon333@gmail.com", ln=True, align='C')

    filename = f"{name}_report.pdf"
    pdf.output(filename)
    return filename

# -------------------- DATA STORAGE --------------------
def save_to_csv(data):
    df_new = pd.DataFrame([data])
    if os.path.exists(DATA_FILE):
        df_old = pd.read_csv(DATA_FILE)
        df = pd.concat([df_old, df_new], ignore_index=True)
    else:
        df = df_new
    df.to_csv(DATA_FILE, index=False)

# -------------------- AUTH PAGE --------------------
def auth_page():
    st.title("🔐 EduPath Authentication")
    choice = st.selectbox("Menu", ["Login", "Sign Up"])

    if choice == "Login":
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")

        if st.button("Login"):
            if check_user(username, password):
                st.session_state.logged_in = True
                st.session_state.username = username
                st.success("Login successful")
                st.rerun()
            else:
                st.error("Invalid credentials")

        st.stop()

    else:
        username = st.text_input("New Username")
        password = st.text_input("New Password", type="password")

        if st.button("Register"):
            if save_user(username, password):
                st.success("Account created successfully. Proceed to Login")
            else:
                st.warning("Username already exists!")

        st.stop()

# -------------------- CAREER LOGIC --------------------
def career_logic(academics, interests, avg_score):
    if "Mathematics" in academics and "Physics" in academics and avg_score >= 65 and ("Technology" in interests or "Science" in interests):
        return ["Computer Science", "Computer Engineering","Mechanical Engineering","Information Technology"], ["UI", "UNILAG", "FUTA"], ["MTN Foundation Scholarship", "NLNG Undergraduate Scholarship", "Chevron Scholarship"]

    elif "Biology" in academics and avg_score >= 70 and "Health" in interests:
        return ["Medicine", "Nursing","Pharmacy", "Animal Health"], ["UNIBEN", "UNILAG", "ABU", "OAU"], ["Shell Scholarship","PTDF Scholarship", "NDDC Scholarship"]

    elif "Biology" in academics and "Chemistry" in academics and avg_score >= 65 and "Science" in interests:
        return ["Chemical Engineering","Biology","Biochemistry","Microbiology","Medical Laboratory Science"], ["UNILAG", "ABU", "UI","OAU","Covenant University"], ["Shell Scholarship", "Chevron Scholarship","Jim Ovia Foundation Scholarship"]

    elif "Economics" in academics and avg_score >= 60 and "Business/Finance" in interests:
        return ["Business Administration","Economics","Accounting","Banking and Finance"], ["Lagos Business School", "UI", "UNILAG","PanAlantic Scholarship"], ["CBN Scholarship", "AACE Scholarship"]
    
    elif "Literature" in academics or "Government" in academics and avg_score >= 65 and "Arts" in interests:
        return ["Law","Mass Communication","International Relations","Journalism","English Language"], ["UNILAG", "ABU", "UI"], ["CBN Scholarship","Nigerian Law School Scholarship", "Chevening Scholarship"]
    
    elif "Geography" in academics and avg_score >= 60 and "Environment" in interests:
        return ["Environmental Science","Urban Planning","Geology","Architecture"], ["UI", "UNILAG", "FUTA"], ["NDDC Scholarship", "Shell Scholarship"]
    
    elif "Government" in academics and avg_score >= 60 and "Arts" in interests:
        return ["Political Science", "Law", "Public administration", "Sociology"], ["UI", "UNILAG"], ["CBN Scholarship"]
    
    elif avg_score >= 55 and "Sports" in interests:
        return ["Physical Education","Sports Management"], ["UI", "UNILAG","ABU"], ["Nigerian Sports Commission Scholarship"]

    else:
        return ["Explore more options"], ["Various"], ["Various"]

# -------------------- MAIN APP --------------------
def main_app():
    st.title("🎓 EduPath Career Guide")
    st.subheader(f"Welcome, {st.session_state.username}!")
    st.write("EduPath helps you find the best career path based on your Academic scores and Personal interests.")

    name = st.text_input("Full Name")
    age = st.number_input("Age", 16, 40)

    st.write("Please enter your details below:")
    academics = st.multiselect(
        "Select Subjects",
        ["Mathematics","English","Biology","Chemistry","Physics","Government","Economics","Literature","Geography"]
    )

    scores = []
    for i, sub in enumerate(academics):
        s = st.number_input(f"{sub} Score", 0, 100, key=f"score_{i}")
        scores.append(s)

    interests = st.multiselect("Interests", ["Science","Technology","Business/Finance","Health","Education","Arts","Environment","Sports"])

    if st.button("Generate"):
        if not name or not academics or not interests:
            st.error("Fill all fields")
            return

        avg_score = sum(scores) / len(scores) if scores else 0

        career, universities, scholarships = career_logic(academics, interests, avg_score)

        st.write("### Careers")
        st.write(career)

        st.write("### Universities")
        st.write(universities)

        st.write("### Scholarships")
        st.write(scholarships)

        save_to_csv({
            "Name": name,
            "Subjects": academics,
            "Interests": interests,
            "Careers": career,
            "Time": datetime.now()
        })

        pdf = generate_pdf(name, academics, interests, career, universities, scholarships)

        with open(pdf, "rb") as f:
            st.download_button("Download PDF", f, file_name=pdf)

# -------------------- DASHBOARD --------------------
def dashboard():
    st.title("📊 Admin Dashboard")

    if not os.path.exists(DATA_FILE):
        st.info("No data yet")
        return

    df = pd.read_csv(DATA_FILE)
    st.dataframe(df)

    st.metric("Total Users", len(df))

# -------------------- MAIN --------------------
def main():
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False

    if not st.session_state.logged_in:
        auth_page()
    else:
        if st.session_state.username == "admin":
            dashboard()
        else:
            main_app()

if __name__ == "__main__":
    main()
