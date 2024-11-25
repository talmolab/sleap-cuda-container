#!/bin/bash

echo 'Updating /etc/hosts file...'
HOSTNAME=$(hostname)
echo "127.0.1.1    $HOSTNAME" >> /etc/hosts

echo "Checking for any existing VNC server on display :1..."
vncserver -kill :1 || echo "No existing VNC server found. Continuing..."

echo "Ensuring xstartup is configured..."
mkdir -p /root/.vnc
cat << EOF > /root/.vnc/xstartup
#!/bin/sh
startxfce4 &
autocutsel -fork &
autocutsel -selection PRIMARY -fork &
EOF
chmod +x /root/.vnc/xstartup

echo "Starting VNC server at $RESOLUTION..."
vncserver -geometry $RESOLUTION &

echo "VNC server started at $RESOLUTION! ^-^"

echo "Keeping the container alive..."
tail -f /dev/null
