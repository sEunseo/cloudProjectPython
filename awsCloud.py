import boto3
from botocore.exceptions import NoCredentialsError, PartialCredentialsError
import sys

# Initialize AWS EC2 Client
def init():
    try:
        ec2 = boto3.client('ec2', region_name='us-east-1')
        return ec2
    except (NoCredentialsError, PartialCredentialsError) as e:
        print("Cannot load the credentials. Make sure your AWS CLI is configured.")
        sys.exit(1)

# List all instances
def list_instances(ec2):
    print("Listing instances....")
    response = ec2.describe_instances()
    for reservation in response['Reservations']:
        for instance in reservation['Instances']:
            print(
                f"[id] {instance['InstanceId']}, "
                f"[AMI] {instance['ImageId']}, "
                f"[type] {instance['InstanceType']}, "
                f"[state] {instance['State']['Name']}, "
                f"[monitoring state] {instance['Monitoring']['State']}"
            )

# List available zones
def available_zones(ec2):
    print("Available zones....")
    try:
        response = ec2.describe_availability_zones()
        for zone in response['AvailabilityZones']:
            print(f"[id] {zone['ZoneId']}, [region] {zone['RegionName']}, [zone] {zone['ZoneName']}")
        print(f"You have access to {len(response['AvailabilityZones'])} Availability Zones.")
    except Exception as e:
        print(f"Error: {e}")

# Start an instance
def start_instance(ec2, instance_id):
    try:
        print(f"Starting instance {instance_id}...")
        ec2.start_instances(InstanceIds=[instance_id])
        print(f"Successfully started instance {instance_id}.")
    except Exception as e:
        print(f"Error: {e}")

# Stop an instance
def stop_instance(ec2, instance_id):
    try:
        print(f"Stopping instance {instance_id}...")
        ec2.stop_instances(InstanceIds=[instance_id])
        print(f"Successfully stopped instance {instance_id}.")
    except Exception as e:
        print(f"Error: {e}")

# Reboot an instance
def reboot_instance(ec2, instance_id):
    try:
        print(f"Rebooting instance {instance_id}...")
        ec2.reboot_instances(InstanceIds=[instance_id])
        print(f"Successfully rebooted instance {instance_id}.")
    except Exception as e:
        print(f"Error: {e}")

# List available regions
def available_regions(ec2):
    print("Available regions....")
    try:
        response = ec2.describe_regions()
        for region in response['Regions']:
            print(f"[region] {region['RegionName']}, [endpoint] {region['Endpoint']}")
    except Exception as e:
        print(f"Error: {e}")

# Create an instance
def create_instance(ec2, ami_id):
    try:
        print(f"Creating an instance with AMI {ami_id}...")
        response = ec2.run_instances(
            ImageId=ami_id,
            InstanceType='t2.micro',
            MinCount=1,
            MaxCount=1
        )
        instance_id = response['Instances'][0]['InstanceId']
        print(f"Successfully created instance {instance_id} based on AMI {ami_id}.")
    except Exception as e:
        print(f"Error: {e}")

# List images
def list_images(ec2):
    print("Listing images....")
    try:
        # Retrieve images owned by the user (self) or public images as a fallback
        response = ec2.describe_images(Owners=['self'])
        
        # Display the images if found
        if 'Images' in response and response['Images']:
            for image in response['Images']:
                print(f"[ImageID] {image['ImageId']}, [Name] {image.get('Name', 'N/A')}, [Owner] {image['OwnerId']}")
        else:
            print("No images found.")
    except Exception as e:
        print(f"Error while listing images: {e}")


def main():
    ec2 = init()
    while True:
        print("\n" + "------------------------------------------------------------")
        print("  1. List instances              2. Available zones")
        print("  3. Start instance              4. Available regions")
        print("  5. Stop instance               6. Create instance")
        print("  7. Reboot instance             8. List images")
        print("                                99. Quit")
        print("------------------------------------------------------------")


        choice = input("Enter an integer: ")
        if not choice.isdigit():
            print("Invalid input. Please enter a number.")
            continue

        choice = int(choice)
        if choice == 1:
            list_instances(ec2)
        elif choice == 2:
            available_zones(ec2)
        elif choice == 3:
            instance_id = input("Enter instance ID: ").strip()
            if instance_id:
                start_instance(ec2, instance_id)
        elif choice == 4:
            available_regions(ec2)
        elif choice == 5:
            instance_id = input("Enter instance ID: ").strip()
            if instance_id:
                stop_instance(ec2, instance_id)
        elif choice == 6:
            ami_id = input("Enter AMI ID: ").strip()
            if ami_id:
                create_instance(ec2, ami_id)
        elif choice == 7:
            instance_id = input("Enter instance ID: ").strip()
            if instance_id:
                reboot_instance(ec2, instance_id)
        elif choice == 8:
            list_images(ec2)
        elif choice == 99:
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()







# condor_status function
