package com.meddetect.capstone

import android.Manifest
import android.app.Activity
import android.content.ContentValues
import android.content.Intent
import android.graphics.Bitmap
import android.os.Build
import android.os.Bundle
import android.os.Environment
import android.provider.MediaStore
import android.util.Log
import io.flutter.embedding.android.FlutterActivity
import io.flutter.embedding.engine.FlutterEngine
import io.flutter.plugin.common.MethodChannel
import java.io.File
import java.io.FileOutputStream
import java.io.OutputStream
import java.io.IOException

class MainActivity: FlutterActivity() {
    private val CHANNEL = "com.meddetect.capstone/camera"
    private val REQUEST_IMAGE_CAPTURE = 1

    override fun configureFlutterEngine(flutterEngine: FlutterEngine) {
        super.configureFlutterEngine(flutterEngine)

        MethodChannel(flutterEngine.dartExecutor.binaryMessenger, CHANNEL)
            .setMethodCallHandler { call, result ->
                when (call.method) {
                    "openNativeCamera" -> {
                        openCamera()
                        result.success(null)
                    }
                    else -> result.notImplemented()
                }
            }
    }

    private fun openCamera() {
        val takePictureIntent = Intent(MediaStore.ACTION_IMAGE_CAPTURE)
        try {
            startActivityForResult(takePictureIntent, REQUEST_IMAGE_CAPTURE)
        } catch (e: Exception) {
            Log.e("MainActivity", "openCamera error: ${e.localizedMessage}")
        }
    }

override fun onActivityResult(requestCode: Int, resultCode: Int, data: Intent?) {
    super.onActivityResult(requestCode, resultCode, data)

    if (requestCode == REQUEST_IMAGE_CAPTURE && resultCode == Activity.RESULT_OK) {
        val imageBitmap = data?.extras?.get("data") as? Bitmap
        imageBitmap?.let {
            saveImageToStorage(it)
        }
    }
}

private fun saveImageToStorage(bitmap: Bitmap) {
    val filename = "captured_image_${System.currentTimeMillis()}.jpg"
    val contentValues = ContentValues().apply {
        put(MediaStore.MediaColumns.DISPLAY_NAME, filename)
        put(MediaStore.MediaColumns.MIME_TYPE, "image/jpeg")
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.Q) {
            put(MediaStore.MediaColumns.RELATIVE_PATH, Environment.DIRECTORY_PICTURES)
        }
    }

    try {
        val uri = contentResolver.insert(MediaStore.Images.Media.EXTERNAL_CONTENT_URI, contentValues)
        uri?.let {
            contentResolver.openOutputStream(it)?.use { fos ->
                if (!bitmap.compress(Bitmap.CompressFormat.JPEG, 100, fos)) {
                    throw IOException("Failed to save bitmap.")
                } else {
                    Log.d("MainActivity", "Image saved to: $uri")
                }
            } ?: throw IOException("Failed to get output stream.")
        } ?: throw IOException("Failed to create new MediaStore record.")
    } catch (e: Exception) {
        Log.e("MainActivity", "Failed to save image", e)
    }
}
}
