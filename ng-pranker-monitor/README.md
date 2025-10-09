# Pranker Monitor

## Running
1. SSH into camera using port forwarding
2. pull the latest monitor image
3. On the Hamerhead run 
```shell
python -m http.server --directory /www/ui-dist --bind 127.0.0.1 27881
```
3. forward ports
```shell
$ ssh -N -L 27272:localhost:27272 hh  # Monitoring UI
$ ssh -N -L 27272:localhost:8765  hh  # Websockets
$ ssh -N -L 27272:localhost:17171 hh  # Thumbnail static files
```
4. Connect to http://localhost:27881 to view the UI



## Checking active ports
```shell
$  sudo lsof -iTCP -sTCP:LISTEN -P -n
COMMAND       PID            USER FD   TYPE   DEVICE SIZE/OFF NODE NAME
systemd         1            root 73u  IPv6     9758      0t0  TCP *:22 (LISTEN)
systemd-r     466 systemd-resolve 12u  IPv4     9733      0t0  TCP *:5355 (LISTEN)
systemd-r     466 systemd-resolve 14u  IPv6     9741      0t0  TCP *:5355 (LISTEN)
systemd-r     466 systemd-resolve 20u  IPv4     9747      0t0  TCP 127.0.0.53:53 (LISTEN)
systemd-r     466 systemd-resolve 22u  IPv4     9749      0t0  TCP 127.0.0.54:53 (LISTEN)
node_expo     492          nobody  3u  IPv6    34873      0t0  TCP *:9100 (LISTEN)
tailscale     709            root 24u  IPv4    36882      0t0  TCP 100.82.213.77:44987 (LISTEN)
tailscale     709            root 25u  IPv6    36883      0t0  TCP [fd7a:115c:a1e0::de01:d54d]:48978 (LISTEN)
smooth-op    1152            root 10u  IPv6    34363      0t0  TCP *:9182 (LISTEN)
smooth-ta    1153            root  3u  IPv6    35248      0t0  TCP *:23176 (LISTEN)
emitteroo  964668            root  4u  IPv6  9323633      0t0  TCP *:8080 (LISTEN)
python    2456202            root 21u  IPv4 18029510      0t0  TCP 127.0.0.1:17623 (LISTEN)
```