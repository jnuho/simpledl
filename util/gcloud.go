package main

import (
	"context"
	"fmt"
	"log"

	"google.golang.org/api/compute/v1"
	"google.golang.org/api/option"
)

func main() {
	ctx := context.Background()

	// Project ID and zone for the VM
	projectID := "your-project-id"
	zone := "us-central1-a"

	// Authentication using service account key file
	computeService, err := compute.NewService(ctx, option.WithCredentialsFile("path/to/your-service-account-key.json"))
	if err != nil {
		log.Fatalf("Failed to create compute service: %v", err)
	}

	// Define the instance
	instance := &compute.Instance{
		Name:        "test-instance",
		MachineType: fmt.Sprintf("zones/%s/machineTypes/n1-standard-1", zone),
		Disks: []*compute.AttachedDisk{
			{
				Boot:       true,
				AutoDelete: true,
				InitializeParams: &compute.AttachedDiskInitializeParams{
					DiskName:    "test-disk",
					SourceImage: "projects/debian-cloud/global/images/family/debian-10",
				},
			},
		},
		NetworkInterfaces: []*compute.NetworkInterface{
			{
				Network: "global/networks/default",
				AccessConfigs: []*compute.AccessConfig{
					{
						Type: "ONE_TO_ONE_NAT",
						Name: "External NAT",
					},
				},
			},
		},
	}

	// Insert the instance
	op, err := computeService.Instances.Insert(projectID, zone, instance).Context(ctx).Do()
	if err != nil {
		log.Fatalf("Could not create instance: %v", err)
	}

	fmt.Printf("Instance creation started: %s\n", op.Name)
}
