import React, {ReactNode} from 'react';
import {Layout} from "@/components/layout/layout";
import MainLayout from "@/components/nav/MainLayout";
import Aside from "@/components/nav/Aside";

export default function DashboardLayout({children,}: {
    children: ReactNode
}) {
    return (
        <div className='flex flex-1 overflow-hidden'>
            {children}
        </div>
    )
}