package main

import (
	"bytes"
	"io/ioutil"
	"log"
	"net/http"
	"net/url"

	"github.com/gin-contrib/cors"
	"github.com/gin-gonic/gin"
)

type urlObject struct {
	URL string `json:"cat_url"`
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
		var catUrl urlObject
		if err := c.BindJSON(&catUrl); err != nil {
			log.Println(err)

			c.JSON(http.StatusBadRequest, gin.H{
				"message": "Invalid request",
			})
			return
		}

		// Validate url format
		_, err := url.ParseRequestURI(catUrl.URL)
		if err != nil {
			c.JSON(http.StatusBadRequest, gin.H{
				"message": "Invalid URL format",
			})
			return
		}

		// Python backend
		jsonData := []byte(`{"key1": "value1", "key2": "value2"}`) // replace with your actual data

		resp, err := http.Post("http://localhost:3002/worker/cat", "application/json", bytes.NewBuffer(jsonData)) // replace with your Python server URL
		if err != nil {
			log.Fatalln(err)
		}

		defer resp.Body.Close()

		body, err := ioutil.ReadAll(resp.Body)
		if err != nil {
			log.Fatalln(err)
		}
		log.Println(string(body))

		// Response
		c.JSON(http.StatusOK, catUrl)
		// c.JSON(http.StatusOK, gin.H{
		// 	"cat_url": catUrl.URL,
		// })
	})

	r.Run("localhost:3001")
}
