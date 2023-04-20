# k8s-example-workload

Example python program that connects to a [cockroachdb](https://www.cockroachlabs.com/). Simple [FastAPI](https://fastapi.tiangolo.com/) app, that let's you create, read or delete records via the integrtated OpenAPI page <http://localhost:8000/docs>.

## Run locally for testing

```sh
docker run --rm -d --name=roach -p 8080:8080 -p 26257:26257 cockroachdb/cockroach:latest start-single-node --insecure
sleep 5  # wait for cockroachdb to be ready
uvicorn main:app --reload
```

## Run in kubernetes with helm

```sh
helm repo add tibeer https://tibeer.github.io/helm-charts/
helm repo refresh
helm install foo tibeer/example-app
```
