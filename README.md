# banana-nana
 
## Ask endpoint and LLM providers

The project includes a POST `/api/ask` endpoint (see `Backend/routers/ask.py`) that uses LangChain retriever + an LLM Chain pattern to retrieve relevant chunks from ChromaDB and return a mocked answer. The endpoint is intentionally mocked for development to avoid relying on external, paid LLM providers.

- Example request:

```
POST /api/ask
Content-Type: application/json

{ "question": "What is the warranty?" }
```

Returns:
```
{ "answer": "...analysis...", "sources": [{"file_id": "...", "filename": "example.pdf"}]}
```

### Mock behavior (default)

This project is configured to always return a mocked answer to `POST /api/ask`, while still performing retrieval so the returned `sources` reflect the most relevant chunks stored in ChromaDB. This avoids external LLM dependency and simplifies development.

If you want to switch to a real LLM provider later, you can update the service to use your chosen provider (OpenAI, Hugging Face, or a local model).

### Environment variables (common)

The endpoint is mocked in this codebase by default; environment variables related to OpenAI or HF are not used.

If you need help configuring a free local model or adding a Hugging Face based LLM provider, ask and I can provide step-by-step instructions.
