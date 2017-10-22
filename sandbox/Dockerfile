FROM node:8
WORKDIR /web

COPY package.json .
RUN npm install

COPY . .

EXPOSE 8888

CMD ["npm", "start"]
