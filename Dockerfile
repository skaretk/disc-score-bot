FROM python:3.9.6

# Install Google Chrome #

# 1. Adding trusting keys to apt for repositories
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -

# 2. Adding Google Chrome to the repositories
RUN sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list'

# 3. Updating apt to see and install Google Chrome
RUN apt-get -y update

# 4. Install google-chrome-stable
RUN apt-get install -y google-chrome-stable

# Install Chrome Driver #

# 1. Installing Unzip
RUN apt-get install -yqq unzip

# 2. Download the Chrome Driver, unzip and remove the .zip from the image
RUN wget -O /tmp/chromedriver.zip http://chromedriver.storage.googleapis.com/`curl -sS chromedriver.storage.googleapis.com/LATEST_RELEASE`/chromedriver_linux64.zip && \
    unzip /tmp/chromedriver.zip chromedriver -d /usr/local/bin/ && \
	rm -rf /tmp/chromedriver.zip && \
	apt-get remove -yqq unzip

# 3. Set display port as an environment variable
ENV DISPLAY=:99

RUN pip install --no-cache-dir --upgrade pip

# Install discbot and dependencies #

RUN mkdir /src
WORKDIR /src

RUN mkdir /src/cfg
VOLUME /src/cfg

COPY requirements.txt /src/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY . /src

CMD [ "python", "discgolfbot" ]