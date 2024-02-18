Save API key securely
```shell
$ python
>>> import keyring, getpass
>>> keyring.set_password('openai', 'api_key', getpass.getpass())
```
Usage:
```python
import keyring
API_KEY = keyring.get_password(service_name='openai', username='api_key')
```
Test:
```shell
python poc/open-ai/call_agent.py --question="How often should I change my chain?"
```
should return
```text
Response: Change your bike chain approximately every 2,000 to 3,000 miles, depending on your riding conditions and maintenance routine. Regularly cleaning and lubricating can extend its life, whereas riding in harsh conditions might necessitate more frequent changes.
```

### Fine-tunning 
Convert expanded jsonl to compact jsonl
```shell
brew install jq
```
```shell
jq -c '.' < q_a.jsonl > q_a_compact.jsonl
```