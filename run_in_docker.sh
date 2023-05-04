if ! docker stop option_pricing_api_container ; then
   echo "There is no running container, go to container removing step"
fi

if ! docker rm option_pricing_api_container ; then
   echo "The container does not exist, safe to create a new container"
fi

docker build -t option_pricing_api_image .
docker run -d --name option_pricing_api_container -p 8000:8000 option_pricing_api_image
