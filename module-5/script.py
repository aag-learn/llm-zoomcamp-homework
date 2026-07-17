from dotenv import load_dotenv
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import ConsoleSpanExporter, SimpleSpanProcessor
from my_rag_helper import RAGTraced

load_dotenv("../.env")

if "provider" in locals():
    print("Reusing existing provider in local scope")
else:
    print("Initializing provider...")
    provider = TracerProvider()
    provider.add_span_processor(SimpleSpanProcessor(ConsoleSpanExporter()))

    trace.set_tracer_provider(provider)
    tracer = trace.get_tracer("llm-zoomcamp")

from starter import index, client

rag = RAGTraced(index=index, llm_client=client, tracer=tracer)

query = "How does the agentic loop keep calling the model until it stops?"
answer = rag.rag(query)
print(answer)
