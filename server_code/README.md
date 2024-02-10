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
Inference on a GGUF model file on disk 
```shell
python server_code/send_llm_query.py --question="How often should I change my chain?" --local_model
```
Should give a response like
```text
As a general guideline, you should replace your bike chain every 2,000 to 3,000 miles (3,200 to 4,800 kilometers) of use. However, this can vary depending on several factors such as riding conditions, maintenance habits, and the specific brand and type of chain you have. If you ride frequently in harsh weather conditions or on rough terrain, you may need to replace your chain more often. On the other hand, if you're a recreational rider who mostly rides on smooth roads and keeps up with regular cleaning and lubrication, your chain might last longer. It's always best to consult the manufacturer's recommendations for specific advice based on your particular setup. By replacing your chain at appropriate intervals, you can help ensure optimal performance, efficiency, and longevity of your bike drivetrain.
```
### Local server
Start a local server at http://localhost:1234
```shell
python server_code/llm_server.py
```
and send a query to the server
```shell
python server_code/send_llm_query.py --question="How often should I change my chain?" --local_server
```


# Deployment

## HuggingFace

