# FROM node:20-alpine

# # Create app directory
# WORKDIR /app

# # Copy package.json and package-lock.json
# COPY package*.json ./

# # Install dependencies as root
# RUN npm install

# # Copy rest of the source
# COPY . .

# # Make sure the container user owns the app folder (optional)
# RUN chown -R node:node /app

# # Use non-root user
# USER node

# EXPOSE 3000

# CMD ["npm", "run", "dev"]


FROM node:20-bullseye

WORKDIR /app

# Copy package files and install deps
COPY package*.json ./
RUN npm install

# Copy code
COPY . .

EXPOSE 3000

# Default to dev mode
CMD ["npm", "run", "dev"]

