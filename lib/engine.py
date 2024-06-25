import hashlib
import logging
from .utils.files import read_txt, read_docx, read_vtt, split_text
from .utils.chains import create_chain
from .utils.cache import load_from_cache, save_to_cache

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Loading config yaml for chains
transcript_config = "transcript.yaml"
docs_config = "docs.yaml"

# Setting chunk size
chunk_size = 1000

def transcript_processing(file, context, type):
    """
    Process the transcript file with given context and transcript type.
    """
    try:
        if file.type == "text/plain":
            transcript_content = read_txt(file)
        elif file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
            transcript_content = read_docx(file)
        elif file.type == "text/vtt":
            transcript_content = read_vtt(file)
        else:
            raise ValueError("Unsupported file type")

        transcript_hash = hashlib.md5(transcript_content.encode()).hexdigest()

        # Check if the processed transcript is already cached
        cached_transcript = load_from_cache(transcript_hash)
        if cached_transcript:
            logging.info("Loading cached transcript.")
            return cached_transcript

        logging.info("No cached transcript found. Processing new transcript.")
        transcript_chain = create_chain(transcript_config)
        chunks = split_text(transcript_content, chunk_size)

        # Invoking chain using parallelized batch method
        response = transcript_chain.batch([{"context" : context,
                                            "transcript_type" : type,
                                            "transcript" : chunk} for chunk in chunks])
        
        # Extracting responses from LLM
        rewritten_transcript = [text["text"] for text in response]

        # Joining fragmented responses into joint transcript
        final_transcript = ' '.join(rewritten_transcript)

        # Cache the processed transcript
        save_to_cache(transcript_hash, final_transcript)

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