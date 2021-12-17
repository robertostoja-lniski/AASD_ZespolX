$path = pwd
docker run -d --name prosody -p 5222:5222 `
 -v $path/prosody/prosody.cfg.lua:/etc/prosody/prosody.cfg.lua `
 -v $path/prosody/accounts.sh:/setup.sh `
 -v etc:/etc/prosody `
 -v var:/var/lib/prosody `
  prosody/prosody:0.9.12