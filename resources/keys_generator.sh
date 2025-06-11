echo "Generating Server's RSA Key Pair..."
openssl genrsa -aes256 -out rsa_private_server_enc.pem 4096
openssl rsa -in rsa_private_server_enc.pem -outform PEM -pubout -out rsa_public_server.pem 
openssl rsa -in rsa_private_server_enc.pem -out rsa_private_server.pem -outform PEM
rm rsa_private_server_enc.pem
echo "Done!"
echo

echo "Generating Client's AES Key..."
openssl genrsa -aes256 -out aes_client_enc.pem 4096
openssl rsa -in aes_client_enc.pem -out aes_client.pem -outform PEM
rm aes_client_enc.pem
echo "Done!"
