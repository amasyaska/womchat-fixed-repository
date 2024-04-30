# Load postgres image
FROM node:20

# Set the working directory in the container
WORKDIR /app

# Copy the code into the container
COPY . .

# Install dependencies
RUN npm install

# Build the app
RUN npm run build

# Expose port
EXPOSE 3000

# Run the command to start the app
CMD ["npm", "run", "dev", "--", "--port", "3000"]
