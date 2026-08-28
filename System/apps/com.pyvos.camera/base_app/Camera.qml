import QtQuick
import QtQuick.Controls
import QtMultimedia
import QtCore

ApplicationWindow {
    id: window
    visible: true
    width: 360
    height: 640
    title: "QML Camera"

    property bool videoMode: false
    property bool recording: false
    property int currentCameraIndex: 0

    MediaDevices {
        id: mediaDevices
    }

    Camera {
        id: camera
        cameraDevice: mediaDevices.videoInputs.length > 0
                      ? mediaDevices.videoInputs[currentCameraIndex]
                      : null
        torchMode: Camera.TorchOff
    }

    ImageCapture {
        id: imageCapture
    }

    MediaRecorder {
        id: recorder
        outputLocation: StandardPaths.writableLocation(
            StandardPaths.MoviesLocation
        ) + "/video_" + Date.now() + ".mp4"
    }

    CaptureSession {
        id: session
        camera: camera
        videoOutput: videoOutput
        imageCapture: imageCapture
        recorder: recorder
    }

    VideoOutput {
        id: videoOutput
        anchors.fill: parent
        fillMode: VideoOutput.PreserveAspectCrop
    }

    /* ===== TORCH BUTTON ===== */
    Button {
        text: camera.torchMode === Camera.TorchOn ? "🔦 ON" : "🔦 OFF"
        anchors.top: parent.top
        anchors.left: parent.left
        anchors.margins: 15

        onClicked: {
            if (camera.isActive) {
                camera.torchMode =
                    camera.torchMode === Camera.TorchOn
                    ? Camera.TorchOff
                    : Camera.TorchOn
            }
        }
    }

    /* ===== SWITCH CAMERA ===== */
    Button {
        text: "🔄"
        anchors.top: parent.top
        anchors.right: parent.right
        anchors.margins: 15

        onClicked: {
            if (mediaDevices.videoInputs.length < 2)
                return

            camera.stop()

            currentCameraIndex =
                (currentCameraIndex + 1) % mediaDevices.videoInputs.length

            camera.cameraDevice =
                mediaDevices.videoInputs[currentCameraIndex]

            camera.torchMode = Camera.TorchOff

            Qt.callLater(function() {
                camera.start()
            })
        }
    }

    /* ===== MODE SELECTOR ===== */
    Rectangle {
        width: 220
        height: 40
        radius: 20
        color: "#66000000"
        anchors.horizontalCenter: parent.horizontalCenter
        anchors.bottom: captureButton.top
        anchors.bottomMargin: 20

        Row {
            anchors.fill: parent

            Rectangle {
                width: parent.width / 2
                height: parent.height
                radius: 20
                color: videoMode ? "transparent" : "white"

                Text {
                    anchors.centerIn: parent
                    text: "PHOTO"
                    color: videoMode ? "white" : "black"
                    font.bold: true
                }

                MouseArea {
                    anchors.fill: parent
                    onClicked: videoMode = false
                }
            }

            Rectangle {
                width: parent.width / 2
                height: parent.height
                radius: 20
                color: videoMode ? "white" : "transparent"

                Text {
                    anchors.centerIn: parent
                    text: "VIDEO"
                    color: videoMode ? "black" : "white"
                    font.bold: true
                }

                MouseArea {
                    anchors.fill: parent
                    onClicked: videoMode = true
                }
            }
        }
    }

    /* ===== CAPTURE BUTTON ===== */
    Rectangle {
        id: captureButton
        width: 80
        height: 80
        radius: 40
        color: recording ? "red" : "white"
        anchors.horizontalCenter: parent.horizontalCenter
        anchors.bottom: parent.bottom
        anchors.bottomMargin: 20

        MouseArea {
            anchors.fill: parent
            onClicked: {
                if (!videoMode) {
                    imageCapture.captureToFile(
                        StandardPaths.writableLocation(
                            StandardPaths.PicturesLocation
                        ) + "/photo_" + Date.now() + ".jpg"
                    )
                } else {
                    if (!recording) {
                        recorder.record()
                        recording = true
                    } else {
                        recorder.stop()
                        recording = false
                    }
                }
            }
        }
    }

    Component.onCompleted: {
        console.log("Detected cameras:", mediaDevices.videoInputs.length)

        if (mediaDevices.videoInputs.length > 0) {
            Qt.callLater(() => camera.start())
        }
    }
}