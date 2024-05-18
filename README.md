# BBros LLM foundation app

## Installation

1. Run `docker-composer up`
2. In Docker Decktop go into the 'Olama-1' container and got to the "Exec" tabs, here you can run Ollama commands to get the necessary models.
3. In Ollama-1, run `ollama pull phi3`. Then run `ollama pull nomic-embed-text`.
4. Should be albe to go to 'http://localhost:5000/chat/123123123/load'


## Note

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