import gradio as gr
from search_system import search_system

def search_courses(query):
    results = search_system.search(query)
    response = search_system.generate_response(query, results)
    
    output = f"AI Assistant: {response}\n\nTop 3 Relevant Courses:\n"
    for i, r in enumerate(results, 1):
        output += f"{i}. {r['course']['title']}\n   Score: {r['score']:.2f}\n   URL: {r['course']['url']}\n\n"
    
    return output

iface = gr.Interface(
    fn=search_courses,
    inputs=gr.Textbox(lines=2, placeholder="Enter your search query here..."),
    outputs="text",
    title="Analytics Vidhya Free Courses Smart Search",
    description="Search for relevant free courses on Analytics Vidhya using natural language queries."
)

iface.launch(share=True)
