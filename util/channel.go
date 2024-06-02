package main

import (
	"encoding/json"
	"fmt"
	"log"
	"net/http"
	"os"
	"sync"
	"time"

	"github.com/joho/godotenv"
)

type WeatherData struct {
	Main struct {
		Temp     float64 `json:temp"`
		Humidity float64 `json:humidity"`
	} `json:"main"`
}

type City struct {
	Name    string  `json:"name"`
	Lat     float64 `json:"lat"`
	Lon     float64 `json:"lon"`
	Country string  `json:"country"`
	State   string  `json:"state"`
}

func fetchWeather(city string, apiKey string, ch chan<- WeatherData, wg *sync.WaitGroup) interface{} {
	data := WeatherData{}

	defer wg.Done()

	url := fmt.Sprintf("http://api.openweathermap.org/data/2.5/weather?q=%s&appid=%s", city, apiKey)
	resp, err := http.Get(url)
	if err != nil {
		fmt.Printf("Error fetching weather for %s: %s\n", city, err)
		return data
	}

	defer resp.Body.Close()

	if err := json.NewDecoder(resp.Body).Decode(&data); err != nil {
		fmt.Printf("Error decoding weather data for %s: %s\n", city, err)
		return data
	}

	ch <- data

	return data
}

func getGeoloc(city string, apiKey string) []City {
	data := []City{}

	url := fmt.Sprintf("http://api.openweathermap.org/geo/1.0/direct?q=%s&limit=%d&appid=%s", city, 5, apiKey)
	resp, err := http.Get(url)
	if err != nil {
		fmt.Printf("Error fetching weather for %s: %s\n", city, err)
	}
	defer resp.Body.Close()

	if err := json.NewDecoder(resp.Body).Decode(&data); err != nil {
		fmt.Printf("Error decoding weather data for %s: %s\n", city, err)
	}

	return data
}

func getEnvVar(envKey string) string {
	err := godotenv.Load(".env")
	if err != nil {
		log.Fatal("Error loading .env file")
	}
	return os.Getenv(envKey)
}

func main() {
	startNow := time.Now()
	apiKey := getEnvVar("OPENWEATHERMAP_API_KEY")

	// city := getGeoloc("Seoul", apiKey)[0]
	// fmt.Printf("Latitude: %.2f, Longitude: %.2f\n", city.Lat, city.Lon)
	cities := []string{"Toronto", "London", "Paris", "Seoul"}

	ch := make(chan WeatherData)
	var wg sync.WaitGroup

	for _, city := range cities {
		wg.Add(1)
		go fetchWeather(city, apiKey, ch, &wg)
	}

	go func() {
		wg.Wait()
		close(ch)
	}()

	for result := range ch {
		fmt.Printf("This is the data: %v\n", result)
	}

	fmt.Println("This operation took:", time.Since(startNow))
}
