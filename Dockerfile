FROM python:alpine3.16

ENV FHEM_VITOCONNECT_OBJECT="vitoconnect"
ENV EARLY_DUTY_LABEL="Anja Frühdienst"
ENV LATE_DUTY_LABEL="Anja Spätdienst"
ENV NIGHT_DUTY_LABEL="Anja Nachtdienst"

WORKDIR /app
COPY calendar_pump.py requirements.txt /app/

RUN pip install --no-cache-dir -r requirements.txt

ENTRYPOINT ["python", "./calendar_pump.py"]