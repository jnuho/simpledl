package web

import (
	"context"
	"fmt"
	"log"
	"net/http"
	"sync"
	"time"

	"github.com/gin-contrib/cors"
	"github.com/gin-gonic/gin"
)

func oneTimeOp() {
	log.Println("ONE TIME OP - SERVER STARTED")
}

func corsConfig() gin.HandlerFunc {
	config := cors.Config{
		AllowOrigins:     []string{"*"},
		AllowMethods:     []string{"POST", "GET", "OPTIONS"},
		AllowHeaders:     []string{"Origin", "Content-Type"},
		ExposeHeaders:    []string{"Content-Length"},
		AllowCredentials: true,
	}
	return cors.New(config)
}

func StartServer(ctx context.Context, host string, done chan<- error) {
	var once sync.Once
	once.Do(oneTimeOp)

	// Router
	r := gin.Default()

	// Apply the CORS middleware to the router
	r.Use(corsConfig())

	r.GET("/healthz", getMethodHandler)
	r.POST("/web/cat", postMethodHandler)
	r.POST("/weather", func(c *gin.Context) {
		c.String(http.StatusOK, time.Now().Format(time.RFC3339)+" weather")
	})

	server := &http.Server{
		Addr:    host,
		Handler: r,
	}

	go func() {
		if err := server.ListenAndServe(); err != nil && err != http.ErrServerClosed {
			done <- err
		}
	}()

	<-ctx.Done()

	ctxShutDown, cancel := context.WithTimeout(context.Background(), 5*time.Second)
	defer cancel()

	if err := server.Shutdown(ctxShutDown); err != nil {
		done <- fmt.Errorf("server shutdown failed: %v", err)
	}

	done <- nil
}
