# lib/engine.py
import yaml
import logging
import hashlib
import os
import importlib

from langchain.chains import LLMChain
from langchain_core.prompts import PromptTemplate
from langchain_text_splitters import TokenTextSplitter

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Loading config yaml for chains
transcript_config = "transcript.yaml"
docs_config = "docs.yaml"

# Setting chunk size
chunk_size = 1000

# Ensure cache directory exists
cache_dir = 'lib/cache'
if not os.path.exists(cache_dir):
    os.makedirs(cache_dir)

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

def transcript_processing(file, context, type):
    """
    Process the transcript file with given context and transcript type.
    """
    try:
        transcript_content = file.getvalue().decode('utf-8')
        transcript_hash = hashlib.md5(transcript_content.encode()).hexdigest()
        cache_file = f'{cache_dir}/{transcript_hash}.txt'

        # Check if the processed transcript is already cached
        try:
            with open(cache_file, 'r', encoding='utf-8') as cache:
                logging.info("Loading cached transcript.")
                return cache.read()
        except FileNotFoundError:
            logging.info("No cached transcript found. Processing new transcript.")

        transcript_chain = create_chain(transcript_config)
        chunk_overlap = int(chunk_size * 0.05)
        text_splitter = TokenTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
        chunks = text_splitter.split_text(transcript_content)

        rewritten_transcript = []
        for chunk in chunks:
            response = transcript_chain.invoke({"context": context, "transcript": chunk, "transcript_type": type})
            rewritten_text = response["text"]
            rewritten_transcript.append(rewritten_text)

        final_transcript = ' '.join(rewritten_transcript)

        # Cache the processed transcript
        with open(cache_file, 'w', encoding='utf-8') as cache:
            cache.write(final_transcript)

        return final_transcript
    except Exception as e:
        logging.error(f"Error in transcript processing: {e}")
        raise

def docs_generation(transcript, structure, context, type):
    """
    Generate documentation from the transcript with given structure and context.
    """
    try:
        docs_chain = create_chain(docs_config)
        response = docs_chain.invoke({"structure": structure, "transcript": transcript, "context": context, "transcript_type": type})
        docs_text = response["text"]

        return docs_text
    except Exception as e:
        logging.error(f"Error in docs generation: {e}")
        raise