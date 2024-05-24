import {useEffect, useState} from 'react';
import {getMessaging, getToken} from 'firebase/messaging';
import firebaseApp from '../firebase/firebase';
import {IDeviceRegister, notificationService} from "@/services/notification.service";

const useFcmToken = () => {
    const [token, setToken] = useState('');
    const [notificationPermissionStatus, setNotificationPermissionStatus] = useState('');

    useEffect(() => {
        const retrieveToken = async () => {
            try {
                if (typeof window !== 'undefined' && 'serviceWorker' in navigator) {
                    const messaging = getMessaging(firebaseApp);

                    // Retrieve the notification permission status
                    const permission = await Notification.requestPermission();
                    setNotificationPermissionStatus(permission);

                    // Check if permission is granted before retrieving the token
                    if (permission === 'granted') {
                        const currentToken = await getToken(messaging, {
                            vapidKey: 'BKtgDsSRmiA6XD9tFQpfOSQ3HNz4OoVTQT_pBZZly3ZQv3ygcu8FVjDkqPz4q1q-HrpXZGx3SHPwB4ew8Mn5cU8'
                        });
                        if (currentToken) {
                            setToken(currentToken);
                        } else console.log('No registration token available. Request permission to generate one.');
                    }
                }
            } catch (error) {
                console.log('An error occurred while retrieving token:', error);
            }
        };

        retrieveToken();
    }, []);

    return {fcmToken: token, notificationPermissionStatus};
};

export default useFcmToken;