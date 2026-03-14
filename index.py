import streamlit as st
import mysql.connector
import pandas as pd

st.set_page_config(page_title="Student Information Manager")

# Database Connection Function
def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="student_db"
    )

st.title("Student Information Manager")

# Function to load students from the database
def load_students():
    conn = get_db_connection()
    df = pd.read_sql("SELECT * FROM students", conn)
    conn.close()
    return df

tab1, tab2, tab3 = st.tabs(["Add Student", "View/Search Student", "Update/Delete"])

#tab1 - Add Student
with tab1:
    with st.form("student_form", clear_on_submit=True):
        st.subheader("Add New Student")

        col1, col2 = st.columns(2)

        with col1:
            student_id = st.text_input("Student ID")
            full_name = st.text_input("Full Name")
            age = st.number_input("Age", value=None, max_value=120)

        with col2:
            gender = st.radio("Gender", ["Male", "Female"])
            course = st.selectbox("Course", [""] + ["BSIT", "BSCS", "BSHM", "BEED", "BSBA", "BSN"])
            year_level = st.selectbox("Year Level", [""] + ["1st", "2nd", "3rd", "4th"])

        email = st.text_input("Email")

        submitted = st.form_submit_button("Add Student")

        if submitted:
            if student_id.strip()=="" or full_name.strip()=="" or course.strip()=="" or email.strip()=="" or year_level.strip()=="":
                st.error("Please fill in all required fields!")
            else:
                conn = get_db_connection()
                cursor = conn.cursor()

                cursor.execute("""
                    INSERT INTO students (student_id, full_name, age, gender, course, year_level, email)
                    VALUES (%s,%s,%s,%s,%s,%s,%s)
                """,(student_id, full_name, age, gender, course, year_level, email))

                conn.commit()
                cursor.close()
                conn.close()

                st.success(f"Student '{student_id} - {full_name}' added!")

with tab2:
    st.subheader("All Students / Search Student")

    search_input = st.text_input("Search by Full Name or Student ID")
    df = load_students()
    if search_input.strip() != "":
        df = df[
            df["full_name"].str.contains(search_input, case=False) |
            df["student_id"].str.contains(search_input, case=False)
        ]

    table_placeholder = st.empty()
    table_placeholder.dataframe(df)

#tab3 - Update/Delete Student
with tab3:
    with st.form("update_delete_form", clear_on_submit=True):
        st.subheader("Update/Delete Student")

        col1, col2 = st.columns(2)

        with col1:
            student_id = st.text_input("Enter Student ID")
            full_name = st.text_input("Full Name")

        with col2:
            age = st.number_input("Age", value=None, max_value=120)
            gender = st.radio("Gender", ["Male", "Female"])

        course = st.selectbox("Course", [""] + ["BSIT", "BSCS", "BSHM", "BEED", "BSBA", "BSN"])
        year_level = st.selectbox("Year Level", [""] + ["1st", "2nd", "3rd", "4th"])
        email = st.text_input("Email")

        update_btn = st.form_submit_button("Update Student")
        delete_btn = st.form_submit_button("Delete Student")

        # UPDATE
        if update_btn:
            if student_id.strip()=="" or full_name.strip()=="" or course.strip()=="" or email.strip()=="" or year_level.strip()=="":
                st.error("Please fill all fields and enter a valid Student ID!")
            else:
                conn = get_db_connection()
                cursor = conn.cursor()

                cursor.execute("""
                    UPDATE students
                    SET full_name=%s, age=%s, gender=%s, course=%s, year_level=%s, email=%s
                    WHERE student_id=%s
                """,(full_name, age, gender, course, year_level, email, student_id))

                conn.commit()
                cursor.close()
                conn.close()

                st.success("Student updated successfully!")

        # DELETE
        if delete_btn:
            if student_id.strip()=="" or full_name.strip()=="":
                st.error("Please enter both Student ID and Full Name before deleting!")
            else:
                conn = get_db_connection()
                cursor = conn.cursor()

                cursor.execute(
                    "SELECT * FROM students WHERE student_id=%s AND full_name=%s",
                    (student_id, full_name)
                )

                record = cursor.fetchone()

                if record:
                    cursor.execute(
                        "DELETE FROM students WHERE student_id=%s",
                        (student_id,)
                    )
                    conn.commit()
                    st.success("Student deleted successfully!")
                else:
                    st.error("Student ID and Full Name do not match any record.")

                cursor.close()
                conn.close()