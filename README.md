<p align="center">
  <img src="assets/icon.png" width="128" height="128" alt="qmdec">
</p>

<h1 align="center">qmdec</h1>

<p align="center">QQ Music encrypted file decryptor with C-accelerated decrypt, full metadata + lyrics</p>

<p align="center">
  <a href="#installation">Install</a> •
  <a href="#quick-start">Quick Start</a> •
  <a href="#commands">Commands</a> •
  <a href="#中文说明">中文</a>
</p>

---

## Installation

```bash
pip install git+https://github.com/Sophomoresty/qmdec.git
```

Requires Python 3.10+ and `gcc` (for C-accelerated decrypt, auto-builds on first run; falls back to pure Python if unavailable).

## Quick Start

```bash
# 1. QQ Music desktop must be running and logged in (VIP)
qmdec auth

# 2. Download a song (search + download + decrypt + tag in one step)
qmdec download "周杰伦 晴天" -o ~/Music -q flac

# 3. Or batch-download an entire artist's discography
qmdec album 004AlfUb0cVkN1 -o ~/Music/BIGBANG -q flac -w 16
```

## Commands

| Command | Description |
|---------|-------------|
| `qmdec auth` | Extract login cookie from running QQ Music process |
| `qmdec download <keyword>` | Search + download + decrypt + tag (single song) |
| `qmdec album <singer_mid>` | Batch download all albums for a singer |
| `qmdec decrypt <path>` | Decrypt local .mflac/.mgg files |
| `qmdec search <keyword>` | Search songs |
| `qmdec cache-keys <path>` | Pre-fetch ekeys for offline decrypt |
| `qmdec doctor` | Check configuration status |

### `qmdec download <keyword> [-o dir] [-q flac|320|128]`

Search, download, decrypt, and write full metadata in one command.

```bash
qmdec download "BIGBANG BANG BANG BANG" -o ./music -q flac
```

### `qmdec album <singer_mid> -o <dir> [-q flac] [-w 16]`

Download all albums for a singer with concurrent workers. Skips existing files.

```bash
# BIGBANG (singer_mid: 004AlfUb0cVkN1)
qmdec album 004AlfUb0cVkN1 -o "/mnt/e/音视频/音乐" -q flac -w 16

# Find singer_mid: search any song by the artist, check the API response
```

### `qmdec decrypt <path> [-o output_dir] [--no-tag]`

Decrypt local encrypted files. Supports `.mflac`, `.mgg`, `.qmc0`, `.qmc2`, `.qmc3`, `.qmcflac`, `.qmcogg`.

```bash
qmdec decrypt ~/Music/VipSongsDownload -o ~/Music/Decoded
```

### `qmdec auth`

Scans QQMusic.exe process memory to extract session cookie. Requires QQ Music running and logged in.

### `qmdec cache-keys <path>`

Pre-fetch ekeys while cookie is valid. After caching, decrypt works offline.

## Metadata

Every downloaded/decrypted file gets complete metadata:

- **Title** / **Artist** / **Album Artist** / **Album**
- **Track number** / **Disc number**
- **Year** / **Genre** / **Language**
- **Lyrics** (LRC timed + Chinese translation when available)
- **Cover art** (500x500 album artwork)

## Performance

Decrypt uses a C-accelerated QMC2 implementation (MapCipher + RC4) that auto-compiles on first use:

- ~39x faster than pure Python
- 30MB FLAC: ~0.3s (C) vs ~12s (Python)
- Falls back to pure Python if `gcc` is unavailable

## How it works

1. **Auth** — Reads QQMusic.exe process memory via Win32 API to extract session cookie
2. **Ekey** — Calls QQ Music API (`CgiGetVkey`) to get per-song decryption keys, cached locally
3. **Decrypt** — QMC2 cipher (MapCipher for keys ≤300 bytes, RC4 for longer keys)
4. **Tag** — Fetches metadata + lyrics from QQ Music API, writes to FLAC/OGG tags with cover art

## Offline mode

