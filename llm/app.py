import os

from flask import Flask, render_template, request
from langchain_community.llms import Ollama
from langchain_community import embeddings
from langchain_community.document_loaders import TextLoader
from langchain_chroma import Chroma
from langchain_text_splitters import MarkdownTextSplitter 
from langchain_community.embeddings import OllamaEmbeddings

ollama_url="http://ollama:11434"
llm = Ollama(base_url=ollama_url, model="phi3")
#print(llm.invoke("Why is the sky orange?"))

app = Flask(__name__)

# Vecorizing input.md
# loader = TextLoader("input.md")
# documents = loader.load()

# text_splitter = MarkdownTextSplitter()

# documents = text_splitter.split_documents(documents)


ollama_embed = OllamaEmbeddings(base_url=ollama_url, model="nomic-embed-text")
# db = Chroma.from_documents(documents, oembed, persist_directory="./chroma_db")

db = Chroma(persist_directory="./chroma_db", embedding_function=ollama_embed)

@app.route("/test")
def hello_world():
    joke = llm.invoke("Why is the sky orange?")
    return joke

@app.route("/embed")
def embed_test():
    query = "Tell me about the glossary"
    docs = db.similarity_search(query, k=3)
    return docs[0].page_content

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/', methods=['POST'])
def submit():
    input_text = request.form['input_text']
    response_text = llm.invoke(input_text)
    return render_template('index.html', response_text=response_text)

@app.route('/upload')
def upload():
    return render_template('upload.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return 'No file part'
    file = request.files['file']
    if file.filename == '':
        return 'No selected file'
    if file:
        filename = file.filename
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return 'File uploaded successfully'



if __name__ == '__main__':
    app.run(debug=True)