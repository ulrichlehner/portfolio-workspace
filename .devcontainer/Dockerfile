# Dev environment for Portfolio Performance: Java 21 and Maven as used by upstream CI,
# plus Node.js and the OpenSpec CLI for spec-driven planning.
FROM maven:3.9-eclipse-temurin-21

RUN apt-get update \
    && apt-get install -y --no-install-recommends git \
    && rm -rf /var/lib/apt/lists/*

# Node.js from the official image (OpenSpec needs Node.js 20.19 or newer)
COPY --from=node:22-slim /usr/local/bin/node /usr/local/bin/node
COPY --from=node:22-slim /usr/local/lib/node_modules /usr/local/lib/node_modules
RUN ln -s /usr/local/lib/node_modules/npm/bin/npm-cli.js /usr/local/bin/npm \
    && ln -s /usr/local/lib/node_modules/npm/bin/npx-cli.js /usr/local/bin/npx

# keep in sync with the version in the generated skills (openspec update after upgrading)
ARG OPENSPEC_VERSION=1.14.3
RUN npm install -g "@fission-ai/openspec@${OPENSPEC_VERSION}" && npm cache clean --force

ENV MAVEN_OPTS=-Xmx4g \
    OPENSPEC_TELEMETRY=0