Once ekeys are cached (`cache-keys` or after first decrypt), decryption works without network or valid cookie. Cached keys never expire.

## FAQ

**Q: Can I use this without VIP?**
A: No. Encrypted files and ekeys require VIP authentication.

**Q: Cookie expired?**
A: Run `qmdec auth` again with QQ Music open and logged in.

**Q: Works on Linux/macOS?**
A: `decrypt`, `download`, `album`, `search` work anywhere. `auth` requires Windows (reads QQMusic.exe memory).

**Q: How to find singer_mid?**
A: Search any song by the artist on QQ Music web, the URL contains the singer mid. Or use `qmdec search` and check the API response.

## Acknowledgments

- [GenericAgent](https://github.com/lsdefine/GenericAgent) — Core development powered by GA
- [linux.do](https://linux.do) — Community & inspiration

[![Powered by GenericAgent](https://img.shields.io/badge/Powered%20by-GenericAgent-blue)](https://github.com/lsdefine/GenericAgent)
[![linux.do](https://img.shields.io/badge/linux.do-Community-orange)](https://linux.do)

## License

MIT

---

# 中文说明

## 安装

```bash
pip install git+https://github.com/Sophomoresty/qmdec.git
```

需要 Python 3.10+ 和 `gcc` (C 加速解密, 首次运行自动编译; 无 gcc 时自动回退纯 Python).

## 快速开始

```bash
# 1. 打开 QQ 音乐客户端, 确保已登录 VIP 账号
qmdec auth

# 2. 下载单曲 (搜索+下载+解密+打标签一步完成)
qmdec download "周杰伦 晴天" -o ~/Music -q flac

# 3. 批量下载歌手全部专辑 (16 并发)
qmdec album 004AlfUb0cVkN1 -o ~/Music/BIGBANG -q flac -w 16
```

## 元信息

每首下载/解密的歌曲自动写入完整元信息:

- 标题 / 歌手 / 专辑艺术家 / 专辑
- 曲目号 / 碟号
- 年份 / 流派 / 语言
- 歌词 (LRC 时间轴 + 中文翻译)
- 封面 (500x500 专辑封面)

## 性能

解密使用 C 加速 QMC2 实现 (MapCipher + RC4), 首次使用自动编译:

- 比纯 Python 快 ~39 倍
- 30MB FLAC: ~0.3s (C) vs ~12s (Python)
- 无 gcc 时自动回退纯 Python

## 命令

| 命令 | 说明 |
|------|------|
| `qmdec auth` | 从 QQ 音乐进程提取登录凭证 |
| `qmdec download <关键词>` | 搜索+下载+解密+打标签 (单曲) |
| `qmdec album <歌手mid>` | 批量下载歌手全部专辑 |
| `qmdec decrypt <路径>` | 解密本地加密文件 |
| `qmdec search <关键词>` | 搜索歌曲 |
| `qmdec cache-keys <路径>` | 预缓存密钥 (离线解密) |
| `qmdec doctor` | 检查配置状态 |

## 离线模式

密钥缓存后 (通过 `cache-keys` 或首次解密), 后续解密不需要网络和有效 cookie. 缓存永不过期.

## 常见问题

**Q: 没有 VIP 能用吗?**
A: 不能. 加密文件和密钥都需要 VIP 认证.

**Q: Cookie 过期了?**
A: 重新运行 `qmdec auth` (QQ 音乐需在线登录).

**Q: Linux/macOS 能用吗?**
A: `decrypt`/`download`/`album`/`search` 跨平台. `auth` 需要 Windows (读取 QQMusic.exe 内存).

## 致谢

- [GenericAgent](https://github.com/lsdefine/GenericAgent) — 本项目核心开发依仗 GA 提供的 AI 能力
- [linux.do](https://linux.do) — 社区支持

[![Powered by GenericAgent](https://img.shields.io/badge/Powered%20by-GenericAgent-blue)](https://github.com/lsdefine/GenericAgent)
[![linux.do](https://img.shields.io/badge/linux.do-Community-orange)](https://linux.do)
