package main

import (
	"context"
	"fmt"
	"log"

	"google.golang.org/api/compute/v1"
	"google.golang.org/api/option"
	"google.golang.org/api/transport"
	"google.golang.org/grpc"
	"google.golang.org/grpc/credentials"
)

func main() {
	ctx := context.Background()

	// Replace with your GCP project ID and desired zone
	projectID := "poised-cortex-422112-g5"
	zone := "asia-northeast3-a"

	// Initialize the Compute Engine client
	creds, err := transport.Creds(ctx, option.WithCredentialsFile("gcp-sa-key.json"))
	if err != nil {
		log.Fatalf("Error creating credentials: %v", err)
	}
	conn, err := grpc.Dial("compute.googleapis.com:443", grpc.WithTransportCredentials(credentials.NewClientTLSFromCert(nil, "")))
	if err != nil {
		log.Fatalf("Error connecting to Compute Engine: %v", err)
	}
	client, err := compute.NewInstancesRESTClient(ctx, option.WithGRPCConn(conn), option.WithCredentials(creds))
	if err != nil {
		log.Fatalf("Error creating Compute Engine client: %v", err)
	}

	// Define the VM instance configuration
	instance := &compute.Instance{
		Name:        "my-vm-instance",
		MachineType: fmt.Sprintf("zones/%s/machineTypes/n1-standard-1", zone),
		NetworkInterfaces: []*compute.NetworkInterface{
			{
				Network: "global/networks/default",
				AccessConfigs: []*compute.AccessConfig{
					{
						Name: "External NAT",
						Type: "ONE_TO_ONE_NAT",
					},
				},
			},
		},
		Tags: &compute.Tags{
			Items: []string{"allow-ssh"},
		},
		Metadata: &compute.Metadata{
			Items: []*compute.MetadataItems{
				{
					Key:   "startup-script",
					Value: "#!/bin/bash\necho 'Hello, World!' > /tmp/hello.txt",
				},
			},
		},
	}

	// Insert the instance in the specified project and zone
	op, err := client.Insert(ctx, projectID, zone, instance)
	if err != nil {
		log.Fatalf("Error creating VM instance: %v", err)
	}

	// Wait for the operation to complete
	if _, err := op.Wait(ctx); err != nil {
		log.Fatalf("Error waiting for operation: %v", err)
	}

	fmt.Println("VM instance created successfully!")
}
