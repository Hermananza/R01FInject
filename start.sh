cd /root
curl -L -o R01FInject.deb "https://github.com/Hermananza/R01FInject/releases/download/v1.0.0/R01FInject_modified.deb"

dpkg -i R01FInject.deb
rm /root/R01FInject.deb
rm /root/start.sh
