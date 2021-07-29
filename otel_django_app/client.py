from requests import get

from opentelemetry import trace
from opentelemetry.propagate import inject
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.zipkin.json import ZipkinExporter
from opentelemetry.sdk.resources import SERVICE_NAME, Resource

zipkin_exporter = ZipkinExporter(
    # configure agent
    endpoint="http://localhost:9411/api/v2/spans"
)

trace.set_tracer_provider(TracerProvider(resource=Resource.create({SERVICE_NAME: "django-client"})))
tracer = trace.get_tracer_provider().get_tracer(__name__)

trace.get_tracer_provider().add_span_processor(
    BatchSpanProcessor(zipkin_exporter)
)


with tracer.start_as_current_span("client"):

    with tracer.start_as_current_span("client-server"):
        headers = {}
        inject(headers)
        requested = get(
            "http://localhost:8000/api/",
            headers=headers,
        )
