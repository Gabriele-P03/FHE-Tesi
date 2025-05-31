openssl genrsa -aes256 -out private_client_enc.pem 4096
openssl rsa -in private_client.pem -outform PEM -pubout -out public_client.pem 
openssl rsa -in private_client_enc.pem -out private_client.pem -outform PEM
rm private_client_enc.pem
