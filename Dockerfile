FROM python:3.5

#Stupid proxy :(
ENV http_proxy http://proxy.ocado.com
ENV https_proxy http://proxy.ocado.com
ENV no_proxy .ocado.com,.lastmile.com
ENV PYPI_INDEX_URL https://euw1-pypi.eu-west-1.aws.shd.prd.lastmile.com/pypi/

# From python onbuild
RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app
COPY requirements.txt /usr/src/app/
RUN pip install --no-cache-dir -r requirements.txt
COPY . /usr/src/app
# End stupid proxy

CMD ["/usr/src/app/chaos.py"]
