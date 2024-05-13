'use server'

import {cookies} from "next/headers";
import {EnumTokens} from "@/services/auth.service";

const connections = new Map();

export const closeById = async (id: string) => {
    const ws = connections.get(id);
    if (ws) ws.close();
}

export const openSocket = async (id: string): Promise<WebSocket> => {
    const accessToken = cookies().get(EnumTokens.ACCESS_TOKEN)?.value
    const refreshToken = cookies().get(EnumTokens.REFRESH_TOKEN)?.value

    return new Promise((resolve, reject) => {
        const ws = new WebSocket(`ws://127.0.0.1:8000/ws/?access_token=${accessToken}&refresh_token=${refreshToken}`);

        ws.onopen = () => {
            console.log('open' + id)
            connections.set(id, ws);
            console.log(connections)
            resolve(ws);
        };

        ws.onclose = () => {
            console.log('close' + id)
            connections.delete(id);
        };

        ws.onerror = (error) => {
            console.log('error' + id)
            console.error('WebSocket error:', error);
            ws.close()
            reject(error);
        };
    });
}
