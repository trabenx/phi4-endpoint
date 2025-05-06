```bash
docker-compose up --build
```

```bash
./
├── backend
│   ├── Dockerfile         # Builds FastAPI app with model
│   ├── requirements.txt   # Python dependencies
│   └── app.py             # HTTP endpoint implementation
├── frontend
│   ├── Dockerfile         # Builds React app
│   ├── package.json       # React project config
│   └── src
│       ├── App.js         # Main UI
│       └── index.js       # Entry point
└── docker-compose.yml     # Orchestrates backend+frontend
```