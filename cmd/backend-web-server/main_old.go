package main

import (
	"bytes"
	"encoding/json"
	"flag"
	"fmt"
	"io"
	"log"
	"net/http"
	"net/url"
	"time"

	"github.com/gin-contrib/cors"
	"github.com/gin-gonic/gin"
	"github.com/golang/glog"
)

type requestParam struct {
	URL string `json:"cat_url"`
}

type responseParam struct {
	URL    string `json:"cat_url"`
	STATUS string `json:"status"`
}

func oneTimeOp() {
	fmt.Println("one time op start")
	time.Sleep(3 * time.Second)
	fmt.Println("one time op started")
}

// handle GET request from client
func getMethodHandler(c *gin.Context) {
	// once.Do(oneTimeOp)
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

// Send POST Request to another backend python server
func callPythonBackend(catURL string) (*responseParam, error) {
	jsonData, _ := json.Marshal(map[string]string{
		"cat_url": catURL,
	})
	resp, err := http.Post("http://be-py-service:3002/worker/cat", "application/json", bytes.NewBuffer(jsonData))
	// resp, err := http.Post("http://be-py:3002/worker/cat", "application/json", bytes.NewBuffer(jsonData))
	if err != nil {
		return nil, fmt.Errorf("request to python failed: %v", err)
	}
	defer resp.Body.Close()

	b, err := io.ReadAll(resp.Body)
	if err != nil {
		return nil, fmt.Errorf("reading python server response failed: %v", err)
	}

	var result responseParam
	err = json.Unmarshal(b, &result)
	if err != nil {
		return nil, fmt.Errorf("unmarshal python response body failed: %v", err)
	}

	return &result, nil
}

// handle POST request from client
func postMethodHandler(c *gin.Context) {
	log.Printf("Before python call\n")
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
		c.AbortWithStatus(http.StatusForbidden)
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

// func customErrorHandler(c *gin.Context) {
// 	c.Next() // Execute the remaining handlers

// 	// Check if the response status is 403
// 	if c.Writer.Status() == http.StatusForbidden {
// 		// Log additional details (e.g., request path)
// 		fmt.Printf("403 error for path: %s\n", c.Request.URL.Path)
// 		// You can log other relevant information here
// 	}
// }

func StartServer(host string) error {
	// Router
	r := gin.Default()

	// Apply the CORS middleware to the router
	config := cors.Config{
		// AllowOrigins:     []string{"http://localhost"}, // or use "*" to allow all origins
		AllowOrigins:     []string{"*"}, // or use "*" to allow all origins
		AllowMethods:     []string{"POST", "GET"},
		AllowHeaders:     []string{"Origin", "Content-Type"},
		ExposeHeaders:    []string{"Content-Length"},
		AllowCredentials: true,
	}
	r.Use(cors.New(config))

	r.GET("/", getMethodHandler)
	r.POST("/", postMethodHandler) // in k8s ingress env
	// r.POST("/web/cat", postMethodHandler) // in docker env

	// NOTE: r.Run("localhost:3001") means your server will only be accessible
	// via the same machine on which it is running. So, another docker container cannot access it.
	err := r.Run(host)
	return err
}

func main() {
	// ./go-app -web-host=":3001"
	host := flag.String("web-host", ":3001", "Specify host and port for backend.")
	flag.Parse()
	err := StartServer(*host)
	if err != nil {
		glog.Fatal(err)
	}
}
