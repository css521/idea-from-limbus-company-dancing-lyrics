"""Experimental macOS adapter, adapted from qingyin-alice-zhong's mac-version.

Source: 5109df2c99ee87ee6ad5370fed70fa5d880336a5 (MIT).
nowplaying-cli is an external GPLv3 program; no binary is bundled here.
All subprocess/network work runs off the Qt thread. Playback is read-only.
"""
from collections import OrderedDict
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass, replace
import json
import logging
import math
import os
from pathlib import Path
import re
import shutil
import subprocess
import tempfile
import time
import unicodedata
import urllib.parse
import urllib.request

from PySide6.QtCore import QObject, QTimer, Signal
from lrc import LyricDocument, LyricLine, TimedWord, parse_lrc, chinese_translation

logger = logging.getLogger(__name__)
MAX_TIME = 24 * 3600 * 1000


class OffsetStore:
    """Per-song offsets; zero is an explicit choice, not a missing value."""
    def __init__(self, path):
        self.path = Path(path)
        self.error = ""
        self._data = {}
        if self.path.exists():
            try:
                raw = json.loads(self.path.read_text(encoding="utf-8-sig"))
                if not isinstance(raw, dict) or any(not isinstance(k, str) or type(v) is not int
                                                   or abs(v) > 10000 for k, v in raw.items()):
                    raise ValueError("偏移文件内容无效")
                self._data = raw
            except (OSError, ValueError):
                self.error = "歌曲偏移文件损坏，已保留原文件；请备份并移走 offsets.json 后重试。"

    @staticmethod
    def _key(title, artist):
        return json.dumps([title, artist], ensure_ascii=False)

    def get(self, title, artist, default=0):
        # Read offsets written by the original experimental branch as well.
        return self._data.get(self._key(title, artist), self._data.get(f"{title}|{artist}", default))

    def set(self, title, artist, value):
        if self.error:
            raise ValueError(self.error)
        data = dict(self._data)
        data[self._key(title, artist)] = max(-10000, min(10000, int(value)))
        self.path.parent.mkdir(parents=True, exist_ok=True)
        temporary = None
        try:
            with tempfile.NamedTemporaryFile(dir=self.path.parent, suffix=".tmp", delete=False) as stream:
                temporary = Path(stream.name)
                stream.write(json.dumps(data, ensure_ascii=False, indent=2).encode("utf-8"))
            temporary.replace(self.path)
            self._data = data
        finally:
            if temporary is not None:
                temporary.unlink(missing_ok=True)


NETEASE_BUNDLES = ("com.netease.163music", "com.netease.cloudmusic")
QQMUSIC_BUNDLES = ("com.tencent.QQMusicMac",)
ALLOWED_BUNDLES = NETEASE_BUNDLES + QQMUSIC_BUNDLES


@dataclass(frozen=True)
class NowPlaying:
    state: str
    title: str
    artist: str
    duration_ms: int
    position_ms: int
    song_id: str = ""
    rate: float = 1.0
    album: str = ""
    bundle: str = ""


def find_nowplaying_cli():
    candidates = (os.environ.get("NOWPLAYING_CLI"), shutil.which("nowplaying-cli"),
                  "/opt/homebrew/bin/nowplaying-cli", "/usr/local/bin/nowplaying-cli")
    return next((str(Path(p)) for p in candidates if p and Path(p).is_file() and os.access(p, os.X_OK)), None)


def _finite(value, maximum):
    if isinstance(value, bool):
        raise ValueError("播放时间无效")
    result = float(value or 0)
    if not math.isfinite(result) or not 0 <= result <= maximum:
        raise ValueError("播放时间无效")
    return result


