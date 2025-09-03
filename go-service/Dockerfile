# build стадия
FROM golang:1.21-alpine AS builder
WORKDIR /src
COPY go.mod ./
RUN go mod download
COPY . .
RUN CGO_ENABLED=0 GOOS=linux go build -ldflags="-s -w" -o /go-service ./cmd/server/main.go

# run-стадия (минимальный образ)
FROM alpine:3.18
RUN apk add --no-cache ca-certificates
COPY --from=builder /go-service /go-service
EXPOSE 8080
ENTRYPOINT ["/go-service"]