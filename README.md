# Edge Device Data Stream Producer

### Installing

A step-by-step series of examples that tell you how to get a development environment running:
1. Clone the repository to your local machine.
2. Navigate to the project directory.
3. Use the following command to build and start the project:

```bash
docker-compose up --build && docker build -t kafka . && docker run --name kafka -v icicle:/app/logs kafka
```

This command performs several actions:
- `docker-compose up --build` builds and starts the containers defined in your `docker-compose.yml`.
- The subsequent commands manage a specific container named `producer`, ensuring it's removed if it already exists, then rebuilt and run with specific volume and name settings.

## Built With

- [Docker](https://www.docker.com/) - Containerization platform
- [Python](https://www.python.org/) - Programming language used