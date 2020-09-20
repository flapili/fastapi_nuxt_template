FROM node:12.18.3-alpine3.9

WORKDIR /app
ADD src/frontend/package.json /app


RUN yarn

ADD src/frontend /app
RUN ["yarn", "run", "build", "--modern=client"]

ENTRYPOINT ["yarn", "run", "start"]
# FROM nginx:1.19.1-alpine
# COPY --from=0 /app/dist /usr/share/nginx/html