from gpt_api import gptapi
gptapi.setup_key(openai_key_path='/Users/xiaomeng/.openai/api_secret_key')
gptapi.set_budget(5)


def get_llm_model(model_name):
    if model_name == "gpt-4":
        return gptapi

    raise ValueError("Invalid llm model")