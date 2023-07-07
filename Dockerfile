FROM public.ecr.aws/docker/library/python:3.11.3-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    gcc \
    git \
    libffi-dev \
    libssl-dev \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

ADD ./requirements /requirements
RUN pip install -r /requirements/base.txt
# copy sqladmin static files to /var/app/statics for hosting those using nginx
RUN mkdir -p /var/app/statics
RUN cp -r /usr/local/lib/python3.11/site-packages/sqladmin/statics /var/app/statics/sqladmin
RUN ls /usr/local/lib/python3.11/site-packages/sqladmin/statics/
RUN ls /var/app/statics/sqladmin/

ADD ./cremusic /var/app/cremusic
WORKDIR /var/app
CMD ["uvicorn", "cremusic.admin:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "4"]
