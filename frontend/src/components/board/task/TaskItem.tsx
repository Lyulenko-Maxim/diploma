import React, {FC} from 'react';
import {ITaskList, PriorityEnum} from "@/types/task.types";
import {Card, CardBody, Chip, Tooltip, User} from "@nextui-org/react";
import {CardHeader} from "@nextui-org/card";
import {useProfile} from "@/hooks/user.hooks";
import {Draggable, DraggableProvided} from "@hello-pangea/dnd";
import {User as UserIcon, Grip, SignalHigh, SignalLow} from "lucide-react";
import Link from "next/link";
import {useProjectParams} from "@/app/me/projects/[projectId]/providers";
import {PRIVATE_URLS} from "@/app/urlsConfig";
import {formatDate, formatDateTime} from "@/app/utils";

export interface ITaskItemProps {
    task: ITaskList,
    dragProvided: DraggableProvided
}

const TaskItem: FC<ITaskItemProps> = ({task, dragProvided}) => {
    const projectId = useProjectParams()
    const priorityMap = (priority: string) => {
        switch (priority) {
            case PriorityEnum.LOWEST:
                return {color: 'bg-green-500', text: 'Самый низкий'};
            case PriorityEnum.LOW:
                return {color: 'bg-green-700', text: 'Низкий'};
            case PriorityEnum.MEDIUM:
                return {color: 'bg-yellow-500', text: 'Средний'};
            case PriorityEnum.HIGH:
                return {color: 'bg-orange-500', text: 'Высокий'};
            case PriorityEnum.HIGHEST:
                return {color: 'bg-red-500', text: 'Очень высокий'};
            case PriorityEnum.CRITICAL:
                return {color: 'bg-red-700', text: 'Критический'};
            default:
                return {color: 'bg-yellow-500', text: 'Средний'};
        }
    };
    return (
        <Link href={PRIVATE_URLS.TASK(projectId, task.id)}>
            <div
                {...dragProvided.draggableProps}
                ref={dragProvided.innerRef}
                className='my-2'
            >
                <Card className="p-4 bg-content1 mx-auto w-[350px]" radius='sm'>
                    <CardHeader className="p-0">
                        <div className="flex flex-col flex-1 gap-4">
                            {task.markers.length > 0 ?
                                <div className='flex flex-wrap items-center text-sm gap-2'>
                                    {task.markers.map(marker => (
                                        <Tooltip key={marker.id}
                                                 placement={'top'}
                                                 showArrow
                                                 className='text-center'
                                                 radius={'sm'}
                                                 content={marker.name}>
                                            <div key={marker.id} className={'group rounded-full h-1.5 px-8'}
                                                 style={{backgroundColor: marker.color_hex}}>
                                            </div>
                                        </Tooltip>
                                    ))}
                                </div>
                                : null}

                            <div className='w-full flex items-center justify-between'>
                                <span className='text-lg font-medium'>{task.title}</span>
                                <div {...dragProvided.dragHandleProps}>
                                    <Grip/>
                                </div>
                            </div>

                        </div>
                    </CardHeader>
                    <CardBody className="mt-6 p-0 flex flex-col gap-4 ">
                        <div className='w-full flex items-center justify-between'>
                            <span className='text-sm text-foreground/50'>Приоритет:</span>
                            <Chip variant={'dot'} radius={'sm'} classNames={{
                                dot: priorityMap(task.priority).color
                            }}>
                                {priorityMap(task.priority).text}
                            </Chip>
                        </div>

                        <div className='flex justify-between'>
                            <div className='flex gap-2 items-center'>
                                <span className='text-sm text-foreground/50'>Автор:</span>
                                <User
                                    className='justify-start items-center text-sm '
                                    name={null}
                                    // description={(task.author.profile.first_name + ' ' || '') + (task.author.profile.last_name || '')}
                                    avatarProps={{
                                        isBordered: false,
                                        size: 'sm',
                                        src: task.author.profile.photo,
                                        fallback: <UserIcon/>
                                    }}
                                />
                            </div>

                            {task.assignee ?
                                <div className='flex gap-2 items-center'>
                                    <span className='text-sm text-foreground/50'>Исполнитель:</span>
                                    <User
                                        className='justify-start items-center text-sm gap-0'
                                        name={null}
                                        avatarProps={{
                                            isBordered: false,
                                            size: 'sm',
                                            src: task.author.profile.photo,
                                            fallback: <UserIcon/>
                                        }}
                                    />
                                </div> : null
                            }
                        </div>


                        <div className={'flex justify-between'}>
                            <span
                                className={'text-sm text-foreground/50'}>Обновлена {task.updated_at && formatDateTime(task.updated_at)}
                        </span>
                        </div>

                    </CardBody>
                </Card>

            </div>

        </Link>
    );
};

export default TaskItem;