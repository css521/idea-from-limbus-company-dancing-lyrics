"""Portable mac adapter tests. Fixtures do not claim live macOS verification."""
import os
os.environ["QT_QPA_PLATFORM"] = "offscreen"
from concurrent.futures import Future
from pathlib import Path
import json
import shutil
import subprocess
import tempfile
import threading
from types import SimpleNamespace
import unittest
from unittest.mock import patch

from PySide6.QtCore import Qt, QTimer
from PySide6.QtTest import QTest
from PySide6.QtWidgets import QApplication
import macos_netease as mac
from lrc import LyricDocument, LyricLine, TimedWord, word_timing_status

APP = QApplication.instance() or QApplication([])
ROOT = Path(__file__).resolve().parents[1]


def info(title="Hello", position=1000, state="playing", artist="Artist", duration=60000):
    return mac.NowPlaying(state, title, artist, duration, position)


class ManualExecutor:
    def __init__(self):
        self.jobs = []

    def submit(self, function, *args):
        future = Future()
        self.jobs.append((function, args, future))
        return future

    def finish(self, index, result=None, error=None):
        if error:
            self.jobs[index][2].set_exception(error)
        else:
            self.jobs[index][2].set_result(result)


class MacParsingTests(unittest.TestCase):
    def snapshot(self, **updates):
        data = {"kMRMediaRemoteNowPlayingInfoTitle": "歌曲", "kMRMediaRemoteNowPlayingInfoArtist": "歌手",
                "kMRMediaRemoteNowPlayingInfoDuration": 120.25,
                "kMRMediaRemoteNowPlayingInfoElapsedTime": 1.75,
                "kMRMediaRemoteNowPlayingInfoPlaybackRate": 1}
        data.update(updates)
        return data

    def test_seconds_convert_to_ms_and_pause_is_explicit(self):
        result = mac.parse_nowplaying(self.snapshot())
        self.assertEqual((result.position_ms, result.duration_ms, result.state), (1750, 120250, "playing"))
        self.assertEqual(mac.parse_nowplaying(self.snapshot(kMRMediaRemoteNowPlayingInfoPlaybackRate=0)).state, "paused")

    def test_malformed_nonfinite_and_other_source_are_not_accepted(self):
        for data in (None, [], {}, self.snapshot(bundleIdentifier="com.apple.Music")):
            self.assertIsNone(mac.parse_nowplaying(data))
        for value in (True, float("nan"), float("inf"), -1, "invalid"):
            with self.subTest(value=value), self.assertRaises((TypeError, ValueError)):
                mac.parse_nowplaying(self.snapshot(kMRMediaRemoteNowPlayingInfoElapsedTime=value))
        self.assertIsNotNone(mac.parse_nowplaying(self.snapshot(bundleIdentifier="com.netease.163music")))

    def test_cli_discovery_has_no_import_time_process_and_read_is_only_get_raw(self):
        with patch.object(mac, "find_nowplaying_cli", return_value=None), patch.object(mac.subprocess, "run") as run:
            player = mac.MacNeteasePlayer(autostart=False)
            self.assertIn("brew install", player.status)
            run.assert_not_called()
            player.stop()
        with patch.object(mac.subprocess, "run", return_value=SimpleNamespace(stdout=json.dumps(self.snapshot()))) as run:
            self.assertEqual(mac.query_nowplaying("/a path/中文/nowplaying-cli").position_ms, 1750)
            self.assertEqual(run.call_args.args[0], ["/a path/中文/nowplaying-cli", "get-raw"])
            self.assertEqual(run.call_args.kwargs["timeout"], 2)
        with patch.object(mac.subprocess, "run", side_effect=subprocess.TimeoutExpired("helper", 2)):
            with self.assertRaises(subprocess.TimeoutExpired):
                mac.query_nowplaying("helper")

    def test_search_requires_title_artist_and_duration_and_does_not_swap_instrumental(self):
        songs = [
            {"id": 1, "name": "Another", "artists": [{"name": "Artist"}], "duration": 60000},
            {"id": 2, "name": "Hello", "artists": [{"name": "Other"}], "duration": 60000},
            {"id": 3, "name": "Hello", "artists": [{"name": "Artist"}], "duration": 180000},
            {"id": 4, "name": "Hello", "artists": [{"name": "Artist"}], "duration": 60000},
        ]
        with patch.object(mac, "_api", return_value={"result": {"songs": songs}}):
            self.assertEqual(mac.search_song("Hello", "Artist", 60000), "4")
            self.assertIsNone(mac.search_song("Hello", "Wrong", 60000))
        with patch.object(mac, "search_song", return_value="4"), patch.object(mac, "_api", return_value={"nolyric": True}) as api:
            self.assertIsNone(mac.load_song_lyrics(info()))
            self.assertEqual(api.call_count, 1)

    def test_lrc_blank_boundaries_multiple_stamps_and_real_words_preserved(self):
        data = {"lrc": {"lyric": "[offset:100]\n[00:01.00]你好\n[00:02.00]\n[00:03][00:04]再见"},
                "yrc": {"lyric": "[1000,800](1000,200,0)你(1200,300,0)好"},
                "tlyric": {"lyric": "[00:01.00]中文翻译"}}
        doc = mac.parse_lyrics(data)
        self.assertEqual([line.start_ms for line in doc.lines], [1000, 2000, 3000, 4000])
        self.assertEqual(doc.lines[1].text, "")
        self.assertEqual(doc.lines[0].words, (TimedWord(1000, 1200, 0, 1), TimedWord(1200, 1500, 1, 2)))
        self.assertEqual((doc.offset_ms, doc.lines[0].translation), (100, "中文翻译"))

    def test_yrc_multiword_emoji_and_combining_marks_are_not_split_or_guessed(self):
        original = "Hi é 👩‍💻"
        doc = mac.parse_lyrics({"lrc": {"lyric": f"[00:01]{original}"}, "yrc": {"lyric":
            "[1000,1000](1000,200,0)Hi (1300,200,0)é (1700,200,0)👩‍💻"}})
        self.assertEqual(len(doc.lines[0].words), 3)
        self.assertEqual([original[w.text_start:w.text_end] for w in doc.lines[0].words], ["Hi ", "é ", "👩‍💻"])
        self.assertEqual(word_timing_status(doc), "逐字时间可用")

    def test_unaligned_bad_and_missing_lyrics_fall_back(self):
        for yrc in ("[1000,800](1000,200,0)different", "[1251,800](1251,200,0)Hello", "bad data"):
            doc = mac.parse_lyrics({"lrc": {"lyric": "[00:01]Hello"}, "yrc": {"lyric": yrc}})
            self.assertEqual(doc.lines[0].words, ())
        self.assertIsNone(mac.parse_lyrics({}))
        self.assertIsNone(mac.parse_lyrics({"nolyric": True}))
        self.assertIsNone(mac.parse_lyrics({"lrc": {"lyric": "[00:00]纯音乐，请欣赏"}}))
        doc = mac.parse_lyrics({"yrc": {"lyric": "[1000,500](1000,500,0)Hello"}})
        self.assertEqual(doc.lines[0].text, "Hello")
        self.assertEqual(doc.lines[0].words, (TimedWord(1000, 1500, 0, 5),))

    def test_parse_nowplaying_qqmusic_bundle_and_album(self):
        qq_data = self.snapshot(
            kMRMediaRemoteNowPlayingInfoClientBundleIdentifier="com.tencent.QQMusicMac",
            kMRMediaRemoteNowPlayingInfoAlbum="测试专辑"
        )
        parsed = mac.parse_nowplaying(qq_data)
        self.assertIsNotNone(parsed)
        self.assertEqual(parsed.bundle, "com.tencent.QQMusicMac")
        self.assertEqual(parsed.album, "测试专辑")
        self.assertIsNone(mac.parse_nowplaying(qq_data, allowed_bundles=mac.NETEASE_BUNDLES))
        self.assertIsNotNone(mac.parse_nowplaying(qq_data, allowed_bundles=mac.QQMUSIC_BUNDLES))


