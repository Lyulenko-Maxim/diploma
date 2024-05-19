'use client'
import React, {FC, useEffect, useState} from 'react';
import {ProjectDetailsProps} from "@/app/me/projects/[id]/page";
import {useStatusList, useStatusPatch} from "@/hooks/status.hooks";
import StatusItem from "@/components/board/status/StatusItem";
import {useTaskList, useTaskMove, useTaskPatch} from "@/hooks/task.hooks";
import {DragDropContext, DraggableLocation, Droppable, DropResult} from "@hello-pangea/dnd";
import {ITask} from "@/types/task.types";
import {IStatus} from "@/types/status.types";


const StatusList: FC<ProjectDetailsProps> = ({params}) => {
    const {items: statuses, setItems: setStatuses} = useStatusList(params.id)
    const {items: tasks, setItems: setTasks} = useTaskList(params.id)
    const {mutate: statusPatch} = useStatusPatch()
    const {mutate: taskMove} = useTaskMove()

    const groupTasksByStatus = (tasks: ITask[], statuses: IStatus[]): Record<string, ITask[]> => {
        const initialStatusMap = statuses.reduce((acc, status) => {
            acc[status.id] = [];
            return acc;
        }, {} as Record<string, ITask[]>);

        return tasks.reduce((acc, task) => {
            const {status} = task;
            if (!acc[status]) {
                acc[status] = [];
            }
            acc[status].push(task);
            return acc;
        }, initialStatusMap);
    };

    const [tasksByStatus, setTasksByStatus] = useState<Record<string, ITask[]>>();

    useEffect(() => {
        if (tasks && statuses) {
            setTasksByStatus(groupTasksByStatus(tasks, statuses));
            console.log('ya')
        }
    }, [tasks, statuses]);

    if (!statuses || !tasks ! || !tasksByStatus) return <div></div>


    const handleColumnMove = (statusId: string, sourceIndex: number, destinationIndex: number) => {
        const result = Array.from(statuses);
        const [removed] = result.splice(sourceIndex, 1);
        result.splice(destinationIndex, 0, removed);
        setStatuses(result)
        statusPatch({projectId: params.id, id: statusId, data: {order: destinationIndex}});
    };

    const handleTaskMove = (draggableId: string, source: DraggableLocation, destination: DraggableLocation) => {
        console.log(destination.droppableId)
        const sourceTasks = Array.from(tasksByStatus[source.droppableId]);
        const destinationTasks = Array.from(tasksByStatus[destination.droppableId]);
        const [removedTask] = sourceTasks.splice(source.index, 1);

        if (source.droppableId === destination.droppableId) {
            sourceTasks.splice(destination.index, 0, removedTask);
            setTasksByStatus(prev => ({
                ...prev,
                [source.droppableId]: sourceTasks,
            }));
            taskMove({
                projectId: params.id,
                id: draggableId,
                data: {order: destination.index, status: destination.droppableId}
            })
            return;
        }

        destinationTasks.splice(destination.index, 0, removedTask);
        setTasksByStatus(prev => ({
            ...prev,
            [source.droppableId]: sourceTasks,
            [destination.droppableId]: destinationTasks,
        }));
        taskMove({
            projectId: params.id,
            id: draggableId,
            data: {order: destination.index, status: destination.droppableId}
        })
        return;
    };

    const onDragEnd = (result: DropResult) => {
        const {source, destination, type, draggableId} = result;

        if (!destination) {
            return;
        }

        if (source.droppableId === destination.droppableId
            && source.index === destination.index) return;

        if (type === 'COLUMN') {
            handleColumnMove(result.draggableId, source.index, destination.index);
        } else if (type === 'TASK') {
            handleTaskMove(draggableId, source, destination);
        }
    }


    return (
        <div className="flex gap-10 rounded-sm">
            <DragDropContext onDragEnd={onDragEnd}>
                <Droppable
                    droppableId="board"
                    type={'COLUMN'}
                    direction={'horizontal'}
                >
                    {(provided) => (
                        <div className='inline-flex' ref={provided.innerRef} {...provided.droppableProps}>
                            {statuses.map((status, key) => (
                                <StatusItem
                                    key={status.id}
                                    index={key}
                                    status={status}
                                    // tasks={tasksByStatus[status.id].sort((a, b) => a.order > b.order ? 1 : -1)}
                                    tasks={tasksByStatus[status.id]}
                                    params={params}
                                />
                            ))}
                            {provided.placeholder}
                        </div>
                    )}
                </Droppable>
            </DragDropContext>

        </div>
    );
};

export default StatusList;