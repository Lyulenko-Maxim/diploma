import React, {FC, MutableRefObject, PropsWithChildren} from 'react';
import {useOnline} from "@/hooks/auth.hooks";

interface IToken {
    token: string | null,
    wsRef: MutableRefObject<WebSocket | null>
}

const OnlineProvider: FC<PropsWithChildren & IToken> = ({children, wsRef, token}) => {
    useOnline(wsRef, token)
    return <>{children}</>

};

export default OnlineProvider;