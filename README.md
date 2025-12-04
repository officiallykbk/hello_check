# Navigate to your project directory
cd c:\Users\user\Desktop\CiCdTry

# Build the Docker image
docker build -t fastapi-app .

# Run the container
docker run -d -p 8000:8000 --name my-fastapi-app fastapi-app