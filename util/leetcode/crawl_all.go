package main

import (
	"fmt"

	"github.com/gocolly/colly/v2"
)

func main() {
	// Create a new collector
	c := colly.NewCollector(
		colly.Async(true), // Enable asynchronous scraping
	)

	// Set up event listeners

	// Step 1: OnRequest - Called before a request is made
	c.OnRequest(func(r *colly.Request) {
		// Add headers to mimic a browser request
		r.Headers.Set("User-Agent", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3")
		// You can add more headers if needed
		fmt.Println("Visiting", r.URL.String())
	})

	// Step 2: OnError - Called if an error occurs during the request
	c.OnError(func(r *colly.Response, err error) {
		fmt.Println("Request URL:", r.Request.URL, "failed with response:", string(r.Body), "\nError:", err)
	})

	// Set up event listeners
	c.OnHTML("meta[name=description]", func(e *colly.HTMLElement) {
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
	c.Visit(url)

	// Wait until all threads are finished
	c.Wait()
}
