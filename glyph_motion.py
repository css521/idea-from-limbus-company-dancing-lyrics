"""Stateless character choreography: the song position is the only animation clock."""
from dataclasses import dataclass
import math
from PySide6.QtCore import QRectF
from PySide6.QtGui import QTransform


@dataclass(frozen=True)
class GlyphState:
    x: float
    y: float
    opacity: float = 1
    scale: float = 1
    rotation: float = 0
    emphasis: float = 0
    split: float = 0


def smooth(value):
    value = max(0., min(1., value))
    return value * value * (3 - 2 * value)


def noise_value(seed, rank, axis, sample):
    value = (seed * 0x9E3779B1 + rank * 0x85EBCA77 + axis * 0xC2B2AE3D + sample) & 0xFFFFFFFF
    value = ((value ^ (value >> 16)) * 0x7FEB352D) & 0xFFFFFFFF
    value = ((value ^ (value >> 15)) * 0x846CA68B) & 0xFFFFFFFF
    return ((value ^ (value >> 16)) / 0xFFFFFFFF) * 2 - 1


def noise(seed, rank, axis, seconds, frequency=6):
    clock = seconds * frequency
    sample = math.floor(clock)
    weight = smooth(clock - sample)
    first = noise_value(seed, rank, axis, sample)
    return first + (noise_value(seed, rank, axis, sample + 1) - first) * weight


def stagger(position, start, end, rank, count, duration):
    total = max(0., end - start)
    if total == 0:
        return float(position >= end)
    duration = min(duration, total)
    delay = (total - duration) * rank / (count - 1) if count > 1 else 0
    return max(0., min(1., (position - start - delay) / duration))


def word_emphasis(glyph, words, position):
    weight = 0.
    for word in words:
        if glyph.text_start < word.text_end and glyph.text_end > word.text_start and word.start_ms <= position < word.end_ms:
            ramp = min(80, (word.end_ms - word.start_ms) / 4)
            weight = max(weight, smooth(min((position - word.start_ms) / ramp, (word.end_ms - position) / ramp)))
    return weight


