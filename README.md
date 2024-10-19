# Interactify
Interactify is an AI-powered learning platform designed to enhance the way users interact with study materials. Using AI and machine learning, this platform allows users to upload slides, ask detailed questions, and receive intelligent explanations. It also offers customized learning resources and a history feature to track progress.

This project was developed using Streamlit for the frontend, and it integrates NLP models via the Gemini API to generate responses to user questions about document content.

## Features
Multi-Page Navigation: Easily navigate between different sections of the app, including Home, Career Pathways, Ask Me About Your Slide, and History.
Interactive Study Assistant: Upload files (PDF, DOCX, PPTX), view specific pages or slides, and ask questions about the content.
Personalized Study Materials: Tailored guides and quizzes to help students master different academic fields.
Download Feature: Generate and download custom content related to your field of study in a single click.
File Support: Upload files in PDF, DOCX, or PPTX format, and interact with them directly in the app.
Gemini API Integration: Uses the Gemini API to provide intelligent, AI-generated responses to questions based on document content.

# Table of Contents
Installation
Usage
Pages
Home
Career Pathways
Ask Me About Your Slide
History
Features to be Implemented
Technologies Used

Contributing

License

Installation
To run this project locally, follow these steps:

Clone the repository:

bash
Copy code
git clone https://github.com/Xtley001/Interactify.git
Install the dependencies: Navigate to the project directory and run:

bash
Copy code
pip install -r requirements.txt
Set up environment variables: You will need to configure your Gemini API key by setting it as an environment variable.

Run the application: Use Streamlit to run the app:

bash
Copy code
streamlit run app.py
Usage
Once the app is running locally, you can interact with different pages by selecting options in the sidebar. You can upload files, ask questions, and explore career pathways based on your selected field of study.

Pages
Home
Displays an overview of the platform and allows users to explore features such as custom study materials and quizzes. Downloadable guides and content tailored to specific fields are available.
Career Pathways
Users can explore various career options and the skills required for each field. This page is helpful for those looking to understand career growth and the educational steps required.
Ask Me About Your Slide
Upload your PDF, DOCX, or PPTX files, select specific pages, and ask questions about the content. The AI model processes the content and returns meaningful answers based on the file’s text.
History
A placeholder page to display user interaction history. This will show previously asked questions and interactions in future versions.
Features to be Implemented
Advanced Search: A feature to search through the uploaded documents for keywords or topics.
History Tracking: Keep track of previous document uploads and the questions asked.
Premium Features: Differentiate between free and premium user features, including access to advanced analytics and personalized learning insights.
Technologies Used
Python
Streamlit: For building the front-end user interface.
Gemini API: For natural language processing and generating answers based on user queries.
PDF, DOCX, PPTX Processing: Extracting text from various document formats to provide insights.
Contributing
Contributions are welcome! To contribute:

Fork the repository.
Create a new branch (git checkout -b feature/your-feature).
Commit your changes (git commit -m 'Add some feature').
Push to the branch (git push origin feature/your-feature).
Open a pull request.
Please ensure that your code follows the project’s coding guidelines and has relevant tests.

License
This project is licensed under the MIT License. See the LICENSE file for more details.
