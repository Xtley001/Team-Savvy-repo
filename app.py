import streamlit as st
import google.generativeai as genai
import os
import PyPDF2 as pdf
from docx import Document
from pptx import Presentation
from dotenv import load_dotenv
import json
import io

# Load environment variables
load_dotenv()

# Configure Gemini API
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Function to get response from Gemini API
def get_gemini_response(input_text):
    model = genai.GenerativeModel('gemini-pro')
    try:
        if not input_text.strip():
            st.error("Input text is empty. Cannot generate response.")
            return "{}"  # Return empty JSON

        response = model.generate_content(input_text)
        if response and response.text:
            return response.text
        else:
            st.error("Received an empty response from the model.")
            return "{}"  # Return empty JSON
    except Exception as e:
        st.error(f"Error while getting response from API: {str(e)}")
        return "{}"  # Return empty JSON

# Function to extract text from uploaded PDF file
def input_pdf_text(uploaded_file):
    reader = pdf.PdfReader(uploaded_file)
    text = []
    for page_num in range(len(reader.pages)):
        page = reader.pages[page_num]
        text.append(page.extract_text() or "")
    return text

# Function to extract text from uploaded Word document
def input_word_text(uploaded_file):
    doc = Document(uploaded_file)
    text = []
    for para in doc.paragraphs:
        text.append(para.text or "")
    return text

# Function to extract text from uploaded PPT file
def input_ppt_text(uploaded_file):
    presentation = Presentation(uploaded_file)
    text = []
    for slide in presentation.slides:
        for shape in slide.shapes:
            if hasattr(shape, "text"):
                text.append(shape.text or "")
    return text

# Function to generate DOCX file from content
def generate_docx(generated_content):
    doc = Document()
    doc.add_heading('Generated Content', level=1)

    for content in generated_content:
        doc.add_heading(f'Page {content["Page"]}', level=2)
        doc.add_paragraph(f"**Explanation:**\n{content.get('Explanation', 'No explanation available.')}")
        doc.add_paragraph(f"**Example:**\n{content.get('Example', 'No example available.')}")
        doc.add_paragraph(f"**Test:**\n{content.get('Test', 'No test available.')}")
        doc.add_paragraph(f"**Solution:**\n{content.get('Solution', 'No solution available.')}")
        doc.add_paragraph()  # Add a blank line for spacing

    byte_io = io.BytesIO()
    doc.save(byte_io)
    byte_io.seek(0)
    return byte_io

