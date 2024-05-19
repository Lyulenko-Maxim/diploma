import React, {FC, useEffect, useRef, useState} from 'react';
import {IStatus, StatusCategoryEnum} from "@/types/status.types";
import {ITask} from '@/types/task.types';
import {Draggable} from "@hello-pangea/dnd";
import TaskList from "@/components/board/task/TaskList";
import {Button, Card, CardBody, Chip, Textarea} from "@nextui-org/react";
import {Circle, GripHorizontal, Plus, SquarePlus} from "lucide-react";
import CreateTaskItem from "@/components/board/task/CreateTaskItem";
import {ProjectDetailsProps} from "@/app/me/projects/[id]/page";

export interface IStatusItemProps {
    status: IStatus;
    index: number,
    tasks: ITask[]
}

const StatusItem: FC<IStatusItemProps & ProjectDetailsProps> = ({status, tasks, index, params}) => {

    return (
        <Draggable draggableId={status.id} index={index}>
            {(provided, snapshot) => (
                <div className='flex flex-col mx-8 w-[350px] rounded-sm'
                     ref={provided.innerRef}
                     {...provided.draggableProps}
                     {...provided.dragHandleProps} >
                    <Card radius='sm' className="my-4 ">
                        <CardBody>
                            <div className='flex gap-4'>
                                <GripHorizontal/>
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
                        <CreateTaskItem params={params} status={status}/>}
                    <TaskList statusId={status.id} tasks={tasks}/>
                </div>
            )}
        </Draggable>
    );
};

export default StatusItem;