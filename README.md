# Usage

## Starting the Spark cluster

```bash
docker compose up --build
```

## Running a job

```bash
docker compose --profile spark-job-sparkie run --build --rm spark-job-sparkie \
    uv run python -m sparkie.main
```

The command is kind of heavym, but the relevant parts are roughly:

```
docker compose
    --profile spark-job-sparkie run  # Run only the pyspark job, not the cluster.
    --build                          # Build the container to get recent changes.
    --rm                             # Delete the container after use.
    spark-job-sparkie                # The name of the Docker compose service to start.
    uv run python -m sparkie.main    # The command to run inside the container.
```
