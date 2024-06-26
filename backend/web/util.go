package web

import (
	"bytes"
	"encoding/json"
	"fmt"
	"net/http"
	"net/url"
	"os"

	"github.com/gin-gonic/gin"
	"github.com/jnuho/simpledl/pkg"
)

type requestParam struct {
	URL string `json:"cat_url"`
}

type responseParam struct {
	URL    string `json:"cat_url"`
	STATUS int    `json:"status"`
}

func validateRequest(c *gin.Context) (*requestParam, error) {
	catObj := requestParam{}
	if err := c.BindJSON(&catObj); err != nil {
		return nil, fmt.Errorf("invalid request: %v", err)
	}

	_, err := url.ParseRequestURI(catObj.URL)
	if err != nil {
		return nil, fmt.Errorf("invalid URL format: %v", err)
	}

	return &catObj, nil
}

func callPythonBackend(catURL string) (*responseParam, error) {
	url := os.Getenv("PYTHON_URL")

	jsonData, err := json.Marshal(map[string]string{
		"cat_url": catURL,
	})
	if err != nil {
		return nil, fmt.Errorf("failed to marshal request data: %v", err)
	}

	resp, err := http.Post(url, "application/json", bytes.NewBuffer(jsonData))
	if err != nil {
		return nil, fmt.Errorf("request to python failed: %v", err)
	}
	defer resp.Body.Close()
	if resp.StatusCode != http.StatusOK {
		return nil, fmt.Errorf("python backend returned non-200 status: %d", resp.StatusCode)
	}

	var result responseParam
	if err := json.NewDecoder(resp.Body).Decode(&result); err != nil {
		return nil, fmt.Errorf("failed to decode python backend response: %v", err)
	}

	return &result, nil
}

func callWeatherAPi() ([]pkg.WeatherResponse, error) {
	list := pkg.GetWeatherInfo()
	if len(list) == 0 {
		return nil, fmt.Errorf("failed to get weather info")
	}
	return list, nil
}
