import os
import tempfile

from markitdown import MarkItDown
from support.logger_manager import logger


def save_output(content):
    with open("output/user_curriculum.md", "w", encoding="utf-8") as f:
        f.write(content)
    logger.debug("Markdown written to user_curriculum.md")


def process_file(file):
    filename = file.name
    ext = os.path.splitext(filename)[1].lower()

    if ext in ['.txt', '.md']:
        try:
            content = file.read().decode('utf-8')
            logger.debug(f"Read text content from {filename}")
            save_output(content)
            return content
        except Exception as e:
            logger.error(f"Error reading text file: {str(e)}")
            return None

    elif ext in ['.pdf', '.docx']:
        with tempfile.NamedTemporaryFile(delete=False, suffix=ext) as tmp:
            tmp.write(file.read())
            tmp_path = tmp.name
            logger.debug(f"Temporary file created at: {tmp_path}")

        try:
            md = MarkItDown(enable_plugins=False)  # Set to True to enable plugins
            result = md.convert(tmp_path)
            markdown = result.text_content
            save_output(markdown)
            return markdown
        except Exception as e:
            logger.error(f"Error converting file: {str(e)}")
            return None
