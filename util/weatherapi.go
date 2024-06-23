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
type WeatherResponse struct {
	// Coord      Coord       `json:"coord"`
	// Weather    []Weather   `json:"weather"`
	// Base       string      `json:"base"`
	Main Main `json:"main"`
	// Visibility int         `json:"visibility"`
	// Wind       Wind        `json:"wind"`
	// Rain       Rain        `json:"rain"`
	// Clouds     Clouds      `json:"clouds"`
	// Dt         int64       `json:"dt"`
	// Sys        Sys         `json:"sys"`
	// Timezone   int         `json:"timezone"`
	// ID         int         `json:"id"`
	Name string `json:"name"`
	// Cod        int         `json:"cod"`
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

func fetchWeather(city string, apiKey string, ch chan<- WeatherData, wg *sync.WaitGroup) {
	data := WeatherData{}

	defer wg.Done()

	url := fmt.Sprintf("http://api.openweathermap.org/data/2.5/weather?q=%s&appid=%s", city, apiKey)
	resp, err := http.Get(url)
	if err != nil {
		log.Printf("Error fetching weather for %s: %s\n", city, err)
		// return data
	}

	defer resp.Body.Close()

	if err := json.NewDecoder(resp.Body).Decode(&data); err != nil {
		log.Printf("Error decoding weather data for %s: %s\n", city, err)
		// return data
	}

	ch <- data

	// return data
}

// city: {city name},{state code},{country code}
// apiKey: {your_api_key}
// func getGeoloc(city string, apiKey string, city_info chan City) {
func getGeoloc(city string, apiKey string) City {
	data := []City{}

	limit := 1
	url := fmt.Sprintf("http://api.openweathermap.org/geo/1.0/direct?q=%s&limit=%d&appid=%s", city, limit, apiKey)
	resp, err := http.Get(url)
	if err != nil {
		log.Printf("Error fetching weather for %s: %s\n", city, err)
		// city_info <- City{}
		return City{}
	}

	defer resp.Body.Close()

	if err := json.NewDecoder(resp.Body).Decode(&data); err != nil {
		log.Fatalf("Error decoding weather data for %s: %s\n", city, err)
		// city_info <- City{}
		return City{}
	}
	return data[0]
}

func getCurrWeather(city, apiKey string, ch chan<- WeatherResponse, wg *sync.WaitGroup) {
	defer wg.Done()

	// city_info := make(chan City)
	// info := <-city_info
	info := getGeoloc(city, apiKey)
	if info.Name == "" {
		log.Fatalf("Error getGeoloc empty response\n")
		return
	}

	// api to get temperature and humidity for a given (lat, lon)
	data := &WeatherResponse{}

	units := "metric"
	url := fmt.Sprintf("https://api.openweathermap.org/data/2.5/weather?lat=%.2f&lon=%.2f&units=%s&appid=%s", info.Lat, info.Lon, units, apiKey)
	resp, err := http.Get(url)
	if err != nil {
		log.Fatalf("Error fetching weather for lat,lon =(%.2f, %.2f), %v\n", info.Lat, info.Lon, err)
	}
	defer resp.Body.Close()

	if err := json.NewDecoder(resp.Body).Decode(&data); err != nil {
		log.Fatalf("Error decoding weather data for (%.2f, %.2f): %s\n", info.Lat, info.Lon, err)
	}

	ch <- *data
}

func getEnvVar(envKey string) string {
	err := godotenv.Load(".env")
	if err != nil {
		log.Fatal("Error loading .env file")
	}
	return os.Getenv(envKey)
}

const (
	// YYYY-MM-DD: 2022-03-23
	YYYYMMDD = "2006-01-02"
	// 24h hh:mm:ss: 14:23:20
	HHMMSS24h = "15:04:05"
	// 12h hh:mm:ss: 2:23:20 PM
	HHMMSS12h = "3:04:05 PM"
	// text date: March 23, 2022
	TextDate = "January 2, 2006"
	// text date with weekday: Wednesday, March 23, 2022
	TextDateWithWeekday = "Monday, January 2, 2006"
	// abbreviated text date: Mar 23 Wed
	AbbrTextDate = "Jan 2 Mon"
)

func main() {
	log.SetPrefix(time.Now().Format(YYYYMMDD+" "+HHMMSS24h) + ": ")
	// log.SetFlags(log.Ltime)
	log.SetFlags(log.Lshortfile)

	startNow := time.Now()
	apiKey := getEnvVar("WEATHER_API_KEY")
	// 840,158,410
	// cities := []string{"Los Angeles", "Taipei", "Seoul"}

	ch := make(chan WeatherResponse)
	var wg sync.WaitGroup
	cities := []string{"Los Angeles,CA,US", "Taipei,TW", "Seongnam-si,KR"}
	for _, city := range cities {
		wg.Add(1)
		go getCurrWeather(city, apiKey, ch, &wg)
	}

	go func() {
		wg.Wait()
		close(ch)
	}()

	for result := range ch {
		str := fmt.Sprintf("Name: %v\n", result.Name)
		str += fmt.Sprintf("Temperature: %v\n", result.Main.Temp)
		str += fmt.Sprintf("Humidity: %v\n", result.Main.Humidity)
		log.Println(str)
	}

	log.Println("This operation took:", time.Since(startNow))
}