# Define input prompts for generating content
input_prompts = {
    "Architecture & Design": """
    You are an expert in Architecture & Design. Your task is to provide an in-depth explanation
    of the page content, drawing on both historical and modern architectural principles, design 
    theory, and real-world applications. When explaining architectural principles, reference key 
    movements such as Gothic, Baroque, Modernism, and Postmodernism, as well as the role of cultural 
    and technological advancements in shaping these movements. Include detailed analysis on how 
    materials like wood, steel, concrete, and glass have influenced architectural design over time. 
    Discuss the increasing focus on sustainability and how it affects design choices today, including 
    the use of renewable resources, green building technologies, and sustainable urban planning. 

    Beyond the technical aspects of architecture, discuss the balance between form and function in 
    design, considering the aesthetic and practical demands placed on architects. Explore the 
    influence of social, cultural, and political factors on architectural styles, from the rise of 
    monumental buildings in ancient civilizations to the minimalist and eco-friendly trends of 
    today. How does architecture respond to the needs of the society it serves? How do different 
    environments—urban vs rural, public vs private—shape architectural solutions? 

    In addition to theory, provide an example of a modern architectural project that embodies these 
    principles. Discuss in detail how this project balances aesthetics with functionality, how it 
    incorporates sustainable materials, and how it adapts to its cultural and environmental context. 
    You could consider projects like the Burj Khalifa, The Gherkin, or any other globally recognized 
    structures. 

    After providing this explanation and example, create a mini-test designed to assess the reader’s 
    understanding of the fundamental concepts of design and architecture. Include multiple choice 
    questions, short-answer questions, and problems that require the application of theoretical 
    knowledge to real-world scenarios. Ensure the test comprehensively covers the discussed 
    principles, and provide detailed solutions for each question. 

    Page Content: {page_content}

    I want the response in the following structured format:
    {{"Explanation": "", "Example": "", "Test": "", "Solution": ""}}
    """,
    "Arts": """
    You are an expert in Arts. Your task is to explain the content on the given page in detail, 
    addressing key concepts and theories from various art movements such as Renaissance, Romanticism, 
    Impressionism, Expressionism, and Contemporary Art. Discuss the evolution of art through history, 
    from classical art forms to modern digital mediums, while considering how different cultures and 
    societies have influenced artistic expression. Your explanation should include a detailed 
    analysis of various art techniques (such as painting, sculpture, digital art) and how these 
    techniques contribute to the overall impact of a work of art. 

    Also, explore the relationship between art and its audience. How does art communicate emotion, 
    provoke thought, or reflect societal values? How do different mediums—from traditional forms 
    like painting to newer forms like performance art—engage the viewer in different ways? 

    Once the explanation is complete, provide a relevant example of an artwork or artist that 
    embodies the discussed principles. You may refer to works by artists like Leonardo da Vinci, 
    Vincent van Gogh, Pablo Picasso, or contemporary digital artists. Discuss how this artwork 
    fits within its historical and cultural context, and what makes it significant in the art world. 

    Finally, create a mini-test to assess the reader’s understanding of the artistic concepts covered. 
    Include questions that evaluate both theoretical knowledge (e.g., identifying characteristics of 
    an art movement) and practical application (e.g., analyzing a given artwork). Be sure to provide 
    comprehensive solutions for each question, explaining the reasoning behind the correct answers. 

    Page Content: {page_content}

    I want the response in the following structured format:
    {{"Explanation": "", "Example": "", "Test": "", "Solution": ""}}
    """,
    "Business & Economics": """
    You are an expert in Business & Economics. Your task is to provide an in-depth explanation of 
    the given page content, drawing upon economic theories and business practices. Discuss key 
    economic concepts such as supply and demand, market structures, and fiscal and monetary policy. 
    Explain how these concepts affect businesses, economies, and the global market. Provide insights 
    into how different economic systems (capitalism, socialism, mixed economies) influence the 
    organization and operation of businesses. 

    Furthermore, analyze modern business strategies, including topics such as organizational behavior, 
    management practices, marketing, and financial management. Discuss the impact of technological 
    advancements, globalization, and social responsibility on modern businesses. Provide detailed 
    examples of companies or business practices that have successfully navigated these modern 
    challenges. 

    Your explanation should also include real-world examples of economic phenomena or business case 
    studies that illustrate the principles discussed. For example, consider examining how businesses 
    like Amazon, Tesla, or Google operate in competitive markets, or how economic events such as the 
    2008 financial crisis have shaped modern business practices. 

    After providing a thorough explanation and example, create a mini-test to assess the reader’s 
    understanding. Include questions that cover fundamental economic concepts, business management 
    strategies, and case-based analysis. Provide detailed solutions for each question, ensuring that 
    the reader not only knows the correct answer but understands the reasoning behind it. 

    Page Content: {page_content}

    I want the response in the following structured format:
    {{"Explanation": "", "Example": "", "Test": "", "Solution": ""}}
    """,
    "Education": """
    You are an expert in Education. Your task is to provide an in-depth explanation of the page 
    content, focusing on educational theories, practices, and policies. Discuss major educational 
    theories such as constructivism, behaviorism, and experiential learning. Explain how these 
    theories are applied in modern educational settings, from early childhood education to higher 
    education and lifelong learning. 

    Include a detailed analysis of teaching methodologies, such as differentiated instruction, 
    inquiry-based learning, and technology-enhanced learning. Discuss how these methodologies are 
    used to engage students with diverse learning needs and how they contribute to the development 
    of critical thinking, problem-solving, and collaboration skills. Explore how education systems 
    are adapting to the challenges of the 21st century, such as remote learning, inclusion, and the 
    integration of technology in the classroom. 

    After the explanation, provide an example of an educational initiative or policy that reflects 
    these principles. You might discuss the implementation of STEM education, the role of project-based 
    learning, or international education models such as Finland's or Singapore's systems. 

    Finally, create a mini-test designed to assess the reader’s understanding of educational theories 
    and practices. Include multiple choice questions, short-answer questions, and scenarios where the 
    reader must apply educational principles to solve problems. Provide comprehensive solutions with 
    detailed explanations for each question. 

    Page Content: {page_content}

    I want the response in the following structured format:
    {{"Explanation": "", "Example": "", "Test": "", "Solution": ""}}
    """,
    "Engineering & Technology": """
    You are an expert in Engineering & Technology. Your task is to provide an in-depth explanation 
    of the page content, focusing on key engineering principles and technological advancements. 
    Discuss major branches of engineering such as civil, mechanical, electrical, and software 
    engineering, explaining the core concepts and problem-solving techniques unique to each field. 

    Provide an analysis of how engineering has evolved over time, from the Industrial Revolution to 
    the modern era of automation and artificial intelligence. Discuss how engineers apply mathematical 
    and scientific principles to design solutions that meet the needs of society, considering factors 
    like safety, cost-effectiveness, and environmental impact. Explain how technological innovations 
    such as robotics, nanotechnology, and renewable energy sources are shaping the future of engineering 
    and transforming industries. 

    Include a real-world example of a technological innovation or engineering project that demonstrates 
    these principles. For instance, you might discuss the development of electric vehicles, smart cities, 
    or the use of AI in healthcare. Provide a detailed breakdown of the engineering challenges involved 
    in these projects and how they were addressed through innovative solutions. 

    After the explanation and example, create a mini-test designed to assess the reader’s understanding 
    of engineering principles and technological advancements. Include a variety of question types, such 
    as multiple choice, short-answer, and problem-solving questions that require the reader to apply 
    their knowledge to practical situations. Provide detailed solutions for each question, explaining 
    the reasoning behind the correct answers. 

    Page Content: {page_content}

    I want the response in the following structured format:
    {{"Explanation": "", "Example": "", "Test": "", "Solution": ""}}
    """,
    "Environmental Studies": """
    You are an expert in Environmental Studies. Your task is to provide an in-depth explanation of 
    the page content, drawing on ecological principles, environmental policies, and sustainable 
    practices. Discuss key concepts such as biodiversity, ecosystems, climate change, and conservation 
    efforts. Provide an analysis of how human activities—such as deforestation, pollution, and urbanization— 
    have impacted the environment and contributed to global environmental issues. 

    Explore the role of international organizations and environmental policies, such as the Paris 
    Agreement, in combating climate change and promoting sustainability. Discuss the importance of 
    environmental stewardship and the role of individuals, communities, and industries in reducing 
    their ecological footprint. Include a detailed analysis of renewable energy technologies, such as 
    solar and wind power, and how they are being integrated into modern energy systems to mitigate 
    environmental degradation. 

    After the explanation, provide an example of an environmental initiative or project that reflects 
    the discussed principles. For instance, you could discuss successful reforestation projects, the 
    implementation of green building standards, or the development of circular economy practices. 
    Provide a detailed analysis of how these initiatives contribute to environmental sustainability 
    and their long-term impact on ecosystems and human well-being. 

    Finally, create a mini-test designed to assess the reader’s understanding of environmental principles 
    and sustainable practices. Include multiple choice questions, short-answer questions, and case studies 
    where the reader must apply their knowledge to solve environmental challenges. Provide comprehensive 
    solutions with detailed explanations for each question. 

    Page Content: {page_content}

    I want the response in the following structured format:
    {{"Explanation": "", "Example": "", "Test": "", "Solution": ""}}
    """,
    "Humanities": """
    You are an expert in Humanities. Your task is to provide an in-depth explanation of the page content, 
    covering key themes in fields such as history, literature, philosophy, and cultural studies. Discuss 
    the historical context of significant cultural and intellectual movements, from the Enlightenment to 
    postmodernism. Explore how these movements have shaped societal values, ethical perspectives, and 
    artistic expressions throughout history. 

    Provide an analysis of the influence of literature, art, and philosophy on contemporary society. 
    Discuss how authors, artists, and thinkers such as William Shakespeare, Virginia Woolf, or Friedrich 
    Nietzsche have contributed to cultural and intellectual discourse. Examine the role of critical theory, 
    postcolonialism, and gender studies in modern humanities scholarship. 

    After the explanation, provide a relevant example from history, literature, or philosophy that embodies 
    the principles discussed. This could be a specific text, such as "The Iliad" or "1984," or a cultural 
    event, such as the French Revolution or the Harlem Renaissance. Provide a detailed analysis of how this 
    example fits within its broader historical and cultural context. 

    Finally, create a mini-test designed to assess the reader’s understanding of humanities concepts. 
    Include multiple choice questions, short-answer questions, and essay prompts where the reader must apply 
    their understanding of historical or philosophical principles to analyze a text or event. Provide 
    comprehensive solutions and explanations for each question. 

    Page Content: {page_content}

    I want the response in the following structured format:
    {{"Explanation": "", "Example": "", "Test": "", "Solution": ""}}
    """,
    "Law": """
    You are an expert in Law. Your task is to provide an in-depth explanation of the page content, covering 
    key legal principles, case law, and statutory analysis. Discuss foundational legal concepts such as 
    common law, civil law systems, and the rule of law. Explain the roles of different branches of 
    government and how they interact within the legal system. 

    Provide an analysis of major areas of law, such as contract law, tort law, criminal law, and constitutional 
    law. Discuss how legal principles are applied in real-world scenarios and how legal precedents influence 
    judicial decisions. Consider recent developments in law, such as issues of privacy, intellectual property, 
    and international law, and how they are shaping legal discourse today. 

    After the explanation, provide a relevant example from case law or legal practice that demonstrates the 
    application of these principles. You might consider discussing landmark cases such as Brown v. Board of 
    Education, Roe v. Wade, or more recent decisions that reflect evolving legal challenges. Provide a 
    detailed analysis of how the court reached its decision and the broader legal and societal implications 
    of the ruling. 

    Finally, create a mini-test designed to assess the reader’s understanding of legal concepts. Include 
    multiple choice questions, short-answer questions, and case-based problems that require the reader to 
    apply legal principles to hypothetical situations. Provide comprehensive solutions with detailed 
    explanations for each question. 

    Page Content: {page_content}

    I want the response in the following structured format:
    {{"Explanation": "", "Example": "", "Test": "", "Solution": ""}}
    """,
    "Medicine & Health Sciences": """
    You are an expert in Medicine & Health Sciences. Your task is to provide an in-depth explanation of the 
    page content, covering key medical concepts, clinical practices, and recent advancements in healthcare. 
    Discuss major areas of medicine such as anatomy, physiology, pharmacology, and medical ethics. Explain 
    how these fields contribute to the diagnosis, treatment, and prevention of diseases. 

    Provide an analysis of how medical knowledge has evolved over time, from early practices such as herbal 
    medicine and bloodletting to modern techniques like gene therapy and robotic surgery. Discuss the role of 
    healthcare professionals in delivering patient care, and how medical technologies like telemedicine and 
    electronic health records are transforming the field. 

    Include a relevant example of a medical case or recent healthcare innovation that demonstrates the 
    principles discussed. For instance, you might consider discussing the development of COVID-19 vaccines, 
    breakthroughs in cancer treatment, or the implementation of artificial intelligence in diagnostics. 

    After providing the explanation and example, create a mini-test designed to assess the reader’s understanding 
    of medical principles. Include multiple choice questions, short-answer questions, and clinical scenarios 
    where the reader must apply their knowledge to diagnose or treat a hypothetical patient. Provide comprehensive 
    solutions with detailed explanations for each question. 

    Page Content: {page_content}

    I want the response in the following structured format:
    {{"Explanation": "", "Example": "", "Test": "", "Solution": ""}}
    """,
    "Natural Sciences": """
    You are an expert in Natural Sciences. Your task is to provide an in-depth explanation of the page content, 
    covering topics such as biology, chemistry, physics, and earth sciences. Discuss key scientific principles, 
    such as the laws of thermodynamics, chemical bonding, evolutionary theory, and ecological systems. 

    Explain how scientific discoveries have advanced over time, from early experiments with electricity and 
    magnetism to the development of quantum mechanics and biotechnology. Provide an analysis of how natural 
    sciences interact with technology and other fields, such as engineering and medicine, to solve global 
    challenges like climate change, disease, and resource scarcity. 

    After providing this explanation, offer a detailed example of a scientific experiment, discovery, or 
    technological innovation that demonstrates the principles discussed. You could reference significant 
    experiments like the discovery of DNA's double helix structure or technological advancements like the 
    Large Hadron Collider. Discuss the implications of these discoveries on our understanding of the natural 
    world and how they have influenced further scientific research. 

    Finally, create a mini-test designed to assess the reader’s understanding of natural science principles. 
    Include multiple choice questions, short-answer questions, and problems that require the reader to apply 
    their knowledge to real-world scenarios, such as calculating the force in a physics problem or analyzing 
    a chemical reaction. Provide detailed solutions with explanations for each question. 

    Page Content: {page_content}

    I want the response in the following structured format:
    {{"Explanation": "", "Example": "", "Test": "", "Solution": ""}}
    """,
    "Social Sciences": """
    You are an expert in Social Sciences. Your task is to provide an in-depth explanation of the page content, 
    covering key themes in fields such as sociology, psychology, anthropology, and political science. Discuss 
    important theories, such as social contract theory, cognitive behavioral theory, and cultural relativism. 
    Explain how these theories are applied to understand social behavior, institutions, and cultural dynamics. 

    Provide an analysis of how social sciences have evolved over time, from early works like those of Karl Marx 
    and Max Weber to contemporary research on topics like globalization, identity politics, and social media's 
    impact on human interaction. Explore how social scientists use both qualitative and quantitative methods 
    to investigate social phenomena and the implications of their findings on public policy and social reform. 

    After the explanation, provide a relevant example from sociology, psychology, or political science that 
    illustrates the discussed principles. You could consider a case study on social movements, political behavior, 
    or psychological experiments like the Stanford prison experiment or Milgram's obedience study. Provide a 
    detailed analysis of the case study and its broader implications for understanding human society. 

    Finally, create a mini-test designed to assess the reader’s understanding of social science concepts. Include 
    multiple choice questions, short-answer questions, and case-based problems that require the reader to apply 
    social science theories to real-world situations. Provide comprehensive solutions with detailed explanations 
    for each question. 

    Page Content: {page_content}

    I want the response in the following structured format:
    {{"Explanation": "", "Example": "", "Test": "", "Solution": ""}}
    """,
    "Mathematics & Computer Science": """
    You are an expert in Mathematics & Computer Science. Your task is to provide an in-depth explanation of the 
    page content, covering key topics such as algorithms, data structures, calculus, linear algebra, and discrete 
    mathematics. Discuss how mathematical principles are applied in computer science to solve complex problems, 
    from designing efficient algorithms to modeling real-world systems. 

    Provide an analysis of how both fields have evolved over time, from the early days of computing and the 
    development of Boolean algebra to modern advancements in artificial intelligence and quantum computing. 
    Discuss how mathematical models and computational techniques are used in various applications, such as 
    cryptography, machine learning, and network security. 

    After the explanation, provide a relevant example of a mathematical concept or computer science application 
    that demonstrates the principles discussed. For example, you could explain the application of graph theory 
    in social network analysis or the use of differential equations in modeling biological systems. Provide a 
    detailed explanation of how this example is used in real-world scenarios and its broader impact on technology 
    and society. 

    Finally, create a mini-test designed to assess the reader’s understanding of mathematical and computational 
    principles. Include multiple choice questions, short-answer questions, and problems that require the reader 
    to apply mathematical concepts to real-world computing challenges. Provide comprehensive solutions with 
    detailed explanations for each question. 

    Page Content: {page_content}

    I want the response in the following structured format:
    {{"Explanation": "", "Example": "", "Test": "", "Solution": ""}}
    """,
    "Interdisciplinary Studies": """
    You are an expert in Interdisciplinary Studies. Your task is to provide an in-depth explanation of the page 
    content, covering how different academic disciplines intersect to address complex real-world problems. Discuss 
    the importance of drawing on knowledge from diverse fields, such as economics, engineering, environmental science, 
    and social sciences, to develop holistic solutions to issues like climate change, public health, and global 
    development. 

    Provide an analysis of how interdisciplinary research is conducted, including the methodologies used to integrate 
    knowledge from multiple disciplines. Explain how collaboration between experts in different fields can lead to 
    innovative solutions and breakthroughs that would not be possible within the boundaries of a single discipline. 

    After the explanation, provide a relevant example of an interdisciplinary project or initiative that demonstrates 
    the principles discussed. You might consider discussing a large-scale global challenge, such as the COVID-19 pandemic, 
    and how professionals from fields like medicine, economics, and public policy have worked together to address its 
    various dimensions. Provide a detailed analysis of how this interdisciplinary collaboration led to more effective 
    solutions and outcomes. 

    Finally, create a mini-test designed to assess the reader’s understanding of interdisciplinary studies. Include 
    multiple choice questions, short-answer questions, and case-based problems that require the reader to apply 
    interdisciplinary principles to solve complex issues. Provide comprehensive solutions with detailed explanations 
    for each question. 

    Page Content: {page_content}

    I want the response in the following structured format:
    {{"Explanation": "", "Example": "", "Test": "", "Solution": ""}}
    """
}

