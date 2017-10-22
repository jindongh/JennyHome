FROM node:8

# Install chromium
RUN apt-get update \
	&& wget http://launchpadlibrarian.net/341807203/chromium-browser_62.0.3202.62-0ubuntu0.14.04.1204_armhf.deb \
	&& dpkg -i --force-depends chromium-browser_62.0.3202.62-0ubuntu0.14.04.1204_armhf.deb \
	&& apt-get install -f -y \
	&& dpkg -i --force-depends chromium-browser_62.0.3202.62-0ubuntu0.14.04.1204_armhf.deb \
	&& wget http://launchpadlibrarian.net/341807199/chromium-codecs-ffmpeg-extra_62.0.3202.62-0ubuntu0.14.04.1204_armhf.deb \
	&& dpkg -i chromium-codecs-ffmpeg-extra_62.0.3202.62-0ubuntu0.14.04.1204_armhf.deb


# Copy files
COPY . /home/node/
RUN chown -R node:node /home/node

# Install nodejs lib.
USER node
WORKDIR /home/node/
ENV PUPPETEER_SKIP_CHROMIUM_DOWNLOAD true
ENV PUPPETEER_DEFAULT_CHROMIUM=/usr/bin/chromium-browser
RUN npm install

EXPOSE 10000

CMD ["npm", "start"]
