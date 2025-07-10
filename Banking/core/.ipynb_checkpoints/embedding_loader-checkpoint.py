from core.config_loader import load_config

def load_embedding_model():
    config = load_config()
    provider = config["embedding"]["provider"]
    model_name = config["embedding"]["model"]

    if provider == "openai":
        from langchain_openai import OpenAIEmbeddings
        return OpenAIEmbeddings(
            model=model_name,
            openai_api_key=config["openai"]["api_key"],
            organization=config["openai"]["org_id"]
        )
