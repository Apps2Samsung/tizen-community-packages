# 🌐 Tizen Community Packages
[![Sync Tizen Community Packages](https://github.com/Apps2Samsung/tizen-community-packages/actions/workflows/sync-packages.yml/badge.svg)](https://github.com/Apps2Samsung/tizen-community-packages/actions/workflows/sync-packages.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Packages](https://img.shields.io/badge/packages-141-blue.svg)](#-current-packages)
[![Contributions Welcome](https://img.shields.io/badge/Contributions-Welcome-green.svg)](../../issues)
[![Tizen](https://img.shields.io/badge/Platform-Tizen-lightgrey.svg)](https://www.tizen.org/)
[![Community](https://img.shields.io/badge/Community-Driven-orange.svg)](#)

> **Community-curated bundles of Tizen applications (`.wgt` and `.tpk` packages)**:  
> compiled into single, convenient releases for easier installation and testing on your Tizen devices.

---

## 📑 Table of Contents

- [What Is This?](#-what-is-this)
- [Current Packages](#-current-packages)
- [Contributing & Requesting Apps](#-contributing--requesting-apps)
- [Run Your Own Repository](#-run-your-own-repository)
- [Security Scanning](#-security-scanning)
- [Disclaimer](#️-disclaimer)
- [Additional Note](#-additional-note)
- [License](#-license)

---

## 📦 What Is This?

This repository provides bundled releases containing multiple Tizen applications (`.wgt` web apps and `.tpk` native apps).  
Instead of downloading and installing each app individually, you can grab a single **bundle** that includes several community apps, ready for side-loading onto your Tizen devices.

Each release represents a curated collection of useful, fun, or open-source Tizen apps.

---

## 📋 Current Packages

Apps included in the latest community bundle, grouped by category. Click a category to expand it.  
Please check the [Releases](../../releases) page for version-specific details.

<!-- packages:start -->

<details>
<summary><b>📼 Media servers & players</b> (35)</summary>

| 🧩 Application | 📝 Description | ⚙️ Version |
|----------------|----------------|------------|
| **Aerial Screensaver**<br>[jeancarlos](https://github.com/jeancarlos/aerial-tizen) | Apple TV Aerial screensavers: 115 videos streamed from Apple's CDN and decoded in hardware as HEVC 4K via AVPlay. | `3f80ef0` |
| **AmorecoFlix**<br>[Pablitorox](https://github.com/Pablitorox/AmorecoFlix) | Personal Netflix-style player for a USB drive plugged into the TV: posters, synopses, continue watching, next episode, skip intro, audio and subtitle choice. | `e6212b3` |
| **Beam-TV**<br>[TAGISWILD](https://github.com/TAGISWILD/beam-tv) | Open-source USB and DLNA media player for Samsung Tizen TVs: subtitles, resume playback, remote navigation, and a local companion server. | `v1.0.1` |
| **Chorus2-Tizen**<br>[Chorus2-Tizen](https://github.com/PatrickSt1991/chorus2-tizen) | Chorus2-Tizen (Kodi) Samsung Tizen. | `tizen-v21.x-1.0.1-2026-05-21-1443` |
| **Fladder**<br>[popdollar](https://github.com/popdollar/Fladder-Tizen) | Jellyfin client for Samsung Tizen TV, built with Flutter (native .tpk). | `Tizen` |
| **Flixor-Tizen**<br>[Flixor-Tizen](https://github.com/PatrickSt1991/flixor-tizen) | Modern cross-platform Plex client. | `v1.0.1-2026-11-08-0607` |
| **Immich TV**<br>[Immich TV for Samsung](https://github.com/rfsmason/immich-tv-for-samsung) | Read-only Immich photo and video client for Samsung TVs: timeline, albums, people, memories, search, slideshows. | `v0.1.2-beta.3` |
| **ImmiTV**<br>[xHiqhAim](https://gitlab.com/xHiqhAim/immitv) | Lightweight Immich photo and video client for Samsung Tizen 4.0 TVs: remote-control navigation, hardware-accelerated AVPlay video playback and a month-based timeline. | `142e6ae` |
| **Jellyfin + Bonfire**<br>[jellyfin](https://github.com/jellyfin/jellyfin-tizen) | Official Jellyfin Tizen client patched with the Bonfire loader for multi-user profile switching. | `31408c1` |
| **JellyLean**<br>[MaCHeaMaRoBi](https://github.com/MaCHeaMaRoBi/JellyLean) | Fast, lightweight Jellyfin client without jellyfin-web: AVPlay playback with transcode fallback, Quick Connect, subtitles, SyncPlay and skip intro. | `v1.0.9` |
| **Kodi**<br>[Ricrdsson1](https://github.com/Ricrdsson1/kodi-tizen-wasm) | Unofficial WebAssembly port of Kodi for Samsung Tizen TVs (alpha). | `Alpha-0.0.8` |
| **Kodi-TeX**<br>[PatrickSt1991](https://github.com/PatrickSt1991/tex-tizen) | Kodi TeX web interface ported to Samsung Tizen. | `tex-tizen-v1.3.0-2026-06-09-0952` |
| **KROMA**<br>[kromatv](https://github.com/kromatv/kroma) | Client for KROMA, a self-hosted direct-play media server for your NAS. | `v0.1.38` |
| **Lumen TV**<br>[cloke-tech](https://github.com/cloke-tech/Lumen-TV) | Receiver app for Lumen, plays Blu-ray, DVD and files from a computer or USB. | `v1.17.1` |
| **Moonfin (Lica fork)**<br>[Licaa21](https://github.com/Licaa21/Smart-TV) | Fork of the Moonfin Jellyfin/Emby client with extra features: Emby Connect sign-in, an EPUB reader with bookmarks and themes, Forgot PIN, remembered audio/subtitle picks per title and more. | `fork-v2.0.8` |
| **Pelagica**<br>[PelagicaApp](https://github.com/PelagicaApp/pelagica) | A modern web, desktop and TV client for Jellyfin | `4.15.0` |
| **Phlix**<br>[detain](https://github.com/detain/phlix-tizen-client) | Samsung Tizen TV client for the Phlix media server: HLS streaming and spatial navigation. | `latest` |
| **PlayerAVPlay**<br>[yadPe](https://github.com/yadPe/PlayerAVPlay) | AVPlayer app | `latest` |
| **Pley**<br>[pley-media-server](https://github.com/pley-media-server/pley) | Client for the Pley media server: movies, shows, music and live TV with a guide, played through the TV's own player (AVPlay). | `b348f68` |
| **Pley (native)**<br>[pley-media-server](https://github.com/pley-media-server/pley) | Native C#/NUI build of the Pley client for Tizen 9 TVs, from the samsung-native releases. | `n/a` |
| **Prairie**<br>[Prairie-Server](https://github.com/Prairie-Server/prairie-smarttv) | Flutter client for the self-hosted Prairie media server (native .tpk): multi-server registry with LAN discovery, profiles with PIN, Quick Connect sign-in and AVPlay playback. | `v0.5.4` |
| **Reiverr**<br>[aleksilassila](https://github.com/aleksilassila/reiverr) | A clean combined interface for Jellyfin, TMDB, Radarr and Sonarr, as well as a replacement to Overseerr. | `3b7351f` |
| **SamSUCKS**<br>[rfaile313](https://github.com/rfaile313/samsucks) | Fast from-scratch Plex client for Samsung Tizen 6.5+ TVs: smooth scrolling, hardware AVPlay playback with direct play, instant search, audio/subtitle picker and up-next autoplay. | `6b00e92` |
| **Sendspin Cinema**<br>[zonya](https://github.com/zonya/sendspin-cinema-tizen) | Minimal cinema-style Sendspin player for Music Assistant on Samsung Tizen 3.0+ TVs: album art with adaptive accent colours, set up from the TV screen. | `0eabc15` |
| **Shutter**<br>[khanh-ly](https://github.com/khanh-ly/shutter) | Unofficial Synology Photos slideshow for Samsung TVs: all photos, favorites, an album or Shared Space, with crossfades, pan/zoom and a clock. | `32df354` |
| **Sonance3**<br>[MrSimmo](https://github.com/MrSimmo/sonance3) | A music player for Samsung Tizen TVs, built to stream from your self-hosted Jellyfin, Navidrome or Subsonic-compatible server. | `v3.15` |
| **SubTizen**<br>[therosaer](https://github.com/therosaer/SubTizen) | Subsonic music client for Navidrome, Airsonic, Gonic and Subsonic: Apple Music-style UI, server playlists, search and synced lyrics. | `v1.0.1` |
| **tacplayer**<br>[sfsdffesfsfg-cloud](https://github.com/sfsdffesfsfg-cloud/tacplayer) | Custom Jellyfin Tizen client with cinematic red UI for Samsung TV | `v0.1.0` |
| **Tessel**<br>[PatrickSt1991](https://github.com/PatrickSt1991/tessel-tizen-tv) | Media player for Samsung TVs: SMB shares, USB drives, network streams and subtitles, with an optional transcode server (formerly VLC-Tizen-tv). | `v1.35.0-20261105-0948` |
| **TubeArchivist TV**<br>[raykholo](https://github.com/raykholo/tubearchivist-tv) | 10-foot client for your self-hosted TubeArchivist: pair from your phone, never type on the remote. | `3cb035f` |
| **TVideoPlayer**<br>[TizenTVWebApp](https://github.com/TizenTVWebApp/TVideoPlayer) | Tizen TV HTML video player based on videojs. | `latest` |
| **VeloVistrix**<br>[zephy-lee](https://github.com/zephy-lee/velovistrix-tizen) | Read-only PhotoPrism viewer for Samsung Tizen 5.0+ TVs, driven by the remote: albums, places, calendar, labels and folders from your own server, with slideshow. | `d136678` |
| **Velox**<br>[SuperDOS](https://github.com/SuperDOS/velox) | Fast Plex client: opens in about a second, smooth scrolling, hardware playback. | `v1.1.0` |
| **Velvet TV**<br>[aroundmyroom](https://github.com/aroundmyroom/Velvet) | Big-screen TV client for the Velvet self-hosted music server. | `6c0a88f` |
| **Vemm**<br>[somefosterkid](https://github.com/somefosterkid/vemm) | Unofficial Plex-compatible media player for Samsung Tizen TVs with AVPlay playback, Direct Play and server transcoding. | `preview-0.10.0` |

</details>

<details>
<summary><b>📡 IPTV & Live TV</b> (20)</summary>

| 🧩 Application | 📝 Description | ⚙️ Version |
|----------------|----------------|------------|
| **APL TV**<br>[Knikt](https://github.com/Knikt/APL-TV-for-TizenOS) | Apple TV style IPTV player for your own M3U playlists and Xtream accounts: live TV with a guide, movies and series with TMDB pages, subtitles and audio menus, OpenSubtitles, Alexa voice search. | `v1.0.11` |
| **AquaPlay IPTV**<br>[AquaPlay IPTV](https://github.com/AquaPlayIPTV/aquaplay-samsung) | Lightweight IPTV player for M3U and Xtream playlists, with a full guide, catch-up and setup from your phone | `v1.0.52` |
| **Chouette TV**<br>[ipaifix](https://github.com/ipaifix/chouette-tv) | IPTV player for Samsung Tizen 2.3+ TVs: Xtream and M3U sources, EPG, favourites, profiles and resume. | `794dbef` |
| **EN TV Player**<br>[Nur-allhi](https://github.com/Nur-allhi/en-tvplayer) | IPTV player for Samsung Tizen TVs with DRM support, M3U/M3U8 playlists, groups and live TV. | `v3.2.0` |
| **FLOH IPTV**<br>[kingflooow](https://github.com/kingflooow/floh-iptv) | A fast IPTV player for Samsung TVs. | `v1.7.0` |
| **HackTV**<br>[kosmodrey](https://github.com/kosmodrey/hackTV) | IPTV client for Samsung Tizen TVs. | `bf27ba9` |
| **IPTV Manager**<br>[matifDreamIt](https://github.com/matifDreamIt/IPTV-Tizen-TV) | IPTV manager for Samsung Tizen TV with Xtream Codes support and HLS playback. | `d8eb66b` |
| **Nyx**<br>[victorreinor](https://github.com/victorreinor/nyx-tv) | IPTV player for your own Xtream or M3U playlist with a simple, remote-first interface. | `v1.7.1` |
| **opencream TV**<br>[opencream-ai](https://github.com/opencream-ai/opencream-tv) | A calm home screen for Samsung TVs with your own Xtream Codes IPTV built in: live TV, films, series, guide search. | `v0.1.4` |
| **OpenIPTV**<br>[shayanline](https://github.com/shayanline/OpenIPTV) | Privacy focused IPTV player for Samsung Tizen TVs with extended M3U playlists, favourites and search. | `1.9.3` |
| **OTTplay FOSS**<br>[prog4food](https://github.com/prog4food/ottplay-foss-thin-clients) | FOSS OTT / IPTV thin client for Tizen. | `Sat, 21 Jan 2023 15:15:16 GMT` |
| **RÚV**<br>[RÚV VOD](https://github.com/sverrirs/ruv-app-samsung) | Apps for RÚV, the Icelandic national broadcaster: Sarpur on demand, Barnaefni for children, Unglingar for teens, Menntun for education, and Útvarp radio (not affiliated with RÚV) | `2026.08.25-2350` |
| **RÚV Live**<br>[RÚV Live](https://github.com/sverrirs/ruv-live-samsung) | Live TV from RÚV, the Icelandic national broadcaster: the RÚV and RÚV 2 channels, with the running schedule and rewind inside the live window (not affiliated with RÚV) | `2026.08.25` |
| **SKY IPTV**<br>[sanwhere](https://github.com/sanwhere/sky-iptv-tizen) | IPTV player for Samsung Tizen 5.0+ TVs: M3U and Xtream playlists, remote-friendly UI, audio and subtitle track switching, embedded mov_text subtitles. | `v1.1.1` |
| **StreamVault**<br>[StreamVault](https://github.com/christopherklint97/streamvault) | IPTV streaming app for Samsung Tizen TVs built with React, TypeScript, and Zustand. | `v0.1.0` |
| **Tizen IPTV Player (Rusty24h)**<br>[Rusty24h](https://github.com/Rusty24h/Tizen-IPTV-Player) | IPTV Player for Samsung Tizen TVs supporting Stalker MAC portals, Xtream Codes, and M3U playlists with 2D EPG and catch-up. | `2.1.0` |
| **Tizen IPTV Player by mhma26395**<br>[mhma26395-ctrl](https://github.com/mhma26395-ctrl/tizen-iptv-player) | Lightweight IPTV player for compatible Samsung Tizen TVs. | `V1.0` |
| **TVapp**<br>[KaashDev](https://github.com/KaashDev/TVapp) | Enable seamless playback of HLS/m3u8 streams as channels. | `latest` |
| **VexonTV**<br>[VexonTV](https://github.com/DvzZDev/VexonTV) | Live TV player for Samsung Tizen TVs: M3U, Xtream Codes and Stalker portals, provider EPG and a remote-first interface. | `9aa670e` |
| **Xtream IPTV Player**<br>[dearbulut](https://github.com/dearbulut/tizen-xtream-iptv) | IPTV player for Samsung Tizen TVs with Xtream API support: live TV, movies and series. | `7fd43a0` |

</details>

<details>
<summary><b>🎬 Streaming</b> (31)</summary>

| 🧩 Application | 📝 Description | ⚙️ Version |
|----------------|----------------|------------|
| **AIOStreams**<br>[Viren070](https://github.com/Viren070/AIOStreams) | Tizen build of AIOStreams, the all-in-one Stremio super-addon for debrid and Usenet sources. | `smart-tv-v0.8.0` |
| **AIOStreams (thomasrtg)**<br>[thomasrtg](https://github.com/thomasrtg/AIOStreams) | Tizen 6 build of AIOStreams, the all-in-one Stremio super-addon for debrid and Usenet sources. | `tizen6-v0.7.0-beta.1` |
| **AniUltimatium Lite**<br>[AdvaithAvinash](https://github.com/AdvaithAvinash/AniUltimatium) | Player for your own Stremio add-ons, debrid account, IPTV playlist and direct streams; nothing built in. | `stable-v1.25` |
| **Apex TV**<br>[Pajuodelis](https://github.com/Pajuodelis/apex-tv) | Independent F1 TV client for Samsung Tizen 6.0+. | `v0.5.14` |
| **bilibili**<br>[titlog](https://github.com/titlog/bilibili-tizen) | Unofficial bilibili client for Samsung TVs, driven entirely by the remote: QR sign-in with multiple accounts, continue-watching row, danmaku, search, live, up to 1080p H.265 (4K with premium). | `v1.4.14` |
| **Crunchyroll**<br>[jhassan8](https://github.com/jhassan8/crunchyroll-tizen) | Unofficial Crunchyroll client for Samsung Tizen TVs with anime streaming support. | `latest` |
| **Douyin (抖音)**<br>[titlog](https://github.com/titlog/douyin-tizen) | Unofficial Douyin client for Samsung Tizen 6.0+ TVs, driven by the remote: Featured, Following and For You feeds, QR sign-in, your history, likes and favourites, creator pages, collections and comments. | `v1.4.6` |
| **F1 TV**<br>[nicbra](https://github.com/nicbra/f1tv-tizen) | Unofficial F1 TV client: live sessions and replays up to 4K HDR, every onboard camera, a synced timing tower, multi-language commentary and spoiler-free mode. | `v1.0.1` |
| **Kick**<br>[Replexo](https://github.com/Replexo/kick-tizen) | Unofficial Kick client modeled on the official TV app: live streams, chat, rewind, clips and 10 languages. | `v1.3.1` |
| **Kick TV 2.0**<br>[janrydzewski](https://github.com/janrydzewski/kick-tv-2.0) | Kick live streams and public archives for Samsung Tizen TVs. | `v2.0.1` |
| **Kick TV TR**<br>[Kick TV TR](https://github.com/igFr0sty/kick-tv-tizen-tr) | Unofficial Kick client with a Following screen and Turkish support. | `v2.4.0` |
| **KickTV**<br>[corekill](https://github.com/corekill/kick-tv-tizen) | Kick.com streaming client for Samsung Tizen TVs. | `v2.3.0` |
| **Lampa**<br>[yumata](https://github.com/yumata/lampa) | Free movie and TV catalogue with info, new releases and trailers. | `v1.4.1` |
| **Nuvio**<br>[NuvioMedia](https://github.com/NuvioMedia/NuvioTVSmart) | TV-first streaming UI for Samsung Tizen. | `1.3.11` |
| **Nuvio Native Legacy**<br>[iqui27](https://github.com/iqui27/nuvio-native-legacy) | Unofficial native C/SDL2 Nuvio client, fast on older TVs. | `v2.0.8` |
| **OmegaTube**<br>[OmegaTube](https://github.com/IIyn/omegatube) | Ad-free YouTube client with SponsorBlock and a native 4K player (Tizen 6+). | `v1.5.0` |
| **OsmTwich**<br>[OsmTwichPlayer](https://github.com/josepvarela/OsmTwichPlayer) | Unofficial Twitch client for Samsung Tizen TV. | `v1.2` |
| **Reelo**<br>[Reelo](https://github.com/ihovsky/Reelo) | TV client for the Reelo service: films and series with a remote-first interface, family profiles and library sync between devices (Russian UI). | `Sat, 07 Nov 2026 18:57:17 GMT` |
| **SeanimeTV**<br>[ihiqhaim](https://github.com/ihiqhaim/SeanimeTV-Tizen) | Unofficial Seanime client for Samsung Tizen TVs with torrent streaming and AVPlay playback. | `4da9288` |
| **Spelunkr**<br>[pedr](https://github.com/pedr/spelunkrtv-tizen-app) | Unofficial spelunkr.tv client: 24/7 synchronized channels of Internet Archive video, driven by the remote, with a fix that lets Samsung's player seek in archive.org videos. | `v1.1.0` |
| **Streamix TV**<br>[gabrielmaialva33](https://github.com/gabrielmaialva33/streamix-tv) | Cinematic 10-foot TV client for the self-hosted Streamix platform. | `v1.0.027` |
| **Stremio (Tizen 4)**<br>[Apps2Samsung](https://github.com/Apps2Samsung/tizen-community-packages) | Stremio media center packaged for Tizen 4.0 devices. | `latest` |
| **StremioK**<br>[Kepler75](https://github.com/Kepler75/StremioK) | From-scratch Stremio-addon streaming client for Samsung Tizen 3.0+ TVs: catalogs, sources and subtitles from the addons you add, Trakt sync, IPTV from your M3U playlists, YouTube and USB playback. | `v2.3.4` |
| **Telegram Videos**<br>[titlog](https://github.com/titlog/telegram-tizen) | Plays the videos in your Telegram groups and channels on Samsung Tizen 6.0+ TVs: QR sign-in, several accounts, MP4 and MKV streamed while downloading, audio tracks and subtitles, search across chats. | `v1.2.6` |
| **TizenTube Old Tizen**<br>[numbereleven-a](https://github.com/numbereleven-a/TizenTube-old-tizen) | Standalone YouTube with SponsorBlock for older Samsung TVs (Tizen 2.4 and 3.0). | `v2.5.0` |
| **TorrStream**<br>[cash94](https://github.com/cash94/TorrStream-Tizen) | Movies and TV shows through TorrServer, with TMDB catalogs and audio and subtitle track names read on the TV. | `v1.1.4` |
| **Twitch**<br>[fgl27](https://github.com/fgl27/smarttv-twitch) | Twitch client for Samsung Smart TVs 2015 and newer models. | `ca31512` |
| **Twitch Old Tizen**<br>[numbereleven-a](https://github.com/numbereleven-a/smarttv-twitch-old-tizen) | Twitch client for older Samsung Tizen TVs (2.4/3.0) with 720p/1080p playback fixes for channels that enable 1440p, plus device-code sign-in. | `4.1.4` |
| **UltimatiumTube**<br>[AdvaithAvinash](https://github.com/AdvaithAvinash/UltimatiumTube) | Ad-free YouTube for Samsung Tizen 5.0 and 5.5 TVs. | `stable-v1.13` |
| **YouTube Dummy**<br>[no-cover](https://github.com/no-cover/youtube-dummy) | Lightweight wrapper around youtube.com/tv that injects the TizenTube userscript (ad-free, SponsorBlock), handles remote-control navigation and exits cleanly back to Smart Hub. | `1.0.0` |
| **YouTube for Tizen**<br>[SushyDev](https://github.com/SushyDev/tizen-youtube) | Ad-free YouTube for Samsung TVs, running in Samsung's own Cobalt engine with SponsorBlock, DeArrow and preferred-quality settings. | `v1.6.0` |

</details>

<details>
<summary><b>🎮 Games & emulators</b> (17)</summary>

| 🧩 Application | 📝 Description | ⚙️ Version |
|----------------|----------------|------------|
| **Chiaki-Tizen**<br>[Chiaki-Tizen](https://github.com/Trent407/chiaki-tizen) | An open source PlayStation remote play project serving as the next-generation of Chiaki. | `v0.2.0` |
| **Doom**<br>[dos-ise](https://github.com/dos-ise/doom-tizen) | Doom for Samsung Tizen TVs, based on Chocolate Doom and WebAssembly. | `v1.21` |
| **EDuke32**<br>[dos-ise](https://github.com/dos-ise/eduke32-tizen) | Duke Nukem 3D for Samsung Tizen TVs, including the shareware episode. | `v0.11` |
| **FreeSerf**<br>[dos-ise](https://github.com/dos-ise/freeserf-tizen) | An open-source recreation of The Settlers 1 (Serf City) compiled to WebAssembly for Samsung Tizen TVs. | `v1.0` |
| **GameBoy-Emulator**<br>[dos-ise](https://github.com/dos-ise/GB-EMU_Tizen) | A Game Boy (DMG) emulator. | `v1.2.1` |
| **Moonlight**<br>[OneLiberty](https://github.com/OneLiberty/moonlight-chrome-tizen) | Open-source client for NVIDIA GameStream and Sunshine. | `v1.2.1` |
| **Moonlight (No Gamemode)**<br>[MrPhaze62](https://github.com/MrPhaze62/moonlight-chrome-tizen-no-gamemode) | Open-source client for NVIDIA GameStream and Sunshine with gamemode disabled. | `samsung_wasm-21031261929` |
| **Moonlight (ToypoodleGaming)**<br>[toypoodlegaming](https://github.com/toypoodlegaming/moonlight-chrome-tizen) | Moonlight NVIDIA GameStream / Sunshine client (ToypoodleGaming fork). | `samsung_wasm-21031332442` |
| **Moonlight Enhanced (AC-3)**<br>[fidoboy](https://github.com/fidoboy/moonlight-tizen-ac3) | Open-source Moonlight client for Tizen OS with optional support for Dolby Digital and Dolby Digital Plus (stereo and 5.1) optical-audio and HDMI passthrough. | `v1.2.3` |
| **Moonlight-Tizen**<br>[BrightCraft](https://github.com/brightcraft/moonlight-tizen) | Open-source client for NVIDIA GameStream and Sunshine Tizen OS 5.5 or higher. | `v1.20.0` |
| **Padthru**<br>[labanmne](https://github.com/labanmne/padthru) | Play PC games over a long HDMI cable with the controller paired to your TV: shows the PC's HDMI input full screen and forwards the controller to the PC over your network. | `v0.5.0` |
| **RetroArch**<br>[Sype0](https://github.com/Sype0/retroarch-tizen) | RetroArch (libretro WebAssembly) for Samsung Tizen 6.5+ TVs: remote-driven launcher, gamepad support, ROMs from a USB drive or a network folder. | `v0.3.2` |
| **RetroTV**<br>[guhcostan](https://github.com/guhcostan/retro-tv) | Retro game console for Samsung Tizen 5.0+ TVs: WebAssembly emulator cores (jsnes and kazuki-4ys builds, hash-pinned) downloaded on first use, games copied over the LAN from the project's companion server on a PC, or streamed from that PC. | `062fb72` |
| **Shmup Cup**<br>[detain](https://github.com/detain/shmup-cup) | A side-scrolling shoot-'em-up written for the TV remote: nine zones, two ships, sixteen routes and a boss at the end of each. | `ef6605c` |
| **Snake**<br>[pvk689](https://github.com/pvk689/snake-game-tizen) | Snake game for Samsung Tizen TVs, played with the remote. | `62ccffc` |
| **Tizen Steam Link**<br>[pebeto](https://github.com/pebeto/tizen-steam-link) | Unofficial Steam Link client for Samsung Tizen 5.5+ TVs: streams games from Steam on a PC or Steam Deck, with the TV's hardware decoder and controllers, keyboard and mouse passed through. | `v0.3.2` |
| **TransportTycoonDeluxe**<br>[dos-ise](https://github.com/dos-ise/openttd-tizen) | OpenTTD is an open source simulation game based upon Transport Tycoon Deluxe. | `v15.3` |

</details>

<details>
<summary><b>📷 Casting & cameras</b> (7)</summary>

| 🧩 Application | 📝 Description | ⚙️ Version |
|----------------|----------------|------------|
| **AirTizen**<br>[MrHumanRebel](https://github.com/MrHumanRebel/airtizen) | AirPlay receiver for Samsung Tizen TV: stream audio/video to older Samsung TVs. | `v2.2.34` |
| **Camera PiP**<br>[dzikus](https://github.com/dzikus/tizen-camera-pip) | Doorbell and driveway cameras on a Samsung Tizen TV: pops up on a trigger (Home Assistant or any webhook), plays through the hardware decoder so the app behind it keeps running, and fires actions like opening the gate from the remote. | `v1.2.0` |
| **FCast**<br>[futo-org](https://github.com/futo-org/fcast) | FCast is an open source protocol that enables wireless streaming of audio and video content between devices. | `Wed, 08 Oct 2025 17:07:02 GMT` |
| **go2rtc**<br>[Edsol](https://github.com/Edsol/go2rtc-tizen) | Watch the cameras of a go2rtc server (standalone or embedded in Frigate): camera grid with previews and full-screen live view. | `v0.1.0` |
| **Reolink Viewer**<br>[Apps2Samsung](https://github.com/Apps2Samsung/ReolinkViewer) | Watch a Reolink camera or NVR on your TV: enter its local IP and login, press Start. | `v1.1.0` |
| **RTSP Camera Viewer**<br>[vzakharchenko](https://github.com/vzakharchenko/rtsp-samsung-tv) | Display RTSP streams from IP cameras on your Samsung TV, with numpad channel switching and a 4-camera grid. | `3aefa34` |
| **UniFi Cameras**<br>[xtantaudio](https://github.com/xtantaudio/unifi-cameras-on-tizen) | Live camera grid for UniFi Protect or any RTSP cameras on Samsung Tizen 6.0+ TVs, D-pad to go fullscreen. | `2f7f8c0` |

</details>

<details>
<summary><b>🛠️ Tools & system</b> (15)</summary>

| 🧩 Application | 📝 Description | ⚙️ Version |
|----------------|----------------|------------|
| **APL Launcher**<br>[Knikt](https://github.com/Knikt/APL-Launcher-for-TizenOS) | Apple-TV-style home screen: Top Shelf, glass dock, Control Center over any app, Settings and Sources. | `v1.0.24` |
| **App Manager**<br>[no-cover](https://github.com/no-cover/appmanager) | Alternative launcher for Samsung Tizen TVs: lists installed third-party and sideloaded apps in one grid to launch them, or hide them from Smart Hub without uninstalling. | `1.0.3` |
| **HyperTizen**<br>[reisxd](https://github.com/reisxd/HyperTizen) | Hyperion / HyperHDR ambient-light capturer for Samsung Tizen TV (native .tpk; requires TizenBrew for the UI). | `v1.0.0` |
| **inet-speed-old-tizen**<br>[numbereleven-a](https://github.com/numbereleven-a/inet-speed-old-tizen) | Internet diagnostics for Samsung Tizen 2.4+ TVs: response times of popular sites and download speed from Cloudflare, Fastly and HOSTKEY test CDNs, plus TV model, firmware and network info. | `v1.1.1` |
| **iperf3 TV**<br>[DmitryMaksakov](https://github.com/DmitryMaksakov/samsung-tv-iperf3) | Measures your Samsung TV's network throughput to an iperf3 server, upload or download. | `d20ac9f` |
| **MonoServer**<br>[cash94](https://github.com/cash94/MonoServer) | TorrServer rewritten in C# (MonoTorrent) that runs as a background service on the TV itself, including Tizen 5.5 where the official TorrServer cannot start. | `v1.0.35` |
| **Tailscale**<br>[PatrickSt1991](https://github.com/PatrickSt1991/tailscale-tizen) | Tailscale exit-node app for Samsung Tizen TV (experimental; advertises the TV as a tailnet exit node). | `tpk-f3a7b39` |
| **Tizen Debug App**<br>[no-cover](https://github.com/no-cover/tizendebugapp) | Developer toolkit for troubleshooting apps and monitoring system state on real Samsung Tizen TV hardware. | `1.0.0` |
| **Tizen OS Ambilight**<br>[exzos28](https://github.com/exzos28/tizen-os-ambilight) | DIY ambilight: reads the screen-edge colors from the TV's video processor and streams them to an ESP32 LED controller or HyperHDR; the launcher shows whether your TV supports capture. | `v1.2.1` |
| **TizenAmbilight**<br>[RitwickVerma](https://github.com/RitwickVerma/TizenAmbilight) | Real-frame ambilight: reads the TV's own video plane in memory and drives a WLED strip over UDP. | `v1.0.0` |
| **TizenBrew**<br>[reisxd](https://github.com/reisxd/TizenBrew) | A way to experience modded websites and you can install newer apps without fighting with Tizen Studio. | `v2.0.5` |
| **TizenUtility**<br>[no-cover](https://github.com/no-cover/tizenutility) | System utility for Samsung Tizen TVs: detailed device, firmware and network info, plus a launcher for hidden built-in Samsung apps that are not reachable from the normal UI. | `1.1.1` |
| **Torr Streaming**<br>[no-cover](https://github.com/no-cover/torr-streaming) | Runs TorrServer as a background service on the TV itself, so local web apps can stream torrents directly without a separate box. | `1.0.0` |
| **TV-Store**<br>[Apps2Samsung](https://github.com/Apps2Samsung/TV-Store) | The Apps2Samsung catalog on the TV itself: browse with the remote and install apps natively through the set's own developer connection, with no PC or phone in the loop after a one-time arming from the Apps2Samsung 3.0 (or newer) toolbox. | `v0.3.26` |
| **Vetro**<br>[andrearicci93](https://github.com/andrearicci93/vetro) | TV management dashboard with root integration: app inventory, controls and diagnostics in your browser. | `aa37060` |

</details>

<details>
<summary><b>📦 Other</b> (15)</summary>

| 🧩 Application | 📝 Description | ⚙️ Version |
|----------------|----------------|------------|
| **/dev/null on TV**<br>[HelgeSverre](https://github.com/HelgeSverre/devnull-tv) | Big-screen client for dev-null.sh, the social network for developers: the commit log of the people you add, drawn as a git graph, with ambient modes. | `8bc5f09` |
| **Ambient TV**<br>[Bryan-Cee](https://github.com/Bryan-Cee/Ambient) | Ambient dashboard for Samsung Tizen 5.5+ TVs: clock, weather, calendar, Google Photos slideshow and daily quotes. | `73bc869` |
| **Arn0 Launcher**<br>[NelsonEU](https://github.com/NelsonEU/arn0-tv) | Minimal remote-friendly home screen for Samsung TVs: a clock, your apps, your consoles and rotating wallpapers. | `b35c292` |
| **Baobab Signage**<br>[Gonqas](https://github.com/Gonqas/baobab) | Player for Baobab, open-source local digital signage: plays the playlist your own Baobab server on the LAN assigns to this screen. | `6ee8491` |
| **Copenhagen Weather**<br>[cocodedk](https://github.com/cocodedk/copenhagen-weather-tv) | Current conditions, hourly and 7-day forecast for Copenhagen on Samsung Tizen 6.0+ TVs. | `1a934d6` |
| **Frame Dashboard**<br>[joseamijares](https://github.com/joseamijares/frame-dashboard) | Daily dashboard for the Samsung Frame TV: a public-domain painting beside your calendar, focus and tasks. | `8cc81fe` |
| **Free My TV**<br>[simbasjungles](https://github.com/simbasjungles/free-my-tv) | Fast, ad-free home screen with your app shelf, weather, sunset-based day/night theme and a photo screensaver. | `v1.4.0` |
| **Haven**<br>[natureglass](https://github.com/natureglass/haven-tizen-ha) | Home Assistant powered home screen: sensors, lights and scenes by room, weather, live cameras, a Jellyfin client and music from Home Assistant's media folder. | `18ffa3e` |
| **Lobby**<br>[Lobby](https://github.com/CtznSniiips/Lobby) | Home screen for Samsung TVs with your Emby (or Jellyfin) server's Continue Watching, Live TV and teams, and Seerr's trending titles. | `efb4c05` |
| **Nhà Mình**<br>[meocong](https://github.com/meocong/prj-tv-samsung) | Apple TV-style home screen for Samsung Tizen TVs: your installed apps, a YouTube shelf, weather, a lunar calendar, news, an English word of the day read aloud, Bing wallpapers and a family photo screensaver. | `v1.4.0` |
| **Sportlink Club Viewer**<br>[PatrickSt1991](https://github.com/PatrickSt1991/Sportlink.Club.Info.Viewer) | Solution for sports clubs to display match information in real time and in a clear, organized way on screens throughout the club! | `v1.1.0` |
| **TizenTVAudioRecorder**<br>[TizenTVWebApp](https://github.com/TizenTVWebApp/TizenTVAudioRecorder) | HTML5 Audio Recorder (kalaoke App). | `latest` |
| **TV Clock**<br>[anandhuremanan](https://github.com/anandhuremanan/samsung-tizen-clock-app) | Simple clock and screen saver for Samsung Tizen 6.0+ TVs. | `1b9ad6f` |
| **TV Dashboard**<br>[lvndry](https://github.com/lvndry/tv-dashboard) | A calm remote-first home screen: weather and news as a short letter, an app rack, and an ambient art gallery. | `d2b0c47` |
| **Wall**<br>[no-cover](https://github.com/no-cover/wall) | Digital photo frame for Samsung Tizen TVs: give it the URL of a ZIP of images, it downloads them and runs a configurable slideshow, with a background service that auto-starts it on boot. | `1.0.0` |

</details>

<details>
<summary>🔞 <b>Adult (18+)</b>: 1 package(s). Hidden in Apps2Samsung until you turn on its 18+ toggle.</summary>

| 🧩 Application | 📝 Description | ⚙️ Version |
|----------------|----------------|------------|
| **StashZen**<br>[StashZen](https://github.com/Stashified/StashZen) | A Stash client for Samsung Tizen TVs. | `v0.44.0` |

</details>

<!-- packages:end -->

> 💡 Want your app listed here? See the [Contributing](#-contributing--requesting-apps) section below.

---

## 🤝 Contributing & Requesting Apps

We welcome **community contributions** and **app suggestions**!

### 💬 Request an App
Open a new [Issue](../../issues/new?template=request-app.yml) to suggest an app for future bundles.  
Include:
- App name
- Description
- Link to source or homepage

### 📦 Contribute an App
Each app is defined by **one JSON file** in the [`packages/`](packages/) folder. You don't need to edit anything else.

1. **Fork** this repository.
2. **Add** a file named `packages/<owner>__<repo>.json` for your app (copy an existing one as a template). See [`packages/README.md`](packages/README.md) for every field and worked examples of the three types (`release`, `build`, `direct`).
3. **Pick a `category`** from [`data/categories.json`](data/categories.json) (what goes where: [Category, group and variant](packages/README.md#%EF%B8%8F-category-group-and-variant)). None fits? Use `other` and suggest a new one in the pull request.
4. **Open a pull request.** A bot automatically validates your file against [`packages.schema.json`](packages.schema.json) and the category list: a green check means it's ready to merge. Once merged, it's picked up by the next automated build.

Your app should:
- Meet [What we accept](packages/README.md#-what-we-accept): open source under any license that allows redistribution, or closed
  source with the author's permission and the `closed-source` label
- Be virus/malware-free
- Be tested on at least one Tizen device or emulator

> Just want to *suggest* an app without packaging it yourself? Use the **Request an App** option above.

> 🔞 **Adult (18+) apps** are accepted under the same rules, with `"adult": true` in the manifest. They ship in the
> bundle like any other package, but Apps2Samsung hides them until the user turns on its 18+ toggle, and this README
> lists them in their own collapsed 18+ section instead of under a category. Keep the `name` and `description`
> plain: they are the only thing shown before the user opts in.

> ⚠️ **Important:**  
> We can only include applications whose author allows redistribution, see [What we accept](packages/README.md#-what-we-accept).  
> Please make sure you have the legal right to redistribute any software you contribute.

### 🚫 What We Can't Include

- **Commercial streaming apps**: Netflix, Disney+, Prime Video, HBO Max, Spotify, official YouTube and friends.
  These are partner-signed and their DRM is provisioned against the TV they shipped on, so a copied `.wgt`
  can't legally be redistributed and wouldn't activate even if it installed. They're already built into most
  Samsung TVs.
- **Modded, cracked or "premium unlocked" builds** of paid apps or services.
- **Closed-source packages without the author's permission** to redistribute them ([What we accept](packages/README.md#-what-we-accept)).
- **Apps that come with unlicensed content** built in (IPTV playlists, pirate-site scrapers, torrent indexers), or that preset an add-on source providing it.
- **Rebrands of other projects** that remove the original credits or license.

Requests for these get closed as `wontfix`. It isn't gatekeeping: they simply can't work as side-loaded packages.

> 🗂️ **Your own app doesn't fit [What we accept](packages/README.md#-what-we-accept)?** You can still offer it from
> your [own repository](#-run-your-own-repository): users add it in Apps2Samsung themselves, and you are
> responsible for having the right to distribute what you publish there.

> 🏨 **Hospitality / hotel TVs (`HG…` models):** side-loading needs developer mode, which is enabled from the
> Smart Hub **Apps** screen, and hospitality firmware doesn't expose it. Nothing in this repo can be installed on
> those sets until the TV is taken out of hospitality mode.

---

## 🗂️ Run Your Own Repository

Don't want to wait for a review here, or does your app fall outside [What we accept](packages/README.md#-what-we-accept)? Publish your
own **signed repository** from your own GitHub repo. Users add it in Apps2Samsung and see your apps next to
this catalog, labelled with your repository's name.

Copy [`templates/independent-repo/`](templates/independent-repo/), add a signing key as a secret, and the
workflow publishes a signed manifest to your GitHub Pages. A finished setup to look at is
[Apps2Samsung/repository-example](https://github.com/Apps2Samsung/repository-example). The format is in
[`docs/repositories.md`](docs/repositories.md).

What you publish there isn't reviewed here: you are responsible for having the right to distribute it.

---

## 🔍 Security Scanning

Nobody on this project reads the source of every app in the bundle, and we don't pretend to. What we
do instead is run the same **automated scan** over every package, every time, and publish the result:

- **Before a PR is merged**: the [validate workflow](.github/workflows/validate-packages.yml) downloads
  the upstream artifact of each new or changed package and scans it, so the maintainer sees what the app
  asks for before it lands in the catalog.
- **Before every release**: the [sync workflow](.github/workflows/sync-packages.yml) scans every file in
  the bundle. Packages with a critical finding are dropped from that bundle. The report ships with the
  release as `scan-report.md` (and machine-readable `scan.json`) next to the packages.
- **On demand**: [Scan Release Packages](../../actions/workflows/scan-release.yml) re-scans any published
  bundle with fresh virus definitions.

The scanner is [`scripts/scan-packages.py`](scripts/scan-packages.py). For each `.wgt` / `.tpk` it reports:

| Check | What it tells you |
|-------|-------------------|
| **Privileges** | Every `tizen:privilege` the app requests, with partner/platform-level ones flagged and camera, microphone, storage and app-launch privileges called out. |
| **Hosts referenced** | Every hostname and public IP mentioned in the app's HTML/JS, plus any `<script src>` that loads code from the network at runtime. |
| **Signatures** | Who signed the package (author and distributor certificate subjects), when it carries a signature. |
| **Background behaviour** | Services that start at TV boot, background-support, any-origin network access. |
| **Code smells** | Known JavaScript packers/obfuscators, `eval`/`new Function`, native binaries inside a web app, a package nested inside a package. |
| **Known malware** | ClamAV with current definitions, and a short list of crypto-miner signatures. |

What it can't do: tell you whether the app's *logic* is benign. A Tizen web app runs sandboxed in the TV's web
runtime and can only do what its privileges allow, but within those limits the scan only shows you *what*
an app can reach, not *why*. Read the report, look at the upstream repository, and if something looks off,
[open an issue](../../issues). To check a bundle yourself:

```bash
gh release download --repo Apps2Samsung/tizen-community-packages -p '*.wgt' -p '*.tpk' -D bundle
python3 scripts/scan-packages.py bundle --md scan-report.md
```

---

## ⚠️ Disclaimer

This is a **community-driven project** and is **not officially affiliated with or endorsed by Samsung** or the Tizen Project.

> **THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND.**  
> All applications remain the property of their respective owners.  
> Please support the original developers by visiting their official pages.

---

## 📝 Additional Note

You need to make a Samsung Certificate (Tools > Certificate Manager) to run any of the packages listed above. In case you're having any issues, refer to [Connection Guide](https://developer.samsung.com/smarttv/develop/getting-started/using-sdk/tv-device.html).

---

## 📄 License

This repository (including the bundling scripts and metadata) is licensed under the [MIT License](LICENSE).

Each included application retains its **original license**.  
Please refer to the source links in the *Current Packages* table for individual licensing information.