class MacOffsetTests(unittest.TestCase):
    def test_zero_offsets_unicode_paths_and_reload(self):
        with tempfile.TemporaryDirectory() as temporary:
            path = Path(temporary) / "中文 设置" / "offsets.json"
            store = mac.OffsetStore(path)
            store.set("歌|名", "人", 200)
            store.set("歌", "名|人", 0)
            restored = mac.OffsetStore(path)
            self.assertEqual(restored.get("歌|名", "人"), 200)
            self.assertEqual(restored.get("歌", "名|人", 400), 0)
            self.assertEqual(restored.get("新歌", "人", 400), 400)

    def test_corrupt_and_failed_atomic_write_preserve_original(self):
        with tempfile.TemporaryDirectory() as temporary:
            path = Path(temporary) / "offsets.json"
            path.write_text("broken", encoding="utf-8")
            store = mac.OffsetStore(path)
            with self.assertRaises(ValueError):
                store.set("song", "artist", 100)
            self.assertEqual(path.read_text(), "broken")
            path.write_text('{"song|artist": 200}', encoding="utf-8")
            store = mac.OffsetStore(path)
            with patch.object(mac.Path, "replace", side_effect=PermissionError("save failed")), self.assertRaises(OSError):
                store.set("song", "artist", 400)
            self.assertEqual(store.get("song", "artist"), 200)
            self.assertEqual(mac.OffsetStore(path).get("song", "artist"), 200)
            self.assertEqual(list(path.parent.glob("*.tmp")), [])


