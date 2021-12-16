$path = pwd
docker run -d --name prosody -p 5222:5222 `
 -e LOCAL=test `
 -e DOMAIN=localhost `
 -e PASSWORD=1qaz@WSX `
  prosody/prosody:0.9.12