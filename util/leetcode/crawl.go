package main

import (
	"fmt"
	"log"
	"net/http"
	"os"

	"github.com/gocolly/colly/v2"
)

// problem: 문제번호
// desc: 문제설명
func WriteToFile(problem, desc string) {
	// If the
	fname := "problems/" + problem + ".go"
	f, err := os.OpenFile(fname, os.O_APPEND|os.O_CREATE|os.O_WRONLY, 0644)
	if err != nil {
		log.Fatal(err)
	}
	if _, err := f.Write([]byte(desc)); err != nil {
		f.Close() // ignore error; Write error takes precedence
		log.Fatal(err)
	}
	if err := f.Close(); err != nil {
		log.Fatal(err)
	}
}

// https://leetcode.com/api/problems/algorithms/
func main() {
	// Create a new collector
	c := colly.NewCollector(
		colly.MaxDepth(2),
		colly.Async(true), // Enable asynchronous scraping
	)
	c.Limit(&colly.LimitRule{DomainGlob: "*", Parallelism: 2})

	// Set up event listeners

	// Step 1: OnRequest - Called before a request is made
	c.OnRequest(func(r *colly.Request) {
		// Add headers to mimic a browser request
		// r.Headers.Set("User-Agent", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3")
		r.Headers.Set("User-Agent", "Chrome/125.0.6422.142")
		// You can add mre headers if needed
		fmt.Println("Visiting", r.URL.String())
	})

	c.WithTransport(&http.Transport{
		DisableKeepAlives: true,
	})

	// Step 2: OnError - Called if an error occurs during the request
	c.OnError(func(r *colly.Response, err error) {
		fmt.Println("Request URL:", r.Request.URL, "failed with response:", string(r.Body), "\nError:", err)
	})

	// Set up event listeners
	// c.OnHTML("meta[name=description]", func(e *colly.HTMLElement) {
	c.OnHTML("div.elfjS", func(e *colly.HTMLElement) {
		description := e.Attr("content")
		fmt.Println("Problem description:", description)
	})
	// Step 3: OnHTML - Called right after OnResponse if the received content is HTML
	c.OnHTML("meta[name=description]", func(e *colly.HTMLElement) {
		description := e.Attr("content")
		fmt.Println("Problem description:", description)
	})

	// Define the URL to crawl
	url := "https://leetcode.com/problems/two-sum/description/"

	// Start scraping
	c.Visit(url)

	// Wait until all threads are finished
	c.Wait()

	// Write(Append) to file
	//defer WriteToFile(problem, result)
}
