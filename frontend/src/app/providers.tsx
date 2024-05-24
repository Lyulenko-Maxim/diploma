"use client";
import * as React from "react";
import {Card, NextUIProvider, User} from "@nextui-org/react";
import {ThemeProvider as NextThemesProvider, useTheme as useNextTheme} from "next-themes";
import {ThemeProviderProps} from "next-themes/dist/types";
import {QueryClient, QueryClientProvider} from '@tanstack/react-query'
import {ReactQueryDevtools} from '@tanstack/react-query-devtools'
import {useEffect, useState} from 'react'
import {toast, Toaster} from "sonner";
import {useRouter} from "next/navigation";

import {onMessage} from "@firebase/messaging";
import firebaseApp from "@/firebase/firebase";
import useFcmToken from "@/firebase/useFcmToken";
import {getMessaging} from "firebase/messaging";
import {IDeviceRegister, notificationService} from "@/services/notification.service";
import Link from "next/link";
import {PRIVATE_URLS} from "@/app/urlsConfig";


export interface ProvidersProps {
    children: React.ReactNode;
    themeProps?: ThemeProviderProps;
}

export interface NotificationData {
    action: any;
    task?: any;
    actor?: any;
}

export const Providers = ({children, themeProps}: ProvidersProps) => {
    const {fcmToken, notificationPermissionStatus} = useFcmToken();
    const renderNotification = (data: NotificationData) => {
        const {action, task, actor} = data;
        switch (action) {
            case 'task_deleted':
                return <h5>удалил задачу <Link href={PRIVATE_URLS.PROJECT(task.project.id)}
                                               className='font-medium'>{task.title}</Link></h5>
            case 'task_updated':
                return <h5>обновил задачу <Link href={PRIVATE_URLS.TASK(task.project.id, task.id)}
                                                className='font-medium'>{task.title}</Link>
                </h5>
            case 'task_moved':
                return <h5>переместил задачу <Link
                    href={PRIVATE_URLS.TASK(task.project.id, task.id)} className='font-medium'>{task.title}</Link></h5>
            case 'expelled':
                return <h5>исключил Вас из проекта</h5>
            default:
                return null
        }
    }
    useEffect(() => {
        if (fcmToken) {
            console.log('FCM token:', fcmToken);
            const data: IDeviceRegister = {
                registration_id: fcmToken,
                active: true,
                cloud_message_type: 'FCM'
            };

            notificationService.registerDevice(data);
        }
    }, [fcmToken]);


    useEffect(() => {
        if (typeof window !== 'undefined' && 'serviceWorker' in navigator) {
            const messaging = getMessaging(firebaseApp);
            const unsubscribe = onMessage(messaging, (payload) => {
                console.log('Foreground push notification received:', payload);
                const {data} = payload;
                if (data) {
                    console.log(data)
                    const notificationData: NotificationData = {
                        action: JSON.parse(data.action),
                        task: JSON.parse(data.task),
                        actor: JSON.parse(data.actor),
                    };
                    console.log(notificationData)
                    toast.custom((t) => (
                        <div className='shadow p-4 flex flex-col items-start gap-2 z-[200]'>
                            <h1>{notificationData.task?.project?.name}</h1>
                            <div className='w-[300px]'>
                                <h5 className='text-sm'>Участник {notificationData.actor?.profile?.username}</h5>
                                {renderNotification(notificationData)}
                            </div>
                        </div>
                    ));
                } else {
                    toast.success(payload.notification?.title)
                }

            });
            return () => {
                unsubscribe();
            };
        }
    }, []);

    const router = useRouter();

    const [client] = useState(new QueryClient({
            defaultOptions: {
                queries: {
                    // refetchOnWindowFocus: false,
                    retry: false,

                }
            },
        })
    )
    const {setTheme, resolvedTheme} = useNextTheme();
    const getTheme = () => {
        if (resolvedTheme === "light") return "light";
        if (resolvedTheme === "dark") return "dark";
        if (resolvedTheme === "system") return "system";
    }
    return (
        <NextUIProvider navigate={router.push}>
            <NextThemesProvider defaultTheme="system" attribute="class" {...themeProps}>
                <QueryClientProvider client={client}>
                    <Toaster expand
                             visibleToasts={3}
                             richColors
                             pauseWhenPageIsHidden={true}
                             duration={15000}
                             position='bottom-right'
                             closeButton
                    />
                    {children}
                    {/*<OnlineProvider wsRef={wsRef} token={token}>*/}
                    {/*    {children}*/}
                    {/*</OnlineProvider>*/}
                    {/*<ReactQueryDevtools initialIsOpen={false}/>*/}
                </QueryClientProvider>
            </NextThemesProvider>
        </NextUIProvider>
    );
};
