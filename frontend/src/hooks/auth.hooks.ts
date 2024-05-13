import {MutableRefObject, useEffect} from "react";

export const useOnline = (wsRef: MutableRefObject<WebSocket | null>, token: string | null) => {

    useEffect(() => {
        const openWebSocketConnection = () => {
            if (token) {
                const newWs = new WebSocket(`ws://127.0.0.1:8000/ws/?token=${token}`);
                wsRef.current = newWs;

                newWs.onopen = () => console.log("WebSocket connection opened with new token!");
                newWs.onclose = () => console.log("WebSocket connection closed with new token!");

                return () => {
                    if (newWs) {
                        newWs.close();
                        wsRef.current = null;
                    }
                };
            }
        };

        const closeWebSocketConnection = () => {
            if (wsRef.current) {
                wsRef.current.close();
                wsRef.current = null;
            }
        };

        window.addEventListener('beforeunload', closeWebSocketConnection);

        openWebSocketConnection();

        return () => {
            window.removeEventListener('beforeunload', closeWebSocketConnection);
            closeWebSocketConnection();
        };
    }, [wsRef, token]);
};