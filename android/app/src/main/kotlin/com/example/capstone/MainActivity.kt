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
import okhttp3.MediaType.Companion.toMediaTypeOrNull
import okhttp3.RequestBody.Companion.toRequestBody
import okhttp3.OkHttpClient
import okhttp3.Request
import okhttp3.MultipartBody
import okhttp3.Call
import okhttp3.Callback
import okhttp3.Response

class MainActivity : FlutterActivity() {
    private val CHANNEL = "com.meddetect.capstone/camera"
    private val REQUEST_IMAGE_CAPTURE = 1
    private var imageUris: MutableList<Uri> = mutableListOf()

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
                val imageUri = saveImageToStorage(it)
                imageUri?.let { uri ->
                    imageUris.add(uri)
                    
                    if (imageUris.size < 2) {
                        openCamera()  // Take the second picture
                    } else {
                        sendImagesToServer(imageUris)
                        imageUris.clear()  // Clear the list for next session
                    }
                }
            }
        }
    }

    private fun saveImageToStorage(bitmap: Bitmap): Uri? {
        val filename = "captured_image_${System.currentTimeMillis()}.jpg"
        val contentValues = ContentValues().apply {
            put(MediaStore.MediaColumns.DISPLAY_NAME, filename)
            put(MediaStore.MediaColumns.MIME_TYPE, "image/jpeg")
            if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.Q) {
                put(MediaStore.MediaColumns.RELATIVE_PATH, Environment.DIRECTORY_PICTURES)
            }
        }

        return contentResolver.insert(MediaStore.Images.Media.EXTERNAL_CONTENT_URI, contentValues)?.also { uri ->
            contentResolver.openOutputStream(uri)?.use { fos ->
                if (!bitmap.compress(Bitmap.CompressFormat.JPEG, 100, fos)) {
                    Log.e("MainActivity", "Failed to save bitmap.")
                } else {
                    Log.d("MainActivity", "Image saved to: $uri")
                }
            }
        }
    }

private fun sendImagesToServer(imageUris: List<Uri>) {
    val client = OkHttpClient()
    val requestBodyBuilder = MultipartBody.Builder().setType(MultipartBody.FORM)

    imageUris.forEachIndexed { index, uri ->
        val fileBody = contentResolver.openInputStream(uri)?.readBytes()?.toRequestBody("image/jpeg".toMediaTypeOrNull())
        fileBody?.let {
            // Correctly label images as "image1" and "image2"
            val imageLabel = "image${index + 1}" // will be image1 for the first image and image2 for the second
            requestBodyBuilder.addFormDataPart(imageLabel, "${imageLabel}.jpg", it)
        }
    }

    val requestBody = requestBodyBuilder.build()
    val request = Request.Builder()
        .url("http://10.0.0.242:8000/pill_vault/api/scan-image/") // Make sure this URL is correct
        .post(requestBody)
        .build()

    client.newCall(request).enqueue(object : Callback {
        override fun onFailure(call: Call, e: IOException) {
            Log.e("MainActivity", "Failed to send image", e)
        }

        override fun onResponse(call: Call, response: Response) {
            Log.d("MainActivity", "Response received: ${response.body?.string()}")
        }
    })
}

}
