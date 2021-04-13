package com.example.taxictrl;

import androidx.annotation.NonNull;
import androidx.appcompat.app.AppCompatActivity;
import androidx.core.app.ActivityCompat;
import androidx.lifecycle.ViewModelProvider;

import android.Manifest;
import android.annotation.SuppressLint;
import android.content.Context;
import android.content.Intent;
import android.content.pm.PackageManager;
import android.location.Address;
import android.location.Geocoder;
import android.location.Location;
import android.location.LocationListener;
import android.location.LocationManager;
import android.media.audiofx.BassBoost;
import android.os.Bundle;
import android.os.Looper;
import android.provider.Settings;
import android.text.Html;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.Switch;
import android.widget.TextView;
import android.widget.Toast;

import com.google.android.gms.location.FusedLocationProviderClient;
import com.google.android.gms.location.LocationCallback;
import com.google.android.gms.location.LocationRequest;
import com.google.android.gms.location.LocationResult;
import com.google.android.gms.location.LocationServices;
import com.google.android.gms.tasks.OnCompleteListener;
import com.google.android.gms.tasks.Task;

import java.io.IOException;
import java.net.DatagramPacket;
import java.net.DatagramSocket;
import java.net.InetAddress;
import java.net.SocketException;
import java.text.SimpleDateFormat;
import java.util.Date;
import java.util.List;
import java.util.Locale;

public class MainActivity extends AppCompatActivity {
    //Initialize variable
    Switch swLocation;
    TextView lat,lng,tms;
    FusedLocationProviderClient fusedLocationProviderClient;
    Boolean SWST;
    EditText IP;
    String IP2;
    Integer PORT= 13550;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        //Assign variable
        swLocation = (Switch) findViewById(R.id.sw_location);
        lat = (TextView) findViewById(R.id.text_lat);
        lng = (TextView) findViewById(R.id.text_lng);
        tms = (TextView) findViewById(R.id.text_tms);


        //Initialize fusedLocationProviderClient
        fusedLocationProviderClient = LocationServices.getFusedLocationProviderClient(MainActivity.this);
    }

    public void validarSW(View view) {
        //Check condition
        SWST = swLocation.isChecked();
        if (ActivityCompat.checkSelfPermission(MainActivity.this,Manifest.permission.ACCESS_FINE_LOCATION) == PackageManager.PERMISSION_GRANTED && ActivityCompat.checkSelfPermission(MainActivity.this,
                    Manifest.permission.ACCESS_COARSE_LOCATION) == PackageManager.PERMISSION_GRANTED && ActivityCompat.checkSelfPermission(MainActivity.this,
                Manifest.permission.INTERNET) == PackageManager.PERMISSION_GRANTED&& SWST){

            
            getCurrentLocation();

        }else{
            //When permission is denied
            //Request permission
            ActivityCompat.requestPermissions(MainActivity.this,new String[]{
                    Manifest.permission.ACCESS_FINE_LOCATION, Manifest.permission.ACCESS_COARSE_LOCATION,Manifest.permission.INTERNET},100);
            finish();
            System.exit(0);
        }
    }
    @SuppressLint("MissingPermission")
    private void getCurrentLocation() {
        //Initialize location manager
        LocationManager locationManager = (LocationManager) getSystemService(
                Context.LOCATION_SERVICE);
        locationManager.requestLocationUpdates(LocationManager.GPS_PROVIDER, 2000, 0, new LocationListener() {
            @Override
            public void onLocationChanged(@NonNull Location location) {
                //Set Lat on TextView
                lat.setText(String.valueOf(location.getLatitude()));
                //Set Long on TextView
                lng.setText(String.valueOf(location.getLongitude()));
                //Set Tmstmp on TextView
                long time = location.getTime();
                Date date =new Date(time);
                SimpleDateFormat sdf = new SimpleDateFormat("yyyy-MM-dd HH:mm:ss");
                tms.setText(sdf.format(date));
                SendData();

            }

        });
    }
    public void SendData(){
        new Thread(new Runnable() {
            @Override
            public void run() {
                try {
                    String IP2 = ((EditText) findViewById(R.id.phone)).getText().toString();
                    DatagramSocket udpSocket = new DatagramSocket(PORT);
                    InetAddress serverAddr = InetAddress.getByName(IP2);
                    byte[] buf = ("'"+lng.getText().toString()+"', '"+lat.getText().toString()+"', '"+tms.getText().toString()+"'").getBytes();
                    DatagramPacket packet = new DatagramPacket(buf, buf.length,serverAddr, PORT);
                    udpSocket.send(packet);
                    udpSocket.close();
                } catch (SocketException e) {
                    Log.e("Udp:", "Socket Error:", e);
                } catch (IOException e) {
                    Log.e("Udp Send:", "IO Error:", e);
                }
            }
        }).start();
    }
}