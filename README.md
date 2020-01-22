# SAG_spatial_factory

## How to setup
1. Install prosody:
```bash
sudo apt-get install prosody graphviz graphviz-dev
```
2. Configure prosody:
```bash
echo -e 'VirtualHost "localhost"\nallow_registration = true\nwhitelist_registration_only = false' | sudo tee -a /etc/prosody/prosody.cfg.lua
```
3. Restart prosody:
```bash
sudo prosodyctl restart
```
4. Install python3:
```bash
sudo apt install python3
```
5. Install modules:
```bash
sudo pip3 install requirements.txt
```
6. Run the project:
```bash
python3 main.py
```