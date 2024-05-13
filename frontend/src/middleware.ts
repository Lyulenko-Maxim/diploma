import {NextRequest, NextResponse} from 'next/server'

import {EnumTokens} from '@/services/auth.service'

export async function middleware(request: NextRequest, response: NextResponse) {
    const {url, cookies, nextUrl} = request

    const token = cookies.get(EnumTokens.ACCESS_TOKEN)?.value

    const isProtectedRoute = url.includes('/me')

    if (!token && isProtectedRoute) {
        return NextResponse.redirect(new URL('/auth/login', request.url))
    }

    const isAuthRoute = url.includes('/auth')

    if (nextUrl.pathname === '/auth') {
        return NextResponse.redirect(new URL('/auth/login', request.url))
    }

    if (token && isAuthRoute) {
        return NextResponse.redirect(new URL('/me', request.url))
    }

    return NextResponse.next()
}

export const config = {
    matcher: ['/me/:path*', '/auth/:path*']
}
