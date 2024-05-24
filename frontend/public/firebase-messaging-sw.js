importScripts('https://www.gstatic.com/firebasejs/8.8.0/firebase-app.js');
importScripts('https://www.gstatic.com/firebasejs/8.8.0/firebase-messaging.js');

const firebaseConfig = {
    apiKey: "AIzaSyC50HmhZ-_PGPD80fvKEaNM3-VkHPQRNIA",
    authDomain: "taskmanagement-12345.firebaseapp.com",
    projectId: "taskmanagement-12345",
    storageBucket: "taskmanagement-12345.appspot.com",
    messagingSenderId: "288834990680",
    appId: "1:288834990680:web:c2f64897b992e6d718102d",
    measurementId: "G-5EPSXFDGYF"
};

firebase.initializeApp(firebaseConfig);
const messaging = firebase.messaging();

messaging.onBackgroundMessage((payload) => {
    console.log(
        '[firebase-messaging-sw.js] Received background message ',
        payload
    );
    const notificationTitle = payload.notification.title;
    const notificationOptions = {
        body: payload.notification.title,
        icon: './logo.svg',
    };
    self.registration.showNotification(notificationTitle, notificationOptions);
});