def glyph_states(glyphs, prefs, item, position_ms, energy, pixels, seed=0, angle=0, moving=True):
    visible = [glyph for glyph in glyphs if not glyph.path.isEmpty()]
    count, rank = len(visible), 0
    seconds = position_ms / 1000
    amplitude = prefs.jump * (.35 + .65 * max(0., min(1., energy)))
    falling = prefs.animation_style.startswith("fall_") or prefs.animation_style.startswith("corrosion_")
    glitch = prefs.animation_style.startswith("glitch_")
    corrosion = prefs.animation_style.startswith("corrosion_")
    bloom = prefs.animation_style.startswith("bloom_")
    shaking = prefs.animation_style.endswith("_shake")
    radians = math.radians(angle)
    result = []
    for glyph in glyphs:
        if glyph.path.isEmpty():
            result.append(GlyphState(glyph.x, glyph.baseline, 0))
            continue
        emphasis = word_emphasis(glyph, item.words, position_ms) if prefs.singing_sync else 0
        if prefs.animation_style == "classic":
            dy = -prefs.jump * energy * (0.6 + 0.4 * math.sin(seconds * 8 - glyph.index * .6)) if moving else 0
            scale = (1 + .04 * energy if moving else 1) * (1 + .08 * emphasis)
            result.append(GlyphState(glyph.x, glyph.baseline + dy, 1, scale, 0, emphasis))
            continue
        entering = stagger(position_ms, item.start_ms, item.entry_end_ms, rank, count, 140 * 100 / prefs.entry_speed)
        leaving = stagger(position_ms, item.exit_start_ms, item.end_ms, rank, count,
                          (350 if falling else 200) * 100 / prefs.exit_speed)
        opacity = smooth(entering) * (1 - smooth(leaving))
        if shaking:
            dx = amplitude * .3 * noise(seed, rank, 0, seconds, prefs.shake_frequency)
            dy = amplitude * .5 * noise(seed, rank, 1, seconds, prefs.shake_frequency)
        else:
            dx = 0
            if corrosion:
                c_wave = math.sin(seconds * 2 * math.pi * 1.3 - rank * .7)
                drip_mult = 1.7 if c_wave > 0 else 0.7
                dy = amplitude * .45 * c_wave * drip_mult
            else:
                dy = amplitude * .4 * math.sin(seconds * 2 * math.pi * 1.5 - rank * .6)
        if corrosion:
            distance = prefs.fall_distance * pixels / 32 * (leaving ** 1.5) * 1.0
            rotation = (10 if noise_value(seed, rank, 2, 0) >= 0 else -10) * (leaving ** 1.5)
        elif falling:
            distance = prefs.fall_distance * pixels / 32 * leaving ** 2
            rotation = (8 if noise_value(seed, rank, 2, 0) >= 0 else -8) * leaving ** 2
        else:
            distance = 0
            rotation = 0
        split = 0.0
        scale = 1 + .08 * emphasis if opacity > 0 else 1

        if glitch and prefs.jump > 0:
            jump_ratio = min(1.0, prefs.jump / 10.0)
            enter_dx = enter_rot = enter_split = 0.0
            if entering < 1.0:
                e_step = math.floor(seconds * 20)
                e_jitter = noise_value(seed, rank, 3, e_step)
                enter_dx = e_jitter * (1.0 - entering) * 8.0 * jump_ratio
                enter_rot = e_jitter * (1.0 - entering) * 5.0 * jump_ratio
                enter_split = (1.0 - entering) * (2.0 + 3.0 * abs(e_jitter)) * jump_ratio

            leave_dx = leave_rot = leave_split = 0.0
            if leaving > 0.0:
                l_step = math.floor(seconds * 18)
                l_jitter = noise_value(seed, rank, 4, l_step)
                leave_dx = l_jitter * leaving * 10.0 * jump_ratio
                leave_rot = l_jitter * leaving * 6.0 * jump_ratio
                leave_split = leaving * 5.0 * jump_ratio

            burst_clock = math.floor(seconds * 7)
            burst_hash = noise_value(seed, 0, 7, burst_clock)
            burst_thresh = 0.60 - 0.25 * max(0.0, min(1.0, energy))
            if burst_hash > burst_thresh and entering >= 1.0 and leaving <= 0.0:
                b_step = math.floor(seconds * 21)
                b_jitter = noise_value(seed, rank, 8, b_step)
                burst_dx = b_jitter * (3.5 + 4.5 * max(0.0, min(1.0, energy))) * jump_ratio
                burst_rot = b_jitter * 3.5 * jump_ratio
                burst_split = (1.5 + 2.5 * abs(b_jitter)) * jump_ratio
            else:
                burst_dx = burst_rot = 0.0
                burst_split = (emphasis * 2.0) * jump_ratio if opacity > 0 else 0.0

            dx += enter_dx + leave_dx + burst_dx
            rotation += enter_rot + leave_rot + burst_rot
            split = max(enter_split, leave_split, burst_split)

        elif corrosion and prefs.jump > 0:
            jump_ratio = min(1.0, prefs.jump / 10.0)
            tremor_step = math.floor(seconds * 14)
            tremor = noise_value(seed, rank, 19, tremor_step) * 1.8 * jump_ratio
            droop = (1.5 + 0.8 * math.sin(seconds * 3.0 + rank * 0.4)) * jump_ratio
            dx += tremor
            dy += droop

            enter_dy = enter_split = 0.0
            if entering < 1.0:
                enter_dy = (1.0 - entering) * 12.0 * jump_ratio
                dy += enter_dy
                enter_split = (1.0 - entering) * 3.5 * jump_ratio

            leave_dx = leave_split = 0.0
            if leaving > 0.0:
                l_step = math.floor(seconds * 16)
                leave_dx = noise_value(seed, rank, 13, l_step) * leaving * 7.0 * jump_ratio
                dx += leave_dx
                leave_split = leaving * 5.0 * jump_ratio

            steady_split = (2.2 + 1.2 * math.sin(seconds * 3.5 + rank * 0.5) + 1.6 * max(0.0, min(1.0, energy)) + emphasis * 2.5) * jump_ratio if opacity > 0 else 0.0
            twitch_step = math.floor(seconds * 6)
            twitch = (1.8 * jump_ratio) if (noise_value(seed, rank, 23, twitch_step) > 0.65 and opacity > 0) else 0.0
            split = max(enter_split, leave_split, steady_split + twitch)

        elif bloom:
            enter_split = leave_split = 0.0
            enter_s = leave_s = 1.0
            breathe_scale = 1.0
            if prefs.jump > 0:
                jump_ratio = min(1.0, prefs.jump / 10.0)
                float_dy = (-3.5 - 2.5 * math.sin(seconds * 2.0 - rank * 0.5)) * jump_ratio
                dy += float_dy

                breathe = math.sin(seconds * 2.8 - rank * 0.4)
                breathe_scale = 1.0 + (0.04 + 0.03 * breathe + 0.06 * max(0.0, min(1.0, energy))) * jump_ratio if opacity > 0 else 1.0

                if entering < 1.0:
                    enter_dy = (1.0 - entering) * -10.0 * jump_ratio
                    dy += enter_dy
                    enter_split = (1.0 - entering) * 3.0 * jump_ratio
                    enter_s = 1.0 - 0.15 * (1.0 - smooth(entering)) * jump_ratio
                if leaving > 0.0:
                    leave_dy = -leaving * 16.0 * jump_ratio
                    dy += leave_dy
                    leave_split = leaving * 4.5 * jump_ratio
                    leave_s = 1.0 + 0.15 * smooth(leaving) * jump_ratio
                steady_split = (2.2 + 1.0 * math.sin(seconds * 3.2 + rank * 0.6) + 1.5 * max(0.0, min(1.0, energy)) + emphasis * 2.2) * jump_ratio if opacity > 0 else 0.0
                split = max(enter_split, leave_split, steady_split)
            scale = enter_s * leave_s * breathe_scale * (1 + .08 * emphasis if opacity > 0 else 1)

        # Convert screen-vertical fall to the tilted sentence's local coordinates.
        result.append(GlyphState(glyph.x + dx + math.sin(radians) * distance,
                                 glyph.baseline + dy + math.cos(radians) * distance,
                                 opacity, scale, rotation,
                                 emphasis if opacity > 0 else 0, split))
        rank += 1
    return result


