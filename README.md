Firstly you need to setup requirements (I think you can setup venv by yourself before that):
```bash
pip install -r requirements.txt
```
Then create a txt file with API-key for vk service named `vk_key.txt` and place it in folder with `run.sh`

Edit run script to point to your venv and script folder and run it with `./run.sh` or with `./run.sh > /dev/null 2>&1 &` in background
