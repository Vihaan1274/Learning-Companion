import logging
import textwrap
import os

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler()]
)

def clean_text(text: str) -> str:
    """Normalize whitespace and strip empty lines."""
    return "\n".join(line.strip() for line in text.splitlines() if line.strip())

def format_chunks(chunks, max_chars=500):
    """Format chunks into a readable string with size control."""
    formatted = []
    for c in chunks:
        snippet = textwrap.shorten(c, width=max_chars, placeholder="...")
        formatted.append(snippet)
    return "\n---\n".join(formatted)

def save_uploaded_file(uploaded_file, save_dir="uploads"):
    """Save uploaded files to disk for processing."""
    os.makedirs(save_dir, exist_ok=True)
    path = os.path.join(save_dir, uploaded_file.name)
    with open(path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    return path
