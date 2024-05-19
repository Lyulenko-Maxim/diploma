"use client";
import * as React from "react";
import {Card, CardBody, NextUIProvider, User} from "@nextui-org/react";
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


export interface ProvidersProps {
    children: React.ReactNode;
    themeProps?: ThemeProviderProps;
}

export const Providers = ({children, themeProps}: ProvidersProps) => {
    const {fcmToken, notificationPermissionStatus} = useFcmToken();
    fcmToken && console.log('FCM token:', fcmToken);

    useEffect(() => {
        if (typeof window !== 'undefined' && 'serviceWorker' in navigator) {
            const messaging = getMessaging(firebaseApp);
            const unsubscribe = onMessage(messaging, (payload) => {
                console.log('Foreground push notification received:', payload);
                const data = payload.data;
                if (data) {
                    data.action = JSON.parse(data.action);
                    data.task = JSON.parse(data.task);
                    data.actor = JSON.parse(data.actor);

                    toast.custom((t) => (
                        <div className='shadow p-4 flex flex-col items-start gap-2'>
                            <h1>{data.task["project"].name}</h1>
                            <div className=''>
                                <h5 className='text-sm'>{data.actor.profile.username}</h5>
                                <h5>удалил(-а) задачу 5</h5>
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
                    <ReactQueryDevtools initialIsOpen={false}/>
                </QueryClientProvider>
            </NextThemesProvider>
        </NextUIProvider>
    );
};
