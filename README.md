# 🌐 Tizen Community Packages
[![Sync Tizen Community Packages](https://github.com/Apps2Samsung/tizen-community-packages/actions/workflows/sync-packages.yml/badge.svg)](https://github.com/Apps2Samsung/tizen-community-packages/actions/workflows/sync-packages.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
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

| 🧩 Application | 📝 Description | 🔗 Repository |
|----------------|----------------|------------------|
| **Moonlight-Tizen** | Open-source client for NVIDIA GameStream and Sunshine Tizen OS 5.5 or higher. | [BrightCraft](https://github.com/brightcraft/moonlight-tizen) |
| **Moonlight** | Open-source client for NVIDIA GameStream and Sunshine. | [OneLiberty](https://github.com/OneLiberty/moonlight-chrome-tizen) |
| **Moonlight (No Gamemode)** | Open-source client for NVIDIA GameStream and Sunshine with gamemode disabled. | [MrPhaze62](https://github.com/MrPhaze62/moonlight-chrome-tizen-no-gamemode) |
| **Fireplace** | Transform your Samsung Smart TV into a fireplace. | [thonythony](https://github.com/thonythony/fireplace) |
| **TVapp** | Enable seamless playback of HLS/m3u8 streams as channels. | [KaashDev](https://github.com/KaashDev/TVapp) |
| **Twitch** | Twitch client for Samsung Smart TVs 2015 and newer models. | [fgl27](https://github.com/fgl27/smarttv-twitch) |
| **Sportlink Club Viewer** | Solution for sports clubs to display match information in real time and in a clear, organized way on screens throughout the club! | [PatrickSt1991](https://github.com/PatrickSt1991/Sportlink.Club.Info.Viewer) |
| **VLC-Tizen-tv** | VLC Like player for your Samsung TV. | [PatrickSt1991](https://github.com/PatrickSt1991/vlc-tizen-tv) |
| **TizenBrew** | A way to experience modded websites and you can install newer apps without fighting with Tizen Studio. | [reisxd](https://github.com/reisxd/TizenBrew) |
| **TizenTVAudioRecorder** | HTML5 Audio Recorder (kalaoke App). | [TizenTVWebApp](https://github.com/TizenTVWebApp/TizenTVAudioRecorder) |
| **TVideoPlayer** | Tizen TV HTML video player based on videojs. | [TizenTVWebApp](https://github.com/TizenTVWebApp/TVideoPlayer) |
| **PlayerAVPlay** | AVPlayer app | [yadPe](https://github.com/yadPe/PlayerAVPlay) |
| **FCast** | FCast is an open source protocol that enables wireless streaming of audio and video content between devices. | [futo-org](https://github.com/futo-org/fcast) |
| **Doom** | A WebAssembly-powered port of Doom packaged as a Samsung Tizen TV application. | [dos-ise](https://github.com/dos-ise/doom-tizen) |
| **TransportTycoonDeluxe** | OpenTTD is an open source simulation game based upon Transport Tycoon Deluxe. | [dos-ise](https://github.com/dos-ise/OpenTTD-Tizen) |
| **Reiverr** | A clean combined interface for Jellyfin, TMDB, Radarr and Sonarr, as well as a replacement to Overseerr. | [aleksilassila](https://github.com/aleksilassila/reiverr) |
| **Nuvio** | TV-first streaming UI for Samsung Tizen. | [NuvioMedia](https://github.com/NuvioMedia/NuvioWeb) |
| **Chorus2-Tizen** | Chorus2-Tizen (Kodi) Samsung Tizen. | [Chorus2-Tizen](https://github.com/PatrickSt1991/chorus2-tizen) |
| **Flixor-Tizen** | Modern cross-platform Plex client. Ported to Tizen OS. | [Flixor-Tizen](https://github.com/PatrickSt1991/flixor-tizen) |

> 💡 Want your app listed here? See the [Contributing](#-contributing--requesting-apps) section below.

---

## 🤝 Contributing & Requesting Apps

We welcome **community contributions** and **app suggestions**!

### 💬 Request an App
Open a new [Issue](../../issues/new?template=request-app.md) to suggest an app for future bundles.  
Include:
- App name
- Description
- Link to source or homepage

### 📦 Contribute an App
If you’ve built or packaged a `.wgt` file that’s open-source, you can submit it for inclusion:
1. Open an [Issue](../../issues/new?template=contribute-app.md) to discuss it.
2. Ensure your app is:
   - Open-source (or redistributable under a permissive license)
   - Virus/malware-free
   - Tested on at least one Tizen device or emulator

> ⚠️ **Important:**  
> We can only include applications that are **open-source** and **freely distributable**.  
> Please make sure you have the legal right to redistribute any software you contribute.

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
