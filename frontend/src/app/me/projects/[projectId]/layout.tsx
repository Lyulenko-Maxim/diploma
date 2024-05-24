import React, {ReactNode} from 'react';
import Aside from "@/components/nav/Aside";
import {ProjectParamsProvider} from "@/app/me/projects/[projectId]/providers";

export default function ProjectLayout({children, params}: {
    children: ReactNode,
    params: {
        projectId: string
    }
}) {
    return (
        <ProjectParamsProvider projectId={params.projectId}>
            <div className='flex flex-1 overflow-hidden'>
                <Aside/>
                <section className="flex flex-1 overflow-hidden">
                    {children}
                </section>
            </div>
        </ProjectParamsProvider>

    )
}