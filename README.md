# BBros LLM foundation app

## Installation steps

Steps for local development.


### 1. Start an Ollama server

Ash: The Ollama server was behaving strangely on my machine, so an alterative was to just run the native windows version of the Ollama server. The key thing is to get a server running on localhost.


#### Pull docker ollama

`docker pull ollama/ollama`


#### Run the Ollama container 

Passing the volume definition allows you to store the models outside of the container. This is useful if you want to delete the container (e.g. for an upgrade) and you want to keep your downloaded models.

`docker run -d -v ${PWD}/ollama:/root/.ollama -p 11434:11434 --name ollama ollama/ollama`

After this point you should be able to see the server on `localhost:11434`


#### Download the models 

Run this wherever Ollama is running, e.g. in the docker container to download the models. 

Note 'phi3' is a relatively small LLM model. The 'nomic-embed-text' is the embedding model.

`ollama pull phi3` 
`ollama pull nomic-embed-text` 



### 2. Start a Chroma server

#### Pull Docker image

`docker pull chromadb/chroma`


#### Run the Chroma DB server

Passing the volume definition allows you to store the vector store outside of the container. I.e. in ./chroma. If it's not there this will be created when the app runs.

`docker run -e "ALLOW_RESET=TRUE" -e "IS_PERSISTENT=TRUE" -d -v ${PWD}/chroma:/chroma/chroma -p 8000:8000 --name chroma chromadb/chroma`

You should be able to visit `http://localhost:8000/api/v1` to see that the server is running. 


### 3. Run the app 

Create a venv (virtual environment).

`python -m venv app-env`

Start the venv (windows powershell)

`.\app-env\Scripts\activate.ps1`

Install dependencies

`pip install -r app\requirements.txt`

Run the app

`flask --app app\app.py run --reload`


## Script notes - app/chromatest.py 

This script gives a simple demonstration of adding the embeddings of some texts samples into a vector store.




## General Notes

### build the image
docker build -f OllamaDockerfile -t ashley-g/llm-app .
docker build --no-cache -t ashley-g/llm-app .
docker build -t ashley-g/llm-app .

### list the available image
docker image ls

### run the image (by image ID)
docker run -p 5000:3000 c10e3c1b552a
docker run -p 5000:5000 -v ${PWD}:/app -w /app --name ash-llm-app 74356e2a7195
docker run -p 5000:5000 -v ${PWD}:/app -w /app --name ash-llm-app ashley-g/llm-app


### command line in container (or use docker desktop)
docker exec -it 737c5583a628 bash


### list python dependancies
pip freeze

### run the python app with reloading
flask --app app.py run --reload

### create and start the python venv (activate command is windows only)
python -m venv app-env
.\app-env\Scripts\activate.ps1


