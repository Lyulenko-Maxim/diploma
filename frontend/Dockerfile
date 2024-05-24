FROM node:18.20-alpine as builder

WORKDIR /app

COPY package.json yarn.lock ./

RUN yarn install --frozen-lockfile

COPY . .

ARG DEBUG
RUN if [ "$DEBUG" = "1" ]; \
    then yarn dev; \
    else yarn build; \
    fi

FROM node:18.20-alpine

WORKDIR /app

COPY --from=builder /app/package.json /app/yarn.lock ./
COPY --from=builder /app/.next ./.next

RUN yarn install --frozen-lockfile --production

EXPOSE 3000

CMD ["yarn", "start"]