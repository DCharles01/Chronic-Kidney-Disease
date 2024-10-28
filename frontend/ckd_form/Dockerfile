# Stage 1: Build the React app
FROM node:16 as build

# Set working directory
WORKDIR /app

# Copy package.json and package-lock.json to the working directory
COPY package*.json ./

# Install dependencies
RUN npm install

# Copy the rest of the application code to the working directory
COPY . .

# Build the app for production
RUN npm run build

# Stage 2: Serve the app with nginx
FROM nginx:alpine

# Copy the build output to nginx's web directory
COPY --from=build /app/build /usr/share/nginx/html

# Expose port 8080 to the Docker host
EXPOSE 8080

# Start nginx server
CMD ["nginx", "-g", "daemon off;"]
