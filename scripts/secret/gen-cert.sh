#!/bin/bash

set -o nounset \
    -o errexit \
    -o verbose \
    -o xtrace

mkdir secrets
cd "./secrets/"

# openssl req -x509 -newkey rsa:4096 -keyout ca_private_key.pem -out ca_cert.pem -days 365 -subj '//CN=kafka-0-1/OU=TEST/O=CONFLUENT/L=PaloAlto/S=Ca/C=US' -passin pass:confluent -passout pass:confluent

# openssl req -new -newkey rsa:4096 -keyout my_private_key.pem -out my_cert_req.pem -subj '//CN=kafka-0-1/OU=TEST/O=CONFLUENT/L=PaloAlto/S=Ca/C=US' -passin pass:confluent -passout pass:confluent

# openssl x509 -req -in my_cert_req.pem -days 365 -CA ca_cert.pem -CAkey ca_private_key.pem -CAcreateserial -out my_signed_cert.pem -passin pass:confluent 


# for i in broker1 broker2 broker3 producer consumer
# for i in kafka-0-1 kafka-0-2 schema-registry-0-1 

# do
i=nifi
echo $i
# openssl req -x509 -newkey rsa:4096 -keyout ca_private_key.pem -out ca_cert.pem -days 365 -subj '//CN=ca1.test.confluent.io/OU=TEST/O=CONFLUENT/L=PaloAlto/S=Ca/C=US' -passin pass:confluent -passout pass:confluent

# openssl req -new -newkey rsa:4096 -keyout my_private_key.pem -out my_cert_req.pem -subj '//CN=ca1.test.confluent.io/OU=TEST/O=CONFLUENT/L=PaloAlto/S=Ca/C=US' -passin pass:confluent -passout pass:confluent

# openssl x509 -req -in my_cert_req.pem -days 365 -CA ca_cert.pem -CAkey ca_private_key.pem -CAcreateserial -out my_signed_cert.pem -passin pass:confluent 

openssl req -x509 -newkey rsa:4096 -keyout ca_private_key.pem -out ca_cert.pem -days 365 -subj "//SKIP=skip/CN=$i/OU=TEST/O=CONFLUENT/L=PaloAlto/S=Ca/C=US" -passin pass:confluent -passout pass:confluent

openssl req -new -newkey rsa:4096 -keyout my_private_key.pem -out my_cert_req.pem -subj "//SKIP=skip/CN=$i/OU=TEST/O=CONFLUENT/L=PaloAlto/S=Ca/C=US" -passin pass:confluent -passout pass:confluent

openssl x509 -req -in my_cert_req.pem -days 365 -CA ca_cert.pem -CAkey ca_private_key.pem -CAcreateserial -out my_signed_cert.pem -passin pass:confluent 

openssl pkcs12 -export -out $i-keyStore.p12 -inkey my_private_key.pem -in my_signed_cert.pem -certfile ca_cert.pem -passin pass:confluent -passout pass:confluent

keytool -keystore $i.truststore.jks -alias CARoot -import -file ca_cert.pem -storepass confluent -keypass confluent

echo "confluent" > ${i}_sslkey_creds
echo "confluent" > ${i}_keystore_creds
echo "confluent" > ${i}_truststore_creds

# done

echo 'SUCCESS'