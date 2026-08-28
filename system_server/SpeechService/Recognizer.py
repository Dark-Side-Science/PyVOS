import wave
import time
from PySide6.QtMultimedia import (
    QAudioSource,
    QAudioFormat,
    QMediaDevices
)
from PySide6.QtCore import QBuffer, QTimer, QObject, Signal


class SpeechRecognizer(QObject):
    # Signals (like Android callbacks)
    listeningStarted = Signal()
    listeningStopped = Signal()
    audioLevelChanged = Signal(float)

    def __init__(self,
                 sample_rate=44100,
                 channels=1,
                 sample_format=QAudioFormat.Int16):
        super().__init__()

        self.sample_rate = sample_rate
        self.channels = channels
        self.sample_format = sample_format

        self.format = QAudioFormat()
        self.format.setSampleRate(sample_rate)
        self.format.setChannelCount(channels)
        self.format.setSampleFormat(sample_format)

        self.device = QMediaDevices.defaultAudioInput()
        self.audio = QAudioSource(self.device, self.format)

        self.buffer = None
        self.is_listening = False
        self.start_time = None

    # -------------------------------
    # Core Controls
    # -------------------------------

    def startListening(self, duration_ms=None):
        if self.is_listening:
            return

        self.buffer = QBuffer()
        self.buffer.open(QBuffer.WriteOnly)

        self.audio.start(self.buffer)
        self.is_listening = True
        self.start_time = time.time()

        self.listeningStarted.emit()

        if duration_ms:
            QTimer.singleShot(duration_ms, self.stopListening)

    def stopListening(self):
        if not self.is_listening:
            return

        self.audio.stop()
        self.buffer.close()
        self.is_listening = False

        self.listeningStopped.emit()

    def pauseListening(self):
        if self.is_listening:
            self.audio.suspend()

    def resumeListening(self):
        if self.is_listening:
            self.audio.resume()

    # -------------------------------
    # Audio Data Access
    # -------------------------------

    def getRawAudio(self) -> bytes:
        if not self.buffer:
            return b""
        return bytes(self.buffer.data())

    def getWavAudio(self) -> bytes:
        raw = self.getRawAudio()
        if not raw:
            return b""

        wav_bytes = bytearray()
        with wave.open("temp.wav", "wb") as wf:
            wf.setnchannels(self.channels)
            wf.setsampwidth(2)  # 16-bit
            wf.setframerate(self.sample_rate)
            wf.writeframes(raw)

        with open("temp.wav", "rb") as f:
            wav_bytes.extend(f.read())

        return bytes(wav_bytes)

    def saveToFile(self, filename):
        raw = self.getRawAudio()
        if not raw:
            return

        with wave.open(filename, "wb") as wf:
            wf.setnchannels(self.channels)
            wf.setsampwidth(2)
            wf.setframerate(self.sample_rate)
            wf.writeframes(raw)

    # -------------------------------
    # Utilities
    # -------------------------------

    def getListeningDuration(self) -> float:
        if not self.start_time:
            return 0.0
        return time.time() - self.start_time

    def isListening(self) -> bool:
        return self.is_listening

    def reset(self):
        self.stopListening()
        self.buffer = None
        self.start_time = None

    # -------------------------------
    # Future STT Hook
    # -------------------------------

    def recognizeText(self, engine=None):
        """
        Plug any STT engine later:
        - Vosk
        - Whisper
        - Android service
        """
        audio = self.getWavAudio()
        if not engine:
            return audio  # raw fallback

        return engine.recognize(audio)
        
        
        