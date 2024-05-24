'use client'
import React, {FC, useEffect, useState} from 'react';
import {useStatusList, useStatusPatch} from "@/hooks/status.hooks";
import StatusItem from "@/components/board/status/StatusItem";
import {useTaskList, useTaskMove, useTaskPatch} from "@/hooks/task.hooks";
import {DragDropContext, DraggableLocation, Droppable, DropResult} from "@hello-pangea/dnd";
import {ITaskList} from "@/types/task.types";
import {IStatus, StatusCategoryEnum} from "@/types/status.types";
import {Card, CardBody, Chip} from "@nextui-org/react";
import {GripHorizontal} from "lucide-react";
import {useProjectParams} from "@/app/me/projects/[projectId]/providers";


const StatusList = () => {
    const projectId = useProjectParams()
    const {items: statuses, setItems: setStatuses} = useStatusList(projectId)
    const {items: tasks, setItems: setTasks} = useTaskList(projectId)
    const {mutate: statusPatch} = useStatusPatch()
    const {mutate: taskMove} = useTaskMove()

    const groupTasksByStatus = (tasks: ITaskList[], statuses: IStatus[]): Record<string, ITaskList[]> => {
        const initialStatusMap = statuses.reduce((acc, status) => {
            acc[status.id] = [];
            return acc;

        }, {} as Record<string, ITaskList[]>);

        return tasks.reduce((acc, task) => {
            const {id: statusId} = task.status;

            if (!acc[statusId]) acc[statusId] = [];

            acc[statusId].push(task);
            return acc;
        }, initialStatusMap);
    };

    const [tasksByStatus, setTasksByStatus] = useState<Record<string, ITaskList[]>>();

    useEffect(() => {
        if (tasks && statuses) {
            setTasksByStatus(groupTasksByStatus(tasks, statuses));
        }
    }, [tasks, statuses]);

    if (!statuses || !tasks ! || !tasksByStatus) return <div></div>


    const handleColumnMove = (statusId: string, sourceIndex: number, destinationIndex: number) => {
        const result = Array.from(statuses);
        const [removed] = result.splice(sourceIndex, 1);
        result.splice(destinationIndex, 0, removed);
        setStatuses(result)
        statusPatch({projectId: projectId, id: statusId, data: {order: destinationIndex}});
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
                projectId: projectId,
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
            projectId: projectId,
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
        <div className="flex flex-col flex-1 rounded-sm min-w-0 overflow-hidden">

            <DragDropContext onDragEnd={onDragEnd}>
                <Droppable
                    droppableId="board"
                    type={'COLUMN'}
                    direction={'horizontal'}
                >
                    {(provided) => (
                        <div className='flex flex-1 overflow-y-hidden overflow-x-auto'
                             ref={provided.innerRef} {...provided.droppableProps}>
                            {statuses.map((status, key) => (
                                <StatusItem
                                    key={status.id}
                                    index={key}
                                    status={status}
                                    tasks={tasksByStatus[status.id]}
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