class Chunker:
    def __init__(self,chunk_size, overlap):
        self.token_chunk = TokenBasedChunker(chunk_size, overlap)
        self.fixed_length_chunk = FixedLengthChunker(chunk_size, overlap)
    def chunking_method(self, strategy):
        if strategy=="TokenBased":
            return self.token_chunk
        else:
            return self.fixed_length_chunk


class TokenBasedChunker:
    def __init__(self, chunk_size, overlap):
        self.chunk_size = chunk_size
        self.overlap = overlap

    def split_document(self,document):
        """
        Splits a given document into tokens chunks based on specified chunk_size
        """
        if not document:
            return []
        chunks = []
        tokens = document.split()
        n_tokens = len(tokens)
        for i in range(0, n_tokens, self.chunk_size-self.overlap):
            chunk = tokens[i:i+self.chunk_size]
            chunks.append(" ".join(chunk))
        return chunks

class FixedLengthChunker:
    def __init__(self, chunk_size, overlap):
            self.chunk_size = chunk_size
            self.overlap = overlap
    
    def split_document(self,document):
        """
        Splits a given document into chunks based on specified chunk_size
        """
        if not document:
            return []
        
        chunks = []
        len_document = len(document)
        for i in range(0, len_document, self.chunk_size-self.overlap):
            chunk = document[i:i+self.chunk_size]
            chunks.append(chunk)
        return chunks

