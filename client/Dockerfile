# pull official node base image
FROM node:15.8.0-alpine3.12 as build
WORKDIR /app
ENV PATH /app/node_modules/.bin:$PATH
COPY package.json ./
COPY package-lock.json ./
RUN npm ci --silent
RUN npm install react-scripts@3.4.1 -g --silent
COPY . ./
RUN npm run build

# production environment
FROM nginx:1.19.6-alpine
COPY --from=build /app/build /usr/share/nginx/html
COPY nginx/nginx.conf /etc/nginx/conf.d/default.conf

# Copy env_vars file and shell script to container
WORKDIR /usr/share/nginx/html
COPY env.sh .
COPY env_vars .

RUN apk add --no-cache bash
RUN chmod +x env.sh

EXPOSE 80
CMD ["/bin/bash", "-c", "/usr/share/nginx/html/env.sh && nginx -g \"daemon off;\""]
