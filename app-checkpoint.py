import streamlit as st
from langchain_groq import ChatGroq
import random
import matplotlib.pyplot as plt

# Initialize the ChatGroq model
llm = ChatGroq(
    temperature=0,
    groq_api_key='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',  # Replace with your actual API key
    model_name="llama-3.1-70b-versatile"
)

# Define available courses and difficulty levels
courses = ["Data Structures and Algorithms", "Machine Learning", "Web Development", "Database Management", "DevOps"]
difficulty_levels = ["Beginner", "Intermediate", "Advanced"]

# Function to generate study roadmap
def generate_roadmap(selected_course, selected_difficulty):
    prompt = f"Generate a detailed study roadmap for the course: {selected_course} at the {selected_difficulty} difficulty level. Please include relevant links to helpful resources for each topic covered in all difficulty levels and mention the time required to complete each topic."
    response = llm.invoke(prompt)
    return response.content if response.content else "Error: No roadmap generated."

# Function to get quiz based on selected course
def get_quiz(course):
    quizzes = {
        'Data Structures and Algorithms': [
            {'question': 'What is the time complexity of binary search?', 'options': ['O(n)', 'O(log n)', 'O(n^2)', 'O(1)'], 'answer': 'O(log n)', 'topic': 'Time Complexity'},
            {'question': 'Which data structure is used in a queue?', 'options': ['Stack', 'Heap', 'Array', 'Linked List'], 'answer': 'Linked List', 'topic': 'Data Structures'},
            {'question': 'Which of the following is not a sorting algorithm?', 'options': ['Quick Sort', 'Merge Sort', 'Binary Sort', 'Bubble Sort'], 'answer': 'Binary Sort', 'topic': 'Sorting Algorithms'},
        ],
        # Add more quizzes for other courses...
    }
    return quizzes.get(course, [])

# Function to display quiz and handle answer selection
def display_quiz(course):
    st.title(f"{course} Quiz")
    quiz = get_quiz(course)
    
    if f'quiz_{course}' not in st.session_state:
        random.shuffle(quiz)
        st.session_state[f'quiz_{course}'] = quiz
    else:
        quiz = st.session_state[f'quiz_{course}']

    score = 0
    incorrect_topics = []
    correct_topics = []
    user_answers = []

    for i, q in enumerate(quiz):
        st.subheader(f"Q{i+1}: {q['question']}")
        user_answer = st.radio(f"Choose your answer for Q{i+1}:", q['options'], key=f"q{i+1}_{course}")
        user_answers.append((user_answer, q['answer'], q['topic']))

    if st.button("Submit Quiz"):
        for user_answer, correct_answer, topic in user_answers:
            if user_answer == correct_answer:
                st.success(f"Correct answer: {correct_answer}")
                score += 1
                correct_topics.append(topic)
            else:
                st.error(f"Incorrect! The correct answer was: {correct_answer}")
                incorrect_topics.append(topic)

        total_questions = len(quiz)
        st.write(f"Your final score: {score}/{total_questions}")

        # Graphical representation of performance by topic
        topic_performance = {topic: correct_topics.count(topic) for topic in set(correct_topics + incorrect_topics)}
        topics = list(topic_performance.keys())
        correct_counts = [topic_performance[topic] for topic in topics]
        incorrect_counts = [total_questions - correct_count for correct_count in correct_counts]

        fig, ax = plt.subplots()
        ax.barh(topics, correct_counts, color='green', label='Correct')
        ax.barh(topics, incorrect_counts, left=correct_counts, color='red', label='Incorrect')
        ax.set_xlabel('Number of Correct/Incorrect Answers')
        ax.set_title('Performance by Topic')
        ax.legend()

        st.pyplot(fig)

        if (score / total_questions) < 0.7:
            st.warning("You scored less than 70%. Here are some resources to help you:")

            # Providing resources based on incorrect topics
            resources = {
                'Time Complexity': 'Resource: [Time Complexity Basics](https://www.geeksforgeeks.org/time-complexity-analysis/)',
                'Data Structures': 'Resource: [Introduction to Data Structures](https://www.geeksforgeeks.org/data-structures/)',
                'Sorting Algorithms': 'Resource: [Sorting Algorithms Explained](https://www.geeksforgeeks.org/sorting-algorithms/)',
            }

            for topic in set(incorrect_topics):
                st.markdown(resources.get(topic, "Resource not found."))

# Main app
st.sidebar.title("Navigation")
page = st.sidebar.radio("Select a page:", 
    ("🏠 Home", "🗺️ Generate Study Roadmap", "📝  Quizes and Progress  ")
)

if page == "🏠 Home":
    st.title("Welcome to Personalized AI Study Tool 🎓")
    st.write("Use this tool to generate study roadmaps and test your knowledge with quizzes. 🚀")

elif page == "🗺️ Generate Study Roadmap":
    st.title("AI Study Roadmap Generator")
    st.write("Select a course and difficulty level to generate a personalized study roadmap.")
    selected_course = st.selectbox("Choose a course:", courses)
    selected_difficulty = st.selectbox("Select difficulty level:", difficulty_levels)

    if st.button("Generate Roadmap"):
        roadmap = generate_roadmap(selected_course, selected_difficulty)
        st.write("### Your Personalized Study Roadmap:")
        st.write(roadmap)

elif page == "📝  Quizes and Progress  ":
    st.sidebar.title("Course Selection")
    course = st.sidebar.selectbox("Select a course:", ['Data Structures and Algorithms'])
    
    if course:
        display_quiz(course)