def parse_nowplaying(data, allowed_bundles=None):
    if not isinstance(data, dict):
        return None
    bundle = (data.get("bundleIdentifier")
              or data.get("kMRMediaRemoteNowPlayingInfoBundleIdentifier")
              or data.get("kMRNowPlayingClientUserInfoBundleIdentifier")
              or data.get("kMRMediaRemoteNowPlayingInfoClientBundleIdentifier"))
    allowed = ALLOWED_BUNDLES if allowed_bundles is None else allowed_bundles
    if bundle and bundle not in allowed:
        return None
    title = data.get("kMRMediaRemoteNowPlayingInfoTitle", "")
    artist = data.get("kMRMediaRemoteNowPlayingInfoArtist", "") or ""
    album = data.get("kMRMediaRemoteNowPlayingInfoAlbum", "") or ""
    if not isinstance(title, str) or not title.strip() or not isinstance(artist, str):
        return None
    if max(len(title), len(artist), len(str(album))) > 1024:
        return None
    duration = int(_finite(data.get("kMRMediaRemoteNowPlayingInfoDuration"), 86400) * 1000)
    position = int(_finite(data.get("kMRMediaRemoteNowPlayingInfoElapsedTime"), 86400) * 1000)
    rate = _finite(data.get("kMRMediaRemoteNowPlayingInfoPlaybackRate"), 4)
    return NowPlaying("playing" if rate > 0 else "paused", title.strip(), artist.strip(),
                      duration, min(position, duration) if duration else position, rate=rate,
                      album=str(album).strip(), bundle=str(bundle or ""))


def query_nowplaying(cli, allowed_bundles=None):
    if not cli:
        return None
    result = subprocess.run([cli, "get-raw"], capture_output=True, text=True, encoding="utf-8",
                            timeout=2, check=True)
    if not result.stdout.strip() or result.stdout.strip() == "null":
        return None
    return parse_nowplaying(json.loads(result.stdout), allowed_bundles=allowed_bundles)


def load_qqmusic_lyrics(info, cache_reader=None, cancelled=lambda: False):
    from qqmusic import QQSnapshot
    from qqmusic_lyrics import load_song_lyrics as qq_load_lyrics, LyricResult
    snapshot = QQSnapshot(
        title=info.title,
        artist=info.artist,
        album=getattr(info, "album", "") or "",
        duration_ms=info.duration_ms,
        position_ms=info.position_ms,
        playing=info.state == "playing",
        rate=getattr(info, "rate", 1.0),
    )
    if cache_reader is not None:
        try:
            cache_result = cache_reader.load(snapshot, cancelled=cancelled)
            if cache_result and cache_result.document:
                return cache_result
        except Exception as error:
            logger.debug("QQ Music cache lookup skipped: %s", error)

    last_error = None
    result = None
    try:
        result = qq_load_lyrics(snapshot, cancelled=cancelled)
        if result and result.document is not None:
            return result
    except Exception as error:
        last_error = error

    if snapshot.album:
        try:
            fallback = qq_load_lyrics(replace(snapshot, album=""), cancelled=cancelled)
            if fallback and fallback.document is not None:
                return fallback
            if result is None:
                result = fallback
        except Exception as error:
            if last_error is None:
                last_error = error

    try:
        collab_song = _find_mac_collab_song(snapshot, cancelled=cancelled)
        if collab_song is not None:
            collab_doc = _fetch_qq_lyrics_by_mid(collab_song["mid"], collab_song.get("id", 0), cancelled=cancelled)
            if collab_doc is not None:
                return LyricResult(collab_doc, f"QQ 音乐歌词已同步 · {len(collab_doc.lines)} 句", collab_song["mid"])
    except Exception as error:
        if last_error is None:
            last_error = error

    if last_error is not None and (result is None or result.document is None):
        raise last_error
    return result if result is not None else LyricResult(None, "未找到可靠匹配的 QQ 音乐歌词，可点击“重新获取歌词”重试。")


def _fetch_qq_lyrics_by_mid(mid, song_id=0, cancelled=lambda: False):
    from qqmusic_lyrics import request_json, parse_lyrics
    try:
        data = request_json("https://u.y.qq.com/cgi-bin/musicu.fcg", {
            "comm": {"ct": 24, "cv": 0}, "req_0": {
                "module": "music.musichallSong.PlayLyricInfo", "method": "GetPlayLyricInfo",
                "param": {"songMID": mid, "songID": song_id, "qrc": 0, "crypt": 0,
                          "roma": 0, "trans": 1}}})
        part = data.get("req_0", {})
        if isinstance(part, dict) and part.get("code") == 0:
            return parse_lyrics(part.get("data"))
    except Exception:
        pass
    url = "https://c.y.qq.com/lyric/fcgi-bin/fcg_query_lyric_new.fcg?" + urllib.parse.urlencode(
        {"songmid": mid, "format": "json", "nobase64": 1})
    return parse_lyrics(request_json(url), encoded=False)


