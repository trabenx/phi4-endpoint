FROM node:18
WORKDIR /app
COPY package.json package-lock.json ./
RUN npm ci
# Copy the rest of the source code
COPY . ./
CMD ["npm", "start"]