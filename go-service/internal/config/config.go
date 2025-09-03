package config

import (
	"os"
	"strconv"
	"time"
)

type Config struct {
	Addr          string        // :8080
	InternalToken string        // общий секрет с Python
	ReadTimeout   time.Duration // 10s
	WriteTimeout  time.Duration // 10s
	IdleTimeout   time.Duration // 60s
}

func envDefault(key, def string) string {
	if v := os.Getenv(key); v != "" {
		return v
	}
	return def
}

func parseDurationEnv(key string, def time.Duration) time.Duration {
	if v := os.Getenv(key); v != "" {
		if d, err := time.ParseDuration(v); err == nil {
			return d
		}
	}
	return def
}

func Load() *Config {
	return &Config{
		Addr:          envDefault("ADDR", ":8080"),
		InternalToken: envDefault("INTERNAL_TOKEN", ""),
		ReadTimeout:   parseDurationEnv("READ_TIMEOUT", 10*time.Second),
		WriteTimeout:  parseDurationEnv("WRITE_TIMEOUT", 10*time.Second),
		IdleTimeout:   parseDurationEnv("IDLE_TIMEOUT", 60*time.Second),
	}
}

// утилита если вдруг понадобится парсить int из env
func parseIntEnv(key string, def int) int {
	if v := os.Getenv(key); v != "" {
		if i, err := strconv.Atoi(v); err == nil {
			return i
		}
	}
	return def
}