def _find_mac_collab_song(snapshot, cancelled=lambda: False):
    from qqmusic_lyrics import request_json, SEARCH_MODULE, normalized, artist_names
    singers = [re.sub(r"\s*[（(][^()（）]*[)）]\s*$", "", name).strip()
               for name in re.split(r"[/、,，;&]", snapshot.artist) if name.strip()]
    artist_query = " ".join(singers)
    queries = dict.fromkeys((f"{snapshot.title} {artist_query}".strip(), snapshot.title,
                             f"{artist_query} {snapshot.title}".strip()))
    candidates = []
    for q in queries:
        if cancelled():
            return None
        payload = {
            "comm": {"ct": 11, "cv": 0},
            SEARCH_MODULE: {"module": SEARCH_MODULE, "method": "DoSearchForQQMusicDesktop",
                            "param": {"search_type": 0, "query": q, "page_num": 1, "num_per_page": 20}}
        }
        try:
            data = request_json("https://u.y.qq.com/cgi-bin/musicu.fcg", payload)
            sub = data.get(SEARCH_MODULE, {})
            if sub.get("code") == 0:
                songs = sub.get("data", {}).get("body", {}).get("song", {}).get("list", [])
                candidates.extend(songs[:20])
        except Exception:
            continue
    matches = {}
    snap_artists = artist_names(snapshot.artist)
    for s in candidates:
        if not isinstance(s, dict):
            continue
        name = s.get("title", s.get("name", ""))
        singers = s.get("singer", [])
        duration, mid = s.get("interval"), s.get("mid")
        if not isinstance(name, str) or normalized(name) != normalized(snapshot.title):
            continue
        if not isinstance(singers, list) or not singers:
            continue
        names = set().union(*(artist_names(x["name"]) for x in singers if isinstance(x, dict) and isinstance(x.get("name"), str)))
        if not snap_artists.issubset(names):
            continue
        if not isinstance(duration, (int, float)) or not math.isfinite(duration) or abs(duration * 1000 - snapshot.duration_ms) > 2000:
            continue
        if isinstance(mid, str) and re.fullmatch(r"[A-Za-z0-9]{14}", mid):
            matches[mid] = s
    return next(iter(matches.values())) if len(matches) == 1 else None


def _api(path, values, post=False):
    encoded = urllib.parse.urlencode(values).encode("utf-8")
    url = "https://music.163.com/api/" + path
    if not post:
        url += "?" + encoded.decode("ascii")
    request = urllib.request.Request(url, data=encoded if post else None, headers={
        "User-Agent": "Mozilla/5.0", "Referer": "https://music.163.com/",
        "Content-Type": "application/x-www-form-urlencoded",
    })
    with urllib.request.urlopen(request, timeout=5) as response:
        data = json.loads(response.read(2 * 1024 * 1024 + 1))
    if not isinstance(data, dict) or data.get("code", 200) != 200:
        raise ValueError("网易云歌词接口暂不可用")
    return data


def _normalized(text):
    return "".join(unicodedata.normalize("NFKC", str(text)).casefold().split())


def search_song(title, artist, duration_ms=0):
    """Require matching metadata; never substitute a different song for lyrics."""
    data = _api("search/get", {"s": f"{title} {artist}".strip(), "type": 1, "limit": 15}, post=True)
    expected_artists = {_normalized(x) for x in re.split(r"[/,，、;&]", artist) if x.strip()}
    for song in data.get("result", {}).get("songs", []):
        if not isinstance(song, dict) or _normalized(song.get("name", "")) != _normalized(title):
            continue
        names = song.get("artists", song.get("ar", []))
        names = {_normalized(x.get("name", "")) for x in names if isinstance(x, dict)}
        if expected_artists and not expected_artists.issubset(names):
            continue
        length = song.get("duration", song.get("dt", 0))
        if duration_ms and (not isinstance(length, (int, float))
                            or abs(length - duration_ms) > max(2000, min(5000, duration_ms * .02))):
            continue
        if not expected_artists and not duration_ms:
            continue
        identifier = str(song.get("id", ""))
        if identifier.isdecimal():
            return identifier
    return None


def _yrc_lines(text):
    result = []
    for row in str(text).splitlines():
        match = re.fullmatch(r"\[(\d+),(\d+)\](.*)", row.strip())
        if not match:
            continue
        start = int(match[1])
        units = list(re.finditer(r"\((\d+),(\d+),\d+\)([^()]*)", match[3]))
        if not units or start > MAX_TIME:
            continue
        content = "".join(unit[3] for unit in units)
        trim = len(content) - len(content.lstrip())
        original = content.strip()
        offset, words = -trim, []
        for unit in units:
            begin, duration, unit_text = int(unit[1]), int(unit[2]), unit[3]
            a, b = max(0, offset), min(len(original), offset + len(unit_text))
            if a < b and 0 < duration and begin + duration <= MAX_TIME:
                words.append(TimedWord(begin, begin + duration, a, b))
            offset += len(unit_text)
        if original:
            result.append(LyricLine(start, original, tuple(words)))
    return result