def motion_bounds(ink, pixels, jump, style, angle=0, fall_distance=48, singing_sync=False):
    """Conservative local bounds including rotation, shake, glitch, corrosion, bloom and screen-vertical fall."""
    if style == "classic":
        scale = 1.04 * (1.08 if singing_sync else 1)
        scaled = ink.united(QRectF(ink.x() * scale, ink.y() * scale, ink.width() * scale, ink.height() * scale))
        return scaled.united(scaled.translated(0, -jump))
    if singing_sync:
        ink = ink.united(QRectF(ink.x() * 1.08, ink.y() * 1.08, ink.width() * 1.08, ink.height() * 1.08))
    bounds = QRectF(ink)
    if style.startswith("fall_"):
        for rotation in (-8, 8):
            bounds = bounds.united(QTransform().rotate(rotation).mapRect(ink))
        radians = math.radians(angle)
        distance = fall_distance * pixels / 32
        bounds = bounds.united(bounds.translated(math.sin(radians) * distance,
                                                math.cos(radians) * distance))
    elif style.startswith("corrosion_"):
        for rotation in (-8, 8):
            bounds = bounds.united(QTransform().rotate(rotation).mapRect(ink))
        radians = math.radians(angle)
        distance = fall_distance * pixels / 32 * 0.85
        bounds = bounds.united(bounds.translated(math.sin(radians) * distance,
                                                math.cos(radians) * distance))
        bounds = bounds.adjusted(-1, -2, 1, 4)
    elif style.startswith("bloom_"):
        scale = 1.08 * (1.12 if singing_sync else 1.0)
        scaled = ink.united(QRectF(ink.x() * scale, ink.y() * scale, ink.width() * scale, ink.height() * scale))
        bounds = bounds.united(scaled.translated(0, -10 if jump > 0 else 0))
        bounds = bounds.adjusted(-2, -3, 2, 3)
    elif style.startswith("glitch_"):
        bounds = bounds.adjusted(-4, -2, 4, 2)
    return bounds.adjusted(-jump * .3 - 2, -jump * .5 - 2, jump * .3 + 2, jump * .5 + 2)