class MacPlayerTests(unittest.TestCase):
    def setUp(self):
        self.clock = [0.0]
        self.executor = ManualExecutor()
        self.player = mac.MacNeteasePlayer(query=lambda: None, executor=self.executor,
                                         clock=lambda: self.clock[0], autostart=False)
        self.documents = []
        self.player.document_changed.connect(self.documents.append)

    def tearDown(self):
        self.player.stop()

    def test_progress_pause_seek_repeat_snapshot_and_disconnect(self):
        self.player.apply(info())
        self.clock[0] = .5
        self.assertEqual(self.player.position(), 1500)
        self.player.apply(info())  # Identical rounded system snapshot must not reset the clock.
        self.clock[0] = 1
        self.assertEqual(self.player.position(), 2000)
        self.player.apply(info(position=1800, state="paused"))
        self.clock[0] = 20
        self.assertEqual(self.player.position(), 1800)
        self.player.apply(info(position=20000))
        self.assertEqual(self.player.position(), 20000)
        self.player.apply(None)
        self.assertFalse(self.player.playing)
        self.assertIsNone(self.documents[-1])

    def test_late_lyrics_after_switch_and_disconnect_are_discarded(self):
        old = LyricDocument([LyricLine(1000, "old")], [])
        current = LyricDocument([LyricLine(1000, "current")], [])
        self.player.apply(info("old"))
        self.player._tick()
        self.player.apply(info("current"))
        self.executor.finish(1, old)
        self.player._tick()
        self.assertNotIn(old, self.documents)
        self.executor.finish(2, current)
        self.player._tick()
        self.assertIs(self.documents[-1], current)
        self.player.apply(info("third"))
        self.player._tick()
        self.player.apply(None)
        self.executor.finish(3, old)
        self.player._tick()
        self.assertIsNone(self.documents[-1])

    def test_cached_no_lyrics_and_fetched_lyrics_update_status(self):
        self.player.apply(info("instrumental"))
        self.player._tick()
        self.executor.finish(1, None)
        self.player._tick()
        self.assertTrue(self.player.lyrics_received)
        self.assertIn("保持空白", self.player.status)
        self.player.apply(info("other"))
        self.player.apply(info("instrumental"))
        self.assertTrue(self.player.lyrics_received)
        self.assertFalse(self.player._needs_lyrics)

    def test_lookup_failure_retries_and_does_not_change_playback(self):
        self.player.apply(info())
        self.player._tick()
        self.executor.finish(1, error=OSError("offline"))
        with self.assertLogs(mac.logger, level="WARNING"):
            self.player._tick()
        self.assertTrue(self.player.playing)
        self.assertIn("10 秒", self.player.status)
        self.assertEqual(len(self.executor.jobs), 2)
        self.clock[0] = 11
        self.player._tick()
        self.assertEqual(len(self.executor.jobs), 3)

    def test_offsets_and_visual_settings_never_control_music_or_progress(self):
        self.player.apply(info())
        self.player.adjust_offset(200)
        self.assertEqual((self.player.lyric_offset_ms, self.player.position()), (200, 1000))
        with patch.object(mac.subprocess, "run") as run:
            self.player.toggle()
            self.player.seek(40000)
            self.player.set_volume(0)
            self.assertEqual((self.player.position(), self.player.playing), (1000, True))
            run.assert_not_called()
        self.assertFalse(self.player.has_audio_data)
        self.assertEqual(self.player.energy_at(0), 0)

    def test_stop_drops_results_and_cancels_pending_jobs(self):
        self.player.apply(info())
        self.player._tick()
        self.player.stop()
        self.assertTrue(all(future.cancelled() for _, _, future in self.executor.jobs))
        self.player.apply(info("ignored"))
        self.player._tick()
        self.assertEqual(self.player.title, "Hello")
        self.assertEqual(len(self.executor.jobs), 2)

    def test_poll_failure_is_visible_and_does_not_keep_stale_lyrics(self):
        self.player.apply(info())
        self.player._tick()
        self.executor.finish(0, error=ValueError("unsupported helper output"))
        with self.assertLogs(mac.logger, level="WARNING"):
            self.player._tick()
        self.assertFalse(self.player.playing)
        self.assertIn("nowplaying-cli", self.player.status)
        self.assertIsNone(self.documents[-1])
        self.assertGreaterEqual(self.player._next_poll, 2)

    def test_song_offset_zero_is_restored_and_new_song_inherits_without_moving_clock(self):
        with tempfile.TemporaryDirectory() as temporary:
            store = mac.OffsetStore(Path(temporary) / "offsets.json")
            store.set("zero", "Artist", 0)
            self.player.set_offset_store(store)
            self.player.apply(info("first"))
            self.player.adjust_offset(400)
            self.player.apply(info("new"))
            self.assertEqual(self.player.lyric_offset_ms, 400)
            self.player.apply(info("zero"))
            self.assertEqual((self.player.lyric_offset_ms, self.player.position()), (0, 1000))

    def test_blocked_worker_does_not_block_qt_event_loop(self):
        released, entered = threading.Event(), threading.Event()
        def query():
            entered.set()
            released.wait(3)
            return None
        player = mac.MacNeteasePlayer(query=query, autostart=False)
        delivered = []
        try:
            player._tick()
            self.assertTrue(entered.wait(1))
            QTimer.singleShot(0, lambda: delivered.append(True))
            QTest.qWait(30)
            self.assertEqual(delivered, [True])
            self.assertFalse(player._poll_future.done())
        finally:
            released.set()
            player.stop()

    def test_qqmusic_mode_and_auto_detection(self):
        qq_info = mac.NowPlaying("playing", "QQSong", "QQArtist", 180000, 2000,
                                 album="QQAlbum", bundle="com.tencent.QQMusicMac")
        self.player.apply(qq_info)
        self.assertTrue(self.player.is_qqmusic)
        self.assertEqual(self.player.source_name, "QQ 音乐")
        self.assertEqual(self.player.source_short, "QQ 音乐")
        self.assertIn("QQ 音乐", self.player.connect_hint)
        self.assertIn("QQ 音乐", self.player.status)

        # Switch back to NetEase
        netease_info = mac.NowPlaying("playing", "163Song", "163Artist", 180000, 2000,
                                      bundle="com.netease.163music")
        self.player.apply(netease_info)
        self.assertFalse(self.player.is_qqmusic)
        self.assertEqual(self.player.source_short, "网易云")

    def test_qqmusic_retry_and_cache_directory_configuration(self):
        player = mac.MacNeteasePlayer(source_mode="qqmusic", query=lambda: None,
                                      executor=self.executor, clock=lambda: self.clock[0], autostart=False)
        try:
            self.assertTrue(player.is_qqmusic)
            self.assertEqual(player.source_short, "QQ 音乐")
            self.assertIn("QQ 音乐", player.status)
            info = mac.NowPlaying("playing", "Song", "Artist", 120000, 1000, bundle="com.tencent.QQMusicMac")
            player.apply(info)
            self.assertTrue(hasattr(player, "retry_lyrics"))
            self.assertTrue(hasattr(player, "configure_cache_directory"))
            player.retry_lyrics()
            self.assertIn("正在重新获取", player.lyric_status)
            player.configure_cache_directory("/tmp/test_cache")
            self.assertIn("test_cache", player.cache_status)
        finally:
            player.stop()

    def test_load_qqmusic_lyrics_collab_and_album_fallback(self):
        from lrc import LyricDocument, LyricLine
        from qqmusic_lyrics import LyricResult
        doc = LyricDocument([LyricLine(1000, "测试歌词")], [])
        sample_info = mac.NowPlaying("playing", "TestSong", "TestArtist", 180000, 1000, album="WrongAlbum", bundle="com.tencent.QQMusicMac")
        calls = []

        def mock_qq_load(snapshot, cancelled=lambda: False):
            calls.append(snapshot.album)
            if snapshot.album == "WrongAlbum":
                return LyricResult(None, "未找到")
            return LyricResult(doc, "成功", "mid123")

        with patch("qqmusic_lyrics.load_song_lyrics", side_effect=mock_qq_load):
            res = mac.load_qqmusic_lyrics(sample_info)
            self.assertEqual(res.document, doc)
            self.assertEqual(calls, ["WrongAlbum", ""])

        collab_info = mac.NowPlaying("playing", "CollabSong", "ArtistA", 180000, 1000, bundle="com.tencent.QQMusicMac")
        with patch("qqmusic_lyrics.load_song_lyrics", return_value=LyricResult(None, "未找到")), \
             patch("macos_netease._find_mac_collab_song", return_value={"mid": "collab_mid", "id": 123}), \
             patch("macos_netease._fetch_qq_lyrics_by_mid", return_value=doc):
            res2 = mac.load_qqmusic_lyrics(collab_info)
            self.assertEqual(res2.document, doc)
            self.assertEqual(res2.mid, "collab_mid")

    def test_qqmusic_playback_stalled_detects_pause_and_freezes_position(self):
        clock_time = [100.0]
        audio_state = [True]
        def fake_clock():
            return clock_time[0]
        def fake_audio_running():
            return audio_state[0]

        player = mac.MacNeteasePlayer(autostart=False, clock=fake_clock, query=lambda: None, audio_running=fake_audio_running)
        try:
            sample = mac.NowPlaying("playing", "Song", "Artist", 200000, 150000, rate=1.0, bundle="com.tencent.QQMusicMac")
            player.apply(sample, captured=100.0)
            self.assertTrue(player.playing)
            self.assertEqual(player.position(), 150000)

            # 正常推进 1.5s，因音频设备活跃且播放中，时间向前平滑推进到 151500
            clock_time[0] = 101.5
            self.assertEqual(player.position(), 151500)

            # 用户按下暂停，音频设备停止发声（虽然 QQ 音乐的 rate 仍为 1.0，position_ms 没变）
            audio_state[0] = False
            clock_time[0] = 102.0
            player.apply(sample, captured=102.0)
            # 必须识别为暂停！
            self.assertFalse(player.playing)
            # 并且位置冻结在暂停时的实际位置 152000，绝不倒退回 150000 也绝不继续累加
            self.assertEqual(player.position(), 152000)

            # 时间继续过去，位置依然静止
            clock_time[0] = 105.0
            self.assertEqual(player.position(), 152000)

            # 当用户恢复播放，音频设备恢复活跃发声
            audio_state[0] = True
            resumed = mac.NowPlaying("playing", "Song", "Artist", 200000, 152000, rate=1.0, bundle="com.tencent.QQMusicMac")
            player.apply(resumed, captured=105.1)
            self.assertTrue(player.playing)
            self.assertEqual(player.position(), 152000)
        finally:
            player.stop()

    def test_mac_coreaudio_detection(self):
        # 验证 CoreAudio 检测在各种边界条件下返回有效布尔或 None，且不抛出异常
        self.assertIsNone(mac.is_mac_bundle_audio_running(None))
        self.assertIsNone(mac.is_mac_bundle_audio_running(""))
        fake_result = mac.is_mac_bundle_audio_running("com.fake.nonexistent.app.12345")
        self.assertIn(fake_result, (None, False))
        out_running = mac.is_mac_audio_output_running()
        self.assertIsInstance(out_running, bool)
        out_bundle_running = mac.is_mac_audio_output_running("com.fake.nonexistent.app.12345")
        self.assertIsInstance(out_bundle_running, bool)

        # 验证播放器调用音频检测时会传入 bundle
        received_bundles = []
        def probe_audio(bundle=None):
            received_bundles.append(bundle)
            return True

        p = mac.MacNeteasePlayer(autostart=False, query=lambda: None, audio_running=probe_audio)
        try:
            info = mac.NowPlaying("playing", "Song", "Artist", 200000, 10000, rate=1.0, bundle="com.tencent.QQMusicMac")
            p.apply(info)
            self.assertIn("com.tencent.QQMusicMac", received_bundles)
        finally:
            p.stop()

    def test_qqmusic_compilation_and_collab_fuzzy_matching(self):
        from lrc import LyricDocument, LyricLine
        from qqmusic_lyrics import LyricResult
        doc = LyricDocument([LyricLine(1000, "测试歌词")], [])
        # 测试张信哲《别怕我伤心》（时长 286000ms，原版 291000ms，差异 5000ms 且专辑为精选集）
        compilation_info = mac.NowPlaying("playing", "别怕我伤心", "张信哲", 286000, 0, album="永恒金曲 影音典藏精选", bundle="com.tencent.QQMusicMac")
        mock_song = {"mid": "000z6RLz2OWlRY", "id": 100, "name": "别怕我伤心", "singer": [{"name": "张信哲"}], "interval": 291, "album": {"name": "等待"}}
        with patch("qqmusic_lyrics.load_song_lyrics", return_value=LyricResult(None, "未找到")), \
             patch("macos_netease._find_mac_collab_song", return_value=mock_song), \
             patch("macos_netease._fetch_qq_lyrics_by_mid", return_value=doc):
            res = mac.load_qqmusic_lyrics(compilation_info)
            self.assertEqual(res.document, doc)
            self.assertEqual(res.mid, "000z6RLz2OWlRY")

    def test_screen_selection_and_overlay_binding(self):
        from overlay import LyricsOverlay
        from settings import Preferences, SettingsStore
        from controls import ControlPanel
        from PySide6.QtWidgets import QApplication

        app = QApplication.instance() or QApplication([])
        prefs = Preferences()
        player = mac.MacNeteasePlayer(autostart=False, query=lambda: None)
        overlay = LyricsOverlay(player, prefs)
        try:
            # 默认跟随主屏
            self.assertEqual(overlay._screen, app.primaryScreen())

            # 若设置了屏幕名称且存在
            screens = app.screens()
            if screens:
                first_name = screens[0].name()
                prefs.target_screen = first_name
                overlay.refresh_preferences()
                self.assertEqual(overlay._screen, screens[0])

            # 若设置了不存在的屏幕名称，优雅回退到主屏
            prefs.target_screen = "NonExistentDisplay"
            overlay.refresh_preferences()
            self.assertEqual(overlay._screen, app.primaryScreen())

            # 测试控制面板中的 screen_combo
            import tempfile
            from pathlib import Path
            with tempfile.TemporaryDirectory() as tmpdir:
                store = SettingsStore(Path(tmpdir) / "settings.ini")
                panel = ControlPanel(player, overlay, prefs, store)
                try:
                    self.assertTrue(hasattr(panel, "screen_combo"))
                    self.assertGreaterEqual(panel.screen_combo.count(), 1)
                    self.assertEqual(panel.screen_combo.itemData(0), "")
                finally:
                    panel.tray.hide()
                    panel.close()
        finally:
            player.stop()
            overlay.close()



