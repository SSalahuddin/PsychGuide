import streamlit as st
import anthropic

# Set the title and introduction
st.title('Psychiatric Patient Diagnosis and Treatment App')
st.write("""
Welcome to the Psychiatric Patient Diagnosis and Treatment App. 
Please provide the following information to receive a personalized diagnosis and treatment recommendation.
Your responses will remain confidential.
""")

# Sidebar for inputs
st.sidebar.header('Patient Information')

# Input for Mental Health History
mental_health_history = st.sidebar.text_area('Mental Health History', 
                                             placeholder="Please describe your past psychiatric history...")

# Input for Current Symptoms
current_symptoms = st.sidebar.multiselect(
    'Current Symptoms', 
    ['Anxiety', 'Depression', 'Insomnia', 'Mood Swings', 'Irritability', 'Fatigue', 'Difficulty Concentrating', 'Panic Attacks', 'Other']
)

# Input for Medication Preferences
medication_pref = st.sidebar.selectbox(
    'Medication Preferences', 
    ['No Preference', 'Prefer Natural Remedies', 'Prefer Prescription Medication', 'Prefer to Avoid Medication']
)

# Input for Treatment Preferences
treatment_pref = st.sidebar.radio(
    'Treatment Preferences', 
    ['Cognitive Behavioral Therapy (CBT)', 'Medication Management', 'Therapy & Medication', 'Mindfulness-Based Therapy', 'Other']
)

# Input for Preferred Communication Method
communication_pref = st.sidebar.selectbox(
    'Preferred Communication Method', 
    ['Text Only', 'Text and Call']
)

# Show additional fields for Text and Call option
patient_name = None
patient_contact_number = None

if communication_pref == 'Text and Call':
    patient_name = st.sidebar.text_input('Patient Name')
    patient_contact_number = st.sidebar.text_input('Contact Number', help="Please enter your phone number")

# Input for Claude AI API key
api_key = st.secrets["claude_api_key"]

# Main section for displaying results
st.header('Personalized Diagnosis and Treatment Plan')

# Button to submit the form
if st.sidebar.button('Submit'):
    if api_key:  # Ensure the API key is provided
        if communication_pref == 'Text and Call' and (not patient_name or not patient_contact_number):
            st.error("Please provide both name and contact number to receive the call.")
        else:
            # Initialize the Claude AI client with the provided API key
            client = anthropic.Anthropic(api_key=api_key)

            # Prepare the prompt to send to Claude AI
            prompt = (
                f"Mental Health History: {mental_health_history}\n"
                f"Current Symptoms: {', '.join(current_symptoms)}\n"
                f"Medication Preferences: {medication_pref}\n"
                f"Treatment Preferences: {treatment_pref}\n"
                f"Preferred Communication Method: {communication_pref}\n\n"
                "Please provide a personalized diagnosis and treatment plan based on the above information."
            )

            # Call Claude AI API
            message = client.messages.create(
                model="claude-3-5-sonnet-20240620",
                max_tokens=280,
                temperature=0.7,  # Adjust temperature for balanced creativity
                system="You are a world-class psychiatrist who specializes in providing personalized mental health diagnoses and treatment plans.",
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            )

            # Extract the response content
            raw_context = message.content
            diagnosis_and_treatment = raw_context[0].text 

            # Display the response in the main section
            st.write(diagnosis_and_treatment)

            # Inform the patient that a call will be placed soon
            if communication_pref == 'Text and Call':
                st.success(f"Thank you, {patient_name}. A call will be placed to you at {patient_contact_number} within the next 24 hours.")
    else:
        st.error("Please enter your Claude API key to receive a diagnosis and treatment plan.")
else:
    st.write("Please complete the form in the sidebar and click 'Submit' to receive your personalized plan.")

# Additional UI/UX features for a calming experience
st.markdown("""
<style>
body {
    background-color: #f4f7f8;
    font-family: 'Arial', sans-serif;
}
.stSidebar {
    background-color: #f0f2f6;
}
.stButton > button {
    background-color: #4CAF50;
    color: white;
}
</style>
""", unsafe_allow_html=True)

# Footer with copyright and year
st.markdown("---")
st.markdown('<div style="text-align: center;">© 2024 PsychGuide by Engr. Sumayyea Salahuddin. All rights reserved.</div>', unsafe_allow_html=True)

