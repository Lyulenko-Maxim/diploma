import React, {FC, useEffect, useRef, useState} from 'react';
import {IStatus, StatusCategoryEnum} from "@/types/status.types";
import {ITaskList} from '@/types/task.types';
import {Draggable} from "@hello-pangea/dnd";
import TaskList from "@/components/board/task/TaskList";
import {Button, Card, CardBody, Chip, Textarea} from "@nextui-org/react";
import {Circle, GripHorizontal, Plus, SquarePlus} from "lucide-react";
import CreateTaskItem from "@/components/board/task/CreateTaskItem";
import {useProjectParams} from "@/app/me/projects/[projectId]/providers";

export interface IStatusItemProps {
    status: IStatus;
    index: number,
    tasks: ITaskList[]
}

const StatusItem: FC<IStatusItemProps> = ({status, tasks, index}) => {

    return (
        <Draggable draggableId={status.id} index={index}>
            {(provided, snapshot) => (
                <div className='flex flex-col shrink-0 mx-4 w-[400px] rounded-sm h-[700px]'
                     ref={provided.innerRef}
                     {...provided.draggableProps}
                >
                    <Card radius='sm' className="my-4 w-[350px] ml-[17.5px]">
                        <CardBody>
                            <div className='flex flex-1 gap-4'>
                                <div {...provided.dragHandleProps}>
                                    <GripHorizontal/>
                                </div>

                                {status.category === StatusCategoryEnum.TODO &&
                                    <Chip variant='dot' radius={'sm'} size={'sm'} color='primary'>
                                        {status.name}
                                    </Chip>
                                }
                                {status.category === StatusCategoryEnum.DEFAULT &&
                                    <Chip variant='dot' radius={'sm'} size={'sm'} color='secondary'>
                                        {status.name}
                                    </Chip>
                                }
                                {status.category === StatusCategoryEnum.COMPLETED &&
                                    <Chip variant='dot' radius={'sm'} size={'sm'} color='success'>
                                        {status.name}
                                    </Chip>
                                }
                            </div>
                        </CardBody>
                    </Card>

                    {status.category === StatusCategoryEnum.TODO &&
                        <CreateTaskItem status={status}/>}
                    <TaskList statusId={status.id} tasks={tasks}/>
                </div>
            )}
        </Draggable>
    );
};

export default StatusItem;