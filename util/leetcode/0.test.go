package main

import (
	"fmt"
	"os"
	"os/signal"
	"syscall"
	"time"
)

func main() {
	c := make(chan int)
	// Both producer and consumer goroutine do not have to coexist
	// i.e. even if the producer goroutine finishes (and closes the channel),
	// the consumer goroutine range loop will receive all the values.

	// producer
	go func() {
		for i := 0; i < 5; i++ {
			c <- i
			time.Sleep(1 * time.Second)
		}
		// Without closing channel, the consumer will wait indefinitely for channel
		close(c)
		fmt.Println("producer finished.")
	}()

	// consumer
	go func() {
		for i := range c {
			fmt.Printf("consumer gets i = %d\n", i)
		}
		fmt.Println("consumer finished. press ctrl+c to exit")
	}()

	e := make(chan os.Signal)
	signal.Notify(e, syscall.SIGINT, syscall.SIGTERM)
	<-e
}
