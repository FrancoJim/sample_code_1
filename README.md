# Change Machine

This is a web page that will display the optimal USD coin combination (fewest number of coins) that fulfills a given USD
dollar value. The web page should take a USD dollar value as input and interact with an API that computes and returns
the optimal coin combination. The results of the API call should be displayed on the web page.

Assume the following USD coins or bills:

- Hundred Dollar Bill ($100.00)
- Fifty Dollar Bill ($50.00)
- Twenty Dollar Bill ($20.00)
- Ten Dollar Bill ($10.00)
- Five Dollar Bill ($5.00)
- One Dollar ($1.00)
- Half Dollar ($0.50)
- Quarter ($0.25)
- Dime ($0.10)
- Nickel ($0.05)
- Penny ($0.01)

## Prerequisites

### Copy `.env.example` to `.env`

```bash
cp .env.example .env
```

## Docker Deployment

### Development

```bash
docker-compose -f docker-compose.yml --profile dev up --build
```

### Production

```bash
docker-compose -f docker-compose.yml --profile prod up -d
```

## Connect to web interface

Go to `http://<DOCKER_HOST>:5000` within web browser. If running locally, `http://127.0.0.1:5000`.

## Contributing

Contributions are accepted in forms of employment or large sums of money.

## License

[MIT](https://choosealicense.com/licenses/mit/)
