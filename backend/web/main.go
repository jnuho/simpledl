package main

import (
	"bytes"
	"encoding/json"
	"fmt"
	"io"
	"log"
	"net/http"
	"net/url"

	"github.com/gin-contrib/cors"
	"github.com/gin-gonic/gin"
)

type param struct {
	URL string `json:"cat_url"`
}

type response struct {
	URL    string `json:"cat_url"`
	STATUS string `json:"status"`
}

func main() {
	// Router
	r := gin.Default()

	// Apply the CORS middleware to the router
	r.Use(cors.New(cors.Config{
		AllowOrigins:     []string{"http://localhost"}, // or use "*" to allow all origins
		AllowMethods:     []string{"POST"},
		AllowHeaders:     []string{"Origin", "Content-Type"},
		ExposeHeaders:    []string{"Content-Length"},
		AllowCredentials: true,
	}))

	// Handle REST API request
	r.POST("/web/cat", func(c *gin.Context) {
		catObj := param{}
		if err := c.BindJSON(&catObj); err != nil {
			log.Println(err)

			c.JSON(http.StatusBadRequest, gin.H{
				"message": "Invalid request",
			})
			return
		}

		// Validate url format
		_, err := url.ParseRequestURI(catObj.URL)
		if err != nil {
			c.JSON(http.StatusBadRequest, gin.H{
				"message": "Invalid URL format",
			})
			return
		}

		// Python backend call
		jsonData := []byte(fmt.Sprintf(`{"cat_url": "%s"}`, catObj.URL))

		resp, err := http.Post("http://localhost:3002/worker/cat", "application/json", bytes.NewBuffer(jsonData))
		if err != nil {
			log.Fatalln(err)
		}

		defer resp.Body.Close()

		b, err := io.ReadAll(resp.Body)
		if err != nil {
			log.Fatalln(err)
		}
		result := response{}
		err = json.Unmarshal(b, &result)
		// err = binary.Read(bytes.NewBuffer(b[:]), binary.BigEndian, &result)
		if err != nil {
			panic(err)
		}
		log.Printf("RESULT FROM Python ASGI SERVER!!! %v\n", result)

		// Response
		// c.JSON(http.StatusOK, catUrl)
		c.JSON(http.StatusOK, gin.H{
			"cat_url":       result.URL,
			"go-server":     "ok",
			"python-server": result.STATUS,
		})
	})

	r.Run("localhost:3001")
}
