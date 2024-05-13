import React, {FC} from 'react';
import {IStatus} from "@/types/status.types";

export interface IStatusItem {
    status: IStatus;
}

const StatusItem: FC<IStatusItem> = ({status}) => {
    return (
        <div className='flex flex-col rounded-sm p-16 bg-default'>
            {status.name}
        </div>
    );
};

export default StatusItem;