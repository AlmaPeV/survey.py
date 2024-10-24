# -*- coding: utf-8 -*-
"""survey.py

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1xRnGzHwo0RSkREru2GUSS3WOkh1WSxna
"""

import streamlit as st
import random

# Define a list of samples (replace with your actual samples)
samples = ["Sample 1", "Sample 2", "Sample 3", "Sample 4", "Sample 5",
           "Sample 6", "Sample 7", "Sample 8", "Sample 9", "Sample 10"]

def conduct_survey():
    remaining_samples = st.session_state.remaining_samples
    round_number = st.session_state.round_number

    if len(remaining_samples) > 1 and round_number <= 10:
        sample_pair = random.sample(remaining_samples, 2)

        st.write(f"\nRound {round_number}:")
        st.write(f"1: {sample_pair[0]}")
        st.write(f"2: {sample_pair[1]}")

        choice = st.radio("Select the sample you like more:", options=['1', '2'], index=0, key=f"round_{round_number}")

        col1, col2 = st.beta_columns(2)
        with col1:
            if st.button("Next Round"):
                if choice == '1':
                    selected_sample = sample_pair[0]
                    remaining_samples.remove(sample_pair[1])
                elif choice == '2':
                    selected_sample = sample_pair[1]
                    remaining_samples.remove(sample_pair[0])

                st.session_state.rounds_info.append({
                    'round': round_number,
                    'appeared_samples': sample_pair,
                    'selected_sample': selected_sample
                })

                st.session_state.remaining_samples = remaining_samples
                st.session_state.round_number += 1
                
                # Simulate page rerun
                st.experimental_rerun()

        with col2:
            if st.button("Finish Survey"):
                st.session_state.survey_completed = True

                # Display thank you message
                st.write("Thank you for participating in the survey!")
    
    else:
        st.write("Thank you for participating in the survey!")
        st.session_state.survey_completed = True

# Streamlit app
st.title("Sample Preference Survey")

# Authentication section
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False

password = st.text_input("Enter password to access the admin panel:", type='password')

if password == '0103':
    st.session_state.authenticated = True
    st.success("Access granted")
elif password != '':
    st.error("Invalid password")

# Survey initialization
if 'survey_completed' not in st.session_state:
    st.session_state.survey_completed = False

if 'round_number' not in st.session_state:
    st.session_state.round_number = 1
    st.session_state.remaining_samples = samples.copy()
    st.session_state.rounds_info = []

# Survey section
if st.session_state.round_number == 1 and not st.session_state.survey_completed:
    participant_name = st.text_input("Enter your name or code to start the survey:", "")
    if participant_name:
        st.session_state.participant_name = participant_name
        if st.button("Start Survey"):
            conduct_survey()
else:
    if not st.session_state.survey_completed:
        conduct_survey()

# Admin panel
if st.session_state.authenticated:
    st.subheader("Admin Panel")
    st.write("Real-time survey results:")

    if 'rounds_info' in st.session_state:
        for info in st.session_state.rounds_info:
            st.write(f"Participant: {st.session_state.participant_name}, Round {info['round']}: Appeared Samples: {info['appeared_samples']}, Selected Sample: {info['selected_sample']}")
