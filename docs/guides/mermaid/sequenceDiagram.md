sequenceDiagram
    participant User
    participant API
    participant Database

    User->>API: GET /data
    API->>Database: Query
    Database-->>API: Results
    API-->>User: JSON Response