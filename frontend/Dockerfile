# ---- Build Stage ----
# Use a specific version of Node.js for reproducibility
FROM node:20-alpine as build

# Set the working directory inside the container
WORKDIR /app

# Copy package.json and package-lock.json (if it exists)
# This allows us to leverage Docker's layer caching for dependencies
COPY package*.json ./

# Install dependencies. `npm ci` is generally recommended for CI/CD environments
# as it installs exact versions from package-lock.json.
RUN npm install

# Copy the rest of the application's source code
COPY . .

# Build the React application for production
# The output will be in the /app/dist directory
RUN npm run build


# ---- Serve Stage ----
# Use a lightweight Nginx image to serve the static files
FROM nginx:1.25-alpine

# Copy the static assets from the build stage to the Nginx html directory
COPY --from=build /app/dist /usr/share/nginx/html

# Copy our custom Nginx configuration
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Expose port 80 for the Nginx server
EXPOSE 80

# The default command for the nginx image is to start the server.
# This command makes it explicit and keeps the container running in the foreground.
CMD ["nginx", "-g", "daemon off;"]
