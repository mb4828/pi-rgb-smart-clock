docker run -d -p 5500:5500 --name pi-rgb-smart-clock --restart unless-stopped --device=/dev/hidraw1 --privileged pi-rgb-smart-clock
