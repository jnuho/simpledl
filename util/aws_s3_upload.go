package main

import (
	"context"
	"fmt"
	"log"
	"os"

	"github.com/aws/aws-sdk-go-v2/config"
	"github.com/aws/aws-sdk-go-v2/service/s3"
	"github.com/aws/aws-sdk-go/aws"
	"github.com/joho/godotenv"
)

func loadEnv() error {
	err := godotenv.Load(".env")
	if err != nil {
		return err
	}
}

func main() {
	// Load .env
	err := loadEnv()
	if err != nil {
		log.Fatalf("Error loading .env file\n")
	}

	// Load AWS SDK configuration
	// sdkConfig, err := config.LoadDefaultConfig(context.TODO())
	sdkConfig, err := config.LoadDefaultConfig(context.TODO(), config.WithSharedConfigProfile("default"))
	if err != nil {
		fmt.Println("Couldn't load default configuration. Have you set up your AWS account?")
		fmt.Println(err)
		return
	}

	// Initialize S3 client
	s3Client := s3.NewFromConfig(sdkConfig)

	// Specify your S3 bucket and image file details
	bucketName := os.Getenv("aws_s3_bucket")
	fileName := "worker_pool_pattern.drawio.png"
	filePath := os.Getenv("aws_s3_local_path") + fileName
	objectKey := fileName

	// Open the local image file
	file, err := os.Open(filePath)
	if err != nil {
		fmt.Println("Error opening local file:", err)
		return
	}
	defer file.Close()

	// Upload the image to S3
	_, err = s3Client.PutObject(context.TODO(), &s3.PutObjectInput{
		Bucket: &bucketName,
		Key:    &objectKey,
		Body:   file,
		// ContentType: aws.String("image/jpeg"), // Set the content type appropriately
		ContentType: aws.String("image/png"), // Set the content type appropriately
	})
	if err != nil {
		fmt.Println("Error uploading image to S3:", err)
		return
	}

	fmt.Println("Image uploaded successfully!")
}
