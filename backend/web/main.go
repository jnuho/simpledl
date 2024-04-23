package main

import (
	"fmt"
	"net/http"

	"github.com/gin-contrib/cors"
	"github.com/gin-gonic/gin"
)

type url struct {
	URL string `json:"cat_url"`
}

func main() {
	// router
	r := gin.Default()
	// encountering a CORS (Cross-Origin Resource Sharing) issue
	// when a web application tries to make a request to a server that’s on a different domain, protocol, or port.
	// Apply the CORS middleware to the router
	r.Use(cors.New(cors.Config{
		AllowOrigins:     []string{"http://localhost"}, // or use "*" to allow all origins
		AllowMethods:     []string{"POST"},
		AllowHeaders:     []string{"Origin", "Content-Type"},
		ExposeHeaders:    []string{"Content-Length"},
		AllowCredentials: true,
	}))

	r.POST("/work/cat", func(c *gin.Context) {
		fmt.Println("hello!!")

		var catUrl url
		if err := c.BindJSON(&catUrl); err != nil {
			fmt.Println(err)
			c.IndentedJSON(http.StatusBadRequest, gin.H{
				"message": "Invalid request",
			})
			return
		}

		// Add the new album to the slice.
		c.IndentedJSON(http.StatusCreated, catUrl)
		// c.JSON(http.StatusOK, gin.H{
		// 	"result":  0,
		// 	"message": "success!",
		// })
	})
	r.GET("/ping", func(c *gin.Context) {
		c.JSON(http.StatusOK, gin.H{
			"message": "pong",
		})
	})
	// listen and serve on 0.0.0.0:8080 (for windows "localhost:8080")
	r.Run("localhost:3001")
	// r.Run()
}
