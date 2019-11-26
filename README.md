# AttackDefense

## IPTABLES Cheat Sheet

### Allow SSH connection

```
iptables -I INPUT 1 -p tcp -m tcp --dport 22 -j ACCEPT
```

### List rules with line numbers

```
sudo iptables -L --line-numbers
```

### Show all rules

```
sudo iptables -L
```
### Save all rules

```
sudo /sbin/iptables-save
```

