FROM selenium/node-base:3.141.59-mercury

LABEL authors=PedidosYa

USER root

#=========
# Firefox
#=========
RUN FIREFOX_DOWNLOAD_URL="{{firefox_url}}" \
  && apt-get update -qqy \
  && apt-get -qqy --no-install-recommends install firefox \
  && rm -rf /var/lib/apt/lists/* /var/cache/apt/* \
  && wget --no-verbose -O /tmp/firefox.tar.bz2 $FIREFOX_DOWNLOAD_URL \
  && apt-get -y purge firefox \
  && rm -rf /opt/firefox \
  && tar -C /opt -xjf /tmp/firefox.tar.bz2 \
  && rm /tmp/firefox.tar.bz2 \
  && mv /opt/firefox /opt/firefox-{{version_number}} \
  && ln -fs /opt/firefox-{{version_number}}/firefox /usr/bin/firefox
{% if version_number < 52 %}
RUN sudo apt-get update -qqy && sudo apt-get -qqy install libasound2
{% endif %}
{% if gecko_driver_version != '' %}
#============
# GeckoDriver
#============
RUN GK_VERSION="{{gecko_driver_version}}" \
  && echo "Using GeckoDriver version: "$GK_VERSION \
  && wget --no-verbose -O /tmp/geckodriver.tar.gz https://github.com/mozilla/geckodriver/releases/download/v$GK_VERSION/geckodriver-v$GK_VERSION-linux64.tar.gz \
  && rm -rf /opt/geckodriver \
  && tar -C /opt -zxf /tmp/geckodriver.tar.gz \
  && rm /tmp/geckodriver.tar.gz \
  && mv /opt/geckodriver /opt/geckodriver-$GK_VERSION \
  && chmod 755 /opt/geckodriver-$GK_VERSION \
  && ln -fs /opt/geckodriver-$GK_VERSION /usr/bin/geckodriver
{% endif %}

USER seluser

COPY template/generate_config /opt/bin/generate_config

# Generating a default config during build time
RUN /opt/bin/generate_config > /opt/selenium/config.json

#====================================
# Scripts to run Selenium Standalone
#====================================
COPY template/start-selenium-standalone.sh /opt/bin/start-selenium-standalone.sh

#==============================
# Supervisor configuration file
#==============================
COPY template/selenium.conf /etc/supervisor/conf.d/

EXPOSE 4444