def parse_lyrics(data):
    if not isinstance(data, dict) or data.get("nolyric") is True:
        return None
    def text(key):
        value = data.get(key)
        return value.get("lyric", "") if isinstance(value, dict) and isinstance(value.get("lyric", ""), str) else ""
    yrc = _yrc_lines(text("yrc"))
    try:
        document = parse_lrc(text("lrc"))
    except ValueError:
        document = LyricDocument(sorted(yrc, key=lambda row: row.start_ms), []) if yrc else None
    if document is None:
        return None
    placeholders = {"纯音乐，请欣赏", "纯音乐，请您欣赏", "纯音乐，请欣赏。", "纯音乐，请您欣赏。"}
    if all(not row.text.strip() or row.text.strip() in placeholders for row in document.lines):
        return None
    try:
        translations = parse_lrc(text("tlyric")).lines
    except ValueError:
        translations = []
    lines = []
    for line in document.lines:
        candidates = [row for row in yrc if row.text == line.text and abs(row.start_ms - line.start_ms) <= 250]
        words = min(candidates, key=lambda row: abs(row.start_ms - line.start_ms)).words if candidates else line.words
        translated = [row for row in translations if abs(row.start_ms - line.start_ms) <= 250
                      and chinese_translation(row.text)]
        translation = min(translated, key=lambda row: abs(row.start_ms - line.start_ms)).text if translated else ""
        lines.append(replace(line, words=words, translation=translation))
    return LyricDocument(lines, list(document.warnings), document.offset_ms)


def load_song_lyrics(info):
    identifier = search_song(info.title, info.artist, info.duration_ms)
    if not identifier:
        return None
    return parse_lyrics(_api("song/lyric", {"id": identifier, "lv": 1, "kv": 1, "tv": -1, "yv": 1}))


