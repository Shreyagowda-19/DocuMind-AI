from langchain_text_splitters import RecursiveCharacterTextSplitter

def split_text(text):

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=100,
        length_function=len,
        is_separator_regex=False,
    )

    chunks = splitter.split_text(text)

    return chunks