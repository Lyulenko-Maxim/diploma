"use client";
import * as React from "react";
import {NextUIProvider} from "@nextui-org/react";
import {ThemeProvider as NextThemesProvider, useTheme as useNextTheme} from "next-themes";
import {ThemeProviderProps} from "next-themes/dist/types";
import {QueryClient, QueryClientProvider} from '@tanstack/react-query'
import {ReactQueryDevtools} from '@tanstack/react-query-devtools'
import {useEffect, useState} from 'react'
import {Toaster} from "sonner";
import {useRouter} from "next/navigation";

import {closeById} from "@/app/actions";

export interface ProvidersProps {
    children: React.ReactNode;
    themeProps?: ThemeProviderProps;
    socketId: string;
}

export const Providers = ({children, themeProps, socketId}: ProvidersProps) => {
    useEffect(() => {

        const closeWebSocket = async () => {
            await closeById(socketId)

        }

        window.addEventListener('beforeunload', closeWebSocket);

        return () => {
            //
            // window.removeEventListener('beforeunload', closeWebSocket);
        };

    }, [socketId]);

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