class MacNeteasePlayer(QObject):
    changed = Signal()
    discontinuity = Signal()
    document_changed = Signal(object)
    offset_changed = Signal()
    error = Signal(str)
    is_external = True
    path = None
    has_audio_data = False
    analysis_error = "macOS 暂未接入真实音频强弱，请选择轻波浪。"

    def __init__(self, parent=None, *, query=None, loader=load_song_lyrics, clock=time.monotonic,
                 executor=None, autostart=True, source_mode="auto", cache_directory="", cache_reader=None):
        super().__init__(parent)
        self.cli = find_nowplaying_cli() if query is None else None
        self.source_mode = source_mode
        self._custom_query = query is not None
        allowed = None
        if source_mode == "qqmusic":
            allowed = QQMUSIC_BUNDLES
        elif source_mode == "netease":
            allowed = NETEASE_BUNDLES
        self._allowed_bundles = allowed
        self._query = query or (lambda: query_nowplaying(self.cli, allowed_bundles=self._allowed_bundles))
        self._loader, self._clock = loader, clock
        self._custom_loader = loader is not load_song_lyrics
        self._executor = executor or ThreadPoolExecutor(max_workers=2, thread_name_prefix="mac-lyrics")
        self._owns_executor = executor is None
        self.playing = self.ended = self.connected = self.lyrics_received = False
        self.enabled = True
        self.song_id = self.title = self.artist = ""
        self.duration = 0
        self._active_source = "qqmusic" if source_mode == "qqmusic" else "netease"
        from qqmusic_cache import QQCacheReader
        self._cache_reader = cache_reader or (QQCacheReader(cache_directory) if (cache_directory or source_mode != "netease") else None)
        self.status = self._default_status()
        self.lyric_status = f"等待{self.source_short}歌词"
        self._anchor = self._at = self._last_poll = 0
        self._rate = 1
        self._last_raw = None
        self.lyric_offset_ms = 0
        self._offset_store = None
        self._cache = OrderedDict()
        self._cache_msg = {}
        self._poll_future = self._lyrics_job = None
        self._generation = 0
        self._info = None
        self._next_poll = self._retry_at = 0
        self._needs_lyrics = self._closed = False
        self.timer = QTimer(self)
        self.timer.setInterval(100)
        self.timer.timeout.connect(self._tick)
        if autostart:
            self.timer.start()

    def _default_status(self):
        if not (self._custom_query or self.cli):
            return "未找到 nowplaying-cli；请先运行 brew install nowplaying-cli，再重新启动。"
        if self.source_mode == "qqmusic":
            return "等待 QQ 音乐播放歌曲"
        elif self.source_mode == "netease":
            return "等待网易云音乐播放"
        else:
            return "等待音乐播放（支持 QQ 音乐 / 网易云）"

    @property
    def is_qqmusic(self):
        if self.source_mode == "qqmusic":
            return True
        if self.source_mode == "netease":
            return False
        return self._active_source == "qqmusic"

    @property
    def source_name(self):
        return "QQ 音乐" if self.is_qqmusic else "网易云音乐"

    @property
    def source_short(self):
        return "QQ 音乐" if self.is_qqmusic else "网易云"

    @property
    def connect_hint(self):
        return ("打开 QQ 音乐并播放歌曲；若未连接，请在 QQ 音乐中播放。"
                if self.is_qqmusic else "请在网易云中点击“都市回响”启用效果。")

    @property
    def cache_status(self):
        return self._cache_reader.status if self._cache_reader else "歌词缓存：自动检测"

    def configure_cache_directory(self, directory):
        from qqmusic_cache import QQCacheReader
        self._cache_reader = QQCacheReader(directory)
        self._cache.clear()
        self._cache_msg.clear()
        if self.connected and self._info and self.is_qqmusic:
            self.retry_lyrics()
        self.changed.emit()

    def retry_lyrics(self):
        if self.connected and self._info:
            self._cache.pop(self.song_id, None)
            self._cache_msg.pop(self.song_id, None)
            self._needs_lyrics = True
            self._retry_at = 0
            if self._lyrics_job:
                self._lyrics_job[2].cancel()
                self._lyrics_job = None
            self.lyric_status = f"正在重新获取{self.source_short}歌词…"
            loader_fn = self._get_loader()
            self._lyrics_job = (self._generation, self.song_id, self._executor.submit(loader_fn, self._info))
            self.changed.emit()

    def _get_loader(self):
        if self._custom_loader:
            return self._loader
        if self.is_qqmusic:
            return lambda info: load_qqmusic_lyrics(info, cache_reader=self._cache_reader)
        return self._loader

    def _capture(self):
        return self._query(), self._clock()

    def _tick(self):
        if self._closed:
            return
        now = self._clock()
        if self._poll_future is not None and self._poll_future.done():
            try:
                info, captured = self._poll_future.result()
                self.apply(info, captured)
            except Exception as error:
                logger.warning("Now Playing read failed: %s", error)
                self.apply(None)
                self.status = "读取系统播放信息失败，请检查 nowplaying-cli 版本；详情见 .state/app.log。"
                self.changed.emit()
                self._next_poll = now + 2
            self._poll_future = None
        if self._poll_future is None and now >= self._next_poll:
            self._poll_future = self._executor.submit(self._capture)
            self._next_poll = now + .5
        if self._lyrics_job is not None:
            generation, key, future = self._lyrics_job
            if future.done():
                self._lyrics_job = None
                if generation == self._generation and key == self.song_id:
                    try:
                        raw_result = future.result()
                        if hasattr(raw_result, "document"):
                            document = raw_result.document
                            message = raw_result.message
                        elif isinstance(raw_result, LyricDocument) or raw_result is None:
                            document = raw_result
                            if self.is_qqmusic:
                                message = (f"QQ 音乐歌词已同步 · {len(document.lines)} 句"
                                           if document else "本曲暂无歌词或为纯音乐，桌面保持空白。")
                            else:
                                message = "已连接网易云音乐" if document else "本曲未匹配到歌词，保持空白。"
                        else:
                            document = None
                            message = "本曲未匹配到歌词，保持空白。"
                        self._cache[key] = document
                        self._cache_msg[key] = message
                        self._cache.move_to_end(key)
                        while len(self._cache) > 32:
                            popped_k, _ = self._cache.popitem(last=False)
                            self._cache_msg.pop(popped_k, None)
                        self._needs_lyrics = False
                        self.lyrics_received = True
                        self.status = message
                        self.lyric_status = message
                        self.document_changed.emit(document)
                    except Exception as error:
                        logger.warning("Mac lyric lookup failed: %s", error)
                        self.lyrics_received = True
                        self._retry_at = now + 10
                        self.status = f"{self.source_short}歌词获取暂时失败，10 秒后自动重试；音乐播放不受影响。"
                        if self.is_qqmusic:
                            self.lyric_status = f"{self.source_short}歌词获取失败，可点击“重新获取歌词”重试。"
                        else:
                            self.lyric_status = self.status
                    self.changed.emit()
        if self._lyrics_job is None and self._needs_lyrics and self.connected and now >= self._retry_at:
            loader_fn = self._get_loader()
            self._lyrics_job = (self._generation, self.song_id, self._executor.submit(loader_fn, self._info))

    def apply(self, info, captured=None):
        if self._closed:
            return
        if info is None:
            if self.connected:
                self._anchor = self.position()
                self.playing = self.connected = False
                self._generation += 1
                self._needs_lyrics = self.lyrics_received = False
                self.song_id = ""
                self.status = f"等待{self.source_short}播放；请确认它是系统当前播放来源。"
                self.lyric_status = f"等待{self.source_short}歌词"
                self.document_changed.emit(None)
                self.changed.emit()
            return
        if getattr(info, "bundle", ""):
            if info.bundle in QQMUSIC_BUNDLES:
                self._active_source = "qqmusic"
            elif info.bundle in NETEASE_BUNDLES:
                self._active_source = "netease"
        now = self._clock() if captured is None else captured
        key = json.dumps([info.title, info.artist, info.duration_ms], ensure_ascii=False)
        switched = key != self.song_id
        playing = info.state == "playing"
        jumped = switched or (self._last_raw != info.position_ms and abs(info.position_ms - self.position()) > 750)
        if switched or self._last_raw != info.position_ms or playing != self.playing:
            self._anchor, self._at = info.position_ms, now
        self._last_poll, self._last_raw = now, info.position_ms
        self._rate = info.rate
        self.connected, self.playing = True, playing
        self.duration = info.duration_ms
        self.ended = bool(self.duration and info.position_ms >= self.duration)
        self.title, self.artist, self.song_id = info.title, info.artist, key
        self._info = info
        if switched:
            self._generation += 1
            self.lyrics_received = False
            self.document_changed.emit(None)
            if self._offset_store:
                self.lyric_offset_ms = self._offset_store.get(info.title, info.artist, self.lyric_offset_ms)
                self.offset_changed.emit()
            self._retry_at = 0
            self._needs_lyrics = key not in self._cache
            self.status = f"正在获取{self.source_short}歌词…" if self.is_qqmusic else "正在匹配网易云歌词…"
            self.lyric_status = self.status
            if key in self._cache:
                self._cache.move_to_end(key)
                self.lyrics_received = True
                doc = self._cache[key]
                msg = self._cache_msg.get(key, f"已连接{self.source_short}" if doc else "本曲未匹配到歌词，保持空白。")
                self.status = msg
                self.lyric_status = msg
                self.document_changed.emit(doc)
        if jumped:
            self.discontinuity.emit()
        self.changed.emit()

    def position(self):
        elapsed = max(0, min(self._clock(), self._last_poll + 1.5) - self._at) * 1000 if self.playing else 0
        value = self._anchor + elapsed * self._rate
        return max(0, min(value, self.duration)) if self.duration else max(0, value)

    def set_offset_store(self, store):
        self._offset_store = store

    def adjust_offset(self, delta_ms):
        value = max(-10000, min(10000, self.lyric_offset_ms + delta_ms))
        try:
            if self._offset_store and self.title:
                self._offset_store.set(self.title, self.artist, value)
        except (OSError, ValueError) as error:
            self.error.emit(str(error))
            return
        self.lyric_offset_ms = value
        self.offset_changed.emit()
        self.discontinuity.emit()

    def energy_at(self, _position=0):
        # No fabricated music energy: the shared light-wave mode is available.
        return 0.0

    def toggle(self):
        pass

    def seek(self, _value):
        pass

    def set_volume(self, _value):
        pass

    def stop(self):
        self._closed = True
        self.timer.stop()
        if self._poll_future:
            self._poll_future.cancel()
        if self._lyrics_job:
            self._lyrics_job[2].cancel()
        if self._owns_executor:
            self._executor.shutdown(wait=False, cancel_futures=True)
        self.playing = False


MacMusicPlayer = MacNeteasePlayer
