apt remove r01finject -y
curl -o start.sh -sSL https://raw.githubusercontent.com/GME09/R01FInject/main/start.sh && chmod +x start.sh && ./start.sh
clear
chmod +x /usr/bin/R01F
systemctl daemon-reload
systemctl enable sshxp
systemctl start sshxp
echo "Done!!"
R01F