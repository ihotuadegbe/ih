import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import mysql.connector as connection
from PIL import Image


joy = connection.connect(host='relational.fit.cvut.cz', database = 'university',user = 'guest', passwd='relational',use_pure=True)




st.set_page_config(page_title="GPA Tracker", page_icon=":books:")




#primaryColor="#b99999"
st.image('images.jpeg', use_column_width=True)
st.sidebar.image('images.jpeg', use_column_width=True)
#t.set_page_config(page_title="GPA Tracker", page_icon=":books:")
#primaryColor="#b99999"
#backgroundColor="#4b2690"
#secondaryBackgroundColor="#9848a4"
#textColor="#f5eded"
#
                  #background_Color="#f5f5f5")# page_bgcolor="lightblue")
#bgcolor = "#F5F5F5"  # light gray
#st.markdown(f"""<style>body{{background-color: {bgcolor}}}</style>""", unsafe_allow_html=True)
st.write("<style> body {background-color: #f0f0f0;}</style>", unsafe_allow_html=True)


df = pd.read_sql_query('select * from registration',joy)

st.write('<style>div.row-widget.stRadio > div{background-color: #E5E5E5;}</style>', unsafe_allow_html=True)



st.title('Grade Tracking System')


# group the dataframe by student_id and calculate the mean grade for each student
student_gpa = df.groupby('student_id')['grade'].mean()

# create a button in the sidebar
if st.sidebar.button("Show Cumulative GPA"):
    # display the cumulative GPA for each student
    st.sidebar.title("Cumulative GPA by Student")
    for student_id, gpa in student_gpa.items():
        st.sidebar.write(f"Student {student_id}: {gpa:.2f}")

#st.sidebar.title("Cumulative GPA")
#cummulative_gpa = df['grade'].mean() 
#cummulative_gpa = df['grade'].mean() 
#st.sidebar.write(f'Cummulative GPA: {cummulative_gpa:2f}')

df['grade'] = pd.to_numeric(df['grade'])


def get_recommended_courses(gpa, interests):
    if gpa >= 3.5:
        return ["Advanced Computer Science", "Artificial Intelligence"]
    elif gpa >= 3.0:
        return ["Data Structures and Algorithms", "Database Systems"]
    else:
        return ["Introduction to Computer Science", "Statistics for Social Science"]
    
st.sidebar.title("Navigation")
menu = ["Home", "Set Target GPA", "Export Course and Grade Information", "Get Recommended Courses"]
choice = st.sidebar.selectbox("Select an option", menu)

if choice == "Home":
    # Get the student ID from the user
    student_id = st.text_input("Enter your student ID")


# Define the top-performing students function
def show_top_performing_students():
    # Sort students by cumulative GPA
    sorted_students = df.groupby('student_id')['grade'].mean().sort_values(ascending=False)
    
    # Display top-performing students
    st.write('Top Performing Students')
    st.write(sorted_students.head(10))

# Define the struggling students function
def show_struggling_students():
    # Identify students with low GPA
    struggling_students = df[df['grade'] < 2.0]
    
    # Display struggling students
    st.write('Struggling Students')
    st.write(struggling_students)

# Add a sidebar button for top-performing students
if st.sidebar.button('Show Top Performing Students'):
    show_top_performing_students()

# Add a sidebar button for struggling students
if st.sidebar.button('Show Struggling Students'):
    show_struggling_students()

# Calculate descriptive statistics
mean_gpa = df['grade'].mean()
median_gpa = df['grade'].median()
min_gpa = df['grade'].min()
max_gpa = df['grade'].max()
std_gpa = df['grade'].std()




with st.sidebar:
    target_gpa = st.slider('Set your target GPA', min_value=0.0, max_value=4.0, step=0.1)
    remaining_points=(target_gpa* len(df)) - df['grade'].sum()
    st.write(f'you need an additional' + str(round(remaining_points, 2)) +  'points to achieve your target GPA of' + str(target_gpa))

gpa_df = df.groupby('student_id').mean() ['grade'].reset_index()

gpa_df = gpa_df.sort_values('grade',ascending=False).reset_index(drop=True)

st.write(df)

selected_course_id = st.sidebar.selectbox('Select a Course',df['course_id'].unique())
selected_course =df[df['course_id'] == selected_course_id]

    # Course Statistics
st.header('Course Statistics')
st.write('Number of Courses:', df['course_id'].nunique())
st.write('Total Courses Taken:', len(df))




# create plot
#fig, ax = plt.subplots()
#ax.plot(df['grade'].cumsum())
#ax.set_xlabel('Semester')
#ax.set_ylabel('Cumulative GPA')

# display plot in Streamlit container
#st.subheader('Cumulative GPA over Time')
#st.pyplot(fig)


# Assuming the index represents the semesters
semester_gpa = df.groupby(df.index)['grade'].mean()
st.header('Semester-wise Performance')
st.line_chart(semester_gpa)


st.header('Grade Distribution')
st.bar_chart(df['grade'])




    
st.header('Grade Comparison')
course_comparison = df.groupby('course_id')['grade'].mean()
st.bar_chart(course_comparison)




    
    
    
    
    
    
    
    
    
    
    
