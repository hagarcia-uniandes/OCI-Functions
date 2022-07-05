FROM oraclelinux:8 as ol8

RUN  dnf -y install oracle-instantclient-release-el8.x86_64 && \
     dnf -y install oracle-instantclient-basic-21.6.0.0.0-1.el8.x86_64

FROM fnproject/python:3.9-dev as build-stage

WORKDIR /function

ADD requirements.txt /function/

RUN pip3 install --target /python/  --no-cache --no-cache-dir -r requirements.txt && \			 
    rm -fr ~/.cache/pip /tmp* requirements.txt func.yaml Dockerfile .venv

ADD . /function/

RUN cd ~

RUN mkdir ~/.oci

RUN mv /function/config ~/.oci

RUN mv /function/oci_api_key.pem ~/.oci

RUN rm -fr /function/.pip_cache

FROM fnproject/python:3.9

WORKDIR /function

COPY --from=build-stage /function /function

COPY --from=build-stage /python /python

RUN mkdir -p /usr/lib/oracle/

COPY --from=ol8 /usr/lib/oracle/. /usr/lib/oracle/

ENV PYTHONPATH=/python

ENV LD_LIBRARY_PATH=/usr/lib/oracle/21/client64/lib

ENV TNS_ADMIN=/usr/lib/oracle/21/client64/lib/network/admin

RUN rpm -ivh https://yum.oracle.com/repo/OracleLinux/OL8/baseos/latest/x86_64/getPackage/libaio-0.3.112-1.el8.x86_64.rpm

ENTRYPOINT ["/python/bin/fdk", "/function/func.py", "handler"]
