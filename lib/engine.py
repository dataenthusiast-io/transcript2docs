import yaml
from langchain.chains import LLMChain
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_text_splitters import TokenTextSplitter

# Loading config yaml for chains
transcript_config = "transcript.yaml"
docs_config = "docs.yaml"

# Setting chunk size
chunk_size = 1000

def load_chain_config(file_name):
    """
    Load LLM chain configuration from a YAML file.
    """
    file_path = f'lib/chains/{file_name}'
    with open(file_path, 'r', encoding='utf-8') as file:
        return yaml.safe_load(file)

def create_chain(chain_config):
    """
    Create an LLM chain based on the provided configuration.
    """
    config = load_chain_config(chain_config)
    llm_config = config['llm']
    llm = ChatOpenAI(model=llm_config['model'], temperature=llm_config['temperature'])
    prompt_template = PromptTemplate.from_template(template=config['prompt'])
    return LLMChain(llm=llm, prompt=prompt_template)

def transcript_processing(file, context, type):
    """
    Process the transcript file with given context and transcript type.
    """
    transcript_content = file.getvalue().decode('utf-8')
    transcript_chain = create_chain(transcript_config)
    chunk_overlap = int(chunk_size * 0.05)
    text_splitter = TokenTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    chunks = text_splitter.split_text(transcript_content)

    rewritten_transcript = []
    for chunk in chunks:
        response = transcript_chain.invoke({"context": context, "transcript": chunk, "transcript_type": type})
        rewritten_text = response["text"]
        rewritten_transcript.append(rewritten_text)

    return ' '.join(rewritten_transcript)

def docs_generation(transcript, structure, context, type):
    """
    Generate documentation from the transcript with given structure and context.
    """
    docs_chain = create_chain(docs_config)
    response = docs_chain.invoke({"structure": structure, "transcript": transcript, "context": context, "transcript_type": type})
    docs_text = response["text"]

    return docs_text
