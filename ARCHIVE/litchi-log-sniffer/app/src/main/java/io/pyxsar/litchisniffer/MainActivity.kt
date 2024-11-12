package io.pyxsar.litchisniffer

import android.os.Bundle
import android.util.Log
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.activity.enableEdgeToEdge
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.padding
import androidx.compose.material3.Scaffold
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Modifier
import androidx.compose.ui.tooling.preview.Preview
import io.pyxsar.litchisniffer.ui.theme.LitchiSnifferTheme
import okhttp3.Call
import okhttp3.Callback
import okhttp3.OkHttpClient
import okhttp3.Request
import okhttp3.Response
import java.io.IOException
import java.io.File
import java.time.LocalDateTime
import java.time.format.DateTimeFormatter

// Main user-defined variables
val latitude: Double    = 34.72215          // Latitude of mobile device [°N, WGS84]
val longitude: Double   = -86.56196         // Longitude of mobile device [°E, WGS84]
val deviceId: String    = "blueMobile"      // Name of mobile device
val connectKey: String  = "hcru_dev"        // CalTopo URL connectioin key
val logFolder: String   = "/data/user/0/io.pyxsar.litchisniffer"    // ISSUE: Cannot access Litchi folder due to Android 10+ security features

val now: LocalDateTime = LocalDateTime.now()
val time_local = now.format(DateTimeFormatter.ofPattern("yy-MM-dd HH:mm"))
val api_endpoint = "https://caltopo.com/api/v1/position/report/" +  // Build URL for CalTopo GET request
        connectKey + "?id=" +
        deviceId + "&lat=" +
        latitude + "&lng=" + longitude

class MainActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        enableEdgeToEdge()
        setContent {
            LitchiSnifferTheme {
                Scaffold(modifier = Modifier.fillMaxSize()) { innerPadding ->
                    DisplayText(
                        // Show main debug screen on device
                        lat = latitude,
                        long = longitude,
                        time = time_local,
                        apiUrl = api_endpoint,
                        modifier = Modifier.padding(innerPadding)
                    )
                }
            }
        }
        getFileList(logFolder)    // Observe contents of Litchi log folder, ideally
    }
}

fun getFileList(path: String) {
    // List contents of targeted directory on mobile device
    // Open Logcat and filter for "DirectoryContents"
    val directory = File(path)
        if (directory.exists() && directory.isDirectory) {
        val files = directory.listFiles()
        if (files != null) {
            for (file in files) {
                Log.i("DirectoryContents", "File: ${file.name}, Is Directory: ${file.isDirectory}")
            }
        } else {
            Log.w("DirectoryContents", "Directory is empty or cannot be accessed")
        }
    } else {
        Log.e("DirectoryContents", "The path does not exist or is not a directory")
    }
    Log.i("DirectoryContents","Target = ${path}")     // Uncomment to debug
}

fun uploadLocation(apiUrl: String, onResult: (String) -> Unit) {
    // Upload lat long to CalTopo API endpoint
    val client = OkHttpClient()
    val request = Request.Builder().url(apiUrl).build()
    client.newCall(request).enqueue(object : Callback {
        override fun onFailure(call: Call, e: IOException) {
            // Handle upload failure
            onResult("Failed to upload: ${e.message}")
        }
        override fun onResponse(call: Call, response: Response) {
            // Handle successful HTTP response(s)
            if (response.isSuccessful) {
                response.body?.string()?.let {
                    onResult(it)
                } ?: run {
                    onResult("No response body")
                }
            } else {
                onResult("Failed with status code: ${response.code}")
            }
        }
    })
}

@Composable
fun DisplayText(lat: Double, long: Double, time: String, apiUrl: String, modifier: Modifier = Modifier) {
    var responseText by remember { mutableStateOf("Fetching data...") }
    // Trigger HTTP request - SHOULD THIS BE MOVED OUTSIDE?
    LaunchedEffect(Unit) {
        uploadLocation(apiUrl) { result ->
            responseText = result
        }
    }
    // Main app display text
    Text(
        text = "Latitude = ${lat}°N\n" +
                "Longitude = ${long}°E\n" +
                "Time = $time CDT\n" +
                responseText,// + "\n" + api_endpoint,
        modifier = modifier
    )
}

@Preview(showBackground = true)
@Composable
fun appPreview() {
    // Application preview for debugging on Android studio
    LitchiSnifferTheme {
        DisplayText(latitude,longitude,time_local,api_endpoint)
    }
}