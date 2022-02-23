FROM node:14-alpine

WORKDIR /app 

COPY ./package.json ./

COPY ./package-lock.json ./

RUN npm install 

COPY . .

EXPOSE 2456

ENTRYPOINT [ "npm" ]

CMD ["start"]