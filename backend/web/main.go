package main

import (
	"bytes"
	"encoding/json"
	"fmt"
	"io"
	"log"
	"net/http"
	"net/url"

	// 	"github.com/jnuho/simpledl/backend/web/"

	"github.com/gin-contrib/cors"
	"github.com/gin-gonic/gin"
)

type requestParam struct {
	URL string `json:"cat_url"`
}

type responseParam struct {
	URL    string `json:"cat_url"`
	STATUS string `json:"status"`
}

func handleGetRequest(c *gin.Context) {
	// handle GET request from client
	c.String(http.StatusOK, "pong")
}

func validateRequest(c *gin.Context) (*requestParam, error) {
	catObj := requestParam{}
	if err := c.BindJSON(&catObj); err != nil {
		return nil, fmt.Errorf("invalid request: %v", err)
	}

	// Validate URL format
	_, err := url.ParseRequestURI(catObj.URL)
	if err != nil {
		return nil, fmt.Errorf("invalid URL format: %v", err)
	}

	return &catObj, nil
}

func callPythonBackend(catURL string) (*responseParam, error) {
	jsonData, _ := json.Marshal(map[string]string{
		"cat_url": catURL,
	})
	resp, err := http.Post("http://be-py-service:3002/worker/cat", "application/json", bytes.NewBuffer(jsonData))
	if err != nil {
		return nil, err
	}
	defer resp.Body.Close()

	b, err := io.ReadAll(resp.Body)
	if err != nil {
		return nil, err
	}

	var result responseParam
	err = json.Unmarshal(b, &result)
	if err != nil {
		return nil, err
	}

	return &result, nil
}

func handlePostRequest(c *gin.Context) {
	// handle POST request from client
	catObj, err := validateRequest(c)
	if err != nil {
		log.Println(err)
		c.JSON(http.StatusBadRequest, gin.H{
			"message": err.Error(),
		})
		return
	}

	// Python backend call
	result, err := callPythonBackend(catObj.URL)
	if err != nil {
		log.Fatalln(err)
		c.JSON(http.StatusInternalServerError, gin.H{
			"message": "Error calling Python backend",
		})
		return
	}
	log.Printf("RESULT FROM Python ASGI SERVER!!! %v\n", result)

	// Response
	// c.JSON(http.StatusOK, catUrl)
	c.JSON(http.StatusOK, gin.H{
		"cat_url":       result.URL,
		"go-server":     "ok",
		"python-server": result.STATUS,
	})

}

func main() {
	// Router
	r := gin.Default()

	// Apply the CORS middleware to the router
	r.Use(cors.New(cors.Config{
		AllowOrigins:     []string{"http://localhost:8080", "http://localhost"}, // or use "*" to allow all origins
		AllowMethods:     []string{"POST", "GET"},
		AllowHeaders:     []string{"Origin", "Content-Type"},
		ExposeHeaders:    []string{"Content-Length"},
		AllowCredentials: true,
	}))
	//r.GET("/ping", func(c *gin.Context) {
	r.GET("/", handleGetRequest)

	//r.POST("/web/cat", func(c *gin.Context) {
	r.POST("/", handlePostRequest)

	// NOTE: r.Run("localhost:3001") means your server will only be accessible
	// via the same machine on which it is running. So, another docker container cannot access it.
	r.Run(":3001")
}
