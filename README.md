# Intro
I'll just add in a disclaimer $-$ this thing is assumed to work only on one GPU. I haven't worked around for using multiple GPUs. That part is iffy to handle. I'll do that some other time.

# How-To

You'll first have to install the dependencies.
```bash
pip install -r requirements.txt
```
Be sure to execute this in a virtual environment.

**main.py** contains most of the running code.
If you're wanting to run it for yourself, be sure to type
```bash
python main.py --help
```
You will have a few arguments to play around with:
- gpu $-$ Which GPU will be used to host the engine (defaults to 0).
- run_type $-$ Whether to run the LLM locally or to host an API for the LLM (defaults to 'local').
- port $-$ Self-explanatory, what port to host the API on (defaults to 50000).

**sample_console_frontend.py** contains rudimentary code on how to get streaming as well as non-streaming responses.

**model.py** and **llm_chat_history.py** are disjointed classes and can be separately loaded into your project. I've made sure to add in docstrings and comments wherever helpful.

It's recommended that you send your prompt to the *generate* URL in a list-of-dictionaries format (one which can be applied to the tokenizer's chat template without issues).

