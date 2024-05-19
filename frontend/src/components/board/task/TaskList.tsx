import React, {FC} from 'react';
import {Draggable, Droppable} from "@hello-pangea/dnd";
import TaskItem from "@/components/board/task/TaskItem";
import {ITask} from '@/types/task.types';

export interface ITaskListProps {
    statusId: string,
    tasks: ITask[]
}

const TaskList: FC<ITaskListProps> = ({statusId, tasks}) => {
    return (
        <Droppable droppableId={statusId} type={'TASK'}>
            {(dropProvided, dropSnapshot) => (
                <div {...dropProvided.droppableProps} className='flex flex-col flex-grow'>
                    <div ref={dropProvided.innerRef} className='flex-grow'>
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

export default TaskList;