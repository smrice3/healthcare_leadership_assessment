import streamlit as st
import pandas as pd
import numpy as np
import io
import base64
from fpdf import FPDF
import matplotlib.pyplot as plt

# Set page config
st.set_page_config(
    page_title="Healthcare Leadership Self-Assessment",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Define the assessment categories and items
assessment_categories = {
    "Emotional Intelligence": [
        "Self-awareness: Ability to recognize your emotions, strengths, weaknesses, values, and impact on others",
        "Self-management: Ability to regulate emotions, demonstrate adaptability, and maintain a positive outlook",
        "Social awareness: Ability to recognize others' emotions and organizational dynamics",
        "Relationship management: Ability to influence, mentor, manage conflict, and foster teamwork"
    ],
    "Communication Excellence": [
        "Audience adaptation: Ability to adjust communication style and content for different stakeholders",
        "Active listening: Ability to fully concentrate, understand, respond, and remember what others communicate",
        "Conflict resolution: Ability to facilitate productive resolution of disagreements",
        "Crisis communication: Ability to communicate effectively under pressure",
        "Team communication: Ability to foster open, transparent communication within teams"
    ],
    "Patient-Centered Leadership": [
        "Patient journey understanding: Comprehension of the full spectrum of patient experiences",
        "Empathy-efficiency balance: Ability to maintain compassionate care while meeting operational requirements",
        "Accountability systems: Ability to establish clear expectations and foster a culture of responsibility"
    ],
    "Strategic Decision-Making": [
        "Workload management: Ability to allocate resources effectively across competing priorities",
        "Strategic thinking: Ability to consider long-term implications and align decisions with organizational vision",
        "Data analysis: Ability to interpret quantitative and qualitative information to inform decisions",
        "Problem-solving: Ability to identify root causes and implement effective solutions"
    ]
}

# Define qualitative questions
qualitative_questions = {
    "Emotional Intelligence": [
        "Describe a recent situation where you successfully managed your emotions in a challenging leadership scenario. What strategies did you use?",
        "In what situations do you find it most difficult to maintain emotional self-regulation? What triggers these challenges?",
        "How do you currently build and maintain relationships with team members? What approaches have been most successful?"
    ],
    "Communication Excellence": [
        "What communication approaches do you currently use to adapt your message to different audiences (e.g., frontline staff, executives, patients)?",
        "Describe your typical approach when faced with team conflict. What works well, and what could be improved?",
        "How do you ensure important information flows effectively within your team or department?"
    ],
    "Patient-Centered Leadership": [
        "How do you currently incorporate patient perspectives into your leadership decisions?",
        "Describe how you balance empathy with operational efficiency in your daily leadership practice.",
        "What accountability mechanisms have you implemented or experienced that effectively support patient-centered care?"
    ],
    "Strategic Decision-Making": [
        "How do you typically approach complex problems in your healthcare setting?",
        "What data sources do you currently use to inform your leadership decisions?",
        "Describe a recent strategic decision you made. What factors did you consider, and how did you evaluate success?"
    ]
}

strength_development_questions = [
    "Identify your top three leadership strengths across the four domains.",
    "Identify three specific areas where you see the greatest opportunity for development.",
    "For each development opportunity, describe why growth in this area matters to your leadership effectiveness.",
    "What specific aspects of this course could help address these development needs?",
    "What would success look like if you improved in these areas?"
]

# Initialize session state
if 'current_step' not in st.session_state:
    st.session_state.current_step = 1
if 'quantitative_responses' not in st.session_state:
    st.session_state.quantitative_responses = {}
if 'qualitative_responses' not in st.session_state:
    st.session_state.qualitative_responses = {}
if 'strength_development_responses' not in st.session_state:
    st.session_state.strength_development_responses = {}

# Navigation functions
def next_step():
    st.session_state.current_step += 1

def prev_step():
    st.session_state.current_step -= 1

# Function to create PDF using fpdf
def create_pdf():
    pdf = FPDF()
    pdf.add_page()
    
    # Set up fonts
    pdf.set_font('Arial', 'B', 16)
    
    # Title
    pdf.cell(0, 10, 'Healthcare Leadership Self-Assessment Report', 0, 1, 'C')
    pdf.ln(5)
    
    # Part 1: Quantitative Assessment
    pdf.set_font('Arial', 'B', 14)
    pdf.cell(0, 10, 'Part 1: Quantitative Self-Assessment', 0, 1, 'L')
    
    pdf.set_font('Arial', '', 10)
    pdf.cell(0, 6, 'Rating Scale:', 0, 1, 'L')
    pdf.cell(0, 6, '1 = Novice: Limited experience or confidence in this area', 0, 1, 'L')
    pdf.cell(0, 6, '2 = Developing: Basic understanding with occasional application', 0, 1, 'L')
    pdf.cell(0, 6, '3 = Competent: Consistent application in routine situations', 0, 1, 'L')
    pdf.cell(0, 6, '4 = Proficient: Adaptable application across diverse situations', 0, 1, 'L')
    pdf.cell(0, 6, '5 = Expert: Intuitive mastery with ability to coach others', 0, 1, 'L')
    pdf.ln(5)
    
    # Create quantitative results tables for each category
    for category, items in assessment_categories.items():
        pdf.set_font('Arial', 'B', 12)
        pdf.cell(0, 10, category, 0, 1, 'L')
        
        pdf.set_font('Arial', 'B', 10)
        
        # Table header
        pdf.cell(160, 8, 'Competency', 1, 0, 'L')
        pdf.cell(30, 8, 'Rating', 1, 1, 'C')
        
        # Table rows
        pdf.set_font('Arial', '', 10)
        for item in items:
            # Adjust text to fit in cell
            competency_text = item
            if len(competency_text) > 80:
                competency_text = competency_text[:77] + '...'
                
            if item in st.session_state.quantitative_responses:
                rating = str(st.session_state.quantitative_responses[item])
            else:
                rating = "Not rated"
                
            pdf.cell(160, 8, competency_text, 1, 0, 'L')
            pdf.cell(30, 8, rating, 1, 1, 'C')
        
        pdf.ln(5)
    
    # Part 2: Qualitative Assessment
    pdf.add_page()
    pdf.set_font('Arial', 'B', 14)
    pdf.cell(0, 10, 'Part 2: Qualitative Self-Assessment', 0, 1, 'L')
    
    for category, questions in qualitative_questions.items():
        pdf.set_font('Arial', 'B', 12)
        pdf.cell(0, 10, category, 0, 1, 'L')
        
        for i, question in enumerate(questions):
            pdf.set_font('Arial', 'B', 10)
            pdf.multi_cell(0, 6, f"Q: {question}", 0, 'L')
            
            key = f"{category}_qualitative_{i}"
            pdf.set_font('Arial', '', 10)
            
            if key in st.session_state.qualitative_responses:
                response = st.session_state.qualitative_responses[key]
                pdf.multi_cell(0, 6, f"A: {response}", 0, 'L')
            else:
                pdf.multi_cell(0, 6, "A: No response provided", 0, 'L')
            
            pdf.ln(5)
    
    # Part 3: Strengths and Development
    pdf.add_page()
    pdf.set_font('Arial', 'B', 14)
    pdf.cell(0, 10, 'Part 3: Strengths and Development Opportunities', 0, 1, 'L')
    
    for i, question in enumerate(strength_development_questions):
        key = f"strength_development_{i}"
        
        pdf.set_font('Arial', 'B', 10)
        pdf.multi_cell(0, 6, question, 0, 'L')
        
        pdf.set_font('Arial', '', 10)
        if key in st.session_state.strength_development_responses:
            response = st.session_state.strength_development_responses[key]
            pdf.multi_cell(0, 6, response, 0, 'L')
        else:
            pdf.multi_cell(0, 6, "No response provided", 0, 'L')
        
        pdf.ln(5)
    
    # Save the PDF to a BytesIO object
    pdf_output = io.BytesIO()
    pdf.output(pdf_output)
    pdf_data = pdf_output.getvalue()
    pdf_output.close()
    
    return pdf_data

# Function to create download link for PDF
def get_pdf_download_link(pdf_data):
    b64 = base64.b64encode(pdf_data).decode()
    href = f'<a href="data:application/pdf;base64,{b64}" download="leadership_self_assessment.pdf">Download PDF Report</a>'
    return href

# Sidebar navigation
st.sidebar.title("Navigation")
st.sidebar.markdown("## Progress")

# Display different progress based on current step
if st.session_state.current_step == 1:
    st.sidebar.markdown("🔵 **Part 1: Quantitative Assessment**")
    st.sidebar.markdown("⚪ Part 2: Qualitative Assessment")
    st.sidebar.markdown("⚪ Part 3: Strengths & Development")
    st.sidebar.markdown("⚪ Generate Report")
elif st.session_state.current_step == 2:
    st.sidebar.markdown("✅ Part 1: Quantitative Assessment")
    st.sidebar.markdown("🔵 **Part 2: Qualitative Assessment**")
    st.sidebar.markdown("⚪ Part 3: Strengths & Development")
    st.sidebar.markdown("⚪ Generate Report")
elif st.session_state.current_step == 3:
    st.sidebar.markdown("✅ Part 1: Quantitative Assessment")
    st.sidebar.markdown("✅ Part 2: Qualitative Assessment")
    st.sidebar.markdown("🔵 **Part 3: Strengths & Development**")
    st.sidebar.markdown("⚪ Generate Report")
elif st.session_state.current_step == 4:
    st.sidebar.markdown("✅ Part 1: Quantitative Assessment")
    st.sidebar.markdown("✅ Part 2: Qualitative Assessment")
    st.sidebar.markdown("✅ Part 3: Strengths & Development")
    st.sidebar.markdown("🔵 **Generate Report**")

# Main content area
st.title("Healthcare Leadership Self-Assessment")

# Part 1: Quantitative Assessment
if st.session_state.current_step == 1:
    st.header("Part 1: Quantitative Self-Assessment")
    
    st.markdown("""
    Rate your current competency level in each area using the following scale:
    - 1 = Novice: Limited experience or confidence in this area
    - 2 = Developing: Basic understanding with occasional application
    - 3 = Competent: Consistent application in routine situations
    - 4 = Proficient: Adaptable application across diverse situations
    - 5 = Expert: Intuitive mastery with ability to coach others
    """)
    
    for category, items in assessment_categories.items():
        st.subheader(category)
        
        for item in items:
            col1, col2 = st.columns([4, 1])
            with col1:
                st.markdown(f"**{item}**")
            with col2:
                key = item
                st.session_state.quantitative_responses[key] = st.selectbox(
                    f"Rate your competency in {item}",
                    options=[1, 2, 3, 4, 5],
                    index=2 if key not in st.session_state.quantitative_responses else st.session_state.quantitative_responses[key] - 1,
                    key=f"quantitative_{category}_{key}",
                    label_visibility="collapsed"
                )
                
    st.button("Next: Qualitative Assessment", on_click=next_step)

# Part 2: Qualitative Assessment
elif st.session_state.current_step == 2:
    st.header("Part 2: Qualitative Self-Assessment")
    
    for category, questions in qualitative_questions.items():
        st.subheader(category)
        
        for i, question in enumerate(questions):
            key = f"{category}_qualitative_{i}"
            st.markdown(f"**{question}**")
            
            # Pre-fill the text area with existing response if available
            existing_response = st.session_state.qualitative_responses.get(key, "")
            
            response = st.text_area(
                f"Your response to: {question}",
                value=existing_response,
                height=150,
                key=f"text_area_{key}",
                label_visibility="collapsed"
            )
            
            st.session_state.qualitative_responses[key] = response
            st.markdown("---")
    
    col1, col2 = st.columns(2)
    with col1:
        st.button("Previous: Quantitative Assessment", on_click=prev_step)
    with col2:
        st.button("Next: Strengths & Development", on_click=next_step)

# Part 3: Strengths and Development
elif st.session_state.current_step == 3:
    st.header("Part 3: Strengths and Development Opportunities")
    
    st.markdown("Based on your quantitative and qualitative assessments, please reflect on the following:")
    
    for i, question in enumerate(strength_development_questions):
        key = f"strength_development_{i}"
        st.markdown(f"**{question}**")
        
        # Pre-fill the text area with existing response if available
        existing_response = st.session_state.strength_development_responses.get(key, "")
        
        response = st.text_area(
            f"Your response to: {question}",
            value=existing_response,
            height=150,
            key=f"text_area_{key}",
            label_visibility="collapsed"
        )
        
        st.session_state.strength_development_responses[key] = response
        st.markdown("---")
    
    col1, col2 = st.columns(2)
    with col1:
        st.button("Previous: Qualitative Assessment", on_click=prev_step)
    with col2:
        st.button("Next: Generate Report", on_click=next_step)

# Generate Report
elif st.session_state.current_step == 4:
    st.header("Generate Your Self-Assessment Report")
    
    st.markdown("""
    ### Assessment Complete!
    
    Thank you for completing the Healthcare Leadership Self-Assessment exercise. 
    
    Your responses have been recorded. Click the button below to generate a PDF report of your self-assessment.
    """)
    
    if st.button("Generate PDF Report"):
        try:
            pdf_data = create_pdf()
            st.markdown(get_pdf_download_link(pdf_data), unsafe_allow_html=True)
            
            # Display a summary of the assessment
            st.subheader("Assessment Summary")
            
            # Calculate average scores per category
            category_scores = {}
            for category, items in assessment_categories.items():
                total = 0
                count = 0
                for item in items:
                    if item in st.session_state.quantitative_responses:
                        total += st.session_state.quantitative_responses[item]
                        count += 1
                
                if count > 0:
                    category_scores[category] = round(total / count, 1)
                else:
                    category_scores[category] = 0
            
            # Create a dataframe for the scores
            df_scores = pd.DataFrame({
                'Category': list(category_scores.keys()),
                'Average Score': list(category_scores.values())
            })
            
            # Create a bar chart using matplotlib
            fig, ax = plt.subplots(figsize=(10, 5))
            bars = ax.bar(df_scores['Category'], df_scores['Average Score'], color='steelblue')
            ax.set_title('Average Scores by Category')
            ax.set_xlabel('Category')
            ax.set_ylabel('Average Score')
            ax.set_ylim(0, 5)
            ax.grid(axis='y', linestyle='--', alpha=0.7)
            
            # Add labels on top of bars
            for bar in bars:
                height = bar.get_height()
                ax.text(bar.get_x() + bar.get_width()/2., height + 0.1,
                        f'{height:.1f}', ha='center', va='bottom')
            
            # Rotate x-axis labels for better readability
            plt.xticks(rotation=45, ha='right')
            plt.tight_layout()
            
            # Display the chart
            st.pyplot(fig)
            
            st.markdown("""
            ### Next Steps
            
            1. Review your full assessment in the downloaded PDF
            2. Reflect on your identified strengths and development areas
            3. Create a personal development plan based on your findings
            4. Share your insights with mentors or coaches as appropriate
            5. Set a date to retake this assessment to track your progress
            """)
        except Exception as e:
            st.error(f"An error occurred while generating the PDF: {str(e)}")
            st.info("Please try again or contact support if the issue persists.")
    
    col1, col2 = st.columns(2)
    with col1:
        st.button("Previous: Strengths & Development", on_click=prev_step)
    with col2:
        if st.button("Start New Assessment"):
            # Reset all session state variables
            st.session_state.current_step = 1
            st.session_state.quantitative_responses = {}
            st.session_state.qualitative_responses = {}
            st.session_state.strength_development_responses = {}
            st.experimental_rerun()

# Display footer
st.markdown("---")
st.markdown("© 2025 Healthcare Leadership Assessment Tool | Developed with Streamlit")
