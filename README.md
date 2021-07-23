# Django Trace Context

`work in progress`

## Application architecture

The purpose is to propagate a message with `traceparent` id throw two api's and one worker using [W3C trace context](https://www.w3.org/TR/trace-context) standard. The `first-api` calls the `second-api` by a http call, on the other hand, the `second-api` has an asynchronous communication with the `worker` by a message broker (I chose [rabbitmq](https://www.rabbitmq.com/) for that). Furthermore, I chose [zipkin](https://zipkin.io/) as default APM tool, being responsible for get the application traces and build the distributed tracing diagram.

![Distributed Trace](doc/w3c-trace-context.png)

The first and second APIs have the [same code base](./src/OpenTelemetryApi), but they're deployed in different containers.

## Running the project

Inside [otel_django_app](./otel_django_app) type the following command:

```bash
python3 manage.py runserver
```

to run jaeger, type the following command:

```bash
docker run -d --name jaeger \
  -e COLLECTOR_ZIPKIN_HOST_PORT=:9411 \
  -p 5775:5775/udp \
  -p 6831:6831/udp \
  -p 6832:6832/udp \
  -p 5778:5778 \
  -p 16686:16686 \
  -p 14268:14268 \
  -p 14250:14250 \
  -p 9411:9411 \
  jaegertracing/all-in-one:1.24
```

to open jaeger dashboard, type the following command:

```bash
http://localhost:16686
```

Inside [src folder](./src), type the command below to up all containers (`first-api`, `second-api`, `worker`, `rabbit` and `zipkin`):

```bash
  docker-compose up
```

wait for all containers get on and then send a request to the `first-api`:

```bash
curl --request POST \
  --url http://localhost:5000/WeatherForecast \
  --header 'Content-Type: application/json' \
  --header 'accept: */*' \
  --data '{
	"temperatureC": 10,
	"summary": "Trace Test"
}'
```

the message that you sent above will travel throughout the flow (`first-api` > `second-api` >  `rabbit` > `worker`) along with the propagation fields (`traceparent` and `tracestate`). To see the generated distributed tracing diagram, access `zipkin` in your browser:

```bash
  http://localhost:9411/
```

at home page, let the search field empty and type `RUN QUERY` to load all traces. Finally, click in your trace, then you'll see a diagram like this:

![Zipkin Diagram](doc/zipkin-diagram.png)
