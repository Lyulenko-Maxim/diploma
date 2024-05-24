import React, {FC, memo} from 'react';
import {Draggable, Droppable} from "@hello-pangea/dnd";
import TaskItem from "@/components/board/task/TaskItem";
import {ITaskList} from '@/types/task.types';

export interface ITaskListProps {
    statusId: string,
    tasks: ITaskList[]
}

const TaskList: FC<ITaskListProps> = ({statusId, tasks}) => {
    return (
        <Droppable droppableId={statusId} type={'TASK'}>
            {(dropProvided, dropSnapshot) => (
                <div {...dropProvided.droppableProps} className='flex flex-1 flex-col overflow-y-hidden h-72'>
                    <div ref={dropProvided.innerRef}
                         className='flex min-h-full flex-1 flex-col overflow-y-scroll pb-[250px]'>
                        {tasks.map((task, index) => (
                            <Draggable key={task.id} draggableId={task.id} index={index}>
                                {(dragProvided, dragSnapshot) => (
                                    <TaskItem key={task.id} task={task} dragProvided={dragProvided}/>
                                )}
                            </Draggable>
                        ))}
                    </div>
                    {dropProvided.placeholder}
                </div>
            )}
        </Droppable>
    );
};

export default memo(TaskList);