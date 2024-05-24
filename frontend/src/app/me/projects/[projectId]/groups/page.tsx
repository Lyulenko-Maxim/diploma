'use client'
import React, {Fragment, useMemo} from 'react';
import {useProjectParams} from "@/app/me/projects/[projectId]/providers";
import {
    BreadcrumbItem,
    Breadcrumbs, Button,
    Table,
    TableBody,
    TableCell,
    TableColumn,
    TableHeader,
    TableRow, Tooltip
} from "@nextui-org/react";
import Link from "next/link";
import {PRIVATE_URLS} from "@/app/urlsConfig";
import {columns} from "./data";
import {useGroupList} from "@/hooks/group.hooks";
import {useRenderGroupsTable} from "@/app/me/projects/[projectId]/groups/renderTable";
import {GripVertical, Lock, SquarePlus} from "lucide-react";
import {DragDropContext, Draggable, Droppable} from "@hello-pangea/dnd";
import ProjectItem from "@/components/projects/ProjectItem";
import {renderCells} from "@/components/projects/renderCells";
import {useMemberCurrent} from "@/hooks/members.hooks";
import {checkPermissions} from "@/app/permissions";

const GroupsPage = () => {
    const projectId = useProjectParams()
    const {items: groups} = useGroupList(projectId)
    const {renderCell} = useRenderGroupsTable()
    const {data: currentMember} = useMemberCurrent(projectId)

    const availableGroups = useMemo(() => {
        if (!groups || !currentMember) return [];

        const currentMemberMaxOrder = currentMember.highest_group.order

        return groups.filter(group => currentMember.is_owner || group.order > currentMemberMaxOrder);

    }, [groups, currentMember])

    const unavailableGroups = useMemo(() => {
        if (!groups) return [];
        if (!availableGroups) return groups;

        return groups.filter(group => !availableGroups.includes(group));
    }, [groups, availableGroups])

    if (!groups || !currentMember) return <></>

    const cols = columns(groups.length)

    const hasGroupPermission = checkPermissions(currentMember.permissions, [])
    return (
        <div className='flex-1 flex-col'>
            <div className='flex flex-col gap-4 pt-4 pb-4 pl-10'>
                <Breadcrumbs size={'md'}>
                    <BreadcrumbItem><Link href={PRIVATE_URLS.PROJECT(projectId)}>Проект</Link></BreadcrumbItem>
                    <BreadcrumbItem><Link href={PRIVATE_URLS.GROUPS(projectId)}>Группы</Link></BreadcrumbItem>
                </Breadcrumbs>

                <div className='flex flex-col flex-1 gap-4'>
                    <h1 className='mr-16 text-2xl font-medium'>Группы</h1>
                    <p className='text-sm text-foreground/75'>Используйте группы для настройки прав доступа участников
                        проекта.</p>
                </div>
            </div>
            <section className="flex flex-1 flex-col overflow-hidden">
                <div
                    className='grid border-opacity-30 px-10 py-4 grid-cols-[.05fr_.3fr_.3fr_.1fr] border-b-1 border-foreground'>
                    {cols.map((column) =>
                        <div key={column.uid}>{column.name}</div>
                    )}
                </div>
                <>
                    {unavailableGroups.map((group, key) => (
                        <div key={group.id}

                             className='grid w-full items-center rounded-sm border-opacity-20 px-10 py-2 border-b-1 border-foreground bg-background grid-cols-[.05fr_.3fr_.3fr_.1fr]'>

                            <Tooltip placement={'right'}
                                     showArrow
                                     className='w-[200px] text-center'
                                     radius={'sm'}
                                     content={

                                         key === unavailableGroups.length - 1
                                             ? 'Группа заблокирована, потому что это ваша самая высокая группа'
                                             : 'Группа заблокирована, потому что она выше, чем ваша самая высокая группа'
                                     }>
                                <Lock className={'cursor-not-allowed'}/>
                            </Tooltip>
                            {cols.map((column, index) => {
                                if (index === 0) return null;
                                return (
                                    <Fragment key={column.uid}>
                                        {renderCell(group, column.uid)}
                                    </Fragment>
                                );
                            })}
                        </div>
                    ))}
                </>
                <DragDropContext onDragEnd={() => {
                }}>
                    <Droppable droppableId="groups">
                        {(provided) => (
                            <div {...provided.droppableProps}
                                 ref={provided.innerRef}>

                                {availableGroups.map((group) => (
                                    <div key={group.id}>
                                        <Draggable
                                            index={group.order}
                                            draggableId={group.id}>
                                            {provided => (
                                                <div key={group.id} ref={provided.innerRef}
                                                     {...provided.draggableProps}
                                                     className='grid w-full items-center rounded-sm border-opacity-20 px-10 py-2 border-b-1 border-foreground bg-background grid-cols-[.05fr_.3fr_.3fr_.1fr]'>

                                                    <div {...provided.dragHandleProps} className='hover:cursor-grab'>
                                                        <GripVertical/>
                                                    </div>

                                                    {cols.map((column, index) => {
                                                        if (index === 0) return null;
                                                        return (
                                                            <Fragment key={column.uid}>
                                                                {renderCell(group, column.uid)}
                                                            </Fragment>
                                                        );
                                                    })}
                                                </div>
                                            )}
                                        </Draggable>
                                    </div>


                                ))}

                                {provided.placeholder}
                            </div>
                        )}
                    </Droppable>
                </DragDropContext>

            </section>

        </div>
    );
};

export default GroupsPage;