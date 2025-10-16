#!/bin/sh

# Define variables for certificate details
CERT_NAME="server"
DAYS_VALID=365
KEY_SIZE=2048
OUTPUT_DIR="/etc/nginx/"
FILE_CHECK_PATH = ${OUTPUT_DIR}/server.crt


if [ -f "$FILE_CHECK_PATH" ]; then
  echo "$FILE_CHECK_PATH exists and is a regular file."
else
  echo "$FILE_CHECK_PATH does not exist or is not a regular file."

    # Create output directory if it doesn't exist
    mkdir -p "$OUTPUT_DIR"

    # Generate the private key and self-signed certificate
    openssl req -x509 -nodes -days "$DAYS_VALID" \
        -newkey rsa:"$KEY_SIZE" \
        -keyout "${OUTPUT_DIR}${CERT_NAME}.key" \
        -out "${OUTPUT_DIR}${CERT_NAME}.crt" \
        -subj "/C=US/ST=State/L=City/O=Organization/OU=Unit/CN=localhost"

    echo "Self-signed certificate and private key created:"
    echo "  Private Key: ${OUTPUT_DIR}${CERT_NAME}.key"
    echo "  Certificate: ${OUTPUT_DIR}${CERT_NAME}.crt"

fi