# Streamlit App
st.set_page_config(page_title="Interactify")
page = st.sidebar.radio("Select Page", ["Home", "Ask Me About Your Slide", "History"])

if page == "Home":
    st.title("Interactify")

    # Dropdown for field selection
    field = st.selectbox("Select Field", [
        "Architecture & Design",
        "Arts",
        "Business & Economics",
        "Education",
        "Engineering & Technology",
        "Environmental Studies",
        "Humanities",
        "Law",
        "Medicine & Health Sciences",
        "Natural Sciences",
        "Social Sciences",
        "Mathematics & Computer Science",
        "Interdisciplinary Studies"
    ])

    # File uploader for slides (PDF, Word, PPT, or text) input
    uploaded_file = st.file_uploader("Upload Your Document (PDF, DOCX, PPTX, TXT)...", type=["pdf", "docx", "pptx", "txt"])

    # Text input for page range
    page_range_input = st.text_input("Any specific page ranges (e.g., 4-7):")

    # Initialize session state for history
    if 'history' not in st.session_state:
        st.session_state.history = []

    # Submit button for processing the document
    submit = st.button("Submit")

    if submit:
        if uploaded_file:
            try:
                # Extract text from the uploaded file
                if uploaded_file.type == "application/pdf":
                    document_text = input_pdf_text(uploaded_file)
                elif uploaded_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
                    document_text = input_word_text(uploaded_file)
                elif uploaded_file.type == "application/vnd.openxmlformats-officedocument.presentationml.presentation":
                    document_text = input_ppt_text(uploaded_file)
                elif uploaded_file.type == "text/plain":
                    document_text = uploaded_file.read().decode("utf-8").split('\n')
                else:
                    st.error("Unsupported file type!")
                    st.stop()

                # Process page ranges
                page_ranges = []
                if page_range_input:
                    try:
                        ranges = page_range_input.split(',')
                        for r in ranges:
                            start, end = map(int, r.split('-'))
                            page_ranges.append(range(start - 1, end))
                    except ValueError:
                        st.error("Invalid page range format! Use the format 'start-end'.")
                        st.stop()
                else:
                    page_ranges = [range(len(document_text))]

                # Process selected pages
                generated_content = []

                for range_set in page_ranges:
                    for page_num in range_set:
                        if page_num < len(document_text):
                            st.markdown(f"#### Page {page_num + 1}")
                            page_content = document_text[page_num]

                            # Prepare prompt with extracted page text
                            input_prompt = input_prompts.get(field, "")
                            if not input_prompt:
                                st.error(f"No prompt template available for field: {field}")
                                continue
                            input_prompt_filled = input_prompt.format(page_content=page_content)

                            # Get response from Gemini API
                            response = get_gemini_response(input_prompt_filled)

                            try:
                                # Parse response
                                response_json = json.loads(response)

                                # Display and collect Explanation, Example, Test, Solution 
                                explanation = response_json.get("Explanation", "No explanation available.")
                                example = response_json.get("Example", "No example available.")
                                test = response_json.get("Test", "No test available.")
                                solution = response_json.get("Solution", "No test solution available.")

                                st.markdown("**Explanation:**")
                                st.write(explanation)

                                st.markdown("**Example:**")
                                st.write(example)

                                st.markdown("**Test:**")
                                st.write(test)

                                st.markdown("**Solution:**")
                                st.write(solution)

                                # Collect generated content in JSON format
                                page_content_json = {
                                    "Page": page_num + 1,
                                    "Explanation": explanation,
                                    "Example": example,
                                    "Test": test,
                                    "Solution": solution,
                                }
                                generated_content.append(page_content_json)
                            except json.JSONDecodeError:
                                st.error("Failed to decode JSON response from the model.")

                        else:
                            st.warning(f"Page {page_num + 1} is out of range.")

                # Add generated content to history
                st.session_state.history.append(generated_content)

                # Provide option to copy generated content
                
                generated_content_str = json.dumps(generated_content, indent=2)
                st.code(generated_content_str)
                if st.button("Copy to Clipboard"):
                    st.experimental_set_query_params(text=generated_content_str)
                    st.success("Content copied to clipboard!")

                # Provide download option for DOCX
                if generated_content:
                    docx_file = generate_docx(generated_content)
                    st.download_button(
                        label="Download Generated Content as DOCX",
                        data=docx_file,
                        file_name='generated_content.docx',
                        mime='application/vnd.openxmlformats-officedocument.wordprocessingml.document'
                    )
            except Exception as e:
                st.error(f"An error occurred while processing the file: {str(e)}")

elif page == "Ask Me About Your Slide":
    st.title("Ask Me About Your Slide")

    # Text input for asking questions
    question = st.text_input("Ask a question about your slide:")

    if question:
        # Get response from Gemini API for the question
        response = get_gemini_response(question)
        st.markdown("### Answer:")
        st.write(response)

elif page == "History":
    st.title("History")

    # Display history
    if 'history' in st.session_state:
        for index, entry in enumerate(st.session_state.history):
            st.subheader(f"History Entry {index + 1}")
            for content in entry:
                st.markdown(f"**Page {content['Page']}**")
                st.markdown(f"**Explanation:**\n{content['Explanation']}")
                st.markdown(f"**Example:**\n{content['Example']}")
                st.markdown(f"**Test:**\n{content['Test']}")
                st.markdown(f"**Solution:**\n{content['Solution']}")
                st.write("---")
    else:
        st.write("No history available.")
        
st.markdown("""
<style>
[data-testid="stAppViewContainer"] {
    background-image: url("https://images.unsplash.com/photo-1698945746290-a9d1cc575e77");
    background-size: cover;
    background-repeat: no-repeat;
    background-position: center;
}
</style>
""", unsafe_allow_html=True)
