<div align="center">

  # helios

[![GitHub Workflow Status](https://img.shields.io/github/actions/workflow/status/haondt/helios/github-actions.yml)](https://github.com/haondt/helios/actions/workflows/github-actions.yml)
[![Docker Pulls](https://img.shields.io/docker/pulls/haumea/helios)](https://hub.docker.com/r/haumea/helios/)
[![GitHub release (latest by date)](https://img.shields.io/github/v/release/haondt/helios)](https://github.com/haondt/helios/releases/latest)

A start page built with Python, htmx and Hyperscript.

<img src="./nighttab.jpg" width="350">


</div>

As much as I love nightTab, I had a few problems with it:

1. It doesn't sync across devices
2. It becomes very tedious to add / edit many bookmarks at once. There are many repeated clicks in the UI just to change a url. It also starts to chug with too many bookmarks.
3. The configuration file is huge. It's much larger and complex than I need it to be. I don't need individual styling for every bookmark, I don't need to store colors as both rgb and hsl, etc. I want to be able to manually read and edit the data file when neccessary.

So I created helios to address these problems. It sacrifices customization for simplicity, which makes it a much more efficient tool.

- It's fast, and can handle many bookmarks easily
- The data file is more compact
- It's hosted
- Editing is done inline, so it's a single click to add or edit a bookmark

<div align="center">
  
# Screenshots

![](./screenshot1.png)

![](./screenshot2.png)

</div>

<div align="center">

# Deployment

</div>

helios can be deployed with docker.

```yml
services:
  helios:
    image: haumea/helios:latest
    volumes:
      - ./helios.yml:/config/helios.yml
```

See the [sample configuration](./example) for a full example. 

<div align="center">

# Development

</div>

Use the development docker compose file.

```bash
docker compose -f docker-compose.dev.yml up
```
