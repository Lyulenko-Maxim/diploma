'use client'
import React from 'react';

import StatusList from "@/components/board/status/StatusList";
import {BreadcrumbItem, Breadcrumbs, Button} from '@nextui-org/react';
import Link from 'next/link';
import {PRIVATE_URLS} from "@/app/urlsConfig";
import {useProjectParams} from "@/app/me/projects/[projectId]/providers";

const BoardPage = () => {
    const projectId = useProjectParams()
    return (
        <div className='flex-1 flex-col'>
            <div className='flex flex-col gap-4 pl-10 pt-4 pb-4'>
                <Breadcrumbs size={'md'}>
                    <BreadcrumbItem><Link href={PRIVATE_URLS.PROJECT(projectId)}>Проект</Link></BreadcrumbItem>
                    <BreadcrumbItem><Link href={PRIVATE_URLS.BOARD(projectId)}>Доска</Link></BreadcrumbItem>
                </Breadcrumbs>

                <div className='flex flex-1 items-center gap-4'>
                    <h1 className='text-2xl font-medium mr-16'>Доска</h1>
                    <Button variant={'bordered'} size={'sm'} radius={'sm'}>
                        Добавить задачу
                    </Button>
                    <Button variant={'bordered'} size={'sm'} radius={'sm'}>
                        Добавить статус
                    </Button>
                </div>
            </div>
            <StatusList/>
        </div>
    );
};

export default BoardPage;