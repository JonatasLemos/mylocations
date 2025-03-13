    FROM node:16-alpine

    WORKDIR /app

    COPY package*.json ./

    RUN npm install

    COPY . .

    RUN chmod -R 777 /app/node_modules
    
    USER node

    EXPOSE 3000
    
    CMD ["npm", "start"]