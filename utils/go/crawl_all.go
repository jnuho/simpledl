package main

import (
	"fmt"
	"log"
	"os"
	"sort"
	"strconv"
	"strings"

	"github.com/gocolly/colly/v2"
)

func main() {

	c := colly.NewCollector(
		colly.MaxDepth(2),
		colly.Async(),
	)
	c.Limit(&colly.LimitRule{DomainGlob: "*", Parallelism: 2})
	//var result string

	//url := "https://leetcode.com/problems"
	url := "https://leetcode.com/problemset/all?page=2"
	//https://leetcode.com/problems
	//div role = "row"
	//	div role="cell"[1]
	// 5번쨰 child a.href
	//	/problems/two-sum
	//url += problem

	problems := make(map[int]string)

	c.OnHTML("div.truncate a", func(e *colly.HTMLElement) {

		pos := strings.Index(e.Text, ".")
		idx, _ := strconv.Atoi(e.Text[:pos])

		problems[idx] = "https://leetcode.com" + e.Attr("href")

		//problems[idx] = "https://leetcode.com" + e.Attr("href")
		//result = "/**\n" + url + "\n\n" + result + "\n*/\n"

		//result += "package main\n\n"
		//result += "import (\n"
		//result += "	\"fmt\"\n"
		//result += ")\n\n"
		//result += "func main() {\n"
		//result += "	\n"
		//result += "}"
	})

	// Start scraping
	c.Visit(url)

	// Wait until threads are finished
	c.Wait()
	keys := make([]int, 0)
	for k := range problems {
		keys = append(keys, k)
	}
	sort.Ints(keys)

	for _, i := range keys {
		//fmt.Println(i, problems[i])
		//fmt.Printf("%d-%s\n", i, problems[i])
		fmt.Printf("%d %s\n", i, problems[i])
	}
	// Write(Append) to file
	//defer writeToFile(problem, result)
}

// problem: 문제번호
// desc: 문제설명
func writeToFile(problem, desc string) {
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
