import React, {FC} from 'react';
import {ITask} from "@/types/task.types";
import {Card, CardBody, Chip, User} from "@nextui-org/react";
import {CardHeader} from "@nextui-org/card";
import {useProfile} from "@/hooks/user.hooks";
import {Draggable, DraggableProvided} from "@hello-pangea/dnd";
import {User as UserIcon, Grip, SignalHigh, SignalLow} from "lucide-react";

export interface ITaskItemProps {
    task: ITask,
    dragProvided: DraggableProvided
}

const TaskItem: FC<ITaskItemProps> = ({task, dragProvided}) => {
    const priorityMap = (priority: string) => {
        switch (priority) {
            case 'lowest':
                return {color: 'bg-green-500', text: 'Самый низкий'};
            case 'low':
                return {color: 'bg-green-700', text: 'Низкий'};
            case 'medium':
                return {color: 'bg-yellow-500', text: 'Средний'};
            case 'high':
                return {color: 'bg-orange-500', text: 'Высокий'};
            case 'highest':
                return {color: 'bg-red-500', text: 'Очень высокий'};
            case 'critical':
                return {color: 'bg-red-700', text: 'Критический'};
            default:
                return {color: 'bg-yellow-500', text: 'Средний'};
        }
    };
    return (
        <div
            {...dragProvided.draggableProps}
            {...dragProvided.dragHandleProps}
            ref={dragProvided.innerRef}
            className='my-4'
        >
            <Card className="p-4 bg-content1" radius='sm'>
                <CardHeader className="p-2">
                    <div className='w-full flex items-center justify-between'>
                        {task.title}
                        <Grip/>
                    </div>

                </CardHeader>
                <CardBody className="p-2 flex flex-col gap-4 ">
                    <div className='w-full flex items-center justify-between'>
                        <Chip variant={'dot'} classNames={{
                            dot: priorityMap(task.priority).color
                        }}>
                            {priorityMap(task.priority).text}
                        </Chip>
                        {task.assignee ?
                            <User
                                name={null}
                                className='justify-start'
                                avatarProps={{
                                    isBordered: false,
                                    // src: typeof task.assignee.profile.photo === 'string' ? task.author.profile.photo : '',
                                    fallback: <UserIcon/>
                                }}
                            /> : null
                        }
                    </div>
                    <span className='text-sm'>Автор</span>
                    <User
                        className='justify-start'
                        name={task.author.profile?.username}
                        avatarProps={{
                            isBordered: false,
                            src: typeof task.author.profile?.photo === 'string' ? task.author.profile.photo : '',
                            fallback: <UserIcon/>
                        }}
                    />

                </CardBody>
            </Card>

        </div>


    );
};

export default TaskItem;