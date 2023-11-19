# Build & Run
1. docker build -t loadboard-server .
2. docker rm loadboard-server && docker run -d -p 80:80 --name loadboard-server loadboard-server