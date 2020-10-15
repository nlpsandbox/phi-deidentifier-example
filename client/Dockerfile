FROM rocker/shiny:4.0.3

# Safer bash scripts with 'set -euxo pipefail'
SHELL ["/bin/bash", "-euxo", "pipefail", "-c"]

# Install dependencies
# hadolint ignore=DL3008
RUN apt-get update -qq -y \
    && apt-get install --no-install-recommends -qq -y \
        libxml2-dev \
        libcairo2-dev \
        libsqlite3-dev \
        libmariadbd-dev \
        libpq-dev \
        libssh2-1-dev \
        unixodbc-dev \
        libcurl4-openssl-dev \
        libssl-dev \
    && apt-get -y autoclean \
    && apt-get -y autoremove \
    && rm -rf /var/lib/apt/lists/*

# Copy app files
COPY /shiny-app/renv.lock ./renv.lock
COPY /shiny-app ./app

# Install renv & restore packages
RUN Rscript -e 'install.packages("renv")'
RUN Rscript -e 'renv::restore()'

EXPOSE 3838

# TODO: replace by s6 init script
CMD ["R", "-e", "shiny::runApp('/app', host = '0.0.0.0', port = 3838)"]