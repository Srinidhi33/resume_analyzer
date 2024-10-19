import streamlit as st
import requests

#set a page title
st.set_page_config(page_title="AI-Powered Resume Analyzer", page_icon="📄", layout="wide")

# Title with icon and header image
st.title("📄 AI-Powered Resume Analyzer")
st.image("curriculum-vitae.png", width=150)  # Adjust the path to your logo

# upload resume file
uploaded_file = st.file_uploader("Upload your resume", type=["pdf", "docx"])

# get job title as well
job_title = st.text_input("Enter the Job Title (e.g., Data Analyst, Software Engineer)", placeholder="e.g., Software Engineer")

# Add a button to trigger the analysis
if st.button("Analyze Resume"):
    if uploaded_file is not None and job_title:
        with st.spinner("Analyzing..."):
            # format the request to the FastAPI server
            files = {'file': (uploaded_file.name, uploaded_file.read(), uploaded_file.type)}
            data = {"job_title": job_title}
            
            # hit the POST request to the FastAPI server
            response = requests.post("http://127.0.0.1:8000/upload_resume/", files=files, data=data)
            
            if response.status_code == 200:
                result = response.json()
                
                # split results using two columns
                col1, col2 = st.columns(2)
                
                #one column shows mathced keywords
                with col1:
                    st.subheader("Filename: ")
                    st.write(result.get("filename"))
                    
                    st.subheader("✅ Keywords that matched:")
                    st.success(", ".join(result.get("matched_keywords", [])))

                #another shows missing keywords
                with col2:
                    st.subheader("❌ Keywords that missed:")
                    st.error(", ".join(result.get("missing_keywords", [])))

                #calculate the mathc score based on the keywords missed
                st.subheader("Score:")
                match_score = result.get("match_score", 0)
                st.progress(int(match_score))  # Show a progress bar for match score
                st.write(f"{match_score:.2f}%")

                #return a feedback
                st.subheader("📋 AI-Generated Feedback:")
                #default feedback if no feedback  available
                feedback = result.get("feedback", "No feedback available")
                st.info(feedback)

            else:
                st.error(f"Error: {response.status_code}, {response.text}")
    else:
        st.warning("Please upload a resume and provide a job title.")

#add a sidebar about the tool and rate-o-meter
with st.sidebar:
    st.markdown("## About This Tool")
    st.write("""
    This tool is powered by **FastAPI** and **Streamlit** to help job applicants analyze their resumes.
    It matches your resume's content with the skills and qualifications required for the job title you’re targeting.
    """)
    rating=st.slider("Rate us ❤️ ",0,10)
    if rating > 8:
        st.image("https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExZXBub2t2c3p4a2R4eWZ4eW44ZmR0enFvdjBpY2lycDR4YWdzODdxZSZlcD12MV9naWZzX3NlYXJjaCZjdD1n/eJT738HFSQDVS/giphy.gif",width=280)
    elif rating > 5 and rating <= 8:
        st.image("https://media.giphy.com/media/SgwPtMD47PV04/giphy.gif?cid=ecf05e47uqcdvv32vmlzbfzrb5ix9b6vj4xwfw5mg34pgqyy&ep=v1_gifs_related&rid=giphy.gif&ct=g",width=280)
    else:
        st.image("https://i.giphy.com/media/v1.Y2lkPTc5MGI3NjExZ3BoYnpib2xhdDJ4N2s4a3lncDQxdWF3MHF0YTFyM2NuaTJxZ3h3NCZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/OPU6wzx8JrHna/giphy.gif", width=280)  # Adjust the path to your logo

    
# Add a footer
st.markdown("""
    <style>
    footer {visibility:visible;}
    </style>
    <footer>
        <p><center>AI can make <b>mistakes</b> :( <b>||</b> Developed with ❤️ using <b>Streamlit</b> and <b>FastAPI</b> <b>||</b> © 2024 All Rights Reserved. Privacy Policy</center></p>
    </footer>
    """, unsafe_allow_html=True)

