# Build

## Build the image

```bash
docker compose build
```

## Run the container

```bash
docker compose up
```

## Stop the container

```bash
docker compose down
```

## Run backend tests

```bash
docker compose up -d
docker compose run --rm --use-aliases backend --test 
```