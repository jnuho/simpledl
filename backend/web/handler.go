package web

import (
	"log"
	"net/http"

	"github.com/gin-gonic/gin"
)

func getMethodHandler(c *gin.Context) {
	c.String(http.StatusOK, "OK")
}

func catPostHandler(c *gin.Context) {
	catObj, err := validateRequest(c)
	if err != nil {
		log.Println("Validation error: ", err)
		c.JSON(http.StatusBadRequest, gin.H{
			"message": err.Error(),
		})
		return
	}

	result, err := callPythonBackend(catObj.URL)
	if err != nil {
		log.Println("Python backend call error:", err)
		c.JSON(http.StatusInternalServerError, gin.H{
			"message": "Error calling Python backend",
		})
		return
	}

	c.JSON(http.StatusOK, gin.H{
		"cat_url":       result.URL,
		"go-server":     "ok",
		"python-server": result.STATUS,
	})
}

func weatherPostHandler(c *gin.Context) {

	list, err := callWeatherAPi()
	if err != nil {
		log.Println("WeatherApi call error:", err)
		c.JSON(http.StatusInternalServerError, gin.H{
			"message": "Error calling GetWeatherInfo()",
		})
		return
	}

	c.JSON(http.StatusOK, gin.H{
		"weather_list": list,
	})
}
