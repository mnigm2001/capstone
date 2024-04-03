package com.meddetect.capstone

import android.os.Bundle
import io.flutter.embedding.android.FlutterActivity
import io.flutter.embedding.engine.FlutterEngine
import io.flutter.plugin.common.MethodChannel
import android.content.Context
import android.hardware.camera2.CameraManager

class MainActivity: FlutterActivity() {
    private lateinit var cameraService: CameraService
    private val CHANNEL = "com.example.camera/channel"

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        cameraService = CameraService(this)
    }

    override fun configureFlutterEngine(flutterEngine: FlutterEngine) {
        super.configureFlutterEngine(flutterEngine)
        MethodChannel(flutterEngine.dartExecutor.binaryMessenger, CHANNEL).setMethodCallHandler {
            call, result ->
            when (call.method) {
                "openNativeCamera" -> {
                    cameraService.openCamera()
                    result.success(null)
                }
                else -> result.notImplemented()
            }
        }
    }
}

class CameraService(private val activity: Activity) {
    fun openCamera() {
        val cameraManager = activity.getSystemService(Context.CAMERA_SERVICE) as CameraManager
        try {
            val cameraId = cameraManager.cameraIdList[0] // just an example to get the first camera
            // You can now use the cameraManager to open the camera, etc.
        } catch (e: Exception) {
            e.printStackTrace()
        }
    }
}

