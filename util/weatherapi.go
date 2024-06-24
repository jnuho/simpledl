package main

import (
	"context"
	"encoding/json"
	"fmt"
	"log"
	"net/http"
	"os"
	"sync"
	"time"

	"github.com/joho/godotenv"
)

type GeoCityResponse struct {
	Name    string  `json:"name"`
	Lat     float64 `json:"lat"`
	Lon     float64 `json:"lon"`
	Country string  `json:"country"`
	State   string  `json:"state"`
}

type WeatherResponse struct {
	Main    Main      `json:"main"`
	Name    string    `json:"name"`
	Weather []Weather `json:"weather"`
}

type Main struct {
	Temp      float64 `json:"temp"`
	FeelsLike float64 `json:"feels_like"`
	TempMin   float64 `json:"temp_min"`
	TempMax   float64 `json:"temp_max"`
	Pressure  int     `json:"pressure"`
	Humidity  int     `json:"humidity"`
	SeaLevel  int     `json:"sea_level"`
	GrndLevel int     `json:"grnd_level"`
}

type Weather struct {
	ID          int    `json:"id"`
	Main        string `json:"main"`
	Description string `json:"description"`
	Icon        string `json:"icon"`
}

func getGeoloc(ctx context.Context, city, apiKey string) (GeoCityResponse, error) {
	var data []GeoCityResponse

	limit := 1
	url := fmt.Sprintf("http://api.openweathermap.org/geo/1.0/direct?q=%s&limit=%d&appid=%s", city, limit, apiKey)

	// create a new HTTP request with the provided context.
	req, err := http.NewRequestWithContext(ctx, "GET", url, nil)
	if err != nil {
		return GeoCityResponse{}, fmt.Errorf("error creating request: %w", err)
	}

	// send the HTTP request and receive the response.
	resp, err := http.DefaultClient.Do(req)
	if err != nil {
		return GeoCityResponse{}, fmt.Errorf("error fetching geolocation for %s: %w", city, err)
	}
	defer resp.Body.Close()

	if resp.StatusCode != http.StatusOK {
		return GeoCityResponse{}, fmt.Errorf("non-200 response: %s", resp.Status)
	}

	if err := json.NewDecoder(resp.Body).Decode(&data); err != nil {
		return GeoCityResponse{}, fmt.Errorf("error decoding geolocation data for %s: %w", city, err)
	}
	if len(data) == 0 {
		return GeoCityResponse{}, fmt.Errorf("no geolocation data found for %s", city)
	}
	return data[0], nil
}

func getCurrWeather(ctx context.Context, city, apiKey string, ch chan<- WeatherResponse, wg *sync.WaitGroup) {
	defer wg.Done()

	info, err := getGeoloc(ctx, city, apiKey)
	if err != nil {
		log.Printf("Error getting geolocation: %v\n", err)
		return
	}

	var data WeatherResponse
	units := "metric"
	url := fmt.Sprintf("https://api.openweathermap.org/data/2.5/weather?lat=%.2f&lon=%.2f&units=%s&appid=%s", info.Lat, info.Lon, units, apiKey)

	// create a new HTTP request with the provided context.
	req, err := http.NewRequestWithContext(ctx, "GET", url, nil)
	if err != nil {
		log.Printf("Error creating request: %v\n", err)
		return
	}

	// send the HTTP request and receive the response.
	resp, err := http.DefaultClient.Do(req)
	if err != nil {
		log.Printf("Error fetching weather for lat,lon =(%.2f, %.2f): %v\n", info.Lat, info.Lon, err)
		return
	}
	defer resp.Body.Close()

	if resp.StatusCode != http.StatusOK {
		log.Printf("Non-200 response fetching weather for lat,lon =(%.2f, %.2f): %s\n", info.Lat, info.Lon, resp.Status)
		return
	}

	if err := json.NewDecoder(resp.Body).Decode(&data); err != nil {
		log.Printf("Error decoding weather data for (%.2f, %.2f): %v\n", info.Lat, info.Lon, err)
		return
	}

	ch <- data
}

func getEnvVar(envKey string) string {
	err := godotenv.Load(".env")
	if err != nil {
		log.Fatal("Error loading .env file")
	}
	return os.Getenv(envKey)
}

const (
	YYYYMMDD  = "2006-01-02"
	HHMMSS24h = "15:04:05"
)

func main() {
	log.SetPrefix(time.Now().Format(YYYYMMDD+" "+HHMMSS24h) + ": ")
	log.SetFlags(log.Lshortfile)

	startNow := time.Now()
	apiKey := getEnvVar("WEATHER_API_KEY")
	cities := []string{"Los Angeles,CA,US", "Seattle,WA,US", "Taipei,TW", "Seongnam-si,KR"}

	ctx, cancel := context.WithTimeout(context.Background(), 3*time.Second)
	defer cancel()

	ch := make(chan WeatherResponse)
	var wg sync.WaitGroup

	for _, city := range cities {
		wg.Add(1)
		go getCurrWeather(ctx, city, apiKey, ch, &wg)
	}

	go func() {
		wg.Wait()
		close(ch)
	}()

	str := ""
	for result := range ch {
		// fmt.Printf("→ %v  %v °C, Humidity: %v, Weather: %v\n", result.Name, result.Main.Temp, result.Main.Humidity, result.Weather[0])
		str += fmt.Sprintf("→ %v  %v °C, Humidity: %v, Weather: %v\n", result.Name, result.Main.Temp, result.Main.Humidity, result.Weather[0])
		// fmt.Printf("ICON= https://openweathermap.org/img/wn/%s@2x.png\n", result.Weather[0].Icon)
	}

	// fmt.Printf("\nThis operation took: %v\n\n", time.Since(startNow))
	str += fmt.Sprintf("\nThis operation took: %v\n\n", time.Since(startNow))
	fmt.Print(str)

}
