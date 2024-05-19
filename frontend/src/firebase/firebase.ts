import { initializeApp } from '@firebase/app';


const firebaseConfig = {
    apiKey: "AIzaSyC50HmhZ-_PGPD80fvKEaNM3-VkHPQRNIA",
    authDomain: "taskmanagement-12345.firebaseapp.com",
    projectId: "taskmanagement-12345",
    storageBucket: "taskmanagement-12345.appspot.com",
    messagingSenderId: "288834990680",
    appId: "1:288834990680:web:c2f64897b992e6d718102d",
    measurementId: "G-5EPSXFDGYF"
};

const firebaseApp = initializeApp(firebaseConfig);
export default firebaseApp;


