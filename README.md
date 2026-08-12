## Git Key
### Start with the "Title" followed by:
- "[NOTE] _description of commit_" --> Only when necessary to denote specific details.
- "[+] _description of feature_" --> A feature was added / improved.
- "[-] _description of feature_" --> A feature was removed/ reduced.
- "[%] _description of feature_" --> A feature was modified/ Changed.


## Running LavaLink
### IPV6 rotation:
- sudo sysctl -w net.ipv6.ip_nonlocal_bind=1
- (To make it permanent run) echo "net.ipv6.ip_nonlocal_bind = 1" | sudo tee -a /etc/sysctl.conf

## Using docker
### Starting:
- docker compose up --build
### Clean shutdown and cache remove
- docker compose down