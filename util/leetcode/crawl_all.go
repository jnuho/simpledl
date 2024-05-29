package main

import (
	"fmt"
	"sort"

	"github.com/gocolly/colly/v2"
)

func main() {

	// 새로운 Collector 생성
	c := colly.NewCollector()
	// c := colly.NewCollector(
	// 	colly.MaxDepth(2),
	// 	colly.Async(),
	// )
	// c.Limit(&colly.LimitRule{DomainGlob: "*", Parallelism: 2})
	//var result string

	url := "https://leetcode.com/problems"
	// url := "https://leetcode.com/problemset/all?page=2"
	//https://leetcode.com/problems
	//div role = "row"
	//	div role="cell"[1]
	// 5번쨰 child a.href
	//	/problems/two-sum
	//url += problem

	problems := make(map[int]string)

	// a 태그의 href 속성을 찾아 모든 링크 방문
	c.OnHTML("a[href]", func(e *colly.HTMLElement) {
		link := e.Attr("href")
		fmt.Printf("Link found: %q -> %s\n", e.Text, link)
		c.Visit(e.Request.AbsoluteURL(link))

		// pos := strings.Index(e.Text, ".")
		// idx, _ := strconv.Atoi(e.Text[:pos])

		// problems[idx] = "https://leetcode.com" + e.Attr("href")

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

	// Request 이벤트 핸들러
	c.OnRequest(func(r *colly.Request) {
		fmt.Println("Visiting", r.URL)
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
	//defer WriteToFile(problem, result)
}
