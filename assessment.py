import streamlit as st
import pandas as pd
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from io import BytesIO
import base64

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

# Function to create PDF
def create_pdf():
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    styles = getSampleStyleSheet()
    
    # Create a custom title style
    styles.add(ParagraphStyle(
        name='Title',
        parent=styles['Heading1'],
        alignment=TA_CENTER,
        fontSize=16,
        spaceAfter=12
    ))
    
    # Create a custom heading style
    styles.add(ParagraphStyle(
        name='Heading2',
        parent=styles['Heading2'],
        fontSize=14,
        spaceAfter=6,
        spaceBefore=12
    ))
    
    styles.add(ParagraphStyle(
        name='Heading3',
        parent=styles['Heading3'],
        fontSize=12,
        spaceAfter=6,
        spaceBefore=6
    ))
    
    # Create content for the PDF
    content = []
    
    # Add title
    content.append(Paragraph("Healthcare Leadership Self-Assessment Report", styles['Title']))
    content.append(Spacer(1, 12))
    
    # Part 1: Quantitative Assessment
    content.append(Paragraph("Part 1: Quantitative Self-Assessment", styles['Heading2']))
    content.append(Paragraph("Rating Scale:", styles['Normal']))
    content.append(Paragraph("1 = Novice: Limited experience or confidence in this area", styles['Normal']))
    content.append(Paragraph("2 = Developing: Basic understanding with occasional application", styles['Normal']))
    content.append(Paragraph("3 = Competent: Consistent application in routine situations", styles['Normal']))
    content.append(Paragraph("4 = Proficient: Adaptable application across diverse situations", styles['Normal']))
    content.append(Paragraph("5 = Expert: Intuitive mastery with ability to coach others", styles['Normal']))
    content.append(Spacer(1, 12))
    
    # Create quantitative results tables for each category
    for category, items in assessment_categories.items():
        content.append(Paragraph(category, styles['Heading3']))
        
        data = []
        data.append(["Competency", "Rating"])
        
        for item in items:
            if item in st.session_state.quantitative_responses:
                rating = st.session_state.quantitative_responses[item]
                data.append([item, rating])
            else:
                data.append([item, "Not rated"])
        
        table = Table(data, colWidths=[400, 50])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (1, 0), colors.lightgrey),
            ('TEXTCOLOR', (0, 0), (1, 0), colors.black),
            ('ALIGN', (0, 0), (1, 0), 'CENTER'),
            ('ALIGN', (1, 1), (1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (1, 0), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0, 0), (1, 0), 12),
            ('BACKGROUND', (0, 1), (1, -1), colors.white),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        
        content.append(table)
        content.append(Spacer(1, 12))
    
    # Part 2: Qualitative Assessment
    content.append(Paragraph("Part 2: Qualitative Self-Assessment", styles['Heading2']))
    
    for category, questions in qualitative_questions.items():
        content.append(Paragraph(category, styles['Heading3']))
        
        for i, question in enumerate(questions):
            key = f"{category}_qualitative_{i}"
            content.append(Paragraph(f"<b>Q: {question}</b>", styles['Normal']))
            
            if key in st.session_state.qualitative_responses:
                response = st.session_state.qualitative_responses[key]
                content.append(Paragraph(f"A: {response}", styles['Normal']))
            else:
                content.append(Paragraph("A: No response provided", styles['Normal']))
            
            content.append(Spacer(1, 6))
        
        content.append(Spacer(1, 6))
    
    # Part 3: Strengths and Development
    content.append(Paragraph("Part 3: Strengths and Development Opportunities", styles['Heading2']))
    
    for i, question in enumerate(strength_development_questions):
        key = f"strength_development_{i}"
        content.append(Paragraph(f"<b>{question}</b>", styles['Normal']))
        
        if key in st.session_state.strength_development_responses:
            response = st.session_state.strength_development_responses[key]
            content.append(Paragraph(f"{response}", styles['Normal']))
        else:
            content.append(Paragraph("No response provided", styles['Normal']))
        
        content.append(Spacer(1, 6))
    
    # Build the PDF
    doc.build(content)
    pdf_data = buffer.getvalue()
    buffer.close()
    
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
        
        # Display the scores
        st.bar_chart(df_scores.set_index('Category'))
        
        st.markdown("""
        ### Next Steps
        
        1. Review your full assessment in the downloaded PDF
        2. Reflect on your identified strengths and development areas
        3. Create a personal development plan based on your findings
        4. Share your insights with mentors or coaches as appropriate
        5. Set a date to retake this assessment to track your progress
        """)
    
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
