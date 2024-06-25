import yaml
import importlib
from langchain.chains import LLMChain
from langchain_core.prompts import PromptTemplate

def load_chain_config(file_name):
    """
    Load LLM chain configuration from a YAML file.
    """
    file_path = f'lib/config/chains/{file_name}'
    with open(file_path, 'r', encoding='utf-8') as file:
        return yaml.safe_load(file)

def load_provider_config(provider_name):
    """
    Load provider configuration from a YAML file.
    """
    file_path = f'lib/config/providers/{provider_name.lower()}.yaml'
    with open(file_path, 'r', encoding='utf-8') as file:
        return yaml.safe_load(file)

def create_llm(llm_config):
    """
    Create an LLM instance based on the provided configuration.
    """
    provider = llm_config['provider']
    model = llm_config['model']
    temperature = llm_config['temperature']

    provider_config = load_provider_config(provider)
    library_name = provider_config[provider]['library']
    component_name = provider_config[provider]['component']

    # Dynamically import the required library and component
    library = importlib.import_module(library_name)
    component = getattr(library, component_name)

    return component(model=model, temperature=temperature)

def create_chain(chain_config):
    """
    Create an LLM chain based on the provided configuration.
    """
    config = load_chain_config(chain_config)
    llm_config = config['llm']
    llm = create_llm(llm_config)
    prompt_template = PromptTemplate.from_template(template=config['prompt'])
    return LLMChain(llm=llm, prompt=prompt_template)