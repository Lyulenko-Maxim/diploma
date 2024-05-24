'use client'
import React, {useMemo} from 'react';
import TaskEditor from "@/components/editors/TaskEditor";
import {useTaskRetrieve} from "@/hooks/task.hooks";
import {useProjectParams} from "@/app/me/projects/[projectId]/providers";
import {
    BreadcrumbItem,
    Breadcrumbs,
    Card,
    CardBody,
    Chip,
    Divider,
    Select,
    SelectItem,
    Textarea,
    Tooltip
} from '@nextui-org/react';
import {CardFooter, CardHeader} from "@nextui-org/card";
import {useStatusList} from "@/hooks/status.hooks";
import {StatusCategoryEnum} from "@/types/status.types";
import {useMemberCurrent, useMemberList} from "@/hooks/members.hooks";
import {checkPermissions, PERMISSIONS} from "@/app/permissions";
import {Lock} from "lucide-react";
import Link from "next/link";
import {PRIVATE_URLS} from "@/app/urlsConfig";


export interface TaskDetailsProps {
    params: { taskId: string }
}

const TaskPage = ({params}: TaskDetailsProps) => {
    const projectId = useProjectParams()
    const {data: currentMember} = useMemberCurrent(projectId)
    const {data: task} = useTaskRetrieve(projectId, params.taskId)
    const {items: statuses, setItems: setStatuses} = useStatusList(projectId)
    const {items: members, setItems: setMembers} = useMemberList(projectId)
    if (!task || !statuses || !members || !currentMember) {
        return <div></div>;
    }

    const hasTaskPermission = checkPermissions(currentMember.permissions, [])

    return (
        <div className="flex flex-1 gap-2 overflow-y-hidden">

            <div className="flex w-1/2 flex-col gap-8 overflow-y-auto p-8">
                <div className='flex flex-col gap-4 pt-4 pb-4 pl-10'>
                    <Breadcrumbs size={'md'}>
                        <BreadcrumbItem><Link href={PRIVATE_URLS.PROJECT(projectId)}>Проект</Link></BreadcrumbItem>
                        <BreadcrumbItem><Link href={PRIVATE_URLS.BOARD(projectId)}>Доска</Link></BreadcrumbItem>
                        <BreadcrumbItem><Link
                            href={PRIVATE_URLS.TASK(projectId, task.id)}>{task.title}</Link></BreadcrumbItem>
                    </Breadcrumbs>

                    <div className='flex gap-4 items-center'>
                        <h1 className='text-2xl font-medium'>{task.title}</h1>
                        {
                            !hasTaskPermission &&
                            <Tooltip isDisabled={hasTaskPermission}
                                     placement={'right'}
                                     showArrow

                                     className='w-[200px] text-center'
                                     radius={'sm'}
                                     content={'У вас не достаточно прав для редактирования задачи'}>
                                <Lock className={'text-warning cursor-not-allowed'}/>
                            </Tooltip>}
                    </div>
                </div>
                {/*<div className="flex items-center gap-4">*/}
                {/*    <h1 className={'font-medium text-2xl'}>{task.title}</h1>*/}
                {/*    {*/}
                {/*        !hasTaskPermission &&*/}
                {/*        <Tooltip isDisabled={hasTaskPermission}*/}
                {/*                 placement={'right'}*/}
                {/*                 showArrow*/}

                {/*                 className='w-[200px] text-center'*/}
                {/*                 radius={'sm'}*/}
                {/*                 content={'У вас не достаточно прав для редактирования задачи'}>*/}
                {/*            <Lock className={'text-warning cursor-not-allowed'}/>*/}
                {/*        </Tooltip>}*/}
                {/*</div>*/}

                <Textarea
                    isReadOnly={!hasTaskPermission}
                    variant="underlined"

                    maxRows={50}
                    label="Описание"
                    labelPlacement="outside"
                    placeholder="Введите описание задачи"
                />

                <div>
                    <h1 className={'font-medium text-2xl'}>Комментарии</h1>

                </div>
            </div>
            <Divider orientation="vertical"/>
            <div className='flex w-1/2 flex-col gap-8 p-8'>
                <h1 className={'font-medium text-2xl'}>Сведения</h1>
                <Select
                    radius={'sm'}
                    variant={'underlined'}
                    label="Статус"
                    defaultSelectedKeys={[task.status.id]}>
                    {statuses.map((status) => (
                        <SelectItem key={status.id} value={status.name}>
                            {status.name}
                            {/*{status.category === StatusCategoryEnum.TODO &&*/}
                            {/*    <Chip variant='dot' radius={'sm'} size={'sm'} color='primary'>*/}
                            {/*        {status.name}*/}
                            {/*    </Chip>*/}
                            {/*}*/}
                            {/*{status.category === StatusCategoryEnum.DEFAULT &&*/}
                            {/*    <Chip variant='dot' radius={'sm'} size={'sm'} color='secondary'>*/}
                            {/*        {status.name}*/}
                            {/*    </Chip>*/}
                            {/*}*/}
                            {/*{status.category === StatusCategoryEnum.COMPLETED &&*/}
                            {/*    <Chip variant='dot' radius={'sm'} size={'sm'} color='success'>*/}
                            {/*        {status.name}*/}
                            {/*    </Chip>*/}
                            {/*}*/}
                        </SelectItem>
                    ))}
                </Select>
                <div className={'flex flex-col'}>
                    <div className={'flex items-center w-[600px]'}>
                        <h3 className={'w-1/3'}>Исполнитель</h3>
                        <Select
                            radius={'sm'}
                            variant={'underlined'}
                            label="Статус"
                            defaultSelectedKeys={[task.status.id]}>
                            {statuses.map((status) => (
                                <SelectItem key={status.id} value={status.name}>
                                    {status.name}
                                </SelectItem>
                            ))}
                        </Select>
                    </div>
                    <div className={'flex items-center w-[600px]'}>
                        <h3 className={'w-1/3'}>Приоритет</h3>
                        <Select
                            radius={'sm'}
                            variant={'underlined'}
                            label="Статус"
                            defaultSelectedKeys={[task.status.id]}>
                            {statuses.map((status) => (
                                <SelectItem key={status.id} value={status.name}>
                                    {status.name}
                                </SelectItem>
                            ))}
                        </Select>
                    </div>
                    <div className={'flex items-center w-[600px]'}>
                        <h3 className={'w-1/3'}>Метки</h3>
                        <Select
                            radius={'sm'}
                            variant={'underlined'}
                            label="Статус"
                            defaultSelectedKeys={[task.status.id]}>
                            {statuses.map((status) => (
                                <SelectItem key={status.id} value={status.name}>
                                    {status.name}
                                </SelectItem>
                            ))}
                        </Select>
                    </div>
                </div>
            </div>

        </div>

    );
};

export default TaskPage;