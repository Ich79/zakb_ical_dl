FROM python:3

WORKDIR /usr/src/app
ENV ENV_CITY Viernheim
ENV ENV_STREET Am Hofböhl
ENV ENV_HOUSENO 1
VOLUME /usr/src/app/calendar.ics


COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD [ "python", "./muell.py" ]