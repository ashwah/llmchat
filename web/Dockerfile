FROM node:14

# Set the working directory inside the container
WORKDIR /app

# # Copy package.json and package-lock.json
# COPY package*.json ./
COPY . .

# # Install dependencies
RUN npm install

# Expose port 3000
EXPOSE 3000

# Command to run the application
CMD ["npm", "start"]