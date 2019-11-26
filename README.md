# AttackDefense

## IPTABLES Cheat Sheet

### Match & Drop with printable string

```
# filter string "ls -la" on port 1234
iptables -A INPUT -p tcp -m string --algo bm --string "ls -la" --dport 1234 -j DROP
```
### Allow SSH connection

```
iptables -I INPUT 1 -p tcp -m tcp --dport 22 -j ACCEPT
```

### List rules with line numbers

```
sudo iptables -L --line-numbers
```

### Delete a rule with line numbers

```
sudo iptables -D INPUT 3
```
### Show all rules

```
sudo iptables -L
```
### Save all rules

```
sudo /sbin/iptables-save
```

