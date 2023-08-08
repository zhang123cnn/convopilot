name_to_model = {}

def get_llm_model(model_name):
    global name_to_model
    if model_name in name_to_model:
        return name_to_model[model_name]
    else:
        if model_name in ("gpt-4", "gpt-3.5"):
            from convopilot.gpt_api import GPTAPI
            register_llm_model("gpt-4", GPTAPI(model_name="gpt-4", budget=5))
            register_llm_model("gpt-3.5", GPTAPI(model_name="gpt-3.5-turbo", budget=5))
            return name_to_model[model_name]

    raise ValueError("Invalid llm model")

def register_llm_model(model_name, model):
    global name_to_model
    name_to_model[model_name] = model
