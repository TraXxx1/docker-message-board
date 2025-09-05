FROM node:24-alpine
WORKDIR /app
RUN apk add --no-cache curl
COPY ./package.json .
RUN npm install 
COPY ./public /app/public
COPY ./server.js .
CMD [ "npm","start" ]



