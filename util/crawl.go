package main

import (
	"fmt"
	"log"
	"net/http"
	"os"
	"strings"
	"time"

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

// Go Colly (version 2) is a powerful scraping library for Golang,
// but it operates at the HTTP level and can parse static HTML documents.
// Unfortunately, it does not execute JavaScript.
// As a result, it cannot handle Client-Side Rendered (CSR/JS) websites directly.
// When dealing with JavaScript-enabled websites, combine go Colly with a Headless Browser
// https://leetcode.com/api/problems/algorithms/
func main() {
	// Create a new collector
	c := colly.NewCollector(
		// colly.MaxDepth(2),
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
		fmt.Println("Request URL:", r.Request.URL, "[status code:", r.StatusCode, "]. failed with response:", string(r.Body), "\nError:", err)
	})

	// Set up event listeners
	// c.OnHTML("meta[name=description]", func(e *colly.HTMLElement) {
	c.OnHTML("div#qd-content", func(e *colly.HTMLElement) {
		fmt.Println(e)
		// description := e.Attr("content")
		// fmt.Println("Problem description:", description)
	})
	dates := make(chan string)
	titles := make(chan string)
	// Step 3: OnHTML - Called right after OnResponse if the received content is HTML
	// c.OnHTML("meta[name=description]", func(e *colly.HTMLElement) {
	// c.OnHTML("a.d-block", func(e *colly.HTMLElement) {
	c.OnHTML("div.fight-date", func(e *colly.HTMLElement) {
		// description := e.Attr("content")
		// fmt.Println("Problem description:", description)
		// fmt.Println(len(e))
		dates <- e.Text
		// fmt.Println(e.Text)
	})
	c.OnHTML("div.fight-title", func(e *colly.HTMLElement) {
		// description := e.Attr("content")
		// fmt.Println("Problem description:", description)
		// fmt.Println(len(e))
		titles <- strings.Trim(e.Text, " ")
		// fmt.Println(title)
	})
	// Wait until all threads are finished
	c.Wait()

	// Define the URL to crawl
	// url := "https://leetcode.com/problems/two-sum/description/"
	url := "https://www.boxingscene.com/schedule"

	go func() {
		for title := range titles {
			fmt.Println(title)
		}
		for date := range dates {
			fmt.Println(date)
		}
	}()
	// Start scraping
	c.Visit(url)
	// Now let's use chromedp to get the rendered HTML
	// ctx, cancel := chromedp.NewContext(context.Background())
	// defer cancel()

	// var htmlContent string
	// err := chromedp.Run(ctx,
	// 	// chromedp.Navigate(startURL),
	// 	chromedp.OuterHTML("html", &htmlContent),
	// )
	// if err != nil {
	// 	log.Fatal(err)
	// }

	// Now you can process the rendered HTML using Colly
	// (e.g., extract data from <div> elements, etc.)
	// fmt.Println("Rendered HTML content:", htmlContent)

	// Wait for a few seconds to allow Colly to finish its work
	time.Sleep(5 * time.Second)
	// Write(Append) to file
	//defer WriteToFile(problem, result)
}
