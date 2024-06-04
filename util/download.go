package main

import (
	"bufio"
	"context"
	"fmt"
	"io"
	"net/http"
	"os"
	"strings"
	"sync"
	"time"
	// "github.com/vbauerster/mpb/v7"
	// "github.com/vbauerster/mpb/v7/decor"
)

// func downloadImage(ctx context.Context, url string, wg *sync.WaitGroup, p *mpb.Progress) {
func downloadImage(ctx context.Context, url string, animal string, idx int, wg *sync.WaitGroup) error {
	defer func() {
		fmt.Printf("[%d], [%s]...done\n", idx, url)
		wg.Done()
	}()

	select {
	case <-ctx.Done():
		return nil
	default:
		response, err := http.Get(url)

		if err != nil {
			// err = fmt.Errorf("failed to download: %s, error: %v", url, err)
			// fmt.Println(err)
			return nil
		}

		if response.StatusCode != http.StatusOK {
			// err = fmt.Errorf("http request failed with status code %d", response.StatusCode)
			return nil
		}
		contentType := response.Header.Get("Content-Type")
		if !strings.HasPrefix(contentType, "image/") {
			// err = fmt.Errorf("url does not point to an image: %s", url)
			return nil
		}
		defer response.Body.Close()

		fileName := fmt.Sprintf("%s_%d.jpg", animal, idx)
		// fileName := strings.Split(url, "/")[len(strings.Split(url, "/"))-1]
		file, err := os.Create("./data/" + animal + "s/" + fileName)
		if err != nil {
			err = fmt.Errorf("failed to create file: %s, error: %v", fileName, err)
			fmt.Println(err)
			return err
		}
		defer file.Close()

		/** Progress bar */
		// bar := p.AddBar(response.ContentLength,
		// 	mpb.PrependDecorators(
		// 		decor.CountersKibiByte("% .2f / % .2f"),
		// 	),
		// 	mpb.AppendDecorators(
		// 		decor.EwmaETA(decor.ET_STYLE_MMSS, 60),
		// 	),
		// )
		// reader := bar.ProxyReader(response.Body)
		_, err = io.Copy(file, response.Body)
		// _, err = io.Copy(file, reader)
		if err != nil {
			err = fmt.Errorf("failed to save file: %s, error: %v", fileName, err)
			os.Remove("./data/" + animal + "s/" + fileName)
			return err
		}

		return nil
	}
}

func getImageUrls(ctx context.Context, url string) ([]string, error) {
	req, err := http.NewRequestWithContext(ctx, http.MethodGet, url, nil)
	if err != nil {
		return nil, err
	}

	resp, err := http.DefaultClient.Do(req)
	if err != nil {
		return nil, err
	}
	defer resp.Body.Close()

	scanner := bufio.NewScanner(resp.Body)
	var urls []string
	for scanner.Scan() {
		urls = append(urls, scanner.Text())
	}

	if err := scanner.Err(); err != nil {
		return nil, err
	}

	return urls, nil
}

// Function to create a directory if it does not exist
func createDirIfNotExist(dir string) error {
	if _, err := os.Stat(dir); os.IsNotExist(err) {
		err = os.MkdirAll(dir, 0755)
		if err != nil {
			return err
		}
	}
	return nil
}

func main() {
	ctx, cancel := context.WithTimeout(context.Background(), 5*time.Second)
	defer cancel()

	animal := "dog"
	listUrl := ""
	if animal == "cat" {
		listUrl = "https://raw.githubusercontent.com/asharov/cute-animal-detector/master/data/kitty-urls.txt"
	} else if animal == "dog" {
		listUrl = "https://raw.githubusercontent.com/iblh/not-cat/master/urls/not-cat/dog-urls.txt"
	}

	urls, err := getImageUrls(ctx, listUrl)
	if err != nil {
		fmt.Println(err)
		os.Exit(1)
	}

	// Now 'urls' contains the list of URLs
	fmt.Println(len(urls))

	// Create the directory if it does not exist
	dir := fmt.Sprintf("./data/%s/", animal+"s")
	err = createDirIfNotExist(dir)
	if err != nil {
		fmt.Println("Failed to create directory:", dir, "Error:", err)
		os.Exit(1)
	}

	// Create a WaitGroup to wait for all goroutines to finish
	var wg sync.WaitGroup

	// Create a channel to handle errors
	errs := make(chan error)

	// Download each image concurrently
	for i, url := range urls {
		wg.Add(1)

		// Initialize the progress bar
		// p := mpb.New(mpb.WithWidth(64))
		// go downloadImage(ctx, url, &wg, p)
		// go downloadImage(ctx, url, i, &wg)
		go func(ctx context.Context, url string, animal string, i int, wg *sync.WaitGroup) {
			// defer wg.Done()
			if err := downloadImage(ctx, url, animal, i, wg); err != nil {
				errs <- err
			}
		}(ctx, url, animal, i, &wg)
		//
		// Wait for all progress bars to finish
		// p.Wait()
	}

	// Wait for all downloads to finish
	wg.Wait()

	// close channel
	close(errs)

	// Print all errors
	for err := range errs {
		if err != nil {
			fmt.Println(err)
		}
	}
}
