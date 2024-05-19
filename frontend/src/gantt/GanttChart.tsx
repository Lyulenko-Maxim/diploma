'use client'
import React, {useEffect} from 'react';
import {GanttComponent, Inject, Edit, Filter, Sort, CriticalPath, Toolbar} from '@syncfusion/ej2-react-gantt';
import {L10n, registerLicense} from '@syncfusion/ej2-base';
import * as RU_LOCALE from './localization.json'

L10n.load(
    RU_LOCALE
);
registerLicense('Ngo9BigBOggjHTQxAR8/V1NBaF1cXmhMYVF0WmFZfVpgdV9GZ1ZRQ2Y/P1ZhSXxXdkBiXH5dcHNVQWlZVUA=');
export const projectResources: object[] = [
    {resourceId: 1, resourceName: 'Project Manager'},
    {resourceId: 2, resourceName: 'Software Analyst'},
    {resourceId: 3, resourceName: 'Developer'},
    {resourceId: 4, resourceName: 'Testing Engineer'}
];

export const data: object[] = [
    {
        TaskID: 1,
        TaskName: 'Project Initiation',
        StartDate: new Date('04/02/2019'),
        EndDate: new Date('04/21/2019'),
        subtasks: [
            {
                TaskID: 2,
                TaskName: 'Identify Site location',
                StartDate: new Date('04/02/2019'),
                Duration: 4,
                Progress: 50,
                resources: [2, 3]
            },
            {
                TaskID: 3,
                TaskName: 'Perform Soil test',
                StartDate: new Date('04/02/2019'),
                Duration: 4,
                Progress: 50,
                resources: [2]
            },
            {
                TaskID: 4,
                TaskName: 'Soil test approval',
                StartDate: new Date('04/02/2019'),
                Duration: 4,
                Predecessor: '3FS',
                Progress: 50,
                resources: [1]
            },
        ]
    },
    {
        TaskID: 5,
        TaskName: 'Project Estimation',
        StartDate: new Date('04/02/2019'),
        EndDate: new Date('04/21/2019'),
        subtasks: [
            {
                TaskID: 6,
                TaskName: 'Develop floor plan for estimation',
                StartDate: new Date('04/04/2019'),
                Duration: 3,
                Progress: 50
            },
            {
                TaskID: 7,
                TaskName: 'List materials',
                StartDate: new Date('04/04/2019'),
                Duration: 3,
                Progress: 50,
                resources: [1, 3, 5]
            },
            {
                TaskID: 8,
                TaskName: 'Estimation approval',
                StartDate: new Date(),
                Duration: 3,
                Predecessor: '7SS',
                Progress: 50
            }
        ]
    },
];
const GanttChart = () => {

    const taskFields: any = {
        id: 'TaskID',
        name: 'TaskName',
        startDate: 'StartDate',
        duration: 'Duration',
        progress: 'Progress',
        child: 'subtasks',
        dependency: 'Predecessor',
        resourceInfo: 'resources'
    };
    const labelSettings: any = {
        rightLabel: 'resources'
    };
    const editSettings: any = {
        allowEditing: true,
        editMode: 'Auto',
        allowTaskbarEditing: true
    };
    const resourceFields: any = {
        id: 'resourceId',
        name: 'resourceName',
    };
    const editOptions = {
        allowAdding: true,
        allowEditing: true,
        allowDeleting: true,
        allowTaskbarEditing: true,
        showDeleteConfirmDialog: true
    };
    const toolbarOptions = ['CriticalPath'];
    return (
        <>
            <GanttComponent dataSource={data}
                            locale={'ru'}
                            allowFiltering={true}
                            allowSorting={true}
                            taskFields={taskFields}
                            editSettings={editSettings}
                            labelSettings={labelSettings}
                            resourceFields={resourceFields}
                            toolbar={toolbarOptions}
                            resources={projectResources}
                            height={'100vh'}
                            className='h-screen'>
                <Inject services={[Edit, Filter, Sort, CriticalPath, Toolbar]}/>
            </GanttComponent>
        </>
    )
};

export default GanttChart;