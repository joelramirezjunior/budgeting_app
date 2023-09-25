# Use an official Node runtime as a parent image
FROM node:14

# Set working directory
WORKDIR /usr/src/app


# Set environment variables
ENV LANG C.UTF-8
ENV LC_ALL C.UTF-8

# Install dependencies
COPY package.json .
RUN npm install

# Copy the current directory contents into the container
COPY . .

# Build and run the application
CMD ["npm", "start"]
