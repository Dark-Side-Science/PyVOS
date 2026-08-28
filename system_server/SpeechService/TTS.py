from PySide6.QtTextToSpeech import QTextToSpeech
from PySide6.QtCore import QLocale


class TextToSpeech:
    def __init__(self):
        self.tts = QTextToSpeech()

        # State callback (optional)
        self.tts.stateChanged.connect(self._on_state_changed)

    # =====================
    # Core control
    # =====================

    def speak(self, text: str):
        """Speak text"""
        if not text:
            return
        self.tts.say(text)

    def stop(self):
        """Stop speaking"""
        self.tts.stop()

    def pause(self):
        """Pause speech"""
        self.tts.pause()

    def resume(self):
        """Resume speech"""
        self.tts.resume()

    # =====================
    # Audio controls (Android-like)
    # =====================

    def setVolume(self, volume: float):
        """
        volume: 0.0 → 1.0
        Android equivalent: setSpeechRate / setPitch / setVolume
        """
        volume = max(0.0, min(volume, 1.0))
        self.tts.setVolume(volume)

    def setSpeechRate(self, rate: float):
        """
        rate: -1.0 → 1.0
        Android equivalent: setSpeechRate()
        """
        rate = max(-1.0, min(rate, 1.0))
        self.tts.setRate(rate)

    def setPitch(self, pitch: float):
        """
        pitch: -1.0 → 1.0
        Android equivalent: setPitch()
        """
        pitch = max(-1.0, min(pitch, 1.0))
        self.tts.setPitch(pitch)

    # =====================
    # Voice & language
    # =====================

    def getAvailableVoices(self):
        """Return list of available voices"""
        return self.tts.availableVoices()

    def setVoice(self, index: int):
        """Set voice by index"""
        voices = self.tts.availableVoices()
        if 0 <= index < len(voices):
            self.tts.setVoice(voices[index])

    def getVoices(self):
        """Return available locales"""
        return self.tts.availableLocales()

    def setLanguage(self, locale: QLocale):
        """Set language/locale"""
        self.tts.setLocale(locale)

    def setLanguage(self, language: QLocale.Language, country=QLocale.AnyCountry):
        """
        Android-style language setter
        Example: setLanguage(QLocale.English, QLocale.India)
        """
        self.tts.setLocale(QLocale(language, country))

    # =====================
    # State & info
    # =====================

    def getState(self):
        """Return current TTS state"""
        return self.tts.state()

    def isSpeaking(self):
        return self.tts.state() == QTextToSpeech.Speaking

    def isPaused(self):
        return self.tts.state() == QTextToSpeech.Paused

    def isReady(self):
        return self.tts.state() == QTextToSpeech.Ready

    def onError(self):
        return self.tts.state() == QTextToSpeech.Error

    # =====================
    # Internal callback
    # =====================

    def _on_state_changed(self, state):
        state_map = {
            QTextToSpeech.Ready: "READY",
            QTextToSpeech.Speaking: "SPEAKING",
            QTextToSpeech.Paused: "PAUSED",
            QTextToSpeech.Error: "ERROR",
        }
        return "[TTS]", state_map.get(state, "UNKNOWN")