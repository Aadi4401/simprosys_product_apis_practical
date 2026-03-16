1> install docker on your device

2>Clone the Repository

3>Create a .env file in the project root and add:
SECRET_KEY=af3c7da2dd39253470cb8f512d54df882250d08855260ec23a55045bd86654c1aeb7baea4e44fb683d7963f5134f245d9c84c5b935d2e94a29d1e1c86a675790c4cb8fb2878dd52061b0fc445f2849e3
AES_KEY=mysecretkey12345


4>use command "docker compose up --build"


| Service          | Port  |
| ---------------- | ----- |
| Auth Service     | 8001  |
| Product Service  | 8002  |
| Category Service | 8003  |
| MongoDB          | 27017 |
| Redis            | 6379  |


**Auth Service**

http://localhost:8001/docs

**Product Service**

http://localhost:8002/docs

**Category Service**

http://localhost:8003/docs


**note: you'll see lock icon in api click and enter username and password **
username: admin
password admin



FastAPI Microservices
│

├── Auth Service (JWT Authentication)

├── Product Service (Product APIs)

├── Category Service (Category APIs)
├── MongoDB (Database)
└── Redis (Background processing)
