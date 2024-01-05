FROM python:3.12.1

# Check chromedriver versions here:
# https://googlechromelabs.github.io/chrome-for-testing/
ENV CHROMEDRIVER_VERSION=120.0.6099.109

### Install Google Chrome
RUN apt-get update && apt-get install -y wget && \
    wget -q https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb && \
	apt-get install -y ./google-chrome-stable_current_amd64.deb && \
	rm -rf ./google-chrome-stable_current_amd64.deb

# Install Chrome Driver
RUN apt-get install -y unzip && \
	wget -O /tmp/chromedriver.zip https://edgedl.me.gvt1.com/edgedl/chrome/chrome-for-testing/$CHROMEDRIVER_VERSION/linux64/chromedriver-linux64.zip && \
    unzip /tmp/chromedriver.zip -d /usr/local/bin/ && \
	rm -rf /tmp/chromedriver.zip && \
	apt-get remove -yqq unzip

# Set display port as an environment variable
ENV DISPLAY=:99

RUN pip install --no-cache-dir --upgrade pip

# Set Working directory
RUN mkdir /src
WORKDIR /src

# Set Configuration Volume
RUN mkdir /src/cfg
VOLUME /src/cfg

# Copy the source
COPY . /src

# Install requirements
RUN pip install --no-cache-dir -r requirements.txt

CMD [ "python", "discgolfbot" ]