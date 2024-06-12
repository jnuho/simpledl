package main

import (
	"fmt"
	"sync"
)

func worker(workerId int, jobs <-chan int, results chan<- int) {
	for job := range jobs {
		results <- job
		fmt.Printf("worker(%d) is doing job-%d\n", workerId, job)
	}
}

func main() {
	// 3 goroutines(workers) on 10 jobs and 10 results
	numOfWorkers := 3
	numOfJobs := 10

	jobs := make(chan int, numOfJobs)
	results := make(chan int, numOfJobs)

	var wg sync.WaitGroup

	// pool of workers
	for i := 1; i <= numOfWorkers; i++ {
		wg.Add(1)
		// consume jobs -> results
		go func(workerId int) {
			defer wg.Done()
			worker(workerId, jobs, results)
		}(i)
	}

	// produce jobs
	for i := 1; i <= numOfJobs; i++ {
		jobs <- i
	}
	close(jobs)

	go func() {
		wg.Wait()
		close(results)
	}()

	// read results
	for result := range results {
		fmt.Printf("reading result: job-%d\n", result)
	}
}
