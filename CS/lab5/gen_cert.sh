#!/bin/bash

mkdir -p /etc/pki/ca/{certs,crl,newcerts,private}
chmod 700 /etc/pki/ca/private
touch /etc/pki/ca/index.txt
echo 1000 > /etc/pki/ca/serial

openssl genrsa -out /etc/pki/ca/private/ca_root_key.pem 4096
chmod 600 /etc/pki/ca/private/ca_root_key.pem

openssl req -new -x509 -days 3650 \
    -key /etc/pki/ca/private/ca_root_key.pem \
    -out /etc/pki/ca/certs/ca_root_cert.pem \
    -subj "/C=US/ST=Internal/L=PKI/O=Organization/OU=IT/CN=Internal Root CA"

generate_user_certificate() {
    local username=$1

    openssl genrsa -out "/etc/pki/ca/private/${username}_key.pem" 2048
    chmod 600 "/etc/pki/ca/private/${username}_key.pem"

    openssl req -new \
        -key "/etc/pki/ca/private/${username}_key.pem" \
        -out "/etc/pki/ca/certs/${username}_csr.pem" \
        -subj "/C=US/ST=Internal/L=PKI/O=Organization/OU=Users/CN=${username}"

    openssl x509 -req -days 365 \
        -in "/etc/pki/ca/certs/${username}_csr.pem" \
        -CA /etc/pki/ca/certs/ca_root_cert.pem \
        -CAkey /etc/pki/ca/private/ca_root_key.pem \
        -set_serial $(openssl rand -hex 16) \
        -out "/etc/pki/ca/certs/${username}_cert.pem"
}

revoke_user_certificate() {
    local username=$1

    openssl ca -revoke "/etc/pki/ca/certs/${username}_cert.pem" \
        -keyfile /etc/pki/ca/private/ca_root_key.pem \
        -cert /etc/pki/ca/certs/ca_root_cert.pem

    openssl ca -gencrl \
        -keyfile /etc/pki/ca/private/ca_root_key.pem \
        -cert /etc/pki/ca/certs/ca_root_cert.pem \
        -out /etc/pki/ca/crl/ca_crl.pem
}

if [[ "$1" == "gen" ]]; then
    generate_user_certificate "$2"
elif [[ "$1" == "rev" ]]; then
    revoke_user_certificate "$2"
fi

openssl x509 -in /etc/pki/ca/certs/ca_root_cert.pem -text -noout
