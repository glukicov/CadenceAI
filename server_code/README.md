# Backend development 

## Model
`Zephyr 7B β` (Llama-type) https://huggingface.co/HuggingFaceH4/zephyr-7b-beta
- fine-tuned from `Mistral 7B`
`llama-2–7b-chat` https://huggingface.co/TheBloke/Llama-2-7B-Chat-GGUF
- GPT-like
- designed to function as an assistant
- 4 bit quantisation available (~4 GB RAM at inference) 
- "acceptable" quality for a PoC

## Local testing 
Install dependencies
```shell
poetry install && poetry shell
```
Check `config.yaml` for model configuration, download models and create some test images in `artifacts/` then:

Inference on a GGUF model file on disk 
```shell
python server_code/send_llm_query.py --question="How often should I change my chain?" --local_model
```
Should give a response like
```text
As a general guideline, you should replace your bike chain every 2,000 to 3,000 miles (3,200 to 4,800 kilometers) of use. However, this can vary depending on several factors such as riding conditions, maintenance habits, and the specific brand and type of chain you have. If you ride frequently in harsh weather conditions or on rough terrain, you may need to replace your chain more often. On the other hand, if you're a recreational rider who mostly rides on smooth roads and keeps up with regular cleaning and lubrication, your chain might last longer. It's always best to consult the manufacturer's recommendations for specific advice based on your particular setup. By replacing your chain at appropriate intervals, you can help ensure optimal performance, efficiency, and longevity of your bike drivetrain.
```
### Local server
Start a local server at http://localhost:8080
```shell
poetry run uvicorn server_code.llm_server:api --reload --host 0.0.0.0 --port 8080
```
and send a query to the server
```shell
python server_code/send_llm_query.py --question="How often should I change my chain?" --local_server
```

### Remote server
Build and start a container 
```shell
APP_NAME="CadenceAI" PORT="8080" docker-compose up --build api
```
or 
```shell
docker build -t cadenceai-api . &&
docker run -p 127.0.0.1:8080:8080/tcp cadenceai-api
(CB cmd: `gcloud builds submit --tag europe-west2-docker.pkg.dev/calm-catfish-302511/cadence-ai/cadence-ai:latest`)
```
and send a query to the locally running server's container for health
```shell
curl -X 'GET' \                                                                                                          INT ✘  3.10.12  
  'http://127.0.0.1:8080/health' \
  -H 'accept: application/json'
```
or model endpoint
```shell
python server_code/send_llm_query.py --question="How often should I change my chain?"
```
Tag and push to AWS ECR
```shell
docker tag cadenceai-api:latest 851725196496.dkr.ecr.eu-west-2.amazonaws.com/cadence-ai:latest &&
docker push 851725196496.dkr.ecr.eu-west-2.amazonaws.com/cadence-ai:latest
````
or GCP Cloud Run, 
```shell
docker tag cadenceai-api europe-west2-docker.pkg.dev/calm-catfish-302511/cadence-ai/cadence-ai:latest &&
docker push europe-west2-docker.pkg.dev/calm-catfish-302511/cadence-ai/cadence-ai:latest
```

and deploy the container to App Runner.

### Vision model in GCP
```shell
python server_code/send_vision_query.py
```
Should give a response like
```text
This is a spacer for a bicycle disc brake caliper.
```

# Deployment


