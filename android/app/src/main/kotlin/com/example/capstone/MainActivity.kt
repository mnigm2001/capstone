package com.meddetect.capstone

import android.app.Activity
import android.content.Context
import android.hardware.camera2.CameraAccessException
import android.hardware.camera2.CameraDevice
import android.hardware.camera2.CameraManager
import android.util.Log

class CameraService(private val activity: Activity) {
    private var cameraDevice: CameraDevice? = null

    fun openCamera() {
        val cameraManager = activity.getSystemService(Context.CAMERA_SERVICE) as CameraManager
        try {
            val cameraId = cameraManager.cameraIdList[0] // just an example to get the first camera
            cameraManager.openCamera(cameraId, object : CameraDevice.StateCallback() {
                override fun onOpened(camera: CameraDevice) {
                    Log.d("CameraService", "Camera opened")
                    cameraDevice = camera
                    // Here you can start the camera preview
                }

                override fun onDisconnected(camera: CameraDevice) {
                    Log.d("CameraService", "Camera disconnected")
                    camera.close()
                    cameraDevice = null
                }

                override fun onError(camera: CameraDevice, error: Int) {
                    Log.d("CameraService", "Error opening camera: $error")
                    camera.close()
                    cameraDevice = null
                }
            }, null) // You might want to handle background threading here
        } catch (e: CameraAccessException) {
            Log.e("CameraService", "Camera access exception", e)
        } catch (e: SecurityException) {
            Log.e("CameraService", "Security exception: ${e.message}")
        }
    }

    // Add a method to close the camera device
    fun closeCamera() {
        cameraDevice?.close()
        cameraDevice = null
    }
}

