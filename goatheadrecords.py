import openai
import gradio as gr
import requests
from bs4 import BeautifulSoup

openai.api_key = "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"

# Scrape artist names from website
url = "https://www.goatheadrecords.com/"
response = requests.get(url)
soup = BeautifulSoup(response.content, "html.parser")
artist_names = [artist.text.strip() for artist in soup.find_all("h2", class_="heading")]
artist_names += ["Sarah Azhari", "Beth Bella", "Morrison Machiavelli", "Y.Rome"]

messages = [
    {"role": "system", "content": "Hi there! I am an AI assistant from Goathead Records."},
]

def chatbot(input):
    if input:
        messages.append({"role": "user", "content": input})
        try:
            if "owner" in input.lower():
                reply = "The owner of Goathead Records is Frank Carrozzo. You can find more information about him on https://www.crunchbase.com/person/frank-carrozzo"
            elif "artists" in input.lower():
                reply = "The artists signed with Goathead Records are: " + ", ".join(artist_names)
            else:
                chat = openai.Completion.create(
                    engine="text-davinci-002",
                    prompt="\n".join([msg["content"] for msg in messages]),
                    max_tokens=1024,
                    n=1,
                    stop=None,
                    temperature=0.7,
                )
                reply = chat.choices[0].text
        except Exception as e:
            print(f"Error: {e}")
            reply = "Sorry, I'm having trouble processing your request. Please try again later."
        messages.append({"role": "assistant", "content": reply})
        return reply

inputs = gr.inputs.Textbox(lines=7, label="Chat with AI")
outputs = gr.outputs.Textbox(label="Reply")

gr.Interface(fn=chatbot, inputs=inputs, outputs=outputs, title="Goathead Records AI Chatbot",
             description="Ask me anything you want!",
             layout="vertical", font_family="Helvetica Neue", font_size="18px").launch(share=True)




