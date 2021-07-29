from django.http import HttpResponse
from opentelemetry import trace
from opentelemetry.exporter.zipkin.json import ZipkinExporter
from opentelemetry.sdk.resources import SERVICE_NAME, Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor

trace.set_tracer_provider(TracerProvider(resource=Resource.create({SERVICE_NAME: "django-server"})))
tracer = trace.get_tracer(__name__)

# create a ZipkinExporter
zipkin_exporter = ZipkinExporter(
    endpoint="http://localhost:9411/api/v2/spans",
)

# Create a BatchSpanProcessor and add the exporter to it
span_processor = BatchSpanProcessor(zipkin_exporter)

# add to the tracer
trace.get_tracer_provider().add_span_processor(span_processor)

def index(request):
    tracer.start_as_current_span('foo')
    return HttpResponse("Hello, world.")