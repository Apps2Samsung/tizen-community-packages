# 🌐 Tizen Community Packages
[![Sync Tizen Community Packages](https://github.com/Apps2Samsung/tizen-community-packages/actions/workflows/sync-packages.yml/badge.svg)](https://github.com/Apps2Samsung/tizen-community-packages/actions/workflows/sync-packages.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Packages](https://img.shields.io/badge/packages-107-blue.svg)](#-current-packages)
[![Contributions Welcome](https://img.shields.io/badge/Contributions-Welcome-green.svg)](../../issues)
[![Tizen](https://img.shields.io/badge/Platform-Tizen-lightgrey.svg)](https://www.tizen.org/)
[![Community](https://img.shields.io/badge/Community-Driven-orange.svg)](#)

> **Community-curated bundles of Tizen web applications (`.wgt` packages)** —  
> compiled into single, convenient releases for easier installation and testing on your Tizen devices.

---

## 📑 Table of Contents

- [What Is This?](#-what-is-this)
- [Current Packages](#-current-packages)
- [Contributing & Requesting Apps](#-contributing--requesting-apps)
- [Security Scanning](#-security-scanning)
- [Disclaimer](#️-disclaimer)
- [Additional Note](#-additional-note)
- [License](#-license)

---

## 📦 What Is This?

This repository provides bundled releases containing multiple Tizen applications (`.wgt` files).  
Instead of downloading and installing each app individually, you can grab a single **bundle** that includes several community apps — ready for side-loading onto your Tizen devices.

Each release represents a curated collection of useful, fun, or open-source Tizen web apps.

---

## 📋 Current Packages

This table lists the applications included in the latest community bundle.  
Please check the [Releases](../../releases) page for version-specific details.

| 🧩 Application | 🏷️ Category | 📝 Description | 🔗 Repository | ⚙️ Version |
|----------------|-------------|----------------|------------------|------------|
| **/dev/null on TV** | Other | Big-screen client for dev-null.sh, the social network for developers: the commit log of the people you add, drawn as a git graph, with ambient modes. Read-only public API, no login. | [HelgeSverre](https://github.com/HelgeSverre/devnull-tv) | `8bc5f09` |
| **30nama** | Streaming | Unofficial 30nama.com client for Samsung Tizen TVs. | [msharifi99](https://github.com/msharifi99/30nama-tizenos) | `v1.2.1` |
| **AIOStreams** | Streaming | Tizen build of AIOStreams, the all-in-one Stremio super-addon for debrid and Usenet sources. | [thomasrtg](https://github.com/thomasrtg/AIOStreams) | `tizen6-v0.4.0-beta.1` |
| **AirTizen** | Casting & cameras | AirPlay receiver for Samsung Tizen TV — stream audio/video to older Samsung TVs. | [MrHumanRebel](https://github.com/MrHumanRebel/airtizen) | `v2.2.34` |
| **Ambient TV** | Other | Ambient dashboard for Samsung Tizen 5.5+ TVs: clock, weather, calendar, Google Photos slideshow and daily quotes. Google Photos and calendar need the project's optional companion service on your LAN. | [Bryan-Cee](https://github.com/Bryan-Cee/Ambient) | `73bc869` |
| **AmorecoFlix** | Media servers & players | Personal Netflix-style player for a USB drive plugged into the TV: posters, synopses, continue watching, next episode, skip intro, audio and subtitle choice. No server needed; PowerShell scripts in the repo organise the library on a PC. Portuguese UI. | [Pablitorox](https://github.com/Pablitorox/AmorecoFlix) | `be7c97c` |
| **AniLiberty** | Streaming | Unofficial AniLibria anime client for Samsung Tizen TV. | [CoreDip](https://github.com/CoreDip/anilibria-tizen-wgt) | `v1.1.0` |
| **AniUltimatium** | Streaming | Anime streaming app for Samsung Tizen TVs. | [AdvaithAvinash](https://github.com/AdvaithAvinash/AniUltimatium) | `stable-v1.14` |
| **Apex TV** | Streaming | Independent F1 TV client for Samsung Tizen 6.0+. Sign in with your own F1 TV subscription. English and Lithuanian menus. | [Pajuodelis](https://github.com/Pajuodelis/apex-tv) | `v0.5.12` |
| **App Manager** | Tools & system | Alternative launcher for Samsung Tizen TVs: lists installed third-party and sideloaded apps in one grid to launch them, or hide them from Smart Hub without uninstalling. | [no-cover](https://github.com/no-cover/appmanager) | `1.0.3` |
| **AquaPlay IPTV** | IPTV & Live TV | Lightweight IPTV player for M3U and Xtream playlists, with a full guide, catch-up and setup from your phone | [AquaPlay IPTV](https://github.com/AquaPlayIPTV/aquaplay-samsung) | `v1.0.50` |
| **Arn0 Launcher** | Other | Minimal remote-friendly home screen for Samsung TVs: a clock, your apps, your consoles and rotating wallpapers. | [NelsonEU](https://github.com/NelsonEU/arn0-tv) | `b35c292` |
| **Baobab Signage** | Other | Player for Baobab, open-source local digital signage: plays the playlist your own Baobab server on the LAN assigns to this screen. Server URL and screen key are written into the package on install. | [Gonqas](https://github.com/Gonqas/baobab) | `6ee8491` |
| **Beam-TV** | Media servers & players | Open-source USB and DLNA media player for Samsung Tizen TVs — subtitles, resume playback, remote navigation, and a local companion server. | [TAGISWILD](https://github.com/TAGISWILD/beam-tv) | `v1.0.1` |
| **bilibili** | Streaming | Unofficial bilibili client for Samsung TVs, driven entirely by the remote: QR sign-in with multiple accounts, continue-watching row, danmaku, search, live, up to 1080p H.265 (4K with premium). Installs on Tizen 3.0+; tested on Tizen 5.5 and 9.0, playback on older sets not confirmed yet. Updates itself. Talks to bilibili directly, no backend or proxy. | [titlog](https://github.com/titlog/bilibili-tizen) | `v1.4.2` |
| **Bisnor** | Streaming | Open-source Persian movie and series client (experimental Tizen TV build): browse, search and play titles from the IranFlix catalogue with AVPlay. Persian UI. | [nikan48g](https://github.com/nikan48g/Bisnor) | `258b10b` |
| **Camera PiP** | Casting & cameras | Doorbell and driveway cameras on a Samsung Tizen TV: pops up on a trigger (Home Assistant or any webhook), plays through the hardware decoder so the app behind it keeps running, and fires actions like opening the gate from the remote. Needs go2rtc or another HLS/MJPEG source; cameras are configured at build time. | [dzikus](https://github.com/dzikus/tizen-camera-pip) | `v1.2.0` |
| **Chiaki-Tizen** | Games & emulators | An open source PlayStation remote play project serving as the next-generation of Chiaki. | [Chiaki-Tizen](https://github.com/Trent407/chiaki-tizen) | `v0.2.0` |
| **Chorus2-Tizen** | Media servers & players | Chorus2-Tizen (Kodi) Samsung Tizen. | [Chorus2-Tizen](https://github.com/PatrickSt1991/chorus2-tizen) | `tizen-v21.x-1.0.1-2026-05-21-1443` |
| **Chouette TV** | IPTV & Live TV | IPTV player for Samsung Tizen 2.3+ TVs: Xtream and M3U sources, EPG, favourites, profiles and resume. Ships with no channels; connect your own source in Settings. French UI. | [ipaifix](https://github.com/ipaifix/chouette-tv) | `794dbef` |
| **Copenhagen Weather** | Other | Current conditions, hourly and 7-day forecast for Copenhagen on Samsung Tizen 6.0+ TVs. Open-Meteo data, no API key and no account. | [cocodedk](https://github.com/cocodedk/copenhagen-weather-tv) | `1a934d6` |
| **Doom** | Games & emulators | A WebAssembly-powered port of Doom packaged as a Samsung Tizen TV application. | [dos-ise](https://github.com/dos-ise/doom-tizen) | `v1.1` |
| **Douyin (抖音)** | Streaming | Unofficial Douyin client for Samsung Tizen 6.0+ TVs, driven by the remote: Featured, Following and For You feeds, QR sign-in, your history, likes and favourites, creator pages, collections and comments. Updates itself. Talks to Douyin directly, no backend or proxy. Chinese UI. | [titlog](https://github.com/titlog/douyin-tizen) | `v1.4.3` |
| **EN TV Player** | IPTV & Live TV | IPTV player for Samsung Tizen TVs with DRM support, M3U/M3U8 playlists, groups and live TV. | [Nur-allhi](https://github.com/Nur-allhi/en-tvplayer) | `v3.2.0` |
| **FCast** | Casting & cameras | FCast is an open source protocol that enables wireless streaming of audio and video content between devices. | [futo-org](https://github.com/futo-org/FCastReceiver) | `Wed, 08 Oct 2025 17:07:02 GMT` |
| **Fladder** | Media servers & players | Jellyfin client for Samsung Tizen TV, built with Flutter (native .tpk). | [popdollar](https://github.com/popdollar/Fladder-Tizen) | `Tizen` |
| **Flixor-Tizen** | Media servers & players | Modern cross-platform Plex client. Ported to Tizen OS. | [Flixor-Tizen](https://github.com/PatrickSt1991/flixor-tizen) | `v1.0.1-2026-07-24-1215` |
| **FLOH IPTV** | IPTV & Live TV | A fast IPTV player for Samsung TVs. You enter the M3U link of your own provider. | [kingflooow](https://github.com/kingflooow/floh-iptv) | `v1.4.1` |
| **Frame Dashboard** | Other | Daily dashboard for the Samsung Frame TV: a public-domain painting beside your calendar, focus and tasks. Thin shell around your own deployment of the hosted dashboard; its URL is written into the package on install. | [joseamijares](https://github.com/joseamijares/frame-dashboard) | `b4fbf67` |
| **Free My TV** | Other | Fast, ad-free home screen with your app shelf, weather, sunset-based day/night theme and a photo screensaver. | [simbasjungles](https://github.com/simbasjungles/free-my-tv) | `v1.1.0` |
| **FreeSerf** | Games & emulators | An open-source recreation of The Settlers 1 (Serf City) compiled to WebAssembly for Samsung Tizen TVs. | [dos-ise](https://github.com/dos-ise/freeserf-tizen) | `v1.0` |
| **GameBoy-Emulator** | Games & emulators | A Game Boy (DMG) emulator. | [dos-ise](https://github.com/dos-ise/GB-EMU_Tizen) | `v1.2` |
| **go2rtc** | Casting & cameras | Watch the cameras of a go2rtc server (standalone or embedded in Frigate): camera grid with previews and full-screen live view. | [Edsol](https://github.com/Edsol/go2rtc-tizen) | `v0.1.0` |
| **HackTV** | IPTV & Live TV | IPTV client for Samsung Tizen TVs. | [kosmodrey](https://github.com/kosmodrey/hackTV) | `bf27ba9` |
| **HyperTizen** | Tools & system | Hyperion / HyperHDR ambient-light capturer for Samsung Tizen TV (native .tpk; requires TizenBrew for the UI). | [reisxd](https://github.com/reisxd/HyperTizen) | `v1.0.0` |
| **ImmiTV** | Media servers & players | Lightweight Immich photo and video client for Samsung Tizen 4.0 TVs: remote-control navigation, hardware-accelerated AVPlay video playback and a month-based timeline. | [xHiqhAim](https://gitlab.com/xHiqhAim/immitv) | `76d693a` |
| **inet-speed-old-tizen** | Tools & system | Internet diagnostics for Samsung Tizen 2.4+ TVs: response times of popular sites and download speed from Cloudflare, Fastly and HOSTKEY test CDNs, plus TV model, firmware and network info. English and Russian UI. No proxy or server needed. | [numbereleven-a](https://github.com/numbereleven-a/inet-speed-old-tizen) | `v1.0.2` |
| **iperf3 TV** | Tools & system | Measures your Samsung TV's network throughput to an iperf3 server, upload or download. Requires a small WebSocket-to-TCP relay on your LAN. | [DmitryMaksakov](https://github.com/DmitryMaksakov/samsung-tv-iperf3) | `d20ac9f` |
| **IPTV Manager** | IPTV & Live TV | IPTV manager for Samsung Tizen TV with Xtream Codes support and HLS playback. | [matifDreamIt](https://github.com/matifDreamIt/IPTV-Tizen-TV) | `d8eb66b` |
| **Jellyfin + Bonfire** | Media servers & players | Official Jellyfin Tizen client patched with the Bonfire loader for multi-user profile switching. Requires the Bonfire plugin on your Jellyfin server. | [jellyfin](https://github.com/jellyfin/jellyfin-tizen) | `31408c1` |
| **Kick TV 2.0** | Streaming | Kick live streams and public archives for Samsung Tizen TVs. | [janrydzewski](https://github.com/janrydzewski/kick-tv-2.0) | `v2.0.1` |
| **KickTV** | Streaming | Kick.com streaming client for Samsung Tizen TVs. | [corekill](https://github.com/corekill/kick-tv-tizen) | `v2.2.3` |
| **Kodi** | Media servers & players | Unofficial WebAssembly port of Kodi for Samsung Tizen TVs (alpha). | [Ricrdsson1](https://github.com/Ricrdsson1/kodi-tizen-wasm) | `Alpha-0.0.8` |
| **Kodi-TeX** | Media servers & players | Kodi TeX web interface ported to Samsung Tizen. | [PatrickSt1991](https://github.com/PatrickSt1991/tex-tizen) | `tex-tizen-v1.3.0-2026-06-09-0952` |
| **KROMA** | Media servers & players | Client for KROMA, a self-hosted direct-play media server for your NAS. Needs your own KROMA server. | [kromatv](https://github.com/kromatv/kroma) | `v0.1.38` |
| **Lampa** | Streaming | Free movie and TV catalogue with info, new releases and trailers. Can be extended with user plugins. | [yumata](https://github.com/yumata/lampa) | `v1.4.1` |
| **Moonlight** | Games & emulators | Open-source client for NVIDIA GameStream and Sunshine. | [OneLiberty](https://github.com/OneLiberty/moonlight-chrome-tizen) | `v1.2.1` |
| **Moonlight (No Gamemode)** | Games & emulators | Open-source client for NVIDIA GameStream and Sunshine with gamemode disabled. | [MrPhaze62](https://github.com/MrPhaze62/moonlight-chrome-tizen-no-gamemode) | `samsung_wasm-21031261929` |
| **Moonlight (ToypoodleGaming)** | Games & emulators | Moonlight NVIDIA GameStream / Sunshine client (ToypoodleGaming fork). | [toypoodlegaming](https://github.com/toypoodlegaming/moonlight-chrome-tizen) | `samsung_wasm-21031332442` |
| **Moonlight Enhanced (AC-3)** | Games & emulators | Open-source Moonlight client for Tizen OS with optional support for Dolby Digital and Dolby Digital Plus (stereo and 5.1) optical-audio and HDMI passthrough. | [fidoboy](https://github.com/fidoboy/moonlight-tizen-ac3) | `v1.0.6` |
| **Moonlight-Tizen** | Games & emulators | Open-source client for NVIDIA GameStream and Sunshine Tizen OS 5.5 or higher. | [BrightCraft](https://github.com/brightcraft/moonlight-tizen) | `v1.19.0` |
| **Nuvio** | Streaming | TV-first streaming UI for Samsung Tizen. | [NuvioMedia](https://github.com/NuvioMedia/NuvioWeb) | `1.2.9` |
| **Nuvio Native Legacy** | Streaming | Unofficial native C/SDL2 Nuvio client, fast on older TVs. Native .tpk per Tizen version (4.0-5.5, 6.0, 6.5-7, 8-9) plus a WebAssembly .wgt for Tizen 5.5+. | [iqui27](https://github.com/iqui27/nuvio-native-legacy) | `v2.0.8` |
| **OpenIPTV** | IPTV & Live TV | Privacy focused IPTV player for Samsung Tizen TVs with extended M3U playlists, favourites and search. | [shayanline](https://github.com/shayanline/OpenIPTV) | `1.9.3` |
| **OTTplay FOSS** | IPTV & Live TV | FOSS OTT / IPTV thin client for Tizen. | [prog4food](https://github.com/prog4food/ottplay-foss-thin-clients) | `Sat, 21 Jan 2023 15:15:16 GMT` |
| **Overscan** | Tools & system | Sideloadable web browser for Samsung Tizen TVs: desktop user agent, JavaScript on, D-pad cursor. | [Apps2Samsung](https://github.com/Apps2Samsung/Overscan) | `build-363c881` |
| **Pelagica** | Media servers & players | A modern web, desktop and TV client for Jellyfin | [PelagicaApp](https://github.com/PelagicaApp/pelagica) | `4.14.0` |
| **PlayerAVPlay** | Media servers & players | AVPlayer app | [yadPe](https://github.com/yadPe/PlayerAVPlay) | `latest` |
| **Prairie** | Media servers & players | Flutter client for the self-hosted Prairie media server (native .tpk): multi-server registry with LAN discovery, profiles with PIN, Quick Connect sign-in and AVPlay playback. | [Prairie-Server](https://github.com/Prairie-Server/prairie-smarttv) | `v0.5.4` |
| **React IPTV** | IPTV & Live TV | IPTV player for Samsung Tizen TV, built with React. | [anandsimmy](https://github.com/anandsimmy/react-iptv) | `7a7dcc2` |
| **Reelo** | Streaming | TV client for the Reelo service: films and series with a remote-first interface, family profiles and library sync between devices (Russian UI). | [Reelo](https://github.com/ihovsky/Reelo) | `Sat, 24 Oct 2026 05:55:36 GMT` |
| **Reiverr** | Media servers & players | A clean combined interface for Jellyfin, TMDB, Radarr and Sonarr, as well as a replacement to Overseerr. | [aleksilassila](https://github.com/aleksilassila/reiverr) | `dbdd50d` |
| **Reolink Viewer** | Casting & cameras | Watch a Reolink camera or NVR on your TV: enter its local IP and login, press Start. Plays the camera's H.264 FLV stream over the LAN, or H.265 main streams over RTSP through a relay inside the app (2018+ TVs). No cloud or helper box. | [Apps2Samsung](https://github.com/Apps2Samsung/ReolinkViewer) | `v1.1.0` |
| **RetroArch** | Games & emulators | RetroArch (libretro WebAssembly) for Samsung Tizen 6.5+ TVs: remote-driven launcher, gamepad support, ROMs from a USB drive or a network folder. Emulator cores are downloaded on first start, so the TV needs internet access. | [Sype0](https://github.com/Sype0/retroarch-tizen) | `v0.3.2` |
| **RetroTV** | Games & emulators | Retro game console for Samsung Tizen 5.0+ TVs: WebAssembly emulator cores downloaded on first use, games copied over the LAN from the project's companion server on a PC, or streamed from that PC. Portuguese UI. | [guhcostan](https://github.com/guhcostan/retro-tv) | `062fb72` |
| **RTSP Camera Viewer** | Casting & cameras | Display RTSP streams from IP cameras on your Samsung TV, with numpad channel switching and a 4-camera grid. Requires the companion rtsp-samsung-tv server (Node or Docker) running on your LAN. | [vzakharchenko](https://github.com/vzakharchenko/rtsp-samsung-tv) | `3aefa34` |
| **RÚV** | IPTV & Live TV | Apps for RÚV, the Icelandic national broadcaster: Sarpur on demand, Barnaefni for children, Unglingar for teens, Menntun for education, and Útvarp radio (not affiliated with RÚV) | [RÚV VOD](https://github.com/sverrirs/ruv-app-samsung) | `2026.08.25-2350` |
| **RÚV Live** | IPTV & Live TV | Live TV from RÚV, the Icelandic national broadcaster: the RÚV and RÚV 2 channels, with the running schedule and rewind inside the live window (not affiliated with RÚV) | [RÚV Live](https://github.com/sverrirs/ruv-live-samsung) | `2026.08.25` |
| **SamSUCKS** | Media servers & players | Fast from-scratch Plex client for Samsung Tizen 6.5+ TVs: smooth scrolling, hardware AVPlay playback with direct play, instant search, audio/subtitle picker and up-next autoplay. Plain JavaScript, no framework. | [rfaile313](https://github.com/rfaile313/samsucks) | `6b00e92` |
| **SeanimeTV** | Streaming | Unofficial Seanime client for Samsung Tizen TVs with torrent streaming and AVPlay playback. | [ihiqhaim](https://github.com/ihiqhaim/SeanimeTV-Tizen) | `4da9288` |
| **Sendspin Cinema** | Media servers & players | Minimal cinema-style Sendspin player for Music Assistant on Samsung Tizen 3.0+ TVs: album art with adaptive accent colours, set up from the TV screen. Needs a Music Assistant server. | [zonya](https://github.com/zonya/sendspin-cinema-tizen) | `0eabc15` |
| **Simple TV Player** | IPTV & Live TV | Minimal jQuery and hls.js channel player for Samsung Tizen 6.0+ TVs. Plays the M3U8 channel list served by the author's API (free-to-air Brazilian channels), navigated with the remote arrows. | [RandoMixs](https://github.com/RandoMixs/simple-tv-player) | `0.0.1` |
| **SKY IPTV** | IPTV & Live TV | IPTV player for Samsung Tizen 5.0+ TVs: M3U and Xtream playlists, remote-friendly UI, audio and subtitle track switching, embedded mov_text subtitles. Bring your own playlist. | [sanwhere](https://github.com/sanwhere/sky-iptv-tizen) | `v1.1.1` |
| **Snake** | Games & emulators | Snake game for Samsung Tizen TVs, played with the remote. | [pvk689](https://github.com/pvk689/snake-game-tizen) | `62ccffc` |
| **Sonance3** | Media servers & players | A music player for Samsung Tizen TVs, built to stream from your self-hosted Navidrome or Subsonic-compatible server. | [MrSimmo](https://github.com/MrSimmo/sonance3) | `v3.14` |
| **Sportlink Club Viewer** | Other | Solution for sports clubs to display match information in real time and in a clear, organized way on screens throughout the club! | [PatrickSt1991](https://github.com/PatrickSt1991/Sportlink.Club.Info.Viewer) | `v1.1.0` |
| **StreamVault** | IPTV & Live TV | IPTV streaming app for Samsung Tizen TVs built with React, TypeScript, and Zustand. | [StreamVault](https://github.com/christopherklint97/streamvault) | `wgt-v1.0.0-39066361899-1` |
| **Stremio (Tizen 4)** | Streaming | Stremio media center packaged for Tizen 4.0 devices. | [Apps2Samsung](https://github.com/Apps2Samsung/tizen-community-packages) | `latest` |
| **StremioK** | Streaming | From-scratch Stremio-addon streaming client for Samsung Tizen 3.0+ TVs: catalogs, sources and subtitles from the addons you add, Trakt sync, IPTV from your M3U playlists, YouTube and USB playback. Hosts no media; needs stream addons that return direct HTTP/HLS URLs. | [Kepler75](https://github.com/Kepler75/StremioK) | `v2.2.0` |
| **tacplayer** | Media servers & players | Custom Jellyfin Tizen client with cinematic red UI for Samsung TV | [sfsdffesfsfg-cloud](https://github.com/sfsdffesfsfg-cloud/tacplayer) | `v0.1.0` |
| **Tailscale** | Tools & system | Tailscale exit-node app for Samsung Tizen TV (experimental; advertises the TV as a tailnet exit node). | [PatrickSt1991](https://github.com/PatrickSt1991/tailscale-tizen) | `tv8-tester` |
| **Telegram Videos** | Streaming | Plays the videos in your Telegram groups and channels on Samsung Tizen 6.0+ TVs: QR sign-in, several accounts, MP4 and MKV streamed while downloading, audio tracks and subtitles, search across chats. Chinese and English UI. Updates itself. | [titlog](https://github.com/titlog/telegram-tizen) | `v1.1.5` |
| **Tessel** | Media servers & players | Media player for Samsung TVs: SMB shares, USB drives, network streams and subtitles, with an optional transcode server (formerly VLC-Tizen-tv). | [PatrickSt1991](https://github.com/PatrickSt1991/tessel-tizen-tv) | `v1.30.0-20261022-1315` |
| **Tizen Debug App** | Tools & system | Developer toolkit for troubleshooting apps and monitoring system state on real Samsung Tizen TV hardware. Hybrid web + .NET/C++ build for Tizen 4.0+, plus a web-only build for Tizen 3.0. | [no-cover](https://github.com/no-cover/tizendebugapp) | `1.0.0` |
| **Tizen Steam Link** | Games & emulators | Unofficial Steam Link client for Samsung Tizen 5.5+ TVs: streams games from Steam on a PC or Steam Deck, with the TV's hardware decoder and controllers, keyboard and mouse passed through. | [pebeto](https://github.com/pebeto/tizen-steam-link) | `v0.2.1` |
| **TizenAmbilight** | Tools & system | Real-frame ambilight: reads the TV's own video plane in memory and drives a WLED strip over UDP. While a streaming app's DRM withholds the plane, falls back to the TV's built-in RGB measurement (coarser and slower). Headless background service (.tpk); no Hyperion/HyperHDR needed. | [RitwickVerma](https://github.com/RitwickVerma/TizenAmbilight) | `v1.0.0` |
| **TizenBrew** | Tools & system | A way to experience modded websites and you can install newer apps without fighting with Tizen Studio. | [reisxd](https://github.com/reisxd/TizenBrew) | `v2.0.5` |
| **TizenFeed** | Other | News / RSS feed sample app for Tizen TV. | [judithsirera](https://github.com/judithsirera/TizenFeed) | `8c42b51` |
| **TizenTube Old Tizen** | Streaming | Standalone YouTube with SponsorBlock for older Samsung TVs (Tizen 2.4 and 3.0). Runs entirely on the TV, no companion server needed. | [numbereleven-a](https://github.com/numbereleven-a/TizenTube-old-tizen) | `v2.3.21` |
| **TizenTVAudioRecorder** | Other | HTML5 Audio Recorder (kalaoke App). | [TizenTVWebApp](https://github.com/TizenTVWebApp/TizenTVAudioRecorder) | `latest` |
| **TizenUtility** | Tools & system | System utility for Samsung Tizen TVs: detailed device, firmware and network info, plus a launcher for hidden built-in Samsung apps that are not reachable from the normal UI. | [no-cover](https://github.com/no-cover/tizenutility) | `1.1.1` |
| **Torr Streaming** | Tools & system | Runs TorrServer as a background service on the TV itself, so local web apps can stream torrents directly without a separate box. Hybrid .NET package with a small launcher widget; Tizen 4.0+. | [no-cover](https://github.com/no-cover/torr-streaming) | `1.0.0` |
| **TransportTycoonDeluxe** | Games & emulators | OpenTTD is an open source simulation game based upon Transport Tycoon Deluxe. | [dos-ise](https://github.com/dos-ise/openttd-tizen) | `Release` |
| **TubeArchivist TV** | Media servers & players | 10-foot client for your self-hosted TubeArchivist: pair from your phone, never type on the remote. Needs the project's gateway and transcoder containers on your LAN; the gateway URL is written into the package on install. | [raykholo](https://github.com/raykholo/tubearchivist-tv) | `3cb035f` |
| **TV Clock** | Other | Simple clock and screen saver for Samsung Tizen 6.0+ TVs. | [anandhuremanan](https://github.com/anandhuremanan/samsung-tizen-clock-app) | `1b9ad6f` |
| **TVapp** | IPTV & Live TV | Enable seamless playback of HLS/m3u8 streams as channels. | [KaashDev](https://github.com/KaashDev/TVapp) | `latest` |
| **TVideoPlayer** | Media servers & players | Tizen TV HTML video player based on videojs. | [TizenTVWebApp](https://github.com/TizenTVWebApp/TVideoPlayer) | `latest` |
| **Twitch** | Streaming | Twitch client for Samsung Smart TVs 2015 and newer models. | [fgl27](https://github.com/fgl27/smarttv-twitch) | `ca31512` |
| **Twitch Old Tizen** | Streaming | Twitch client for older Samsung Tizen TVs (2.4/3.0) with 720p/1080p playback fixes for channels that enable 1440p, plus device-code sign-in. | [numbereleven-a](https://github.com/numbereleven-a/smarttv-twitch-old-tizen) | `4.1.2` |
| **UniFi Cameras** | Casting & cameras | Live camera grid for UniFi Protect or any RTSP cameras on Samsung Tizen 6.0+ TVs, D-pad to go fullscreen. Needs the project's restreamer (ffmpeg and Python) on an always-on LAN host; its address is written into the package on install. | [xtantaudio](https://github.com/xtantaudio/unifi-cameras-on-tizen) | `2f7f8c0` |
| **VeloVistrix** | Media servers & players | Read-only PhotoPrism viewer for Samsung Tizen 5.0+ TVs, driven by the remote: albums, places, calendar, labels and folders from your own server, with slideshow. Sign in with an app password, or straight in if the server runs in public mode. | [zephy-lee](https://github.com/zephy-lee/velovistrix-tizen) | `d136678` |
| **Velvet TV** | Media servers & players | Big-screen TV client for the Velvet self-hosted music server. | [aroundmyroom](https://github.com/aroundmyroom/Velvet) | `c0d278d` |
| **Vemm** | Media servers & players | Unofficial Plex-compatible media player for Samsung Tizen TVs with AVPlay playback, Direct Play and server transcoding. | [somefosterkid](https://github.com/somefosterkid/vemm) | `preview-0.9.0` |
| **VexonTV** | IPTV & Live TV | Live TV player for Samsung Tizen TVs: M3U, Xtream Codes and Stalker portals, provider EPG and a remote-first interface. | [VexonTV](https://github.com/DvzZDev/VexonTV) | `9aa670e` |
| **Wall** | Other | Digital photo frame for Samsung Tizen TVs: give it the URL of a ZIP of images, it downloads them and runs a configurable slideshow, with a background service that auto-starts it on boot. | [no-cover](https://github.com/no-cover/wall) | `1.0.0` |
| **YouTube Dummy** | Streaming | Lightweight wrapper around youtube.com/tv that injects the TizenTube userscript (ad-free, SponsorBlock), handles remote-control navigation and exits cleanly back to Smart Hub. | [no-cover](https://github.com/no-cover/youtube-dummy) | `1.0.0` |
| **YouTube for Tizen** | Streaming | Ad-free YouTube for Samsung TVs, running in Samsung's own Cobalt engine with SponsorBlock, DeArrow and preferred-quality settings. Tizen 5.5+ build plus a separate widget for Tizen 5.0. Requires a Samsung partner certificate. | [SushyDev](https://github.com/SushyDev/tizen-youtube) | `v1.5.1` |

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
Each app is defined by **one JSON file** in the [`packages/`](packages/) folder — you don't need to edit anything else.

1. **Fork** this repository.
2. **Add** a file named `packages/<owner>__<repo>.json` for your app (copy an existing one as a template). See [`packages/README.md`](packages/README.md) for every field and worked examples of the three types (`release`, `build`, `direct`).
3. **Open a pull request.** A bot automatically validates your file against [`packages.schema.json`](packages.schema.json) — a green check means it's ready to merge. Once merged, it's picked up by the next automated build.

Your app should be:
- Open-source (or redistributable under a permissive license)
- Virus/malware-free
- Tested on at least one Tizen device or emulator

> Just want to *suggest* an app without packaging it yourself? Use the **Request an App** option above.

> ⚠️ **Important:**  
> We can only include applications that are **open-source** and **freely distributable**.  
> Please make sure you have the legal right to redistribute any software you contribute.

### 🚫 What We Can't Include

- **Commercial streaming apps** — Netflix, Disney+, Prime Video, HBO Max, Spotify, official YouTube and friends.
  These are partner-signed and their DRM is provisioned against the TV they shipped on, so a copied `.wgt`
  can't legally be redistributed and wouldn't activate even if it installed. They're already built into most
  Samsung TVs.
- **Modded, cracked or "premium unlocked" builds** of paid apps or services.
- **Closed-source packages** with no license that permits redistribution.

Requests for these get closed as `wontfix`. It isn't gatekeeping — they simply can't work as side-loaded packages.

> 🏨 **Hospitality / hotel TVs (`HG…` models):** side-loading needs developer mode, which is enabled from the
> Smart Hub **Apps** screen — hospitality firmware doesn't expose it. Nothing in this repo can be installed on
> those sets until the TV is taken out of hospitality mode.

---

## 🔍 Security Scanning

Nobody on this project reads the source of every app in the bundle, and we don't pretend to. What we
do instead is run the same **automated scan** over every package, every time, and publish the result:

- **Before a PR is merged** — the [validate workflow](.github/workflows/validate-packages.yml) downloads
  the upstream artifact of each new or changed package and scans it, so the maintainer sees what the app
  asks for before it lands in the catalog.
- **Before every release** — the [sync workflow](.github/workflows/sync-packages.yml) scans every file in
  the bundle. Packages with a critical finding are dropped from that bundle. The report ships with the
  release as `scan-report.md` (and machine-readable `scan.json`) next to the packages.
- **On demand** — [Scan Release Packages](../../actions/workflows/scan-release.yml) re-scans any published
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

You need to make a Samsung Certificate (Tools > Certficate Manager) to run any of the packages listed above. In case you're having any issues, refer to [Connection Guide](https://developer.samsung.com/smarttv/develop/getting-started/using-sdk/tv-device.html).

---

## 📄 License

This repository (including the bundling scripts and metadata) is licensed under the [MIT License](LICENSE).

Each included application retains its **original license**.  
Please refer to the source links in the *Current Packages* table for individual licensing information.
