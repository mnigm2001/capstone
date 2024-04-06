package com.meddetect.capstone

import android.Manifest
import android.app.Activity
import android.content.ContentValues
import android.content.Intent
import android.graphics.Bitmap
import android.net.Uri
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
import java.io.IOException
import java.io.OutputStream
import okhttp3.*

class MainActivity : FlutterActivity() {
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
                        // Send the image to the server after saving
                        sendImageToServer(uri)
                    }
                } ?: throw IOException("Failed to get output stream.")
            } ?: throw IOException("Failed to create new MediaStore record.")
        } catch (e: Exception) {
            Log.e("MainActivity", "Failed to save image", e)
        }
    }

    private fun sendImageToServer(imageUri: Uri) {
        val inputStream = contentResolver.openInputStream(imageUri)
        val fileName = "image_${System.currentTimeMillis()}.jpg"

        inputStream?.let { stream ->
            val buffer = stream.readBytes()
            val requestBody = RequestBody.create(MediaType.parse("image/jpeg"), buffer)
            val multipartBody = MultipartBody.Builder()
                .setType(MultipartBody.FORM)
                .addFormDataPart("file", fileName, requestBody)
                .build()

            val request = Request.Builder()
                .url(http://127.0.0.1:8000/pill_vault/api/scan-image/)  // Replace with your actual endpoint URL
                .post(multipartBody)
                .build()

            OkHttpClient().newCall(request).enqueue(object : Callback {
                override fun onFailure(call: Call, e: IOException) {
                    Log.e("MainActivity", "Failed to send image", e)
                }

                override fun onResponse(call: Call, response: Response) {
                    Log.d("MainActivity", "Response received: ${response.body()?.string()}")
                }
            })
        }
    }
}