class MacPlatformTests(unittest.TestCase):
    def test_platform_defaults_and_theme_font_keep_windows_unchanged(self):
        import fonts
        import settings
        import themes
        self.assertEqual(settings.default_font_family("win32"), "Microsoft YaHei UI")
        self.assertEqual(settings.default_font_family("darwin"), "PingFang SC")
        self.assertEqual([value for _, value in fonts.preset_fonts("darwin")], ["PingFang SC", "Songti SC", "Kaiti SC"])
        self.assertEqual([value for _, value in fonts.preset_fonts("win32")], ["Microsoft YaHei UI", "SimSun", "KaiTi"])
        with patch.object(themes, "DEFAULT_FONT_FAMILY", "PingFang SC"):
            self.assertIn("font-family: 'PingFang SC'", themes.theme_stylesheet("light"))
        with patch.object(themes, "DEFAULT_FONT_FAMILY", "Microsoft YaHei UI"):
            self.assertIn("font-family: 'Microsoft YaHei UI'", themes.theme_stylesheet("light"))

    def test_overlay_retains_tool_input_transparency_and_applies_lyric_only_offset(self):
        from overlay import LyricsOverlay
        from settings import Preferences
        player = mac.MacNeteasePlayer(query=lambda: None, clock=lambda: 0, autostart=False)
        player.apply(info())
        player.adjust_offset(200)
        overlay = LyricsOverlay(player, Preferences(delay_ms=300))
        try:
            doc = LyricDocument([LyricLine(1000, "Hello", (TimedWord(1100, 1200, 0, 5),))], [])
            overlay.set_document(doc)
            self.assertEqual(overlay.timeline.lines[0].start_ms, 1100)
            self.assertEqual(overlay.timeline.lines[0].words[0].start_ms, 1200)
            self.assertEqual(player.position(), 1000)
            self.assertEqual(overlay.windowFlags() & Qt.WindowType.WindowType_Mask, Qt.WindowType.Tool)
            self.assertTrue(overlay.windowFlags() & Qt.WindowType.WindowTransparentForInput)
            overlay.close()
            with patch("overlay.sys", SimpleNamespace(platform="darwin")):
                other = LyricsOverlay(player, Preferences())
            self.assertTrue(other.testAttribute(Qt.WidgetAttribute.WA_MacAlwaysShowToolWindow))
            other.close()
            other.deleteLater()
        finally:
            overlay.close()
            overlay.deleteLater()
            player.stop()

    def test_external_control_panel_does_not_move_music_when_changing_effects(self):
        from controls import ControlPanel
        from overlay import LyricsOverlay
        from settings import Preferences, SettingsStore
        with tempfile.TemporaryDirectory() as temporary:
            player = mac.MacNeteasePlayer(query=lambda: None, clock=lambda: 0, autostart=False)
            player.apply(info())
            prefs = Preferences()
            overlay = LyricsOverlay(player, prefs)
            panel = ControlPanel(player, overlay, prefs, SettingsStore(Path(temporary) / "settings.ini"))
            try:
                with patch.object(mac.subprocess, "run") as run:
                    panel.theme_combo.setCurrentIndex(panel.theme_combo.findData("dark"))
                    panel.animation_combo.setCurrentIndex(panel.animation_combo.findData("fall_shake"))
                    panel._refresh_position()
                    self.assertEqual((player.playing, player.position()), (True, 1000))
                    run.assert_not_called()
                self.assertTrue(panel.progress.display_only)
            finally:
                panel.refresh_timer.stop()
                panel.font_preview.timer.stop()
                panel.tray.hide()
                panel.hide()
                panel.deleteLater()
                overlay.close()
                overlay.deleteLater()
                player.stop()

    def test_entry_rejects_windows_and_help_does_not_start_qt(self):
        import main_mac
        with patch.object(main_mac.sys, "platform", "win32"):
            self.assertEqual(main_mac.main([]), 2)
        with patch.object(main_mac.sys, "platform", "darwin"), patch.object(mac, "find_nowplaying_cli", return_value=None):
            self.assertEqual(main_mac.main(["--check"]), 1)

    def test_mac_without_tray_can_restore_panel_from_application_activation(self):
        import controls
        from overlay import LyricsOverlay
        from settings import Preferences, SettingsStore
        with tempfile.TemporaryDirectory() as temporary:
            player = mac.MacNeteasePlayer(query=lambda: None, autostart=False)
            prefs = Preferences()
            overlay = LyricsOverlay(player, prefs)
            with patch.object(controls, "sys", SimpleNamespace(platform="darwin")), \
                    patch.object(controls.QSystemTrayIcon, "isSystemTrayAvailable", return_value=False):
                panel = controls.ControlPanel(player, overlay, prefs, SettingsStore(Path(temporary) / "settings.ini"))
                try:
                    self.assertTrue(panel.tray_button.isEnabled())
                    self.assertEqual(panel.tray_button.text(), "隐藏面板")
                    with patch.object(panel, "show_panel") as show:
                        panel.hide()
                        panel._on_app_state_changed(Qt.ApplicationState.ApplicationActive)
                        show.assert_called_once()
                finally:
                    panel.refresh_timer.stop()
                    panel.font_preview.timer.stop()
                    panel.font_library.close()
                    panel.hide()
                    panel.tray.hide()
                    panel.deleteLater()
                    overlay.close()
                    overlay.deleteLater()
                    player.stop()

    def test_attribution_docs_and_scripts_are_present_without_bundled_helper(self):
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        guide = (ROOT / "MACOS.md").read_text(encoding="utf-8")
        self.assertIn("@qingyin-alice-zhong", readme)
        self.assertIn("5109df2c99ee87ee6ad5370fed70fa5d880336a5", guide)
        self.assertIn("尚未完成 macOS 真机", guide)
        self.assertIn("这些结果不代表真实网易云播放验收", guide)
        self.assertIn("archive/refs/heads/main.zip", guide)
        self.assertIn("macOS", (ROOT / "THIRD_PARTY_NOTICES.md").read_text(encoding="utf-8"))
        self.assertFalse((ROOT / "assets/nowplaying-cli").exists())
        self.assertNotIn("requests", (ROOT / "requirements.txt").read_text())
        from tests.test_workflow_docs import DOCUMENTS
        self.assertIn(ROOT / "MACOS.md", DOCUMENTS)

    def test_qrc_file_loading_support(self):
        import lrc
        with tempfile.TemporaryDirectory() as temporary:
            # Plaintext QRC
            qrc_path = Path(temporary) / "test.qrc"
            qrc_path.write_text("[offset:0]\n[0,1000]你(0,400)好(400,500)\n", encoding="utf-8")
            doc = lrc.load_lrc(qrc_path)
            self.assertEqual(len(doc.lines), 1)
            self.assertEqual(doc.lines[0].text, "你好")
            self.assertEqual(len(doc.lines[0].words), 2)

            # Synthetic encrypted QRC
            synthetic = json.loads((ROOT / "tests/fixtures/qq-cache-synthetic.json").read_text(encoding="utf-8"))
            enc_path = Path(temporary) / "encrypted.qrc"
            enc_path.write_bytes(bytes.fromhex(synthetic["samples"]["qrc"]["hex"]))
            enc_doc = lrc.load_lrc(enc_path)
            self.assertGreater(len(enc_doc.lines), 0)
            self.assertIn("你好", enc_doc.lines[0].text)

    def test_main_mac_cli_options(self):
        import main_mac
        with patch("sys.platform", "darwin"):
            self.assertEqual(main_mac.main(["--check"]), 0 if mac.find_nowplaying_cli() else 1)

    def test_qqmusic_control_panel_ui(self):
        from controls import ControlPanel
        from overlay import LyricsOverlay
        from settings import Preferences, SettingsStore
        player = mac.MacNeteasePlayer(source_mode="qqmusic", query=lambda: None, autostart=False)
        with tempfile.TemporaryDirectory() as temporary:
            store = SettingsStore(Path(temporary) / "settings.ini")
            prefs = Preferences()
            overlay = LyricsOverlay(player, prefs)
            panel = ControlPanel(player, overlay, prefs, store)
            panel.show()
            try:
                self.assertEqual(panel.source_short, "QQ 音乐")
                self.assertEqual(panel.source_name, "QQ 音乐")
                info = mac.NowPlaying("playing", "测试歌曲", "测试歌手", 180000, 5000, bundle="com.tencent.QQMusicMac")
                player.apply(info)
                self.assertEqual(panel.format_label.text(), "QQ 音乐")
                self.assertEqual(panel.external_transport.text(), "QQ 音乐播放")
                self.assertIn("QQ 音乐", panel.music_hint.text())
                self.assertFalse(panel.retry_lyrics_button.isHidden())
                self.assertFalse(panel.qq_cache_controls.isHidden())
            finally:
                panel.refresh_timer.stop()
                panel.font_preview.timer.stop()
                panel.font_library.close()
                panel.hide()
                panel.tray.hide()
                panel.deleteLater()
                overlay.close()
                overlay.deleteLater()
                player.stop()

    def test_shell_syntax_and_non_mac_guard(self):
        git = shutil.which("git")
        git_bash = Path(git).resolve().parents[1] / "bin/bash.exe" if git else None
        bash = str(git_bash) if git_bash and git_bash.is_file() else ("/bin/bash" if Path("/bin/bash").is_file() else None)
        if not bash:
            self.skipTest("本机没有可用 Bash；macOS CI 验证脚本语法")
        for name in ("start.sh", "安装.sh", "卸载.sh", "启动.command", "启动QQ音乐联动.command"):
            result = subprocess.run([bash, "-n", str(ROOT / name)], capture_output=True, text=True, encoding="utf-8")
            self.assertEqual(result.returncode, 0, result.stderr)
        if os.name == "nt":
            result = subprocess.run([bash, str(ROOT / "安装.sh")], capture_output=True, text=True, encoding="utf-8")
            self.assertEqual(result.returncode, 2, result.stdout + result.stderr)


if __name__ == "__main__":
    unittest.main()
