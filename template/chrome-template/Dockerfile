FROM selenium/node-base:3.141.59-mercury

LABEL authors=PedidosYa

USER root

#============================================
# Google Chrome
#============================================

RUN wget  -O google-chrome-stable.deb {{google_path}}

RUN sudo apt update && sudo apt upgrade -y && sudo dpkg --configure -a && sudo apt-get autoclean && apt-get install libcurl3 -y -f

RUN sudo apt install ./google-chrome-stable.deb -y -f

RUN google-chrome -version

{% if chrome_driver_version != '' %}

#=================================
# Chrome Launch Script Wrapper
#=================================
COPY template/wrap_chrome_binary /opt/bin/wrap_chrome_binary
RUN /opt/bin/wrap_chrome_binary

#============================================
# Chrome webdriver
#============================================

RUN echo "Using chromedriver version: {{chrome_driver_version}}" \
  && wget --no-verbose -O /tmp/chromedriver_linux64.zip https://chromedriver.storage.googleapis.com/{{chrome_driver_version}}/chromedriver_linux64.zip \
  && rm -rf /opt/selenium/chromedriver \
  && unzip /tmp/chromedriver_linux64.zip -d /opt/selenium \
  && rm /tmp/chromedriver_linux64.zip \
  && mv /opt/selenium/chromedriver /opt/selenium/chromedriver-{{chrome_driver_version}} \
  && chmod 755 /opt/selenium/chromedriver-{{chrome_driver_version}} \
  && sudo ln -fs /opt/selenium/chromedriver-{{chrome_driver_version}} /usr/bin/chromedriver

{% endif %}

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

