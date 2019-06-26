Set-up :

1. Checking nat rules : ```iptables -t nat -nL```

2. Forward ports (example forward from port 10000 to 8000) : ```iptables -t nat -A PREROUTING -i eth0 -p tcp --dport 10000 -j REDIRECT --to-port 8000```

3. Setting up proxy listen on port 8000 and forward to service

4. For deleting all nat rules, use : ```for i in $( iptables -t nat --line-numbers -L | grep ^[0-9] | awk '{ print $1 }' | tac ); do iptables -t nat -D PREROUTING $i; done```
