# SvitITTask

## Setup

1. Clone the repository:
   ```sh
   git clone git@github.com:MKisil/SvitITTask.git
   ```
2. Navigate to the project directory:
   ```sh
   cd SvitITTask
   ```
3. Start the application using Docker:
   ```sh
   docker compose up
   ```
4. Open your browser and visit:
   ```
   http://localhost:8000
   ```

## Running Tests

To run tests, execute:
```sh
docker-compose run --rm api pytest tests/
```

## How It Works

1. **User Registration**: A user creates an account.
2. **Upload Log Files**: The user uploads log files to the system.
3. **Parsing and Storage**: Log files are parsed and stored in Elasticsearch.
4. **Search Logs**: The user can search logs by:
   - Time
   - Keywords
   - Log Level

## API Documentation

Visit the interactive API docs at:
```
http://localhost:8000/docs
```

