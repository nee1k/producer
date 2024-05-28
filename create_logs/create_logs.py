import docker
import os
import json
import tarfile
import io

# Initialize Docker client
client = docker.from_env()

# Define the volume name and file paths
volume_name = "icicle"
cpu_file_path = "cpu.json"  # Local path to cpu.json
metadata_file_path = "metadata.json"  # Local path to metadata.json

# Ensure the volume exists
try:
    volume = client.volumes.get(volume_name)
except docker.errors.NotFound:
    volume = client.volumes.create(name=volume_name)

# Create a temporary container with the volume mounted
container = client.containers.run(
    "busybox",
    "sh -c 'sleep 3600'",
    name="temp-container",
    volumes={volume_name: {'bind': '/mnt', 'mode': 'rw'}},
    detach=True
)

# Utility function to create a tar archive of the file
def create_tar(file_path):
    tar_stream = io.BytesIO()
    with tarfile.open(fileobj=tar_stream, mode='w') as tar:
        tar.add(file_path, arcname=os.path.basename(file_path))
    tar_stream.seek(0)
    return tar_stream

# Create the tar archive of cpu.json file
cpu_tar_data = create_tar(cpu_file_path)
print(f"Created tar archive for {cpu_file_path}")

# Copy the cpu.json file into the container
container.put_archive("/mnt/app/logs", cpu_tar_data)
print(f"Copied {cpu_file_path} to /mnt/app/logs in container")

# Create the tar archive of metadata.json file
metadata_tar_data = create_tar(metadata_file_path)
print(f"Created tar archive for {metadata_file_path}")

# Copy the metadata.json file into the container
container.put_archive("/mnt/app/logs", metadata_tar_data)
print(f"Copied {metadata_file_path} to /mnt/app/logs in container")

# Clean up: stop and remove the container
container.stop()
container.remove()

print(f"Files {cpu_file_path} and {metadata_file_path} have been copied to volume {volume_name}.")
